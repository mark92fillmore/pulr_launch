import os
from .database import db_session, db_engine
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, create_engine, \
Integer, String, Date, UnicodeText,LargeBinary, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker,\
relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# basedir = os.path.abspath(os.path.dirname(__file__))
# if os.environ.get('DATABASE_URL') is None:
# 	db_engine = create_engine('sqlite:///' + os.path.join(basedir, 'tmp/database.db'))
# else:
# 	db_engine = create_egine(os.environ['DATABASE_URL'])

# db_session = scoped_session(sessionmaker(autocommit=False,\
# 	autoflush=False,\
# 	bind=db_engine))

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# Base = declarative_base()
# Base.query = db_session.query_property()

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(128), unique=True)
	email = Column(String(128), unique=True)

	def __init__(self, name=None, email=None):
		self.name = name
		self.email = email

	def __repr__(self):
		return '<Name: %s>' % self.name

# Deprecated #

#class Note(Base):
#	__tablename__ = 'note'
#
#	id = Column(Integer, primary_key=True, autoincrement=True)
#	title = Column(String(128), unique=False, index=True)
#	publication_date = Column(Date)
#	content = Column(UnicodeText())
#	name = Column(String(128))
#
#	def __repr__(self):
#		return '<Title: %s | Publication Date: %s>' \
#		  % (self.title, self.publication_date)

class Letter(Base):
	__tablename__ = 'letter'

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(128), unique=False, index=True)
	publication_date = Column(Date)
	content = Column(UnicodeText())
	signature_image_url = Column(String(1024))
	name = Column(String(128))

	def __repr__(self):
		return '<Title: %s | Publication Date: %s>' \
		  % (self.title, self.publication_date)

class Announcement(Base):
	__tablename__ = 'announcements'

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(128), unique=False, index=True)
	publication_date = Column(Date)
	content = Column(UnicodeText())

	def __repr__(self):
		return '<Title: %s | Publication Date: %s>' \
		  % (self.title, self.publication_date)

class Post(Base):
	__tablename__ = 'blog_posts'

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(256), unique=True, index=True)
	byline = Column(String(128))
	publication_date = Column(Date)
	featured_post = Column(Boolean)
	content = Column(UnicodeText())
	url = Column(String(128), unique=True, index=True)
	image_url = Column(String(1024))

	def __repr__(self):
		return '<Title: %s | Publication Date: %s>' \
		  % (self.title, self.publication_date)

class Issue(Base):
	__tablename__ = 'issue'

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(256), unique=True, index=True, nullable=False)
	publication_date = Column(Date, nullable=False)
	editor_in_chief = Column(String(128))
	editorial_board = Column(UnicodeText())
	articles = relationship('Article', backref='issue',
                                lazy='dynamic')

	def __repr__(self):
		return '<Title: %s | Publication Date: %s>' \
		  % (self.title, self.publication_date)


class Article(Base):
	__tablename__ = 'article'

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(256), unique=True, index=True, nullable=False)
	byline = Column(String(128), nullable=False)
	publication_date = Column(Date, nullable=False)
	featured_post = Column(Boolean)
	abstract = Column(UnicodeText())
	content = Column(UnicodeText(), nullable=False)
	image_url = Column(String(1024))
	footnotes = Column(UnicodeText())
	works_cited = Column(UnicodeText())
	issue_id = Column(Integer, ForeignKey('issue.id'))

	def __repr__(self):
		return '<Title: %s>' % (self.title)


class Event(Base):
	__tablename__ = 'events'

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(64))
	slug = Column(String(256))
	event_date = Column(Date)
	image_url = Column(String(1024))


def init_db():
	Base.metadata.create_all(bind=db_engine)

#init_db()

if __name__ == '__main__':
	manager.run()
