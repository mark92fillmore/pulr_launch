from . import admin, app, db, mail
from .database import db_session
from .models import User, Post, Article, Event
from flask import abort, flash, request, redirect, render_template, \
     session, url_for
from flask.ext.admin import Admin, AdminIndexView, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.mail import Message, Mail
from flaskext.uploads import UploadSet, DOCUMENTS
from .forms import ContactForm, SubscribeForm
from flask_wtf import Form
from wtforms import validators

###################
#    Base Views   #
###################

@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username.'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password.'
		else:
			session['logged_in'] = True
			flash('You\'ve been successfully logged in.')
			return redirect(url_for('admin.index'))
	return render_template('login.html', error=error)

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('You\'ve been successfully logged out.')
	return 'Logout Page.'

@app.route('/')
def home():
	return redirect(url_for('index'))

@app.route('/index/')
def index():
	# Featured | query_latest_5
	# Events   | query_upcoming_5
	# Posts    | query_featured_5
	#  -- Could just reprint 'featured' articles here

	return render_template('index_update.html')
	# return render_template('index.html', featured=featured, events=events, \
		# posts=posts)

# Later: Use Flatpages (?) and/or Freeze
@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
	form = ContactForm(request.form)

	if request.method == 'POST' and form.validate():
		msg = Message(form.subject.data, \
			sender='fsengsta@princeton.edu',\
			recipients=['fsengsta@princeton.edu'])
		msg.body = """
		From: %s <%s>
		%s
		""" % (form.name.data, form.email.data, form.message.data)
		mail.send(msg)
		return form.redirect('index')

	elif request.method == 'GET':
		return render_template('contact.html', form=form)

	else:
		flash('Please fill out all required fields.')
		return render_template('contact.html', form=form)

@app.route('/subscribe/', methods=['GET', 'POST'])
def subscribe():
	form = SubscribeForm(request.form)

	# Add user to database
	if request.method == 'POST' and form.validate():
		flash('Thank you for signing up!')
		flash('You are now being redirected to the home page.')
		return form.redirect('index')

	elif request.method == 'GET':
		return render_template('subscribe.html', form=form)

	else:
		flash('Please fill out all required fields.')
		return render_template('subscribe.html', form=form)

@app.route('/issues/')
def issues():
	q = db.session.query(User)
	articles = q.all()
	return render_template('issues.html', articles=articles)

@app.route('/blog/')
def blog():
	posts = 1;
	return render_template('blog.html', posts=posts)

@app.route('/events/')
def events():
	return render_template('events.html')

##############################
#    Administrative Views    #
##############################

class AuthIndex(BaseView):
	def is_accessible(self):
		return session['logged_in'] == True

	def _handle_view(self, name, **kwargs):
		if not self.is_accessible():
		  return redirect(url_for('login'))

class AdminIndex(AuthIndex, AdminIndexView):   
  @expose('/')
  def index(self):
  	return self.render('admin/index.html')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Event, db.session))