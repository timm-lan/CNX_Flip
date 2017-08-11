from cnx_flip.models import *
from cnx_flip.db import *
import transaction
import urllib2
import json
import xml.etree.ElementTree as ET

def test_db():
    """
    Add default decks on initializing database
    """
    mockCardsInTestDeck1 = {
        'deck_name': 'test_deck1',
        'cards': [
            Card(term='term1', definition='def1'),
            Card(term='term2', definition='def2'),
            Card(term='term3', definition='def3'),
            Card(term='term4', definition='def4'),
            Card(term='term5', definition='def5'),
            Card(term='term6', definition='def6'),
            Card(term='term7', definition='def7')
        ]
    }
    mockCardsInTestDeck2 = {
        'deck_name': 'test_deck2',
        'cards':[
            Card(term='TERM1', definition='DEF1'),
            Card(term='TERM2', definition='DEF2'),
            Card(term='TERM3', definition='DEF3'),
            Card(term='TERM4', definition='DEF4'),
            Card(term='TERM5', definition='DEF5'),
            Card(term='TERM6', definition='DEF6'),
            Card(term='TERM7', definition='DEF7')
        ]
    }
    mockCardsInTestDeck3 = {
        'deck_name': 'test_deck3',
        'cards':[
            Card(term='haha1', definition='DEFINITION1'),
            Card(term='haha2', definition='DEFINITION2'),
            Card(term='haha3', definition='DEFINITION3'),
            Card(term='haha4', definition='DEFINITION4'),
            Card(term='haha5', definition='DEFINITION5'),
            Card(term='haha6', definition='DEFINITION6'),
            Card(term='haha7', definition='DEFINITION7')
        ]
    }

    mockdecks = [mockCardsInTestDeck1, mockCardsInTestDeck2, mockCardsInTestDeck3]
    user_name = 'admin'
    
    with transaction.manager:
        for deck in mockdecks:
            # add cards
            deck_tmp = DBSession.query(Deck).filter(Deck.title==deck['deck_name'])
            if deck_tmp.count() == 0:
                deck_tmp = Deck(title=deck['deck_name'], color='green')
            else:
                deck_tmp = deck_tmp.first()
            deck_tmp.cards = deck['cards']
            #If overriding cards is unwanted, we have to use deck_tmp + deck['cards']

            # link to the admin user
            admin = DBSession.query(User).filter(User.user_name==user_name)
            if admin.count == 0:
                admin = User(user_name=user_name)
            else:
                admin = admin.first()
            admin.decks.append(deck_tmp)

def importCardsFromCnxDb(uuid, deckid, cnxdbHost):
    """
    Pull terms and definition from CNX Archive and store them as decks in the database
    :param uuid: uuid of a openstax textbook module
    :param deckid: the id of a deck
    :param cnxdbHost: host url
    """
    # Build the request.
    # http://localhost:6543/xpath?id=e79ffde3-7fb4-4af3-9ec8-df648b391597&q=//*[local-name()=%22meaning%22]
    request_headers = {
        "Accept" : "application/json"

        # Unfinished authentication
        # "Authorization" : "Bearer 6879-1aVn-THALZjt82mlGqFRZZKMDV4Db1pGy0iO5xjUbeo"
    }
    request_url = cnxdbHost + "/xpath?id=" + uuid + "&q=//*[local-name()=%22definition%22]"
    request = urllib2.Request(request_url, headers=request_headers)
    response = urllib2.urlopen(request).read()
    response = json.loads(response)
    
    for module in response['results']:
        for term_def_wrap in module['xpath_results']:
            tree = ET.fromstring(term_def_wrap.encode('utf-8'))
            if len(tree) < 2 or tree[1].text == None:
                continue;

            term = tree[0].text.encode('utf-8')
            definition = tree[1].text.encode('utf-8')
            with transaction.manager:
                deck_tmp = DBSession.query(Deck).filter(Deck.id==deckid).first()
                card_tmp = Card(term=term, definition=definition, deck_id=deckid)
                deck_tmp.cards.append(card_tmp)