from pyramid.config import Configurator
#DK how to use engine_from_config
from sqlalchemy import engine_from_config, create_engine
from .models import DBSession, Base

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
#     engine = engine_from_config(settings, 'sqlalchemy.')

    engine = create_engine('postgresql+psycopg2://zhiyangzhang@localhost/flashcarddb')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    ###################################################################
    config.include('pyramid_jinja2')
    config.include('pyramid_mako')
    config.include('pyramid_chameleon')
    ###################################################################
    config.add_static_view('static', 'static', cache_max_age=3600)
    ###################################################################
    config.add_route('home', '/')
#     config.add_route('generate_ajax_data', '/ajax_view')

    # Test routes
    config.add_route('add_card', '/addCard')
    config.add_route('add_card_tmp', '/addCardTmp')

    # Decks
    # config.add_route('get_decks', '/get_decks/{user_id}')
    config.add_route('get_decks', 'api/getDecks')
    config.add_route('api_deck', 'api/decks/{deckid:.*}')
    # config.add_route('api_card_add', 'api/cards')
    config.add_route('api_card', 'api/cards/{cardid:.*}')
    ###################################################################
    # config.add_route('get_one_deck', '/get_one_deck/{deck_id}')
    # config.add_route('add_user', 'addUser')
    # config.add_route('add_deck', 'addDeck')
    config.add_route('update_from_db', 'update')
    config.scan()
    return config.make_wsgi_app()
