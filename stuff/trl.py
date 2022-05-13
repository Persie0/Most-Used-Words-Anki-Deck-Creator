from translatepy import Translator
from translatepy.translators.reverso import ReversoTranslate
from stuff.ankicard import AnkiCard


# could add other translation services with translatepy too

class Transl:

    def __init__(self, fromlang: str, tolang: str):
        self.from_lang = fromlang
        self.to_lang = tolang
        self.reverso = ReversoTranslate()
        self.translator = Translator()

    def add_translations(self, word: str, card: AnkiCard):
        word = word.replace("\n", "")
        # list with maps: from example, to example, from where,...
        example = self.reverso.example(word, destination_language=self.to_lang, source_language=self.from_lang).result
        num = 0
        for i in example:
            num += 1
            if num < 3:
                card.add_q_sentences(i['s_text'])
            if i['s_text'] and i['t_text']:
                card.add_a_sentences(word, i['s_text'], i['t_text'])

        # list with strings, single word translations
        dictionary = self.reverso.dictionary("hablar", "en").result
        for i in dictionary:
            card.add_trans_words(i)

    #TODO: add audio
    def add_audio(self, word:str):
        self.translator.text_to_speech(word)
