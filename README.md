# Most-Used-Words-Anki-Deck-Creator
With this python script you can create an anki deck from a given list with words.

# Possible sources for your decks
- https://github.com/hermitdave/FrequencyWords
- https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists
- Github

# Implement:
- https://pypi.org/project/pystone/
- https://pypi.org/project/dingonyms/
- https://pypi.org/project/zdict/ -> https://github.com/zdict/zdict/tree/6cd5528a49ccec56e243f47b8ab6372bcf6c4a79/zdict/tests/dictionaries
- https://github.com/demian-wolf/pyreverso
- https://github.com/flagist0/reverso_context_api
- https://pypi.org/project/allreverso/
- https://pypi.org/project/translators/
- https://pypi.org/project/translatepy/

# TODO
- **Done:** Make a script that generates a GitHub action file which runs all files of a directory 
- Check if input is an actually existing text file
- Add the Implements

# How to use
<h3>Create one Ankideck (easier, shorter)</h3>

1. Fork this project
2. upload your .txt file from which you want to create an Ankideck to the forked repo
3. run the action "Create Anki release from a given, single file" ("Run Workflow")
4. and type in the parameters 
5. after more or less time depending on how many word you want to translate, the workflow should upload your Ankidecks



<h3>Multiple create multiple Ankidecks at once (harder, longer)</h3>

1. Fork this project
2. upload your .txt files from which you want to create Anki Deck(s) to the forked repo; I recommend to upload into the uploads directory
3. follow this 
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-token=
and create an access token with "repo" and "workflow" ticked (first 2)
4. copy the created token
5. follow this (on your forked repo)
https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository=
call it secret `WORKFLOW_TOKEN` and paste the before created access token 
6. go to the GitHub Actions tab of your forked project
7. go to "Create workflow file" and type in the parameters
8. wait some time until this action is finished
9. then go to the action "'`Foldername you entered at step 7`' : GW"
10. and run it
11. after more or less time depending on how many word you want to translate, the workflow should upload your Ankidecks

