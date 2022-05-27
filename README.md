# Most-Used-Words-Anki-Deck-Creator
With this python script you can create an anki deck from a given list with words.

# Possible sources for your decks
- https://github.com/hermitdave/FrequencyWords
- https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists
- Github

# TODO
- ~~Make a script that generates a GitHub action file which runs all files of a directory~~ 
- add option for folder name as the source language - to translate multiple files from multiple languages
- Add Audio to (Reverso class and) Anki Cards
- Add the Implements
- add monolingual mode (with dictionaries) for advanced vocabulary
- (Check if input is an actually existing text file)

# How to use
All of the words you want to translate have to be in a text file with one word per line!
<h3>Create one Ankideck (easier, shorter)</h3>

1. Fork this project
2. upload your .txt file from which you want to create an Ankideck to the forked repo
3. run the action "single file,..." ("Run Workflow")

 3.1 - "Git push" - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-token=
and create an access token with "repo" and "gist" ticked

 follow this (on your forked repo)
https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository=
call it secret `ADD_NEW` and paste the before created access token; file will be pushed to your repo

 3.2 - "Artifact" - no actions needed; file will be uploaded under Actions
4. and type in the parameters 
5. after more or less time depending on how many word you want to translate, the workflow should upload your Ankidecks



<h3>Create multiple Ankidecks at once (harder, longer)</h3>

1. Fork this project
2. upload your .txt files from which you want to create Anki Deck(s) to the forked repo; I recommend to upload into the uploads directory
3. follow this 
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-token=
and create an access token with admin:org, admin:repo_hook, delete:packages, gist, repo, workflow, write:packages ticked
4. copy the created token
5. follow this (on your forked repo)
https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository=
call it secret `ADD_NEW` and paste the before created access token 
6. go to the GitHub Actions tab of your forked project
7. go to "Create workflow file" and type in the parameters
8. after more or less time depending on how many word you want to translate, the workflow should upload your Ankidecks to your github repo

# Language Codes
Generally the ISO 639-1 (alpha 2) format (like website top domain; eg: "en" for English, "de" for German,...) should be used, others could be supported too.
All language codes (I think):
https://datahub.io/core/language-codes/r/0.html

# ! For Devs
If you run the generate_workflows.py on Windows and push the workflows it won't work. This is due the different directory seperators on Windows and Linux. A possible solotion would be to set the `runs-on:` part from `ubuntu-latest` to `windows-latest`.


# Implement:
<h4>Monolingual:</h4>
- https://pypi.org/project/pystone/
- https://pypi.org/project/dingonyms/
- https://pypi.org/project/allreverso/ -> can get synonyms

<h4>Translation:</h4>
- https://pypi.org/project/zdict/ -> https://github.com/zdict/zdict/tree/6cd5528a49ccec56e243f47b8ab6372bcf6c4a79/zdict/tests/dictionaries
- maybe: https://pypi.org/project/translators/
