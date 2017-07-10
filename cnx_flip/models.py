from sqlalchemy import Table, Column, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

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

map_table_deckcard = Table('deckcard_map', Base.metadata,
    Column('deck_id', Integer, ForeignKey('decks.id')),
    Column('card_id', Integer, ForeignKey('cards.id'))
)

map_table_deckcombodeck = Table('deckcombodeck_map', Base.metadata,
    Column('deckcombo_id', Integer, ForeignKey('deckcombos.id')),
    Column('deck_id', Integer, ForeignKey('decks.id'))
)

map_table_userdeckcombo = Table('userdeckcombo_map', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('deckcombo_id', Integer, ForeignKey('deckcombos.id'))
)

class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(Text, unique=True) 
    deckcombos = relationship("DeckCombo", secondary=map_table_userdeckcombo)
    # decks = relationship("cards")

class DeckCombo(Base):
    __tablename__= 'deckcombos'
    id = Column(Integer, primary_key=True)
    deck_combo_name = Column(Text, unique=True) 
    color = Column(Text)
    decks = relationship("Deck", secondary=map_table_deckcombodeck)

class Deck(Base):
    __tablename__= 'decks'
    id = Column(Integer, primary_key=True)
    title = Column(Text, unique=True)
    cards = relationship("Card", secondary=map_table_deckcard)

class Card(Base):
    __tablename__= 'cards'
    id = Column(Integer, primary_key=True)
    term = Column(Text, unique=True)
    definition = Column(Text)

# ??
class Root(object):
#     __acl__ = [(Allow, Everyone, 'view'),
#                (Allow, 'group:editors', 'edit')]
# 
    def __init__(self, request):
        pass 

    

