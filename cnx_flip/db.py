from sqlalchemy import Table, Column, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

# To use the ORM we will find we'll need:
# * subclasses of declarative base for our models
# * a session to query for those models and persist them
 
# sqlalchemy magic to create a base class for our orm models, giving them
# the power to persist themselves in the db.
# http://docs.sqlalchemy.org/ru/latest/orm/tutorial.html#declare-a-mapping

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()

class Root(object):
    def __init__(self, request):
        pass 

    

