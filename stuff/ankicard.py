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
        for w in self.trans_words:
            if "<br>" in w:
                self.trans_str += self.trans_str
            else:
                self.trans_str = self.trans_str + w + "; "
                self.trans_str = self.trans_str[:-2]

        self.q_sentences_str += "<table>"
        for sen in self.q_sentences:
            if isinstance(sen, str):
                self.q_sentences_str = self.q_sentences_str + "<tr><td>" + sen + "</td></tr>"
        self.q_sentences_str += "</table>"

        self.a_sentences_str += "<table>"
        for key, value in self.a_sentences.items():
            if isinstance(key, str) and isinstance(value, str):
                self.a_sentences_str = self.a_sentences_str + "<tr><td>" + key + "</td><td>" + value + "</td></tr>"
        self.a_sentences_str += "</table>"

    def add_trans_words(self, trans_word: str):
        self.trans_words.add(trans_word)

    def add_q_sentences(self, q_sentence: str):
        self.q_sentences.add(q_sentence)

    def add_a_sentences(self, meaning: str, from_example: str, to_example: str, optional_target_meaning=None):
        meaning = str(meaning)
        from_example = str(from_example)
        to_example = str(to_example)
        optional_target_meaning = str(optional_target_meaning)
        if not isinstance(optional_target_meaning, str):
            self.a_sentences[meaning + "</td><td>" + from_example] = to_example
        else:
            self.a_sentences[meaning + "<br>------------<br>" + optional_target_meaning +
                             "</td><td>" + from_example] = to_example
