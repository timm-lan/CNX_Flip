from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

from cnx_flip.db import Base

class Card(Base):
    __tablename__= 'cards'
    id = Column(Integer, primary_key=True)
    term = Column(Text)
    definition = Column(Text)
    deck_id = Column(Integer, ForeignKey('decks.id'))