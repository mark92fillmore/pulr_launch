import os
from .database import db_session
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask.ext.admin import Admin
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from .forms import ContactForm, SubscribeForm

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize App and configuration
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
  'sqlite:///' + os.path.join(basedir, 'tmp/test.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='password',
    MAIL_SERVER='smtp.google.com',
    MAIL_USERNAME='fsengsta@princeton.edu',
    MAIL_PASSWORD='S3ngstacke*'
	))

mail = Mail(app)
db = SQLAlchemy(app)

from .models import *
from .views import *

###############
#   Database  #
#    Access   #
###############

# Don't move this to database.py.
# Please.
@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()