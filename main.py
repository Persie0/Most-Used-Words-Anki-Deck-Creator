import sys
import time
import ntpath

from stuff.es_palabras import Palabras
from stuff.ankideck import AnkiDeck
from stuff.ankicard import AnkiCard
from stuff.wordreference import WR
from stuff.trl import Transl
from stuff.wiktionary import WiktionaryResult

# lists\es\most-common-spanish-words.txt es en 10

def init_param():
    global start, fromLang, toLang, filename, numberOfWords, ankideck, path
    start = time.time()
    fromLang = sys.argv[2]
    toLang = sys.argv[3]
    # fix as \ in created workflow file just disappears - so made 2
    path = sys.argv[1]
    filename = ntpath.basename(path)
    numberOfWords = int(sys.argv[4])
    if not filename.endswith(".txt"):
        filename += ".txt"
        path += ".txt"
    ankideck = AnkiDeck(filename, path[:-4])


if __name__ == '__main__':
    start, fromLang, toLang, filename, path, numberOfWords, ankideck, count \
        = 0, "", "", "", "", 0, AnkiDeck("", ""), 0
    init_param()
    wikt=WiktionaryResult()
    wr = WR(fromLang, toLang)
    trl = Transl(fromLang, toLang)
    trl_reverse = Transl(toLang, fromLang)

    with open(path, encoding="utf8", errors='replace') as f:
        txt_lines = f.readlines()

    for line in txt_lines:
        # to also see \n or similar
        # print(repr(word))
        line = line.replace("\n", "").replace("\r", "")
        # if there are multiple word in a line seperated by "|"
        words = line.split("|")
        for word in words:
            ankicard = AnkiCard(count, word)

            if trl.add_translations(word, ankicard):
                if len(ankicard.trans_words) != 0:
                    wr.add_sentences_only(word, ankicard)

            # eg translating from es -> en
            # word is "butch", check if word exists in en because wr cant distinguish if result is in en&es
            if len(ankicard.trans_words) == 0:
                if trl_reverse.add_translations(word, ankicard):
                    if len(ankicard.trans_words) != 0:
                        ankicard = AnkiCard(count, word)
                        if fromLang == "es" and toLang == "en":
                            Palabras(word).add_translations(ankicard)
                    else:
                        wr.add_translations(word, ankicard)

            if len(ankicard.trans_words) == 0:
                ankideck.add_not_translated(word)
                continue
            else:
                count += 1
            ankicard.convert()

            ankideck.addnote(count, word, ankicard.q_sentences_str, ankicard.trans_str, ankicard.a_sentences_str)
        # print(count)
        if numberOfWords != 0:
            if count >= numberOfWords:
                break
        end = time.time()
        passed = end - start
        # run for 5h 50min max, to leave time for ankideck.create()
        # print(passed)
        if passed > (60 * 60 * 5.834):
            break
    ankideck.create()
