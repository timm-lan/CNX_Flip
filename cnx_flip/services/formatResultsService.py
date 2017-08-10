import json
import pyramid.httpexceptions as exc
import random
import transaction

from pyramid.view import view_config
from pyramid.response import Response
from cnx_flip.models import * #DBSession, Card, Base
from cnx_flip.db import *

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