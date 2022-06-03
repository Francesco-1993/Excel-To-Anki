import pandas as pd
import genanki
import random
df = pd.read_excel('dp-900.xlsx')

df['Word'] = df['Word'].str.strip()
df['Definition'] = df['Definition'].str.strip()
df['Tags'] = df['Tags'].str.split(';').apply(lambda x: [y.strip() for y in x])
df['Deck'] = df['Deck'].str.strip()
df['Subdeck'] = df['Subdeck'].str.strip()
df['Deck_Subdeck'] = df[['Deck', 'Subdeck']].agg('::'.join, axis=1)

deck_names = df['Deck_Subdeck'].unique().tolist()
decks = []

my_model = genanki.Model(
  random.randrange(1 << 30, 1 << 31),
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

for deck_name in deck_names:
    my_deck = genanki.Deck(
      random.randrange(1 << 30, 1 << 31),
      deck_name)

    for row in df[df.Deck_Subdeck==deck_name].iterrows():
        my_note = genanki.Note(
                      model=my_model,
                      fields=[row[1][0], row[1][1]])
        my_note.tags = [x.replace(' ', '_') for x in row[1][2]]

        my_deck.add_note(my_note)
    decks.append(my_deck)

genanki.Package(decks).write_to_file('output.apkg')
