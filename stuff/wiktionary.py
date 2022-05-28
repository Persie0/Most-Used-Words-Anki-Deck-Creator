import json
import urllib.request
import urllib.error
from io import StringIO
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class Definition:
    def __init__(self):
        self.parsedExamples = {}
        self.examples = []
        self.definition = ""


class WiktionaryResult:
    def __init__(self):
        self.partOfSpeech = ""
        self.definitions = []
        self.definitionList = []
        self.rawResult = dict()

    def query(self, word: str, lang: str):
        api = 'https://en.wiktionary.org/api/rest_v1/page/definition/'
        try:
            with urllib.request.urlopen(api + word) as url:
                data = json.loads(url.read().decode())
                self.rawResult = data
                if "partOfSpeech" in data[lang][0]:
                    self.partOfSpeech = data[lang][0]["partOfSpeech"]
                for definition in data[lang][0]["definitions"]:
                    defi = Definition()
                    content = strip_tags(definition["definition"])
                    defi.definition = content

                    if "parsedExamples" in definition:
                        parsed_examples = definition["parsedExamples"]
                        for entry in parsed_examples:
                            defi.parsedExamples[strip_tags(entry["example"])] = strip_tags(entry["translation"])

                    if "examples" in definition:
                        for example in definition["examples"]:
                            defi.examples.append(strip_tags(example))

                    self.definitions.append(content)
                    self.definitionList.append(defi)
                    return True
        except KeyError:
            print("Word not found in Language")
            return False
        except urllib.error.HTTPError:
            print("No internet or word not found")
            return False


if __name__ == "__main__":

    wr = WiktionaryResult()
    if wr.query(word="essen", lang="de"):
        print(wr.definitions)
        print(wr.partOfSpeech)
        print(wr.definitionList[0].parsedExamples)
        print(wr.definitionList[0].examples)
        print(wr.definitionList[0].definition)
        print(wr.rawResult)
