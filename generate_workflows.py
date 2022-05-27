import ntpath
import sys
import os
import yaml


# python .\generate_workflows.py lists es en 10000

# get all (sub)directory files
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
    # push_to_git = bool(sys.argv[5])
    files = getListOfFiles(directory)
    print(getListOfFiles(directory))
    content = {
        'on': {
            'push': {
                'branches': ["master"]
            }
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
                    'name': 'Push changes',
                    'uses': 'ad-m/github-push-action@master',
                    'with': {
                        'github_token': '${{ secrets.ADD_NEW }}',
                        'branch': '${{ github.ref }}',
                    }
                }]
            }
        }
    }
    content2 = content
    content["jobs"]["build"]["steps"].insert(3, {})
    for i in files:
        content = content2
        print(i)
        new = {
            'name': 'build Anki Deck ' + ntpath.basename(i),
            'run': '\npython main.py ' + i + ' ' + fromLang + ' ' + toLang + ' ' + str(numberOfWords)+'''\n
                    git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"\n
                    git config --local user.name "github-actions[bot]"\n
                    git add CreatedDecks'''
                    "\ngit rm "+'.github/workflows/' + i.replace("/", ".") + '.yml'+
                   '''\ngit commit -m "Uploaded Deck" -a
                   \ngit pull -r
           '''
        }
        content["jobs"]["build"]["steps"][3]=new
        content['name'] = '"' + i + '" - GW'
        f=open('.github/workflows/' + i.replace("/", ".") + '.yml', 'w')
        yaml.dump(content, f)
        f.close()
