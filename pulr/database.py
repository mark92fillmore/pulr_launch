import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
	db_engine = create_engine('sqlite:///' + os.path.join(basedir, 'tmp/database.db'))
else:
	db_engine = create_egine(os.environ['DATABASE_URL'])

db_session = scoped_session(sessionmaker(autocommit=False,\
	autoflush=False,\
	bind=db_engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	import models	
	Base.metadata.create_all(bind=db_engine)