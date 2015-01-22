from . import app, db, mail
from .database import db_session
from flask import abort, flash, request, redirect, render_template, \
     session, url_for
from flask.ext.mail import Message, Mail
from .forms import ContactForm, SubscribeForm
from flask_wtf import Form
from wtforms import validators

###################
#    Base Views   #
###################

@app.route('/login/')
def login():
	return 'Login Page'

@app.route('/logout/')
def logout():
	return 'Logout Page'

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
	articles = 1;
	return render_template('issues.html', articles=articles)

@app.route('/blog/')
def blog():
	posts = 1;
	return render_template('blog.html', posts=posts)

# Static
# For now: styleguide.html contains copy
# Later: Use Flatpages (?) and/or Freeze
@app.route('/events/')
def events():
	return render_template('events.html')

#################
#    Dynamic    #
#################