import os
import re

# Set the directory you want to start from
rootDir = 'DIRECTORY_PATH'
regex = re.compile(r'applicationDefaults \{(.*?)\}', re.DOTALL)
file_extension = 'FILE_EXTENSION'

for dirName, subdirList, fileList in os.walk(rootDir):
    print(f'Found directory: {dirName}')
    for fname in fileList:
        if fname.endswith(file_extension):
            file_path = os.path.join(dirName, fname)
            with open(file_path, 'r') as f:
                contents = f.read()
                matches = regex.findall(contents)
                if matches:
                    print(f'File: {file_path}')
                    print(f'Matches: {matches}')
