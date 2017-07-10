from .models import *
import transaction
mockCardsInTestDeck1 = [Card(term='term1', definition='def1'), \
                        Card(term='term2', definition='def2'), \
                        Card(term='term3', definition='def3'), \
                        Card(term='term4', definition='def4'), \
                        Card(term='term5', definition='def5'), \
                        Card(term='term6', definition='def6'), \
                        Card(term='term7', definition='def7')]
mockCardsInTestDeck2 = [Card(term='TERM1', definition='DEF1'), \
                        Card(term='TERM2', definition='DEF2'), \
                        Card(term='TERM3', definition='DEF3'), \
                        Card(term='TERM4', definition='DEF4'), \
                        Card(term='TERM5', definition='DEF5'), \
                        Card(term='TERM6', definition='DEF6'), \
                        Card(term='TERM7', definition='DEF7')]
mockCardsInTestDeck3 = [Card(term='haha1', definition='DEFINITION1'), \
                        Card(term='haha2', definition='DEFINITION2'), \
                        Card(term='haha3', definition='DEFINITION3'), \
                        Card(term='haha4', definition='DEFINITION4'), \
                        Card(term='haha5', definition='DEFINITION5'), \
                        Card(term='haha6', definition='DEFINITION6'), \
                        Card(term='haha7', definition='DEFINITION7')]
def put_stuff_in_db():
    user_name = 'admin'
    with transaction.manager:
    	deck1 = Deck(title='test_deck1')
    	deck1.cards = mockCardsInTestDeck1
    	deck2 = Deck(title='test_deck2')
    	deck2.cards = mockCardsInTestDeck2
    	all_deck = DeckCombo(deck_combo_name='all_deck',\
        	color='grey')
        all_deck.decks = [deck1, deck2]

        deckCombo = DBSession.query(User).\
            filter(User.user_name=='admin').first().deckcombos
        if not deckCombo:
        	deckCombo = [all_deck]
        
        DBSession.query(DeckCombo).\
            filter(DeckCombo.deck_combo_name =='all_deck').first().decks = [deck1, deck2]
        