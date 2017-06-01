from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)

# This can save the schema part

# Change this config uri later!
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
db = SQLAlchemy(app)


# Create our database model
class Deck(db.Model):
    _tablename = "decks"
    deck_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)

    def __init__(self, title):
        title.email = title

    def __repr__(self):
        return '<Title %r>' % self.title


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/createDeck', methods=['POST'])
def create_deck():
    if request.method == 'POST':
        deck_title = request.form['title']
        # Check if the title already exists
        if not db.session.query(Deck).filter(Deck.title == deck_title).count() < 1:
            new_deck = Deck(deck_title)
            db.session.add(new_deck)
            db.session.commit()
            
            # change the template name later!!
            return render_template('success_create_new_deck.html')
    return render_template('index.html')
