from wiktionary_translate.wiktionary_translate import WiktionaryResult

wr = WiktionaryResult()
if wr.query(word="essen", lang="de"):
    print(wr.definitions)  # ['to eat']
    print(wr.partOfSpeech)  # Verb
    print(wr.definitionList[0].parsedExamples)  # {'Er isst gern Schokolade.': 'He likes eating chocolate.', '...}
    print(wr.definitionList[0].examples)  # ['Er isst gern Schokolade.', 'Ich esse einen Apfel.']
    print(wr.definitionList[0].definition)  # to eat
    print(wr.rawResult)