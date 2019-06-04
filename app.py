from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import os
import time
import threading

import dao
import analysis

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


@app.route('/res')
def res():
    table_name = session.get('shop')
    col = dao.con_db()
    shoplist = col.list_collection_names()
    if table_name not in shoplist:
        dao.insert_list(table_name, table_name)

    rows = dao.find_data(table_name)
    if session.get('select') == 1:
        item = dao.min_price(table_name)
    else:
        item = dao.best(table_name)
    mstr = table_name + item['id']
    hotcomments_path = r"./static/data/{}hotcomments.jpg".format(mstr)
    pcomments_path = r"./static/data/{}pcomments.jpg".format(mstr)

    start = time.time()

    if not item['historyPrice']:
        t0 = threading.Thread(target=analysis.history_price, args=(item, table_name,))
        t0.start()

    if not os.path.exists(hotcomments_path):
        t1 = threading.Thread(target=analysis.get_hot_pic, args=(hotcomments_path, item['id'],))
        t1.start()
    if not os.path.exists(pcomments_path):
        t2 = threading.Thread(target=analysis.get_p_pic, args=(table_name, pcomments_path, item['id'], item['sentiments'], ))
        t2.start()

    try:
        t1.join()
        t2.join()
        t0.join()
    except:
        pass
    item = dao.find_by_id(table_name, item['id'])
    sentiments = list(str(item['sentiments']).split(',')[:-1])
    sentiments_path = analysis.sentiments_pic(sentiments, mstr)
    historyPrice = dao.find_by_id(table_name, item['id'])['historyPrice']
    data = list(historyPrice.keys())
    hp = list(historyPrice.values())
    end = time.time()
    print("Time: %.3f" % float(end - start))
    return render_template('res.html', row=rows, hotcomments_path=hotcomments_path, pcomments_path=pcomments_path,
                           sentiments_path=sentiments_path, item=item, x=data, y=hp, tag=session.get('select'))


@app.route('/res/<shop_id>')
def shop_comments_show(shop_id):
    table_name = session.get('shop')
    mstr = table_name + shop_id
    item = dao.find_by_id(table_name, shop_id)
    hotcomments_path = r"./static/data/{}hotcomments.jpg".format(mstr)
    pcomments_path = r"./static/data/{}pcomments.jpg".format(mstr)
    start = time.time()

    if not item['historyPrice']:
        t0 = threading.Thread(target=analysis.history_price, args=(item, table_name,))
        t0.start()
    if not os.path.exists(hotcomments_path):
        t1 = threading.Thread(target=analysis.get_hot_pic, args=(hotcomments_path, shop_id,))
        t1.start()
    if not os.path.exists(pcomments_path):
        t2 = threading.Thread(target=analysis.get_p_pic, args=(table_name, pcomments_path, shop_id, item['sentiments'], ))
        t2.start()

    try:
        t1.join()
        t2.join()
        t0.join()
    except Exception as e:
        print(e)

    item = dao.find_by_id(table_name, item['id'])
    sentiments = list(str(item['sentiments']).split(',')[:-1])
    sentiments_path = analysis.sentiments_pic(sentiments, mstr)
    historyPrice = dao.find_by_id(table_name, item['id'])['historyPrice']
    data = list(historyPrice.keys())
    hp = list(historyPrice.values())
    end = time.time()

    print("Time: %.3f" % float(end - start))
    return render_template('com.html', hotcomments_path=hotcomments_path, pcomments_path=pcomments_path, item=item,
                           sentiments_path=sentiments_path, x=data, y=hp)


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)
