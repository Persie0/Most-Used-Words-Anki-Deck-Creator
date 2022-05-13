from wrpy import WordReference
from stuff.ankicard import AnkiCard


class WR:

    def __init__(self, fromlang: str, tolang: str):
        self.from_lang = fromlang
        self.to_lang = tolang
        self.wr = WordReference(fromlang, tolang)

    def add_translations(self, word: str, card: AnkiCard):
        word = word.replace("\n", "")
        res = dict()
        try:
            # most used translation
            res = self.wr.translate(word)["translations"][0]['entries']
            # uncommon translations
            res2 = self.wr.translate(word)["translations"][2]['entries']
            # didnt find word on WR
        except NameError:
            return False
        except IndexError:
            res2 = []
        num = 0
        for i in res:
            # word in translations that got fetched included?
            if i['from_word']['source'] == word or word + ',' in i['from_word']['source']:
                num += 1
                valid_translation = (i['to_word'][0]['meaning'] != 'translation unavailable') and (
                        i['to_word'][0]['meaning'] != '-')
                # filter for "-" or 'translation unavailable' as an word_trans result
                if valid_translation:
                    card.add_trans_words(i['to_word'][0]['meaning'])
                if num < 3:
                    card.add_q_sentences(i['from_example'])
                if i['to_example'] and valid_translation:
                    card.add_a_sentences(i['to_word'][0]['meaning'], i['from_example'], i['to_example'][0])
        for i in res2:
            if num < 3:
                card.add_q_sentences(i['from_example'])
                num += 1
            if i['to_example']:
                card.add_a_sentences(i['to_word'][0]['meaning'], i['from_example'], i['to_example'][0],
                                     i['from_word']['source'])
        return True

    def add_uncommon_words(self, word: str, card: AnkiCard):
        num = 0
        res = self.wr.translate(word)["translations"][0]['entries']
        for i in res:
            valid_translation = (i['to_word'][0]['meaning'] != 'translation unavailable') and (
                    i['to_word'][0]['meaning'] != '-')
            # filter for "-" or 'translation unavailable' as an word_trans result
            if valid_translation:
                card.add_trans_words(i['to_word'][0]['meaning'])
            if num < 3:
                card.add_q_sentences(i['from_example'])
            if i['to_example'] and valid_translation:
                card.add_a_sentences(i['to_word'][0]['meaning'], i['from_example'], i['to_example'][0])

#maybe add more sentences
    # def add_sentences_only(self, word: str, card: AnkiCard):
    #     word = word.replace("\n", "")
    #     res = dict()
    #     try:
    #         # most used translation
    #         res = self.wr.translate(word)["translations"][0]['entries']
    #         # uncommon translations
    #         res2 = self.wr.translate(word)["translations"][2]['entries']
    #         # didnt find word on WR
    #     except NameError:
    #         return False
    #     except IndexError:
    #         res2 = []
    #     num = 0
    #     for i in res:
    #         # word in translations that got fetched included?
    #         if i['from_word']['source'] == word or word + ',' in i['from_word']['source']:
    #             num += 1
    #             valid_translation = (i['to_word'][0]['meaning'] != 'translation unavailable') and (
    #                     i['to_word'][0]['meaning'] != '-')
    #             # filter for "-" or 'translation unavailable' as an word_trans result
    #             if valid_translation:
    #                 card.add_trans_words(i['to_word'][0]['meaning'])
    #             if num < 3:
    #                 card.add_q_sentences(i['from_example'])
    #             if i['to_example'] and valid_translation:
    #                 card.add_a_sentences(i['to_word'][0]['meaning'], i['from_example'], i['to_example'][0])
    #     for i in res2:
    #         if num < 3:
    #             card.add_q_sentences(i['from_example'])
    #             num += 1
    #         if i['to_example']:
    #             card.add_a_sentences(i['to_word'][0]['meaning'], i['from_example'], i['to_example'][0],
    #                                  i['from_word']['source'])
    #     return True