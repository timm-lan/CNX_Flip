import pyramid.httpexceptions as exc

import json

from pyramid.view import view_config
from .models import * #DBSession, Card, Base
import transaction
from pyramid.response import Response
from mockdecks import USER1_DECKS
from mock_pull_engine import *
from mock_pull_engine import *

USER = 'admin'
def card2dict(cardResult):
    """
        Convert a RowProxy Object into a json
    """
    d = {'cards': []}
    for card_row in cardResult:
        card = {}
        card['id'] = card_row.id
        card['term'] = card_row.term
        card['definition'] = card_row.definition
        d['cards'].append(card)
    return d

# cards = [
#       { 'id': 1, 'term': 'Test term 1', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
#       { 'id': 2, 'term': 'Test term 2', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
#       { 'id': 3, 'term': 'Test term 3', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
#       { 'id': 4, 'term': 'Test term 4', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
#       { 'id': 5, 'term': 'Test term 5', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
#     ]
# decks = [
#       { 'id': 1, 'name': "Test Deck 1", 'cards': cardss, 'color': 'Green'},
#       { 'id': 2, 'name': "Test Deck 2", 'cards': cardss, 'color': '#8f8f8f'},
#       { 'id': 3, 'name': "Test Deck 3", 'cards': cardss, 'color': '#8f8f8f'},
#       { 'id': 4, 'name': "Test Deck 4", 'cards': cardss, 'color': '#8f8f8f'},
#       { 'id': 5, 'name': "Test Deck 5", 'cards': cardss, 'color': '#8f8f8f'},]


@view_config(route_name='home', renderer = 'templates/index.html.jinja2')
def my_view(request):
    return {'project': 'cnx_flip'}


@view_config(route_name='add_card', renderer = 'templates/success.html.jinja2')
def success_add_card_view(request):
    req_post = request.POST
    term = str(req_post['term'])
    definition = str(req_post['definition'])
    with transaction.manager:
        model = Card(term=term, definition=definition)
        DBSession.add(model)
    return {'project': 'cnx_flip'}


@view_config(route_name='add_card_tmp', renderer = 'json')
def add_card_view(request):
    req_post = request.POST
    term = str(req_post['term'])
    definition = str(req_post['definition'])
    deck_name = str(req_post['deck_name'])
    user_name = str(req_post['user_name'])

    # with transaction.manager:
    #     for user in DBSession.query(User).filter(User.user_name==user_name):
    #         user.decks = [deck1, deck2]
        
        # model = Card(term=term, definition=definition)
        # DBSession.add(model)
    return {'project': 'cnx_flip'}


@view_config(route_name='update_from_db', renderer = 'json')
def update(request):
    put_stuff_in_db()
    return {'update': 'success'}


