from wrpy import WordReference
import stuff.anki as anki
import time
import sys
from boltons.setutils import IndexedSet
import palabras.core



def filter_and_add():
    if (i['to_word'][0]['meaning'] != 'translation unavailable') and (
            i['to_word'][0]['meaning'] != '-') and len(trans_words) < 3:
        trans_words.add(i['to_word'][0]['meaning'])
    if num < 3:
        q_sentences.add(i['from_example'])
    if i['to_example'] and (i['to_word'][0]['meaning'] != 'translation unavailable') and (
            i['to_word'][0]['meaning'] != '-'):
        x = str(i['to_word'][0]['meaning']) + "</td>" + "<td>" + str(i['from_example'])
        a_sentences[x] = i['to_example'][0]


# python .\main.py 10000mostusedspanish.txt es en 0

if __name__ == '__main__':
    start = time.time()
    fromLang = sys.argv[2]
    toLang = sys.argv[3]
    filename = sys.argv[1]
    numberOfWords = int(sys.argv[4])
    if not filename.endswith(".txt"):
        filename += ".txt"
    # fromLang = "es"
    # toLang = "en"
    # filename = '10000mostusedspanish.txt'
    with open("lists/"+filename) as f:
        lines = f.readlines()
    print("Started Deck creation :)")
    ankideck = anki.AnkiDeck(filename)
    count = 0
    not_translated = IndexedSet()
    for word in lines:
        word = word.replace("\n", "")
        wr = WordReference(fromLang, toLang)
        res = list()
        try:
            res = wr.translate(word)["translations"][0]['entries']
            res2 = wr.translate(word)["translations"][2]['entries']
        except NameError:
            not_translated.add(word + "\n")
            continue
        except IndexError:
            res2 = []
        trans_words = IndexedSet()
        count += 1
        q_sentences = IndexedSet()
        a_sentences = dict()
        trans_str = ""
        num = 0
        for i in res:
            if i['from_word']['source'] == word or word + ',' in i['from_word']['source']:
                num += 1
                filter_and_add()
        for i in res2:
            if num < 3:
                q_sentences.add(i['from_example'])
                num += 1
            if i['to_example']:
                y = str(i['to_word'][0]['meaning']) + "<br>------------<br>" + i['from_word'][
                    'source'] + "</td>" + "<td>" + str(i['from_example'])
                a_sentences[y] = i['to_example'][0]
        if len(trans_words) == 0:
            if fromLang == "es" and toLang == "en":
                try:
                    res2 = palabras.core.get_word_info(word)
                    for i in res2.definition_strings:
                        trans_str = trans_str + i + "<br>"
                except palabras.core.WiktionaryPageNotFound:
                    not_translated.add(word + "\n")
                    continue
                except palabras.core.WiktionarySectionNotFound:
                    not_translated.add(word + "\n")
                    continue
            else:
                for i in res:
                    num += 1
                    filter_and_add()
        q_sentences_str = "<table>"
        a_sentences_str = "<table>"
        for w in trans_words:
            trans_str = trans_str + w + "; "

        trans_str = trans_str[0:-2]

        for sen in q_sentences:
            if isinstance(sen, str):
                q_sentences_str = q_sentences_str + "<tr><td>" + sen + "</td></tr>"

        q_sentences_str += "</table>"
        for key, value in a_sentences.items():
            if isinstance(key, str) and isinstance(value, str):
                a_sentences_str = a_sentences_str + "<tr><td>" + key + "</td><td>" + value + "</td></tr>"

        a_sentences_str += "</table>"

        # print([word, q_sentences_str, trans_str, a_sentences_str])
        ankideck.addnote(count, word, q_sentences_str, trans_str, a_sentences_str)
        # time.sleep(0.1)
        if (count % 1000) == 0:
            print(str(count))
        if numberOfWords != 0:
            if (count % numberOfWords) == 0:
                break
        end = time.time()
        if (start - end) > (60 * 60 * 5.997):
            break
    file1 = open("not_translated.txt", "w")
    file1.writelines(not_translated)
    file1.close()
    f.close()
    ankideck.create()
