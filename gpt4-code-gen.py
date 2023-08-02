import os
import re

# Set the directory you want to start from
rootDir = 'DIRECTORY_PATH'
regex = re.compile(r'applicationDefaults\s*\{.*?\}', re.DOTALL)
file_extension = 'FILE_EXTENSION'

#Extract and print
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
                    for match in matches:
                        print(match)

text_to_remove = 'TEXT_TO_REMOVE'

#remove text from file
for dirName, subdirList, fileList in os.walk(rootDir):
    print(f'Found directory: {dirName}')
    for fname in fileList:
        if fname.endswith(file_extension):
            file_path = os.path.join(dirName, fname)
            with open(file_path, 'r') as f:
                lines = f.readlines()
            with open(file_path, 'w') as f:
                for line in lines:
                    if text_to_remove in line:
                        modified_line = line.replace(text_to_remove, '')
                        if modified_line.strip():
                            f.write(modified_line)
                    else:
                        f.write(line)
