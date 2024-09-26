from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    #session['name'] = None
    #session['email'] = None
    
    if form.validate_on_submit():
        # configure user name
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        
        # configure user email
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        # session['email'] = form.email.data        
        if 'utoronto' in form.email.data:
            session['email'] = f"Your UofT email is { form.email.data }"
        else:
            session['email'] = "Please use your UofT email."
        
        return redirect(url_for('index'))
    return render_template('index.html', 
                           form=form,
                           name=session.get('name'),
                           email=session.get('email'))


@app.route('/date')
def date():
    return render_template('date.html', current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

    
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    # function name format for custom validators: validate_<fieldname> 
    def validate_email(self, field):
        if '@' not in field.data:
            raise ValidationError(f'Please include an "@" in the email address. {field.data} is missing an "@".')
        # elif 'utoronto' not in field.data:
        #     raise ValidationError("Please provide a UofT email address.")
