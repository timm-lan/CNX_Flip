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

def update_header(body, origin_url):
    """
    Updates header
    Input: header in json format
    Output: response with headers

    return: response
    """
    response = Response(body)
    response.headers.update({
        'Access-Control-Allow-Origin': origin_url, \
        "Access-Control-allow-methods": 'GET, POST, PUT, DELETE, OPTIONS', \
        "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"
    })
    return response
