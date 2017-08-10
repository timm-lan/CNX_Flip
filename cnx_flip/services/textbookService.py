from cnx_flip.models import * #DBSession, Card, Base
from cnx_flip.db import *
from .requestService import *
from .formatResultsService import *
from .responseService import *

ORIGIN_URL = '*'

def textbook_http_request(request, ori_url):
    ORIGIN_URL = ori_url
    method, params, url_param = get_params(request)
    if method == 'OPTIONS':
        return preflight_handler(request, ORIGIN_URL)

    # Get a deck from database
    if method == "POST":
        params = json.loads(params)
        deckid = int(params['deckid'])
        userid = url_param['userid']
        uuid_list = params['uuids']

        with transaction.manager:
            for uuid in uuid_list:
                importCardsFromCnxDb(uuid, deckid, CNXDB_HOST)
            target_deck = DBSession.query(Deck).filter(
                Deck.id == deckid and Deck.user_id == userid).first()
            deck = card2dict(target_deck.cards)
            deck['title'] = str(target_deck.title)
            deck['color'] = str(target_deck.color)
            deck['id'] = deckid

        response = update_header(json.dumps(deck), ORIGIN_URL)
        return response