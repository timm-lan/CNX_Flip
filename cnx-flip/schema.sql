DROP TABLE IF EXISTS Deck;
DROP TABLE IF EXISTS Card;

CREATE TABLE Card (
  card_id SERIAL PRIMARY KEY,
  term VARCHAR(100),
  definition VARCHAR(1000)
);

CREATE TABLE Deck (
  deck_id SERIAL PRIMARY KEY,
  title VARCHAR(100),
  date_created DATE NOT NULL
);


CREATE TABLE Deck_Card (
  card_id SERIAL REFERENCES Card (card_id) ON UPDATE CASCADE,
  deck_id SERIAL REFERENCES Deck (deck_id) ON UPDATE CASCADE,
  CONSTRAINT deck_card_pk PRIMARY KEY (card_id, deck_id)
);
