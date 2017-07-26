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

# DBSession = scoped_session(
#     sessionmaker())
DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()


# map_table_userdeck = Table('userdeck_map', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('deck_id', Integer, ForeignKey('decks.id'))
# )
# map_table_deckcard = Table('deckcard_map', Base.metadata,
#     Column('deck_id', Integer, ForeignKey('decks.id')),
#     Column('card_id', Integer, ForeignKey('cards.id'))
# )
class User(Base):
    __tablename__= 'users'
    
    # autoincrement has to be False

    id = Column(Integer, primary_key=True)
    user_name = Column(Text, unique=True)
    # This is for many-many
    # decks = relationship("Deck", secondary=map_table_userdeck, back_populates="users")
    decks = relationship("Deck")

    # decks = relationship("Deck", back_populates="users")
    
    
# Deckcome is the actual user deck
# class DeckCombo(Base):
#     __tablename__= 'deckcombos'
#     id = Column(Integer, primary_key=True)
#     deck_combo_name = Column(Text, unique=True) 
#     color = Column(Text)
#     # decks = relationship("Deck", secondary=map_table_deckcombodeck)
#     cards = relationship("Card", secondary=map_table_deckcombocard)

class Deck(Base):
    __tablename__= 'decks'
    id = Column(Integer, primary_key=True)
    title = Column(Text, unique=True)
    # one to many
    user_id = Column(Integer, ForeignKey('users.id'))
    color = Column(Text)
    cards = relationship("Card")

    # user = relationship("User", back_populates="decks")
    # cards = relationship("Card", back_populates="decks")

    # This is for many to many
    # cards = relationship("Card", secondary=map_table_deckcard, back_populates="decks")
    # users = relationship("User", secondary=map_table_userdeck, back_populates="decks")

class Card(Base):
    __tablename__= 'cards'
    id = Column(Integer, primary_key=True)
    term = Column(Text)
    definition = Column(Text)

    deck_id = Column(Integer, ForeignKey('decks.id'))
   
    # decks = relationship("Deck", back_populates="cards")

    # This is for many to many
    # decks = relationship("Deck", secondary=map_table_deckcard, back_populates="cards")

# ??
class Root(object):
#     __acl__ = [(Allow, Everyone, 'view'),
#                (Allow, 'group:editors', 'edit')]
# 
    def __init__(self, request):
        pass 

    

