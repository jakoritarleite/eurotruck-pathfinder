import os
import pathlib

def find_files(path):
    files: list = []

    print(f"Looking up in the [{path}] path")
    for actual_path, directories, files_found in os.walk(path):
        for arq in files_found:
            files.append(os.path.join(actual_path, arq))

    return files

found_files = find_files(str(pathlib.Path().absolute()) + "/Output")

transaction_fingerprint = str(input("What is the fingerprint you want to remove ?\n> "))
new_transaction_fingerprint = str(input("What is the new fingerprint you want to set ?\n> "))

for file in found_files:
    print('Cleaning file: ', file)
    with open(file, 'rb') as infile:
        file_content = infile.read()\
            .replace(transaction_fingerprint.encode(), new_transaction_fingerprint.encode())

        with open(file, 'wb') as outfile:
            outfile.write(file_content)
