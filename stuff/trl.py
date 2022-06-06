import re

from translatepy import Translator
from translatepy.translators.reverso import ReversoTranslate
from stuff.ankicard import AnkiCard

from urllib3 import disable_warnings


class Transl:

    def __init__(self, fromlang: str, tolang: str):
        self.from_lang = fromlang
        self.to_lang = tolang
        self.reverso = ReversoTranslate()
        self.translator = Translator()

    def add_translations(self, target_word: str, card: AnkiCard):
        for i in range(0, 3):
            try:
                disable_warnings()
                times = 0
                # try:
                # list with strings, single word translations
                dictionary = self.reverso.dictionary(target_word, destination_language=self.to_lang,
                                                     source_language=self.from_lang).result
                # map with source sentence, translated sentence, opensubs link, ...
                example_sentences = self.reverso.example(target_word, destination_language=self.to_lang,
                                                         source_language=self.from_lang).result
                # no translated word found?
                if (len(dictionary)) == 0:
                    return False
                num = 0
                for transl_word in dictionary:
                    word_added = False
                    for s in example_sentences:
                        # is there example sentence for the translated word?
                        if "<em>" + transl_word + "</em>" in s['t_text']:
                            if not word_added and times < 6:
                                card.add_trans_words(transl_word)
                                times += 1
                            word_added = True
                            # check if word is at end and replace
                            s_text = re.sub("<em>" + target_word + "</em>" + "(?=[?.!])",
                                            '<FONT COLOR="#106565">' + target_word + '</FONT>', s['s_text'])
                            t_text = re.sub("<em>" + transl_word + "</em>" + "(?=[?.!])",
                                            '<FONT COLOR="#106565">' + transl_word + '</FONT>', s['t_text'])
                            # add 2 example sentences for question
                            # replace <em> tag with color
                            if num < 2:
                                card.add_q_sentences(
                                    s_text.replace("<em>" + target_word + "</em>",
                                                   '<FONT COLOR="#106565">' + target_word + '</FONT>').replace(
                                        "<em>" + target_word.capitalize() + "</em>",
                                        '<FONT COLOR="#106565">' + target_word.capitalize() + '</FONT>'))
                                num += 1
                            # add as many sentences as possible with transl_word and transl_sentence for answer
                            # replace <em> tag with color
                            card.add_a_sentences(transl_word,
                                                 s_text.replace("<em>" + target_word + "</em>",
                                                                '<FONT COLOR="#106565">' + target_word + '</FONT>').replace(
                                                     "<em>" + target_word.capitalize() + "</em>",
                                                     '<FONT COLOR="#106565">' + target_word.capitalize() + '</FONT>'),
                                                 t_text.replace("<em>" + transl_word + "</em>",
                                                                '<FONT COLOR="#106565">' + transl_word + '</FONT>').replace(
                                                     "<em>" + transl_word.capitalize() + "</em>",
                                                     '<FONT COLOR="#106565">' + transl_word.capitalize() + '</FONT>'))
                return True
            except Exception as e:
                if i == 3:
                    print(repr(target_word) + " not translated: ")
                    print(e)
                    return False

    # TODO: add audio
    def add_audio(self, word: str):
        self.translator.text_to_speech(word)
