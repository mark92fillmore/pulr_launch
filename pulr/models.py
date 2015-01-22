import os
from .database import Base
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, UnicodeText

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(String(128), unique=True)
	email = Column(String(64), unique=True)

	def __init__(self, name=None, email=None):
		self.name = name
		self.email = email

	def __repr__(self):
		return '<Name: %s>' % self.name

class Post(Base):
	__tablename__ = 'blog_posts'

	id = Column(Integer, primary_key=True)
	title = Column(String(64), unique=True, index=True)
	byline = Column(String(128))
	publication_date = Column(Date)
	content = Column(UnicodeText())
	# featured_image = Column()

	def __repr__(self):
		return '<Title: %s | Publication Date: %s' \
		  % (self.title, self.publication_date)

class Article(Base):
	__tablename__ = 'article'

	id = Column(Integer, primary_key=True)
	title = Column(String(64), unique=True, index=True)
	byline = Column(String(128))
	publication_date = Column(Date)
	content = Column(UnicodeText(), nullable=False)
	# featured_image = Column()

	def __repr__(self):
		return '<Title: %s | Publication Date: %s' \
		  % (self.title, self.publication_date)

class Event(Base):
	__tablename__ = 'events'

	id = Column(Integer, primary_key=True)
	title = Column(String(64))
	slug = Column(String(256))
	event_date = Column(Date)