from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import os
import time
import threading
from multiprocessing import Pool
import redis
import jieba
from snownlp import SnowNLP

import controler
import analysis
import crawl

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Author: SYJ'
bootstrap = Bootstrap(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


class ShopForm(FlaskForm):
    shop = StringField('Search Shopping', validators=[DataRequired()])
    select = SelectField(label='Select', coerce=int, choices=[(0, 'BestMatch'), (1, 'Cheapest')])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShopForm()
    if form.validate_on_submit():
        session['shop'] = form.shop.data
        session['select'] = form.select.data
        return redirect(url_for('res'))
    return render_template('index.html', form=form)


def get_hot_pic(path, item_id):
    frequent_ci = crawl.hot_comments(item_id)
    analysis.by_frequent(frequent_ci, path)


r = redis.Redis(host='localhost', port=6379, db=0)


# P_COMMERNTS = ""
def get_comments(i, item_id, name):
    print('Run task %s (%s)...' % (i, os.getpid()))
    texts = crawl.private_comments(i, item_id)
    j = ""
    for i in texts:
        j += i.replace('hellip', "") + '\n'
    r.append(name, j)


def get_p_pic(name, path, item_id):
    r.set(name, "")
    p = Pool()
    for i in range(10):
        p.apply_async(get_comments, args=(i, item_id, name))
    p.close()
    p.join()
    try:
        analysis.by_text(path, name)
    except:
        r.set(name, '暂无评价～\n')
        analysis.by_text(path, name)


@app.route('/res')
def res():
    name = session.get('shop')
    col = controler.con_db()
    shoplist = col.list_collection_names()
    if name not in shoplist:
        controler.insert_list(name, name)

    rows = controler.find_data(name)
    if session.get('select') == 1:
        item = controler.min_price(name)
    else:
        item = controler.best(name)
    mstr = name + item['id']
    hotcomments_path = r"./static/data/{}hotcomments.jpg".format(mstr)
    pcomments_path = r"./static/data/{}pcomments.jpg".format(mstr)
    start = time.time()
    if not os.path.exists(hotcomments_path):
        t1 = threading.Thread(target=get_hot_pic, args=(hotcomments_path, item['id'],))
        t1.start()
    if not os.path.exists(pcomments_path):
        t2 = threading.Thread(target=get_p_pic, args=(mstr, pcomments_path, item['id'],))
        t2.start()
    if item['historyPrice']:
        data = list(item['historyPrice'].keys())
        hp = list(item['historyPrice'].values())
    else:
        try:
            historyPrice = crawl.get_history_price(item['id'])
        except:
            historyPrice = {time.strftime("%Y,%m,%d", time.localtime()): item['price']}
        controler.con_table(name).update_one({"id": item['id']}, {"$set": {"historyPrice": historyPrice}})
        data = list(historyPrice.keys())
        hp = list(historyPrice.values())
    try:
        t1.join()
        t2.join()
    except:
        pass
    end = time.time()
    print("Time: %.3f" % float(end - start))

    return render_template('res.html', row=rows, hotcomments_path=hotcomments_path, pcomments_path=pcomments_path,
                           item=item, x=data, y=hp, tag=session.get('select'))


@app.route('/res/<shop_id>')
def shop_comments_show(shop_id):
    name = session.get('shop')
    mstr = name + shop_id
    item = controler.find_by_id(name, shop_id)
    hotcomments_path = r"./static/data/{}hotcomments.jpg".format(mstr)
    pcomments_path = r"./static/data/{}pcomments.jpg".format(mstr)
    start = time.time()
    if not os.path.exists(hotcomments_path):
        t1 = threading.Thread(target=get_hot_pic, args=(hotcomments_path, shop_id,))
        t1.start()
    if not os.path.exists(pcomments_path):
        t2 = threading.Thread(target=get_p_pic, args=(mstr, pcomments_path, shop_id,))
        t2.start()

    if item['historyPrice']:
        data = list(item['historyPrice'].keys())
        hp = list(item['historyPrice'].values())
    else:
        try:
            historyPrice = crawl.get_history_price(item['id'])
        except:
            historyPrice = {time.strftime("%Y,%m,%d", time.localtime()): item['price']}
        controler.con_table(name).update_one({"id": item['id']}, {"$set": {"historyPrice": historyPrice}})
        data = list(historyPrice.keys())
        hp = list(historyPrice.values())
    try:
        t2.join()
        t1.join()
    except:
        pass
    end = time.time()
    print("Time: %.3f" % float(end - start))
    return render_template('com.html', hotcomments_path=hotcomments_path, pcomments_path=pcomments_path, item=item,
                           x=data, y=hp)


if __name__ == '__main__':
    # app.run()
    jieba.add_word('非常好用')
    jieba.add_word('非常满意')
    jieba.add_word('非常喜欢')
    jieba.add_word('非常不错')
    jieba.add_word('很满意')
    jieba.add_word('很好用')
    jieba.add_word('很喜欢')
    jieba.add_word('很不错')
    jieba.add_word('此用户未填写评价内容')
    app.run(host='0.0.0.0', port=5000, debug=True)

