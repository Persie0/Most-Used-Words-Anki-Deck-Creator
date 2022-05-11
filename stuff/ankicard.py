from boltons.setutils import IndexedSet


class AnkiCard:
    def __init__(self, count: int, word: str):
        self.a_sentences = dict()
        self.q_sentences = IndexedSet()
        self.trans_words = IndexedSet()
        self.count = count
        self.word = word

    def add_trans_words(self, trans_word: str):
        self.trans_words.add(trans_word)

    def add_q_sentences(self, q_sentence: str):
        self.q_sentences.add(q_sentence)

    def add_a_sentences(self, meaning: str, from_example: str, to_example: str):
        self.a_sentences[meaning + "</td><td>" + from_example]=to_example
