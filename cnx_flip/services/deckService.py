import json
import pyramid.httpexceptions as exc
import random
import transaction

from pyramid.view import view_config
from pyramid.response import Response
from cnx_flip.models import * #DBSession, Card, Base
from cnx_flip.db import *
from .requestService import *
from .formatResultsService import *
from .responseService import *


def get_decks(request):
    """
    Helper function for loading a list of decks on the deck page
    """
    method, params, url_param = get_params(request)

    # To answer Chrome
    if method == 'OPTIONS':
        return preflight_handler(request)

    # Load the decks of a user
    decks = [];
    with transaction.manager:
        decks_query = DBSession.query(Deck).all()
        for deck_object in decks_query:
            deck = card2dict(deck_object.cards)
            deck['title'] = str(deck_object.title)
            deck['color'] = str(deck_object.color)
            deck['id'] = int(deck_object.id)
            decks.append(deck)
    response = update_header(json.dumps(decks), origin_url)
    return response


def deck_http_request(request, origin_url):
    """
    Get, Create, Update or Delete a deck via GET, POST, PUT, DELETE methods

    request: http request
    origin_url: host url
    """
    method, params, url_param = get_params(request)

    # To answer Chrome
    if method == 'OPTIONS':
        return preflight_handler(request, origin_url)

    # Get decks
    if method == "GET":
        if len(url_param['deckid']) == 0:
            return get_decks(request)

        deck_id = url_param["deckid"]
        user_id = url_param["userid"]
        with transaction.manager:
            target_deck = DBSession.query(Deck).filter(
                Deck.id == deck_id and Deck.user_id == user_id).first()
            deck = card2dict(target_deck.cards)
            deck['title'] = str(target_deck.title)
            deck['color'] = str(target_deck.color)
            deck['id'] = deck_id

            response = update_header(json.dumps(deck), origin_url)
            return response

    # Create a new deck
    elif method == 'POST':
        print "YOU ARE CREATING A NEW DECK"
        userid = int(url_param["userid"])
        print "USER ID is " + str(userid)
        with transaction.manager:
            user_list = DBSession.query(User).filter(User.id==userid)
            print "USER LIST IS " + str(user_list.count())
            # Error handler: check if user exists
            if user_list.count() == 0:
                return exc.HTTPNotFound()
            user = user_list.first()
            print "USER IS" + str(user)

            # Assign a default title to the new deck
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

            response = update_header(json.dumps(results), origin_url)
            return response

    # Update a deck
    elif method == 'PUT':
        params = json.loads(params)
        print "PARAMS ARE " + str(params)

        deck_id = url_param['deckid']
        with transaction.manager:
            deck_list = DBSession.query(Deck).filter(Deck.id == deck_id)

            # Error handler: check if deck exists
            if deck_list.count() == 0:
                return exc.HTTPNotFound()

            db_deck = deck_list.first()
            # same_title_deck = DBSession.query(Deck)\
            #     .filter(Deck.title == params['title'] and Deck.user_id == db_deck.user_id)
            #
            # # Error handler: check for duplicate titles
            # if same_title_deck.count() != 0:
            #     return exc.HTTPConflict()

            db_deck.title = params['title']
            db_deck.color = params['color']

            # Build the response
            results = card2dict(db_deck.cards)
            results['id'] = int(db_deck.id)
            results['title'] = str(db_deck.title)
            results['color'] = str(db_deck.color)

            response = update_header(json.dumps(results), origin_url)
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
