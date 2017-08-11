import json
import pyramid.httpexceptions as exc
import random
import transaction

from pyramid.view import view_config
from pyramid.response import Response
from .importFromCnxDb import *

from cnx_flip.models import * #DBSession, Card, Base
from cnx_flip.db import *
from cnx_flip.services import *
from cnx_flip.services import *

USER = 'admin'
ORIGIN_URL = 'http://localhost:3000'
COLORS = ["#15837D", "#EF5F33", "#1B2152", "#1BB3D3",\
          "#B30B26", "#FDB32F", "#F0C916", "#65A234", "#8f8f8f"]
CNXDB_HOST = 'http://localhost:6543'

@view_config(route_name='home', renderer='templates/index.html.jinja2')
def my_view(request):
    """
    Test to see if the server is running
    """
    return {'project': 'cnx_flip'}


@view_config(route_name='test_db', renderer='json')
def test_db(request):
    """
    Populate the database
    """
    test_db()
    return {'update': 'success'}


@view_config(route_name='api_deck', renderer='json')
def api_deck(request):
    """
    Get, Create, Update or Delete a deck via GET, POST, PUT, DELETE

    :param request: http request
    """
    return deck_http_request(request, ORIGIN_URL)


@view_config(route_name='api_card', renderer='json')
def api_card(request):
    """
    Create, Update or Delete a card via POST, PUT, DELETE methods

    :param request: http request
    """
    return card_http_request(request, ORIGIN_URL);

@view_config(route_name='api_textbook', renderer='json')
def api_textbook(request):
    """
    Add terms and definitions pulled from CNX Archive to database
    :param request: http request
    """
    return text_http_request(request, ORIGIN_URL)

# Unfinished code for adding users
# @view_config(route_name='add_user', renderer = 'json')
# def add_user(request):
#     req_post = request.POST
#     user_name = str(req_post['user_name'])
#     with transaction.manager:
#         model = User(user_name=user_name)
#         DBSession.add(model)
#     return {'add user': 'success'}  

