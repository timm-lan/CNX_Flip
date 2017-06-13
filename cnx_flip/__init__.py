from pyramid.config import Configurator
#DK how to use engine_from_config
from sqlalchemy import engine_from_config, create_engine
from .models import DBSession, Base

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
#     engine = engine_from_config(settings, 'sqlalchemy.')

    engine = create_engine('postgresql+psycopg2://Tim:Qasdew123@localhost/flashcarddb')

    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_mako')
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
#     config.add_route('generate_ajax_data', '/ajax_view')
    config.add_route('add_card', '/addCard')
    config.scan()
    return config.make_wsgi_app()
