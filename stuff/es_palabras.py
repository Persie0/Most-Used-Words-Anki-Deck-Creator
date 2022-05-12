import palabras.core
from stuff.ankicard import AnkiCard


class Palabras:
    def __init__(self, word: str):
        self.word = word

    def add_translations(self, card: AnkiCard):
        try:
            res2 = palabras.core.get_word_info(self.word)
            for i in res2.definition_strings:
                card.add_trans_words(i + "<br>")
        except palabras.core.WiktionaryPageNotFound:
            return False
        except palabras.core.WiktionarySectionNotFound:
            return False
