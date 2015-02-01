from flask import request, url_for, redirect
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, \
  FileField, HiddenField, validators
from wtforms.validators import DataRequired, ValidationError
from urlparse import urlparse, urljoin

def is_safe_url(target):
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))
	return test_url.scheme in ('http', 'https') and \
	       ref_url.netloc == test_url.netloc

def get_redirect_target():
	for target in request.args.get('next'), request.referrer:
		if not target:
			continue
		if is_safe_url(target):
			return target

class RedirectForm(Form):
	next = HiddenField()

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		if not self.next.data:
			self.next.data = get_redirect_target() or ''

	def redirect(self, endpoint='index', **values):
		if is_safe_url(self.next.data):
			return redirect(self.next.data)
		target = get_redirect_target()
		return redirect(target or url_for(endpoint, **values))

class SubscribeForm(RedirectForm):
  name = StringField('Name', [validators.DataRequired('Please enter your name.')])
  email = StringField('Email', \
  	[validators.DataRequired('Please enter a valid email address.'), \
  	validators.Email()])
  submit = SubmitField('Subscribe')

class ContactForm(RedirectForm):
  name = StringField('Name', [validators.DataRequired('Please enter a name.')])
  subject = StringField('Subject')
  email = StringField('Email', \
  	[validators.DataRequired('Please enter a valid email.')]) 
  message = TextAreaField('Your message . . . ', \
  	[validators.DataRequired('Please enter a message in the text area.')])
  submit = SubmitField('Send Message')