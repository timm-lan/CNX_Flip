from pyramid.view import view_config
from .models import * #DBSession, Card, Base
import transaction
from pyramid.response import Response
from mockdecks import USER1_DECKS
from mock_pull_engine import *
import json
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

    # create deck
    if method == 'POST':
        with transaction.manager:
            user = DBSession.query(User).filter(User.user_name=="admin").first()
            new_deck = Deck(title=params['title'], color=params['color'])
            DBSession.add(new_deck)
            user.decks.append(new_deck)

            results = {}
            results['cards'] = []
            results['id'] = int(new_deck.id)
            results['title'] = str(new_deck.title)
            results['color'] = str(new_deck.color)

            response = Response(body=json.dumps(results))
            response.headers.update({'Access-Control-Allow-Origin': '*', \
                "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
            return response
    elif method == 'PUT':
        deck_id = params['id']
        print "LOOK HERE"
        print "deck_id is " + str(deck_id)
        with transaction.manager:
            db_deck = DBSession.query(Deck).filter(Deck.id==int(deck_id)).first()
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

    elif method == 'DELETE':
        # note: need id to be in the param
        deck_id = params['id']
        with transaction.manager:
            # delete cards first to avoid foreign key constraints
            DBSession.query(Card).filter(Card.deck_id==deck_id).delete(synchronize_session="evaluate")
            DBSession.query(Deck).filter(Deck.id==deck_id).delete(synchronize_session="evaluate")
            print "$$$$$$$$$$$$$$$$$$"
            return {'status': 'delete successful'}

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
    # create card
    if method == 'POST':
        print 'post!'
        print params
        deckid = int(params['deckid'])
        with transaction.manager:
            db_deck = DBSession.query(Deck).filter(Deck.id==deckid).first()
            new_card = Card(term=params['term'], definition=params['definition'])
            DBSession.add(new_card)
            db_deck.cards.append(new_card)
            print 'here?'
            results = {}
            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['color'] = str(db_deck.color)
            results['title'] = str(db_deck.title)
            print results
            # return results
            response = Response(body=json.dumps(results))
            response.headers.update({'Access-Control-Allow-Origin': '*', \
                "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
            return response
        
    elif method == 'PUT':
        cardid = params['id']
        with transaction.manager:
            db_card = DBSession.query(Card).filter(Card.id==cardid).first()
            deckid = db_card.deck_id
            db_card.term = params['term']
            db_card.definition = params['definition']
            db_deck = DBSession.query(Deck).filter(Deck.id==deckid).first()
            # build the response
            results = {}
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
        cardid = params['id']
        with transaction.manager:
            # note: some cards in the databse don't have a deckid currently
            db_card = DBSession.query(Card).filter(Card.id==cardid).first()
            deckid = db_card.deck_id
            DBSession.query(Card).filter(Card.id == cardid).delete(synchronize_session='evaluate')
            db_deck = DBSession.query(Deck).filter(Deck.id==deckid).first()          
            
            # build the response of a deck dictionary 
            results = {}
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
