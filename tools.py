import os
import re
import logging
from typing import Union
from common.data import pwd  # noqa
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from share.data import url_regex, USER_AGENT  # noqa


def trimmer(data: Union[dict, list]):
    """
    Remove empty items from dict or list.
    """
    if type(data) is dict:
        new_data = {}
        for key in data:
            if data[key]:
                new_data[key] = trimmer(data[key])
        return new_data
    elif type(data) is list:
        new_data = []
        for index in range(len(data)):
            if data[index]:
                new_data.append(trimmer(data[index]))
        return new_data
    else:
        return data


def trim_key(data: dict, char: str = '_'):
    """
    Remove keys that start with char,
    defaults to '_'.
    """
    trim_list = []
    for i in data:
        if i.startswith(char):
            trim_list.append(i)
    for i in trim_list:
        data.pop(i)
    return data


def find_url(text: str):
    if text:
        result = re.findall(url_regex, text)
        if result:
            return result[0]
    return None


# run this before commit
# for aesthetic purpose

ignored_paths = [
    'archive',
    'share'
]


def sort_imports(path: str = pwd):
    # python_files = [i for i in os.listdir() if i.endswith('.py')]
    for root, dirs, files in os.walk(path):
        for file in files:
            if not any(p in root for p in ignored_paths) and file.endswith('.py'):
                sort_import(os.path.join(root, file))


def sort_import(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    original_lines = lines.copy()

    imports = []
    for line in lines:
        if line.startswith('import ') or line.startswith('from '):
            imports.append(line)
        else:
            break
    if not imports:
        return None

    # sort multiple imports
    # for line in imports:
    # this is not working
    for i in range(len(imports)):
        line = imports[i]
        if ',' in line:
            # is multiple import
            comments = line.split('#')[1] if '#' in line else ''
            import_keyword = line.split('import ')[0] + 'import '
            modules = line.split('#')[0].split('import ')[1].split(',')
            modules = [i.strip() for i in modules]
            modules.sort(key=lambda x: len(x))
            imports[i] = import_keyword + ', '.join(modules)
            if comments:
                imports[i] += '  # ' + comments.strip()
            imports[i] += '\n'

    # sort import lines
    imports.sort(key=lambda x: len(x.split('#')[0].strip()))

    # remove trailing whitespaces
    for i in range(len(imports)):
        imports[i] = imports[i].strip() + '\n'

    # replacing
    # for i in range(len(lines)):
    #     if lines[i].startswith('import ') or lines[i].startswith('from '):
    #         lines[i] = imports.pop(0)
    #     if not imports:
    #         break
    lines = imports + lines[len(imports):]

    if lines != original_lines:
        with open(file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f'{file} sorted')


def get_url_text(url: str) -> str:
    try:
        req = Request(url, headers={'User-Agent': USER_AGENT})
        with urlopen(req) as response:
            return response.read().decode('utf-8')
    except HTTPError:
        logging.warning(f'Failed to get text from {url}')
        return ''


def process_text(text: str) -> str:
    text = text.replace(',', '')
    text = text.replace('\t', '')
    text = text.strip()
    text = text.split('#')[0]
    text = text.split(' ')[0]
    return text


def get_url_int_set(url: str) -> set[int]:
    int_set = set()
    text = get_url_text(url)
    for line in text.splitlines():
        num_text = process_text(line)
        if num_text:
            num = int(num_text)
            int_set.add(num)
    return int_set


def get_url_str_set(url: str) -> set[str]:
    str_set = set()
    text = get_url_text(url)
    for line in text.splitlines():
        str_text = process_text(line)
        if str_text:
            str_set.add(str_text)
    return str_set


def get_url_str(url: str) -> str:
    text = get_url_text(url)
    while text.endswith('\n'):
        text = text[:-1]
    return text.strip()


if __name__ == '__main__':
    sort_imports(pwd)
