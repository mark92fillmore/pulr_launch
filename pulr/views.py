from . import admin, app, db, mail
from .database import db_session
from .models import User, Note, Announcement, Post, Issue, Article, Event
from flask import abort, flash, request, redirect, render_template, \
     session, url_for
from flask.ext.admin import Admin, AdminIndexView, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.mail import Message, Mail
from flaskext.uploads import UploadSet, DOCUMENTS
from .forms import ContactForm, SubscribeForm
from flask_wtf import Form
from wtforms import validators

######################
#  Helper Functions  #
######################
def make_month(x):
    return {
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }[x]


####################
#    Login Views   #
####################

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

###################
#    Home Views   #
###################

@app.route('/')
def home():
	return redirect(url_for('index'))

@app.route('/index/')
def index():
	announcements = db.session.query(Announcement).all()
	a = sorted(announcements, key=lambda announcement: announcement.publication_date, reverse=True)
	notes = db.session.query(Note).all()
	c = sorted(notes, key=lambda note: note.publication_date, reverse=True)
	note = c[0]

	for announcement in a:
		pd = announcement.publication_date
		month = make_month(str(pd.month))
		announcement.date_string = month + " " + str(pd.day) + ", " + str(pd.year)  

	return render_template('index_update.html', announcements=a, note=note)

@app.route('/about/')
def about():
	return render_template('about.html')

###################
#    Form Views   #
###################

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
	form = ContactForm(request.form)

	if request.method == 'POST' and form.validate():
		msg = Message(form.subject.data, \
			sender='pulr.manager@gmail.com', \
			recipients=['pulr.manager@gmail.com'])
		msg.body = """
		From: %s <%s>
		%s
		""" % (form.name.data, form.email.data, form.message.data)
		mail.send(msg)
		flash('Your message was sent successfully!')
		return form.redirect('contact')

	elif request.method == 'GET':
		return render_template('contact.html', form=form)

	else:
		return render_template('contact.html', form=form)

@app.route('/subscribe/', methods=['GET', 'POST'])
def subscribe():
	form = SubscribeForm(request.form)

	if request.method == 'POST' and form.validate():
		user = User(form.name.data, form.email.data)
		db.session.add(user)
		db.session.commit()
		flash('You have been registered successfully!')
		return redirect('subscribe')

	elif request.method == 'GET':
		return render_template('subscribe.html', form=form)

	else:
		return render_template('subscribe.html', form=form)

######################
#    Content Views   #
######################

@app.route('/issues/')
def issues():
	issue_id = request.args.get('i_id')
	article_id = request.args.get('a_id')
	q = db.session.query(Issue)
	query = q.all()
	issues = sorted(query, key=lambda issue: issue.publication_date, reverse=True)

	for issue in issues:
		pd = issue.publication_date
		month = make_month(str(pd.month))
		issue.date_string = month + " " + str(pd.day) + ", " + str(pd.year)

	if issue_id is None:
		i = issues[0]
		a = None
		articles = i.articles
		return render_template('issues.html', issues=issues, i=i, articles=articles, a=a)
	else: 
		i = q.filter(Issue.id == int(issue_id)).all()[0]
		if article_id is None:
			articles = i.articles
			a = None
			return render_template('issues.html', issues=issues, i=i, articles=articles, a=a)
		else:
			a = db.session.query(Article).filter(Article.id == int(article_id)).all()[0]
			articles = []
			return render_template('issues.html', issues=issues, i=i, articles=articles, a=a)

@app.route('/blog/')
def blog():
	page = request.args.get('page')
	page_size = 10
	if page is None:
		page = 0
		newer = None
	else:
		page = int(page)
		newer = page - 1
	first_post = page * page_size
	q = db.session.query(Post)
	posts = q.all()
	p = sorted(posts, key=lambda announcement: announcement.publication_date, reverse=True)

	for blog in p:
		pd = blog.publication_date
		month = make_month(str(pd.month))
		blog.date_string = month + " " + str(pd.day) + ", " + str(pd.year)

	list_size = len(p)
	next_page = first_post + page_size
	if (next_page >= list_size):
		next_page = list_size
		older = None
	else:
		older = page + 1
	posts = p[first_post:next_page]

	return render_template('blog.html', posts=posts, older=older, newer=newer)

@app.route('/events/')
def events():
	return render_template('events.html')

##############################
#    Administrative Views    #
##############################

class AuthIndex(BaseView):
	def is_accessible(self):
		if session['logged_in'] == True:
			return True
		return False 

	def _handle_view(self, name, **kwargs):
		if not self.is_accessible():
		  return redirect(url_for('login'))

class AdminIndex(AuthIndex):
	@expose('/')
	def index(self):
		return self.render('admin/index.html')


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Note, db.session))
admin.add_view(ModelView(Announcement, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Issue, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Event, db.session))
