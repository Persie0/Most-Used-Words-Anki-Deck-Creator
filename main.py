import sys
import time
import ntpath

from stuff.es_palabras import Palabras

from stuff.ankideck import AnkiDeck
from stuff.ankicard import AnkiCard
from stuff.wordreference import WR


# python .\main.py lists/es/10000mostusedspanish.txt es en 0

def init_param():
    global start, fromLang, toLang, filename, numberOfWords, ankideck, path
    start = time.time()
    fromLang = sys.argv[2]
    toLang = sys.argv[3]
    path = sys.argv[1]
    filename = ntpath.basename(path)
    numberOfWords = int(sys.argv[4])
    if not filename.endswith(".txt"):
        filename += ".txt"
    ankideck = AnkiDeck(filename, path[:-4])


if __name__ == '__main__':
    start, fromLang, toLang, filename, path, numberOfWords, ankideck, count \
        = 0, "", "", "", "", 0, AnkiDeck("", ""), 0
    init_param()
    wr = WR(fromLang, toLang)

    with open(path) as f:
        txt_lines = f.readlines()

    for word in txt_lines:
        ankicard = AnkiCard(count, word)

        if wr.add_translations(word, ankicard):
            count += 1
            if len(ankicard.trans_words) == 0:
                if not Palabras(word).add_translations(ankicard):
                    ankideck.add_not_translated(word)

        else:
            if Palabras(word).add_translations(ankicard):
                count += 1
            else:
                ankideck.add_not_translated(word)

        ankicard.convert()
        ankideck.addnote(count, word, ankicard.q_sentences_str, ankicard.trans_str, ankicard.a_sentences_str)
        # print(count)
        if numberOfWords != 0:
            if (count % numberOfWords) == 0:
                break
        end = time.time()
        if (start - end) > (60 * 60 * 5.997):
            break
    ankideck.create()
