from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import threading
import time
from multiprocessing import Pool

import db_control
import generate_comments
import spir

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MY NAME IS SYJ'

bootstrap = Bootstrap(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


class ShopForm(FlaskForm):
    shop = StringField('add shopping', validators=[DataRequired()])
    submit = SubmitField('submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShopForm()
    if form.validate_on_submit():
        session['shop'] = form.shop.data
        return redirect(url_for('res'))
    return render_template('index.html', form=form)


def get_hot_pic(name, path, item_id):
    frequent_ci = spir.hotcomments(item_id)
    generate_comments.generateByfrequent(frequent_ci, path)


# P_COMMERNTS = ""
def get_commts(i, item_id):
    print('Run task %s (%s)...' % (i, os.getpid()))
    texts = spir.pcomments(i, item_id)
    j = ""
    for i in texts:
        j += i.replace('hellip', "") + " "
    return j


def writeTXTcallback(x):
    print("ok")
    ci_path = r"./static/pcomments.txt"
    with open(ci_path, 'a') as f:
        f.write('%s \n' % x)


def get_p_pic(name, path, item_id):
    ci_path = r"./static/pcomments.txt"
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

    # i = db_control.finddata(name)
    # if not i:
    col = db_control.conDB()
    shoplist = col.list_collection_names()
    if name not in shoplist:
        db_control.insertList(name, name)
    i = db_control.finddata(name)
    item_id = db_control.best(name)['id']
    # print('insert_shop_info')
    
    hotcomments_path = r"./static/{}hotcomments.jpg".format(name)
    pcomments_path = r"./static/{}pcomments.jpg".format(name)
    if not os.path.exists(hotcomments_path):
        t1 = threading.Thread(target=get_hot_pic, args=(name, hotcomments_path, item_id, ))
        t1.start()
        t1.join()
    start = time.time()
    if not os.path.exists(pcomments_path):
        get_p_pic(name, pcomments_path, item_id)
    end = time.time()
    print(end - start)
    return render_template('res.html', name=name, row=i, hotcomments_path=hotcomments_path, pcomments_path=pcomments_path)


@app.route('/res/<shop_id>')
def shop_comments_show(shop_id):
    '''
    return "ok"
    '''
    name = session.get('shop')
    mstr = name + shop_id
    hotcomments_path = r"./static/{}hotcomments.jpg".format(mstr)
    pcomments_path = r"./static/{}pcomments.jpg".format(mstr)
    if not os.path.exists(hotcomments_path):
        t1 = threading.Thread(target=get_hot_pic, args=(name, hotcomments_path, shop_id, ))
        t1.start()
        t1.join()
    start = time.time()
    if not os.path.exists(pcomments_path):
        get_p_pic(name, pcomments_path, shop_id)
    end = time.time()
    print(end - start)
    return render_template('com.html', hotcomments_path=hotcomments_path, pcomments_path=pcomments_path)


if __name__ == '__main__':
    app.run()
