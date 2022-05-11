import sys
import time

import palabras.core
from wrpy import WordReference

import stuff.anki as deck
import stuff.ankicard as card


def filter_and_add():
    if (i['to_word'][0]['meaning'] != 'translation unavailable') and (
            i['to_word'][0]['meaning'] != '-') and len(ankicard.trans_words) < 3:
        ankicard.add_trans_words(i['to_word'][0]['meaning'])
    if num < 3:
        ankicard.add_q_sentences(i['from_example'])
    if i['to_example'] and (i['to_word'][0]['meaning'] != 'translation unavailable') and (
            i['to_word'][0]['meaning'] != '-'):
        ankicard.add_a_sentences(i['to_word'][0]['meaning'], i['from_example'], i['to_example'][0])


# python .\main.py 10000mostusedspanish.txt es en 0

if __name__ == '__main__':
    start = time.time()
    fromLang = sys.argv[2]
    toLang = sys.argv[3]
    filename = sys.argv[1]
    numberOfWords = int(sys.argv[4])

    if not filename.endswith(".txt"):
        filename += ".txt"

    with open("lists/" + filename) as f:
        if f.errors:
            print(f.errors)
        else:
            lines = f.readlines()

    print("Started Deck creation :)")
    ankideck = deck.AnkiDeck(filename)
    count = 0
    for word in lines:
        word = word.replace("\n", "")
        wr = WordReference(fromLang, toLang)
        res = list()
        try:
            res = wr.translate(word)["translations"][0]['entries']
            res2 = wr.translate(word)["translations"][2]['entries']
        except NameError:
            ankideck.add_not_translated(word)
            continue
        except IndexError:
            res2 = []

        count += 1
        ankicard = card.AnkiCard(count, word)

        num = 0
        for i in res:
            if i['from_word']['source'] == word or word + ',' in i['from_word']['source']:
                num += 1
                filter_and_add()
        for i in res2:
            if num < 3:
                ankicard.add_q_sentences(i['from_example'])
                num += 1
            if i['to_example']:
                ankicard.add_a_sentences(i['to_word'][0]['meaning'], i['from_example'], i['to_example'][0],
                                         i['from_word']['source'])
        if len(ankicard.trans_words) == 0:
            if fromLang == "es" and toLang == "en":
                try:
                    res2 = palabras.core.get_word_info(word)
                    for i in res2.definition_strings:
                        ankicard.add_trans_words(i + "<br>")
                except palabras.core.WiktionaryPageNotFound:
                    ankideck.add_not_translated(word)
                    continue
                except palabras.core.WiktionarySectionNotFound:
                    ankideck.add_not_translated(word)
                    continue
            else:
                for i in res:
                    num += 1
                    filter_and_add()

        ankicard.convert()
        ankideck.addnote(count, word, ankicard.q_sentences_str, ankicard.trans_str, ankicard.a_sentences_str)
        # time.sleep(0.1)
        if (count % 1000) == 0:
            print(str(count))
        if numberOfWords != 0:
            if (count % numberOfWords) == 0:
                break
        end = time.time()
        if (start - end) > (60 * 60 * 5.997):
            break
        ankideck.create()
        break
