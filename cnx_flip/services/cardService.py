from cnx_flip.models import * #DBSession, Card, Base
from cnx_flip.db import *
from .requestService import *
from .formatResultsService import *
from .responseService import *

def card_http_request(request, origin_url):    
    """
    Create, Update or Delete a card via POST, PUT, DELETE methods
    
    request: http request 
    origin_url: host url
    """
    method, params, url_param = get_params(request)

    # Answer Chrome
    if method == 'OPTIONS':
        return preflight_handler(request, origin_url)

    # Add a card
    if method == "POST":
        print "YOU ARE ADDING A CARD"
        params = json.loads(params)

        # Error handler
        if ("term" not in params) or ("definition" not in params) or (
            "deckid" not in params):
            return exc.HTTPBadRequest()

        deckid = int(params['deckid'])
        userid = int(url_param['userid'])
        print "USER ID is " + str(userid)

        with transaction.manager:
            deck_list = DBSession.query(Deck).filter(
                Deck.id == deckid and Deck.user_id == userid)

            # Error handler: check if deck exists
            if deck_list.count() == 0:
                return exc.HTTPNotFound()

            db_deck = deck_list.first()
            new_card = Card(term=params['term'],
                            definition=params['definition'])
            DBSession.add(new_card)
            db_deck.cards.append(new_card)

            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['color'] = str(db_deck.color)
            results['title'] = str(db_deck.title)

            # Return results
            response = update_header(json.dumps(results), origin_url)
            return response

    # Update a card
    elif method == "PUT":
        print "YOU ARE UPDATING A CARD"

        params = json.loads(params)
        cardid = int(url_param['cardid'])
        with transaction.manager:
            card_list = DBSession.query(Card).filter(Card.id == cardid)

            # Error handler: check if card exists
            if card_list.count() == 0:
                return exc.HTTPNotFound()

            db_card = card_list.first()
            deckid = db_card.deck_id
            db_card.term = params['term']
            db_card.definition = params['definition']

            deck_list = DBSession.query(Deck).filter(Deck.id == deckid)

            # Error handler: check if the card has a corresponding deck
            if deck_list.count() == 0:
                return exc.HTTPNotFound()
            db_deck = deck_list.first()

            # build the response
            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['color'] = str(db_deck.color)
            results['title'] = str(db_deck.title)

            # Return results
            response = update_header(json.dumps(results), origin_url)
            return response

    # Delete a card
    elif method == 'DELETE':
        print "YOU ARE DELETING A CARD"

        cardid = int(url_param['cardid'])
        with transaction.manager:
            card_list = DBSession.query(Card).filter(Card.id == cardid)
            #Error handler: check if card exists
            if card_list.count() == 0:
                return exc.HTTPNotFound()

            db_card = card_list.first()
            deckid = db_card.deck_id

            DBSession.query(Card).filter(Card.id == cardid).delete(
                synchronize_session='evaluate')
            db_deck = DBSession.query(Deck).filter(Deck.id == deckid).first()

            # Build the response of a deck dictionary
            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['color'] = str(db_deck.color)
            results['title'] = str(db_deck.title)

            # Return results
            response = update_header(json.dumps(results), origin_url)
            return response
    return {'status': 'NOT OK'}