from pyramid.view import view_config
from .models import * #DBSession, Card, Base
import transaction
from pyramid.response import Response
from mockdecks import USER1_DECKS
from mock_pull_engine import *
import json

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

@view_config(route_name='add_user', renderer = 'json')
def add_user(request):
    req_post = request.POST
    user_name = str(req_post['user_name'])
    with transaction.manager:
        model = User(user_name=user_name)
        DBSession.add(model)
    return {'add user': 'success'}        

@view_config(route_name='add_deck', renderer = 'json')
def add_deck(request):
    req_post = request.POST
    title = str(req_post['title'])
    color = str(req_post['color'])
    with transaction.manager:
        model = Deck(title=title, color=color)
        DBSession.add(model)
    return {'add deck': 'success'}

@view_config(route_name='update_from_db', renderer = 'json')
def update(request):
    put_stuff_in_db();
    # req_post = request.POST
    # title = str(req_post['title'])
    # color = str(req_post['color'])
    # with transaction.manager:
    #     model = Deck(title=title, color=color)
    #     DBSession.add(model)
    return {'update': 'success'}

@view_config(route_name='get_decks', renderer = 'json')
def get_decks(request):
    print "get here"
    cards = [
      { 'term': 'Test term 1', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
      { 'term': 'Test term 2', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
      { 'term': 'Test term 3', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
      { 'term': 'Test term 4', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
      { 'term': 'Test term 5', 'definition': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed orci nisl, sagittis ac tincidunt lacinia, sodales ac nibh. Fusce venenatis eleifend tortor, nec placerat eros laoreet sit amet. Quisque rhoncus non diam eu elementum. Praesent pulvinar nisi a urna lobortis auctor sit amet sed est. Aliquam eget orci sapien. Vestibulum.' },
    ]
    decks = [
      { 'id': 1, 'name': "Test Deck 1", 'cards': cards, 'color': '#8f8f8f'},
      { 'id': 2, 'name': "Test Deck 2", 'cards': cards, 'color': '#8f8f8f'},
      { 'id': 3, 'name': "Test Deck 3", 'cards': cards, 'color': '#8f8f8f'},
      { 'id': 4, 'name': "Test Deck 4", 'cards': cards, 'color': '#8f8f8f'},
      { 'id': 5, 'name': "Test Deck 5", 'cards': cards, 'color': '#8f8f8f'},
    ]

    response = Response(body=json.dumps(decks))
    print 'here'
    response.headers.update({'access-control-allow-origin': 'http://localhost:3000', "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"})
    print 'done'
    return response
    # return Response(
    #     body=USER1_DECKS,
    #     status='202 Accepted',
    #     content_type='application/json; charset=UTF-8')

@view_config(route_name='testtest', renderer = 'json')
def testtest(request):
    print "get here"
    # print request.GET
    return Response(
        body='hello world!',
        status='202 Accepted',
        content_type='application/json; charset=UTF-8')

# @view_config(route_name='generate_ajax_data', renderer='json')
# def my_ajax_view(request):
#     return {'message': "Hello"}
# 
# @view_config(route_name='home', renderer='templates/mytemplate.jinja2')
# def my_view(request):
#     return {'project': 'cnx_flip'}


