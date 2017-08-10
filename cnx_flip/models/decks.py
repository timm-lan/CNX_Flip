from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

from cnx_flip.db import Base

class Deck(Base):
    __tablename__= 'decks'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    # one to many
    user_id = Column(Integer, ForeignKey('users.id'))
    color = Column(Text)
    cards = relationship("Card")