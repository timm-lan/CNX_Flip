import json
import pyramid.httpexceptions as exc
import random
import transaction

from pyramid.view import view_config
from pyramid.response import Response
from mock_pull_engine import *
from .models import * #DBSession, Card, Base

USER = 'admin'
ORIGIN_URL = 'http://localhost:3000'
COLORS = ["#15837D", "#EF5F33", "#1B2152", "#1BB3D3",\
          "#B30B26", "#FDB32F", "#F0C916", "#65A234", "#8f8f8f"]

def card2dict(cardResult):
    """
    Convert a RowProxy Object into json
    """
    d = {'cards': []}
    for card_row in cardResult:
        card = {}
        card['id'] = card_row.id
        card['term'] = card_row.term
        card['definition'] = card_row.definition
        d['cards'].append(card)
    return d


def preflight_handler(request):
    response = Response()
    response.headers.update({
        'Access-Control-Allow-Origin': ORIGIN_URL, \
        "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS', \
        "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"
    })
    return response


def update_header(body):
    """
    Updates header
    Input: header in json format
    Output: response with headers
    """
    response = Response(body)
    response.headers.update({
        'Access-Control-Allow-Origin': ORIGIN_URL, \
        "Access-Control-allow-methods": 'GET, POST, PUT, DELETE, OPTIONS', \
        "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"
    })
    return response


def get_params(request):
    method = request.method
    params = request.body
    url_param = request.matchdict
    return method, params, url_param


@view_config(route_name='home', renderer='templates/index.html.jinja2')
def my_view(request):
    """
    Test to see if the server is running
    """
    return {'project': 'cnx_flip'}


@view_config(route_name='update_from_db', renderer='json')
def update(request):
    """
    Populate the database
    """
    put_stuff_in_db()
    return {'update': 'success'}


def get_decks(request):
    """
    Helper function for loading a list of decks on the deck page
    """
    method, params, url_param = get_params(request)

    # To answer Chrome
    if method == 'OPTIONS':
        return preflight_handler(request)

    # Load the decks
    decks = [];
    with transaction.manager:
        decks_query = DBSession.query(Deck).all()
        for deck_object in decks_query:
            deck = card2dict(deck_object.cards)
            deck['title'] = str(deck_object.title)
            deck['color'] = str(deck_object.color)
            deck['id'] = int(deck_object.id)
            decks.append(deck)
    response = update_header(body=json.dumps(decks))
    return response


@view_config(route_name='api_deck', renderer='json')
def api_deck(request):
    """
    Get, Create, Update or Delete a deck via
    GET, POST, PUT, DELETE
    Get a list of decks
    """
    method, params, url_param = get_params(request)

    # To answer Chrome
    if method == 'OPTIONS':
        return preflight_handler(request)

    # Get a deck
    if method == "GET":
        if len(url_param['deckid']) == 0:
            return get_decks(request)
        deck_idx = url_param["deckid"]
        with transaction.manager:
            target_deck = DBSession.query(Deck).filter(
                Deck.id == deck_idx).first()
            deck = card2dict(target_deck.cards)
            deck['title'] = str(target_deck.title)
            deck['color'] = str(target_deck.color)
            deck['id'] = deck_idx

            response = update_header(body=json.dumps(deck))
            return response

    # Create a new deck
    elif method == 'POST':
        with transaction.manager:
            user_list = DBSession.query(User).filter(User.user_name==USER)

            # Error handler: check if user exists
            if user_list.count() == 0:
                return exc.HTTPNotFound()
            user = user_list.first()

            # Assign default title and color to the new deck
            deck_name = "untitled"
            same_title_deck = DBSession.query(Deck)\
                .filter(Deck.title == deck_name and Deck.user_id == user.id)

            # Create a new deck name that doesn't conflict with existing deck names
            i = 1
            while same_title_deck.count() != 0:
                deck_name = "untitled" + " (" + str(i) + ")"
                same_title_deck = DBSession.query(Deck)\
                    .filter(Deck.title == deck_name and Deck.user_id == user.id)
                i += 1

            # Assign a random color to the new deck
            deck_color = random.choice(COLORS)

            # Build the new deck
            new_deck = Deck(title=deck_name, color=deck_color)
            DBSession.add(new_deck)
            user.decks.append(new_deck)

            # Build response
            results = {}
            results['cards'] = []
            results['id'] = int(new_deck.id)
            results['title'] = str(new_deck.title)
            results['color'] = str(new_deck.color)

            response = update_header(body=json.dumps(results))
        return response

    # Update a deck
    elif method == 'PUT':
        # Error handling: check correct query
        # if ("title" not in params) or ("color" not in params) or (
        #     "cards" not in params) or ("id" not in params):
        #     return exc.HTTPBadRequest()
        # params = request.body
        params = json.loads(params)
        print "PARAMS ARE " + str(params)

        deck_id = url_param['deckid']
        with transaction.manager:
            deck_list = DBSession.query(Deck).filter(Deck.id == deck_id)

            # Error handler: check if deck exists
            if deck_list.count() == 0:
                return exc.HTTPNotFound()

            db_deck = deck_list.first()
            same_title_deck = DBSession.query(Deck)\
                .filter(Deck.title == params['title'] and Deck.user_id == db_deck.user_id)

            # Error handler: check for duplicate titles
            if same_title_deck.count() != 0:
                return exc.HTTPConflict()

            db_deck.title = params['title']
            db_deck.color = params['color']

            # Build the response
            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['title'] = str(db_deck.title)
            results['color'] = str(db_deck.color)

            response = update_header(body=json.dumps(results))
            return response

    # Delete a deck
    elif method == 'DELETE':
        deck_id = url_param['deckid']
        with transaction.manager:
            deck_list = DBSession.query(Deck).filter(Deck.id==deck_id)

            # Error handler: check if deck exists
            if deck_list.count() == 0:
                return exc.HTTPNotFound()

            # Delete cards in that deck first to avoid foreign key constraints
            DBSession.query(Card).filter(Card.deck_id==deck_id)\
                .delete(synchronize_session="evaluate")
            DBSession.query(Deck).filter(Deck.id==deck_id)\
                .delete(synchronize_session="evaluate")
            return {'status': 'delete successful'}
    return {'status': 'NOT OK'}


@view_config(route_name='api_card', renderer='json')
def api_card(request):
    """
    Create, Update or Delete a card
    via POST, PUT, DELETE methods
    """
    method, params, url_param = get_params(request)

    # Answer Chrome
    if method == 'OPTIONS':
        return preflight_handler(request)

    # Add a card
    if method == "POST":
        params = json.loads(params)

        if ("term" not in params) or ("definition" not in params) or (
            "deckid" not in params):
            return exc.HTTPBadRequest()

        deckid = int(params['deckid'])
        with transaction.manager:
            deck_list = DBSession.query(Deck).filter(Deck.id == deckid)

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
            response = update_header(body=json.dumps(results))
            return response

    # Update a card
    elif method == "PUT":
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
            response = update_header(body=json.dumps(results))
            return response

    # Delete a card
    elif method == 'DELETE':
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

            # build the response of a deck dictionary
            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['color'] = str(db_deck.color)
            results['title'] = str(db_deck.title)

            # Return results
            response = update_header(body=json.dumps(results))
            return response
    return {'status': 'NOT OK'}

# @view_config(route_name='add_user', renderer = 'json')
# def add_user(request):
#     req_post = request.POST
#     user_name = str(req_post['user_name'])
#     with transaction.manager:
#         model = User(user_name=user_name)
#         DBSession.add(model)
#     return {'add user': 'success'}  

