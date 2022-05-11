import genanki


class AnkiDeck:

    def __init__(self, filename: str):
        # Instance Variable
        self.filename = filename[:-4]

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

    def addnote(self, count: int, word: str, q_sentences_str: str, trans_str: str, a_sentences_str: str):
        my_note = genanki.Note(
            sort_field=count,
            model=self.my_model,
            fields=[str(count), word, q_sentences_str, trans_str, a_sentences_str])
        self.my_deck.add_note(my_note)

    def create(self):
        genanki.Package(self.my_deck).write_to_file(self.filename + ".apkg")