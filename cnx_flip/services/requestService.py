import json
import pyramid.httpexceptions as exc
import random
import transaction

from pyramid.view import view_config
from pyramid.response import Response
from cnx_flip.models import * #DBSession, Card, Base
from cnx_flip.db import *

def preflight_handler(request, ori_url):
    response = Response()
    response.headers.update({
        'Access-Control-Allow-Origin': ori_url, \
        "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS', \
        "Access-Control-Allow-Headers": "Content-Type,  Authorization, X-Requested-With, X-XSRF-TOKEN"
    })
    return response


def get_params(request):
    """
    Retrieve parameters of a request
    """
    method = request.method
    params = request.body
    url_param = request.matchdict
    return method, params, url_param