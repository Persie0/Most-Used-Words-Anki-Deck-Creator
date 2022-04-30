from wrpy import WordReference
import genanki
import time

if __name__ == '__main__':
    with open('10000mostusedspanish.txt') as f:
        lines = f.readlines()

    my_deck = genanki.Deck(
        deck_id=6969696969,
        name='Spanish 10000')
    my_model = genanki.Model(
        model_id=6969696969,
        name='Persie0 Model',
        css=".card { font-family: arial; font-size: 3.6vw;text-align: center;color: black;background-color: "
            "white;}.alts { font-size: 1.8vw;}.attrs { font-style: italic; font-size: 14px;}"
            "table, th, td {border: 2px solid;  margin-left: auto; margin-right: auto; padding: 6px; } table {  border-collapse: collapse;  width: 100%;}",
        fields=[
            {'name': 'Index'},
            {'name': 'Question'},
            {'name': 'Question sentences'},
            {'name': 'Answer'},
            {'name': 'Answer sentences and translations'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': "{{Question}}<br>{{#Question sentences}}<br /><span class=\"alts\">{{Question sentences}}</span>{"
                        "{/Question sentences}}",
                'afmt': '{{FrontSide}}<hr id="answer" />{{Answer}}<br>{{#Answer sentences and translations}}<br /><span '
                        'class="alts">{{Answer sentences and translations}}</span>{{/Answer sentences and '
                        'translations}}<div style="display:none;"></div>',
            },
        ]
    )
    count = 0
    for word in lines:
        count += 1
        word=word.replace("\n", "")
        wr = WordReference('es', 'en')  # same as WordReference('esen')
        res = wr.translate(word)["translations"][0]['entries']
        trans_words = set()

        q_sentences = set()
        a_sentences = dict()
        num = 0
        for i in res:
            num += 1
            if num < 3:
                if (i['to_word'][0]['meaning'] != 'translation unavailable') and (i['to_word'][0]['meaning'] != '-'):
                    trans_words.add(i['to_word'][0]['meaning'])
                q_sentences.add(i['from_example'])
            if i['to_example']:
                a_sentences[i['from_example']] = i['to_example'][0]
        print(count)
        print(word)
        print(trans_words)
        print("\n")
        q_sentences_str = "<table>"
        a_sentences_str = "<table>"
        trans_str = ""
        for w in trans_words:
            trans_str = trans_str + w + ", "

        trans_str = trans_str[0:-2]

        for sen in q_sentences:
            q_sentences_str = q_sentences_str + "<tr><td>" + sen + "</td></tr>"

        q_sentences_str += "</table>"
        for key, value in a_sentences.items():
            a_sentences_str = a_sentences_str + "<tr><td>" + key + "</td><td>" + value + "</td></tr>"

        a_sentences_str += "</table>"
        my_note = genanki.Note(
            sort_field=count,
            model=my_model,
            fields=[str(count), word, q_sentences_str, trans_str, a_sentences_str])
        # print([word, q_sentences_str, trans_str, a_sentences_str])
        my_deck.add_note(my_note)
        time.sleep(3)
    genanki.Package(my_deck).write_to_file('output.apkg')
