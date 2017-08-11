from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

from cnx_flip.db import Base

class User(Base):
    __tablename__= 'users'
    # autoincrement has to be False
    id = Column(Integer, primary_key=True)
    user_name = Column(Text, unique=True)
    decks = relationship("Deck")