from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import db_control

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


@app.route('/res')
def res():
    name = session.get('shop')
    print("name")
    i = db_control.showall()
    return render_template('res.html', name=name, row=i)


if __name__ == '__main__':
    app.run()
