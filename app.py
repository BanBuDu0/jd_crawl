from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import os
import threading
import time
from multiprocessing import Pool

import controler
import generate_comments
import crawl

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Author: SYJ'
bootstrap = Bootstrap(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


class ShopForm(FlaskForm):
    shop = StringField('Search Shopping', validators=[DataRequired()])
    select = SelectField(label='Select',coerce=int , choices=[(0, 'Cheapest'), (1, 'BestMatch')])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShopForm()
    if form.validate_on_submit(): 
        session['shop'] = form.shop.data
        session['select'] = form.select.data
        return redirect(url_for('res'))
    return render_template('index.html', form=form)


def get_hot_pic(name, path, item_id):
    frequent_ci =  crawl.hotcomments(item_id)
    generate_comments.generateByfrequent(frequent_ci, path)


# P_COMMERNTS = ""
def get_commts(i, item_id):
    print('Run task %s (%s)...' % (i, os.getpid()))
    texts = crawl.pcomments(i, item_id)
    j = ""
    for i in texts:
        j += i.replace('hellip', "") + " "
    return j


def writeTXTcallback(comments):
    ci_path = r"./data/pcomments.txt"
    with open(ci_path, 'a') as f:
        f.write('%s \n' % comments)
    print("%s ok" % os.getpid())


def get_p_pic(name, path, item_id):
    ci_path = r"./data/pcomments.txt"
    with open(ci_path, 'w') as f:
        f.write('\n' )
    p = Pool()
    for i in range(10):
        p.apply_async(get_commts, args=(i, item_id,), callback=writeTXTcallback)
    p.close()
    p.join()
    generate_comments.generateByText(path)


@app.route('/res')
def res():
    name = session.get('shop')
    col = controler.conDB()
    shoplist = col.list_collection_names()
    if name not in shoplist:
        t0 = threading.Thread(target=controler.insertList, args=(name, name, ))
        t0.start()
        t0.join()
        # controler.insertList(name, name)
    rows = controler.finddata(name)
    if session.get('select') == 0:
        item = controler.minPrice(name)
    else:
        item = controler.best(name)
    mstr = name + item['id']
    hotcomments_path = r"./data/{}hotcomments.jpg".format(mstr)
    pcomments_path = r"./data/{}pcomments.jpg".format(mstr)
    start = time.time()
    if not os.path.exists(hotcomments_path):
        t1 = threading.Thread(target=get_hot_pic, args=(name, hotcomments_path, item['id'], ))
        t1.start()
        t1.join()
    end = time.time()
    print("hotcomments time: %.3f" % float(end - start))
    start = time.time()
    if not os.path.exists(pcomments_path):
        t2 = threading.Thread(target=get_p_pic, args=(name, pcomments_path, item['id'], ))
        t2.start()
        t2.join()
        # get_p_pic(name, pcomments_path, item_id)
    end = time.time()
    print("pcomments time: %.3f" % float(end - start))
    data = list(item['historyPrice'].keys())
    hp = list(item['historyPrice'].values())
    return render_template('res.html', row=rows, hotcomments_path=hotcomments_path, pcomments_path=pcomments_path, item=item, x=data, y=hp)


@app.route('/res/<shop_id>')
def shop_comments_show(shop_id):
    name = session.get('shop')
    mstr = name + shop_id
    item = controler.findByID(name, shop_id)
    hotcomments_path = r"./data/{}hotcomments.jpg".format(mstr)
    pcomments_path = r"./data/{}pcomments.jpg".format(mstr)
    if not os.path.exists(hotcomments_path):
        t1 = threading.Thread(target=get_hot_pic, args=(name, hotcomments_path, shop_id, ))
        t1.start()
        t1.join()
    start = time.time()
    if not os.path.exists(pcomments_path):
        t2 = threading.Thread(target=get_p_pic, args=(name, pcomments_path, shop_id ))
        t2.start()
        t2.join()
    end = time.time()
    print(end - start)
    data = list(item['historyPrice'].keys())
    hp = list(item['historyPrice'].values())
    return render_template('com.html', hotcomments_path=hotcomments_path, pcomments_path=pcomments_path, item=item, x=data, y=hp)


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0',port=5000,debug=True)
    app.jinja_env.variable_start_string = '{{ '
    app.jinja_env.variable_end_string = ' }}'
