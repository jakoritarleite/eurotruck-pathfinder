import os
import string
import pathlib

target_extensions = {
    'inside': ['.tga', '.mat', '.tobj', '.pmd', '.pmc', '.pma', '.sii', '.dds', '.ogg', '.jpg', '.sui'],
    'lookup': {
        '.sii': 0,
        '.pmd': 0,
        '.tobj': 0,
        '.mat': 0
    }
}

found_paths = {
	'all': [],
    'binary': [],
    'text': []
}

def find_files(path):
    files: list = []

    print(f"Looking up in the [{path}] path")
    for actual_path, _, files_found in os.walk(path):
        for arq in files_found:
            ext = os.path.splitext(
                os.path.join(actual_path, arq)
            )[1]

            if target_extensions['lookup'].get(ext) == 0 or not ext:
                files.append(os.path.join(actual_path, arq))

    return files

def format_text_line(line):
    for i in range(len(line)):
        if line[i] == '"' and i != len(line) - 1:
            return line[i:].replace('"', '')

    return line

def format_bin_line(line):
    formatted_line = ''.join([str(char) for char in line if char in string.printable])

    if not formatted_line[0] in ['/', '\\']:
        for i in range(len(formatted_line) - 1):
            if formatted_line[i] in ['/', '\\']:
                formatted_line = formatted_line[i:]
                break

    return formatted_line if formatted_line else line

def create_ext_variation(path):
    _, ext = os.path.splitext(path)

    if ext in ['.tobj', '.dds', '.mat', '.tga']:
        return [
            path.replace(ext, '.tobj'),
            path.replace(ext, '.dds'),
            path.replace(ext, '.mat'),
            path.replace(ext, '.tga')
        ]

    if ext in ['.pmd', '.pmc', '.pmg', '.pma']:
        return [
            path.replace(ext, '.pmd'),
            path.replace(ext, '.pmc'),
            path.replace(ext, '.pmg'),
            path.replace(ext, '.pma')
        ]

    return []

def read_sii_mat_file(file_content):
    content = file_content.split('\n')

    for line in content:
        for extension in target_extensions['inside']:
            if extension in line:
                found_paths['text'].extend(create_ext_variation(format_text_line(line)))
                found_paths['all'].extend(create_ext_variation(format_text_line(line)))

def read_tobj_pmd_file(file_content):
    content = file_content.split('\n')

    for line in content:
        line = line.replace('\x00', '')\
            .replace('\x01', '')\
            .replace('\x02', '')\
            .replace('\x03', '')
        for extension in target_extensions['inside']:
            if extension in line:
                paths_in_line = [e+extension for e in line.split(extension) if e]
                for path in paths_in_line:
                    found_paths['binary'].extend(create_ext_variation(format_bin_line(path)))
                    found_paths['all'].extend(create_ext_variation(format_bin_line(path)))

def read_file(path):
    print(f"Looking up in the {path} file")

    with open(path, 'r', encoding='iso-8859-15') as file_content:
        file_content = file_content.read()
        if '.sii' in path or '.mat' in path:
            read_sii_mat_file(file_content)
        elif '.tobj' in path or '.pmd' in path:
            read_tobj_pmd_file(file_content)

def save_in_file(filename, paths):
    try:
        with open(filename, 'w') as infile:
            infile.write('\n'.join(list(dict.fromkeys(paths))))
    except FileNotFoundError:
        os.mkdir('pathfinder_output')
        save_in_file(filename, paths)

files = find_files(pathlib.Path().absolute())

for file in files:
    read_file(file)

save_in_file('pathfinder_output/text.files', found_paths['text'])
save_in_file('pathfinder_output/binary.files', found_paths['binary'])
save_in_file('list.txt', found_paths['all'])