import ntpath
import sys
import os
import yaml


# python .\generate_workflows.py lists es en 10000

# get all sub/directory files
def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


# load an already existing file to get data
# with open('.github/workflows/multiple.yml') as f:
#     data = yaml.load(f, Loader=yaml.FullLoader)
#     print(data)

if __name__ == '__main__':
    fromLang = sys.argv[2]
    toLang = sys.argv[3]
    directory = sys.argv[1]

    numberOfWords = int(sys.argv[4])
    files = getListOfFiles(directory)
    print(getListOfFiles(directory))

    content = {
        'on': {
            'workflow_dispatch': {
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
    }
    for i in files:
        print(i)
        new = {
            'name': 'build Anki Deck ' + ntpath.basename(i),
            'run': 'python main.py ' + i + ' ' + fromLang + ' ' + toLang + ' ' + str(numberOfWords)
        }
        content["jobs"]["build"]["steps"].insert(3, new)
        content['name']='"'+directory+'" - GW'
    with open('.github/workflows/'+directory.replace("/", ".")+'.yml', 'w') as f:
        yaml.dump(content, f)
