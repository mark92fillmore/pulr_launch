import os
from .database import db_session
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.uploads import patch_request_class
from .forms import ContactForm, SubscribeForm

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize App and configuration
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
  'sqlite:///' + os.path.join(basedir, 'tmp/database.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='8biS29C[UE6zsE#P_1@)KrCu{{b3?R',
    USERNAME='administrator',
    PASSWORD='pulr*2015',
    MAIL_SERVER='smtp.gmail.com',
    MAIL_USERNAME='pulr.manager@gmail.com',
    MAIL_PASSWORD='pulr*2015',
    MAIL_USE_SSL=True,
    MAIL_PORT=465,
    DEFAULT_MAIL_SENDER='pulr.manager@gmail.com',
    UPLOADED_FILES_DEST= lambda app : app.instance_root
	))

mail = Mail(app)
db = SQLAlchemy(app)
admin = Admin(app, name="Princeton Undergraduate Law Review")
patch_request_class(app)

###############
#   Database  #
#    Access   #
###############

# Don't move this to database.py.
# Please.
@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

########################
# Necessary Imports    #
########################

from .models import *
from .views import *