import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import setup_logging, get_appsettings

from cnx_flip.models import *
from cnx_flip.db import *
from sqlalchemy_utils import *
from importFromCnxDb import *


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    dbUrl = settings['sqlalchemy.url']
    if database_exists(dbUrl):
        drop_database(dbUrl)
    create_database(dbUrl)

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    
    with transaction.manager:
        # DBSession.execute('DROP DATABASE IF EXISTS flashcarddb')
        # DBSession.execute('CREATE DATABASE falshcarddb')
        
        model = User(user_name='admin')
        DBSession.add(model)
    test_db()
