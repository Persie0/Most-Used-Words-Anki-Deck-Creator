import genanki
from boltons.setutils import IndexedSet
import os

# has a default Anki model and css
class AnkiDeck:
    # intitialises default Anki model and css, defines anki filename
    def __init__(self, filename: str, path: str):
        self.filename = filename  # remove .txt
        self.not_translated = IndexedSet()
        self.path = "CreatedDecks/"+os.path.dirname(path)
        self.my_deck = genanki.Deck(
            deck_id=3485385385,
            name=filename)
        self.my_model = genanki.Model(
            model_id=3485385385,
            name='Persie0 Model',
            css=".card { font-family: arial; font-size: 5.2vw;text-align: center;color: black;background-color: "
                "white;}.alts { font-size: 3vw;}.attrs { font-style: italic; font-size: 14px;}"
                "table, th, td {border: 2px solid;  margin-left: auto; margin-right: auto; padding: 6px; } table {  "
                "border-collapse: collapse;  width: 100%;}",
            fields=[
                {'name': 'Index'},
                {'name': 'Question'},
                {'name': 'Question sentences'},
                {'name': 'Answer'},
                {'name': 'Answer sentences and translations'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': "{{Question}}<br>{{#Question sentences}}<br /><span class=\"alts\">{{Question "
                            "sentences}}</span>{{/Question sentences}}",
                    'afmt': '{{FrontSide}}<hr id="answer" />{{Answer}}<br>{{#Answer sentences and translations}}<br '
                            '/><span '
                            'class="alts">{{Answer sentences and translations}}</span>{{/Answer sentences and '
                            'translations}}<div style="display:none;"></div>',
                },
            ]
        )

    # add an Note/Card to the deck (eg:  1, the, ... - as "the" is a much used word it's number 1)
    def addnote(self, count: int, word: str, q_sentences_str: str, trans_str: str, a_sentences_str: str):
        my_note = genanki.Note(
            sort_field=count,
            model=self.my_model,
            fields=[str(count), word, q_sentences_str, trans_str, a_sentences_str])
        self.my_deck.add_note(my_note)

    # creates the AnkiDeck-file to import, also generates not_translated.txt file
    def create(self):
        print(self.path)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        # get the directory an filename without .txt
        filedirectory=self.path + "/" + self.filename[:-4]
        genanki.Package(self.my_deck).write_to_file(filedirectory + ".apkg")

        open(filedirectory + "_not_translated.txt", "w").writelines(self.not_translated)

    def add_not_translated(self, word: str):
        self.not_translated.add(word + "\n")
