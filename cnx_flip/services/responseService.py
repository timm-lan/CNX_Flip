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

def update_header(body, ori_url):
    """
    Updates header
    Input: header in json format
    Output: response with headers
    """
    response = Response(body)
    response.headers.update({
        'Access-Control-Allow-Origin': ori_url, \
        "Access-Control-allow-methods": 'GET, POST, PUT, DELETE, OPTIONS', \
        "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"
    })
    return response

# def get_decks(request):
#     """
#     Helper function for loading a list of decks on the deck page
#     """
#     method, params, url_param = get_params(request)

#     # To answer Chrome
#     if method == 'OPTIONS':
#         return preflight_handler(request)

#     # Load the decks of a user
#     decks = [];
#     with transaction.manager:
#         decks_query = DBSession.query(Deck).all()
#         for deck_object in decks_query:
#             deck = card2dict(deck_object.cards)
#             deck['title'] = str(deck_object.title)
#             deck['color'] = str(deck_object.color)
#             deck['id'] = int(deck_object.id)
#             decks.append(deck)
#     response = update_header(body=json.dumps(decks))
#     return response