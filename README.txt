cnx_flip
========

Getting Started
---------------

- Change directory into your newly created project.

    cd CNX_FLIP

- Create a Python virtual environment.

    virtualenv .venv --python=python2.7

- Activate vitual environment (for Mac)
    
    source .venv/bin/activate

- Install

    pyton setup.py install

- Run your project's tests (not many tests now but).

    pytest

-Initialize db
    initialize_db development.ini

- Run your project.

    pserve development.ini --reload


Curl commands for testing api:
------------------------------
*** Add a card ***
curl -H "Content-Type: application/json" -X POST -d '{"deckid":5,"term":"PENTALON", "definition":"PANTS"}' http://localhost:5000/api/cards/

*** Edit a card ***
curl -H "Content-Type: application/json" -X PUT -d '{"cardid":27,"term":"trash", "definition":"junk"}' http://localhost:5000/api/cards/5

*** Delete a card ***
curl -H "Content-Type: application/json" -X DELETE -d '{"cardid": 29}' http://localhost:5000/api/cards/29

*** Add a deck ***
curl -H "Content-Type: application/json" -X POST -d '{"title":"deckIII", "color":"pink", "cards":[]}' http://localhost:5000/api/decks

*** Edit a deck ***
curl -H "Content-Type: application/json" -X PUT -d '{"deckid":5, "title": "changed", "color":"orange", "cards":[]}' http://localhost:5000/api/decks

*** Delete a deck ***
curl -H "Content-Type: application/json" -X DELETE -d '{"deckid": 7}' http://localhost:5000/api/decks

curl -H "Content-Type: application/json" -X POST -d '{"deckid":14,"uuids":["e79ffde3-7fb4-4af3-9ec8-df648b391597"]}' http://localhost:5000/api/textbook/1
