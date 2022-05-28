import re

from wrpy import WordReference

from stuff.ankicard import AnkiCard


def extract(i):
    word_translation = i['from_word']['source']
    print(word_translation)
    given_word = i['to_word'][0]['meaning']
    print(given_word)
    to_example = i['to_example']
    from_example = i['from_example']
    if to_example and from_example:
        to_example = re.sub(re.escape(' ' + word_translation + "(?=[?.!])"),
                            ' <FONT COLOR="#ef9a9a">' + word_translation + '</FONT>', to_example[0])
        to_example = to_example.replace(" " + word_translation + " ",
                                        ' <FONT COLOR="#ef9a9a">' + word_translation + '</FONT> ').replace(
            word_translation.capitalize() + " ", '<FONT COLOR="#ef9a9a">' + word_translation.capitalize() + '</FONT> ')

        from_example = re.sub(re.escape(' ' + given_word + "(?=[?.!])"),
                              ' <FONT COLOR="#ef9a9a">' + given_word + '</FONT>', from_example)
        from_example = from_example.replace(" " + given_word + " ",
                                            ' <FONT COLOR="#ef9a9a">' + given_word + '</FONT> ').replace(
            given_word.capitalize() + " ",
            '<FONT COLOR="#ef9a9a">' + given_word.capitalize() + '</FONT> ')
    valid_translation = (word_translation != 'translation unavailable') and (
            word_translation != '-')
    return from_example, word_translation, to_example, given_word, valid_translation


class WR:

    def __init__(self, fromlang: str, tolang: str):
        self.from_lang = fromlang
        self.to_lang = tolang
        self.wr = WordReference(fromlang, tolang)

    def add_translations(self, word: str, card: AnkiCard):
        res = dict()
        res2=dict()
        for i in range(0, 3):
            try:
                answ = self.wr.translate(word)
                # most used translation
                res = answ["translations"][0]['entries']
                # uncommon translations
                res2 = answ["translations"][2]['entries']
                # didnt find word on WR
            except NameError:
                return False
            except IndexError:
                res2 = []
            except Exception as e:
                if i == 3:
                    print(repr(word) + " not translated: ")
                    print(e)
                    return False
        num = 0
        for i in res:
            from_example, meaning, to_example, translation_from_word, valid_translation = extract(i)
            # word in translations that got fetched included?
            if translation_from_word == word or word + ',' in translation_from_word:
                num += 1
                # filter for "-" or 'translation unavailable' as an word_trans result
                if valid_translation:
                    card.add_trans_words(meaning)
                if num < 3:
                    card.add_q_sentences(from_example)
                if to_example and from_example and valid_translation:
                    card.add_a_sentences(meaning,
                                         from_example,
                                         to_example)
        for i in res2:
            from_example, meaning, to_example, translation_from_word, valid_translation = extract(i)
            if num < 3:
                card.add_q_sentences(from_example)
                num += 1
            if to_example and from_example and valid_translation:
                card.add_a_sentences(meaning,
                                     from_example,
                                     to_example, translation_from_word)
        return True

    # def add_uncommon_words(self, word: str, card: AnkiCard):
    #     num = 0
    #     res = self.wr.translate(word)["translations"][0]['entries']
    #     for i in res:
    #         valid_translation = (i['to_word'][0]['meaning'] != 'translation unavailable') and (
    #                 i['to_word'][0]['meaning'] != '-')
    #         # filter for "-" or 'translation unavailable' as an word_trans result
    #         if valid_translation:
    #             card.add_trans_words(i['to_word'][0]['meaning'])
    #         if num < 3:
    #             card.add_q_sentences(i['from_example'].replace(word,
    #                                                            '<FONT COLOR="#ef9a9a">' + word + '</FONT>'))
    #         if i['to_example'] and valid_translation:
    #             card.add_a_sentences(i['to_word'][0]['meaning'], i['from_example'], i['to_example'][0])

    # maybe add more sentences
    def add_sentences_only(self, word: str, card: AnkiCard):
        res = dict()
        res2 = dict()
        for i in range(0, 3):
            try:
                answ = self.wr.translate(word)
                # most used translation
                res = answ["translations"][0]['entries']
                # uncommon translations
                res2 = answ["translations"][2]['entries']
                # didnt find word on WR
            except NameError:
                return False
            except IndexError:
                res2 = []
            except Exception as e:
                if i == 3:
                    print(repr(word) + " not translated: ")
                    print(e)
                    return False
        for i in res:
            from_example, meaning, to_example, translation_from_word, valid_translation = extract(i)
            # word in translations that got fetched included?
            if i['from_word']['source'] == word or word + ',' in i['from_word']['source']:
                # example sentences?
                if to_example and from_example and valid_translation:
                    card.add_a_sentences(meaning,
                                         from_example,
                                         to_example)
        for i in res2:
            from_example, meaning, to_example, translation_from_word, valid_translation = extract(i)

            if to_example and from_example and valid_translation:
                card.add_a_sentences(meaning,
                                     from_example,
                                     to_example)
        return True
