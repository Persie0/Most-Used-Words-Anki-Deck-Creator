from boltons.setutils import IndexedSet


# has all Anki Card fields included
class AnkiCard:
    def __init__(self, count: int, word: str):
        self.a_sentences = dict()
        self.q_sentences = IndexedSet()
        self.trans_words = IndexedSet()

        self.count = count
        self.word = word
        self.trans_str = ""
        self.q_sentences_str = ""
        self.a_sentences_str = ""

    # convert the lists and map to html-strings that look good in Anki
    def convert(self):
        #len(ankicard.trans_words) < 3
        for w in self.trans_words:
            if "<br>" in w:
                self.trans_str += self.trans_str
            else:
                self.trans_str = self.trans_str + w + "; "
        self.trans_str = self.trans_str[:-2]

        self.q_sentences_str += '<button onmouseover="showExamplesTable()">show examples</button><table id="examplesTable">'
        for sen in self.q_sentences:
            if isinstance(sen, str):
                self.q_sentences_str = self.q_sentences_str + "<tr><td>" + sen + "</td></tr>"
        self.q_sentences_str += "</table>"

        self.a_sentences_str += '<button onmouseover="showExamplesTable2()">show examples</button><table id="examplesTable2">'
        for key, value in self.a_sentences.items():
            if isinstance(key, str) and isinstance(value, str):
                self.a_sentences_str = self.a_sentences_str + "<tr><td>" + key + "</td><td>" + value + "</td></tr>"
        self.a_sentences_str += "</table>"

    def add_trans_words(self, trans_word: str):
        if trans_word.lower()!=self.word.lower():
            self.trans_words.add(trans_word)

    def add_q_sentences(self, q_sentence: str):
        self.q_sentences.add(q_sentence)

    def add_a_sentences(self, to_meaning: str, from_example: str, to_example: str, from_meaning=""):
        to_meaning = str(to_meaning)
        from_example = str(from_example)
        to_example = str(to_example)
        from_meaning = str(from_meaning)
        if from_meaning== "":
            self.a_sentences[to_meaning + "</td><td>" + from_example] = to_example
        else:
            self.a_sentences[to_meaning + "<br>------------<br>" + from_meaning +
                             "</td><td>" + from_example] = to_example