@view_config(route_name='api_deck', renderer = 'json')
def api_deck(request):
    method = request.method
    params = request.body
    print request.method

    # To answer the chrome?
    if method == 'OPTIONS':
        response = Response()
        response.headers.update({'Access-Control-Allow-Origin': '*', \
            "Access-Control-Allow-Method": 'GET, POST, PUT, DELETE, OPTIONS', \
            "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
        return response
    
    params = json.loads(params)

    # create a deck
    if method == 'POST':
        if ("title" not in params) or ("color" not in params) or (
            "cards" not in params):
            return exc.HTTPBadRequest()

        with transaction.manager:
            user_list = DBSession.query(User).filter(User.user_name == "admin")
            if user_list.count() == 0:
                return exc.HTTPBadRequest()
            user = user_list.first()

            new_deck = Deck(title=params['title'], color=params['color'])
            DBSession.add(new_deck)
            user.decks.append(new_deck)

            # build response
            results = {}
            results['cards'] = []
            results['id'] = int(new_deck.id)
            results['title'] = str(new_deck.title)
            results['color'] = str(new_deck.color)

            response = Response(body=json.dumps(results))
            response.headers.update({'Access-Control-Allow-Origin': '*', \
                "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})

    # Edit a deck
    elif method == 'PUT':
        # Error handling
        if ("title" not in params) or ("color" not in params) or (
            "cards" not in params) or ("id" not in params):
            return exc.HTTPBadRequest()
        elif type(params["id"]) != int:
            return exc.HTTPBadRequest

        deck_id = params['id']
        with transaction.manager:
            deck_list = DBSession.query(Deck).filter(Deck.id==int(deck_id))
            if deck_list.count() == 0:
                return exc.HTTPBadRequest

            db_deck = deck_list.first()
            db_deck.title = params['title']
            db_deck.color = params['color']

            # build the response
            results = {}
            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['title'] = str(db_deck.title)
            results['color'] = str(db_deck.color)

            response = Response(body=json.dumps(results))
            response.headers.update({'access-control-allow-origin': '*',
                "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
            return response

    # Delete a deck
    elif method == 'DELETE':
        # Error handler
        if "id" not in params:
            return exc.HTTPBadRequest()
        elif type(params["id"]) != int:
            return exc.HTTPBadRequest

        deck_id = params['id']
        with transaction.manager:
            deck = DBSession.query(Card).filter(Card.deck_id==deck_id)
            if deck.count() == 0:
                return exc.HTTPNotFound

            # delete cards first to avoid foreign key constraints
            DBSession.query(Card).filter(Card.deck_id==deck_id).delete(synchronize_session="evaluate")
            DBSession.query(Deck).filter(Deck.id==deck_id).delete(synchronize_session="evaluate")

    return {'status': 'NOT OK'}


@view_config(route_name='api_card', renderer = 'json')
def api_card(request):
    method = request.method
    params = request.body
    print request.method

    # To answer the chrome?
    if method == 'OPTIONS':
        response = Response()
        response.headers.update({'Access-Control-Allow-Origin': '*', \
            "Access-Control-Allow-Method": 'GET, POST, PUT, DELETE, OPTIONS', \
            "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
        return response

    # params = request.json_body
    params = json.loads(params)

    # Create card
    if method == 'POST':
        if ("term" not in params) or ("definition" not in params) or ("deckid" not in params):
            return exc.HTTPBadRequest()
        elif type(params["deckid"]) != int:
            return exc.HTTPBadRequest

        deckid = int(params['deckid'])
        with transaction.manager:
            deck_list= DBSession.query(Deck).filter(Deck.id==deckid)
            if deck_list.count() == 0:
                return exc.HTTPNotFound

            db_deck = deck_list.first()
            new_card = Card(term=params['term'], definition=params['definition'])
            DBSession.add(new_card)
            db_deck.cards.append(new_card)

            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['color'] = str(db_deck.color)
            results['title'] = str(db_deck.title)

            # return results
            response = Response(body=json.dumps(results))
            response.headers.update({'Access-Control-Allow-Origin': '*', \
                "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
            return response

    # Edit a card
    elif method == 'PUT':
        if ("term" not in params) or ("definition" not in params) or ("deckid" not in params):
            return exc.HTTPBadRequest()
        elif type(params["deckid"]) != int:
            return exc.HTTPBadRequest

        cardid = params['id']
        with transaction.manager:
            card_list = DBSession.query(Card).filter(Card.id==cardid).first()
            if card_list.count() == 0:
                return exc.HTTPNotFound

            db_card = card_list.first()
            deckid = db_card.deck_id
            db_card.term = params['term']
            db_card.definition = params['definition']

            deck_list= DBSession.query(Deck).filter(Deck.id==deckid).first()
            if deck_list.couint() == 0:
                return exc.HTTPNotFound
            db_deck = deck_list.first()

            # build the response
            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['color'] = str(db_deck.color)
            results['title'] = str(db_deck.title)

            # return results
            response = Response(body=json.dumps(results))
            response.headers.update({'access-control-allow-origin': '*', \
                "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
            return response

    elif method == 'DELETE':
        if ("term" not in params) or ("definition" not in params) or ("deckid" not in params):
            return exc.HTTPBadRequest()
        elif type(params["deckid"]) != int:
            return exc.HTTPBadRequest

        cardid = params['id']
        with transaction.manager:
            card_list = DBSession.query(Card).filter(Card.id==cardid)
            if card_list.count() == 0:
                return exc.HTTPNotFound

            db_card = card_list.first()
            deckid = db_card.deck_id

            deck_list = DBSession.query(Card).filter(Card.id == cardid)
            if deck_list.count() == 0:
                return exc.HTTPNotFound
            DBSession.query(Card).filter(Card.id == cardid).delete(synchronize_session='evaluate')
            db_deck = DBSession.query(Deck).filter(Deck.id==deckid).first()          
            
            # build the response of a deck dictionary 
            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['color'] = str(db_deck.color)
            results['title'] = str(db_deck.title)

            # Return results 
            response = Response(body=json.dumps(results))
            response.headers.update({'access-control-allow-origin': '*', \
                "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
            return response

    return {'status': 'NOT OK'}


@view_config(route_name='get_decks', renderer = 'json')
def get_decks(request):
    decks = [];
    with transaction.manager:
        decks_query = DBSession.query(Deck).all()
        for deck_object in decks_query:
            deck = card2dict(deck_object.cards)
            deck['title'] = str(deck_object.title)
            deck['color'] = 'Green'
            deck['id'] = int(deck_object.id)
            decks.append(deck)

    response = Response(body=json.dumps(decks))
    response.headers.update({'access-control-allow-origin': 'http://localhost:3000', \
        "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
    return response


@view_config(route_name='get_deck', renderer = 'json')
def get_deck(request):
    
    # have a ? sign => params
    # otherwise request
    params = request.matchdict
    idx = params['id']
    
    deck = {}
    with transaction.manager:
        decks_query = DBSession.query(Deck).filter(Deck.id==idx).first()
        deck = card2dict(decks_query.cards)
        deck['title'] = str(decks_query.title)
        deck['color'] = 'Green'
        deck['id'] = idx
    
    response = Response(body=json.dumps(deck))    
    response.headers.update({'access-control-allow-origin': 'http://localhost:3000', \
        "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
    return response
    # return Response(
    #     body=USER1_DECKS,
    #     status='202 Accepted',
    #     content_type='application/json; charset=UTF-8')



# @view_config(route_name='add_user', renderer = 'json')
# def add_user(request):
#     req_post = request.POST
#     user_name = str(req_post['user_name'])
#     with transaction.manager:
#         model = User(user_name=user_name)
#         DBSession.add(model)
#     return {'add user': 'success'}  

# @view_config(route_name='add_deck', renderer = 'json')
# def add_deck(request):
#     req_post = request.POST
#     title = str(req_post['title'])
#     color = str(req_post['color'])
#     with transaction.manager:
#         model = Deck(title=title, color=color)
#         DBSession.add(model)
#     return {'add deck': 'success'}
