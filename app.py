from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import threading
import time

import db_control
import generate_comments
import spir

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

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


def get_hot_pic(name, path):
    item = db_control.best(name)
    frequent_ci = spir.hotcomments(item)
    generate_comments.generateByfrequent(frequent_ci, path)


P_COMMERNTS = ""
def get_commts(i, item):
    texts =spir.pcomments(i, item)
    global P_COMMERNTS
    for j in texts:
        P_COMMERNTS += j.replace('hellip', " ")


def get_p_pic(name, path):
    item = db_control.best(name)
    for i in range(10):
        thread = threading.Thread(target=get_commts(i, item), name='get_p_comments')
        thread.start()
    thread.join()
    generate_comments.generateByText(P_COMMERNTS, path)


@app.route('/res')
def res():
    name = session.get('shop')

    # i = db_control.finddata(name)
    # if not i:
    db_control.insertList(name, name)
    i = db_control.finddata(name)
    # print('insert_shop_info')
    
    hotcomments_path = r"./static/{}hotcomments.jpg".format(name)
    pcomments_path = r"./static/{}pcomments.jpg".format(name)
    if not os.path.exists(hotcomments_path):
        t1 = threading.Thread(target=get_hot_pic(name, hotcomments_path), name='get_hot_pic')
        t1.start()
        t1.join()
    start = time.time()
    if not os.path.exists(pcomments_path):
        t2 = threading.Thread(target=get_p_pic(name, pcomments_path), name='get_p_pic')
        t2.start()
        t2.join()
    end = time.time()
    print(end - start)
    return render_template('res.html', name=name, row=i, hotcomments_path=hotcomments_path, pcomments_path= pcomments_path)


if __name__ == '__main__':
    app.run()
