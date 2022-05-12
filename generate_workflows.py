import sys
import os
from collections import OrderedDict
import yaml

# python .\generate_workflows.py lists es en 10000


# load an already existing file to get data
# with open('.github/workflows/multiple.yml') as f:
#     data = yaml.load(f, Loader=yaml.FullLoader)
#     print(data)

if __name__ == '__main__':
    fromLang = sys.argv[2]
    toLang = sys.argv[3]
    directory = sys.argv[1]
    if not directory.endswith("\\"):
        directory += "\\"
    numberOfWords = int(sys.argv[4])

    files = []
    # get all *files* from directory and subdirectories
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            files.append(os.path.join(root, name))
        for name in dirs:
            files.append(os.path.join(root, name))
    content = OrderedDict({
        'name': 'Create Anki releases with multiple files',
        'on': {
            'workflow_dispatch': {
                'inputs': {
                    'textfilename': {
                        'description': 'Name of your .txt file',
                        'required': True,
                        'type': 'string'
                    },
                    'from': {
                        'description': 'Language of words from given .txt file',
                        'required': True,
                        'type': 'choice',
                        'options': ['es', 'en']
                    },
                    'to': {
                        'description': 'Language to which should be translated to',
                        'required': True,
                        'type': 'choice',
                        'options': ['en', 'es']
                    },
                    'numberOfWords': {
                        'description': 'How many Cards/Words your Anki Deck should have (Whole Number!) Write 0 to go '
                                       'through the whole .txt file. There is a 6h Github Action time limit!!! So max. '
                                       'Word (in Github Actions) are ca. 25000',
                        'required': True,
                        'type': 'string'
                    }
                }
            }
        },
        'permissions': {
            'contents': 'read'
        },
        'jobs': {
            'build': {
                'runs-on': 'ubuntu-latest',
                'steps': [{
                    'uses': 'actions/checkout@v3'
                }, {
                    'name': 'Set up Python 3.10',
                    'uses': 'actions/setup-python@v3',
                    'with': {
                        'python-version': '3.10'
                    }
                }, {
                    'name': 'Install dependencies',
                    'run': 'python -m pip install --upgrade pip\npip install wheel\npip install -r requirements.txt\n'
                }, {
                    'name': 'Upload Anki Decks',
                    'uses': 'actions/upload-artifact@v3.0.0',
                    'with': {
                        'name': 'release',
                        'path': 'CreatedDecks',
                        'retention-days': 90
                    }
                }]
            }
        }
    })
    for i in files:
        new = {
            'name': 'build Anki Deck ' + i,
            'run': 'python main.py ' + directory + i + ' ' + fromLang + ' ' + toLang + ' ' + str(numberOfWords) + '\n'
        }
        content["jobs"]["build"]["steps"].insert(3, new)
        # print(content["jobs"]["build"]["steps"][3])

    with open('.github/workflows/multiple.yml', 'w') as f:
        yaml.dump(content, f)
