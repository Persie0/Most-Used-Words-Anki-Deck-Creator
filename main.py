import sys
import time
import ntpath
import codecs

from stuff.es_palabras import Palabras
from stuff.ankideck import AnkiDeck
from stuff.ankicard import AnkiCard
from stuff.wordreference import WR
from stuff.trl import Transl


# lists\es\most-common-spanish-words.txt es en 10

def init_param():
    global start, fromLang, toLang, filename, numberOfWords, ankideck, path
    start = time.time()
    fromLang = sys.argv[2]
    toLang = sys.argv[3]
    # fix as \ in created workflow file just disappears - so made 2
    path = sys.argv[1]
    path=path.replace("\\\\", "\\")
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
    trl = Transl(fromLang, toLang)



    with codecs.open(path, encoding="utf8", errors='replace') as f:
        txt_lines = f.readlines()

    for word in txt_lines:
        #to also see \n or similar
        # print(repr(word))
        word=word.replace("\n", "").replace("\r", "")
        ankicard = AnkiCard(count, word)

        if trl.add_translations(word, ankicard):
            count += 1
            wr.add_sentences_only(word, ankicard)
        elif wr.add_translations(word, ankicard):
            count += 1
            if len(ankicard.trans_words) == 0:
                if fromLang == "es" and toLang == "en":
                    if not Palabras(word).add_translations(ankicard):
                        ankideck.add_not_translated(word)
                        continue
        else:
            ankideck.add_not_translated(word)
            continue

        ankicard.convert()
        ankideck.addnote(count, word, ankicard.q_sentences_str, ankicard.trans_str, ankicard.a_sentences_str)
        # print(count)
        if numberOfWords != 0:
            if (count % numberOfWords) == 0:
                break
        end = time.time()
        # run for 5h 57min max
        if (end - start) > (60 * 60 * 5.95):
            break
    ankideck.create()
