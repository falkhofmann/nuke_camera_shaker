from collections import namedtuple
from collections import OrderedDict

import os


def set_style_sheet(widget):

    styles_file = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                                "stylesheet.css"))

    with open(styles_file, "r") as file_:
        style = file_.read()
        widget.setStyleSheet(style)


def get_directory():
    return '../data'


def get_shakes_files():
    directory = get_directory()
    shake_dict = {}

    shake = namedtuple('shake', 'name path category data')

    for root, subdirs, filenames in os.walk(directory):
        for category in subdirs:
            shake_files = []
            folder_fpn = os.path.join(directory, category)

            if os.path.isdir(folder_fpn):
                files = os.listdir(folder_fpn)

                for shake_file in files:
                    name = os.path.splitext(shake_file)[0]
                    path = os.path.join(folder_fpn, shake_file)
                    data = read_data_from_file(path)
                    shake_files.append(shake(name, path, category, data))

            shake_files.sort()
            shake_dict[category] = shake_files
    return shake_dict


def get_reformatted_shakes():
    directory = get_directory()
    shake_dict = OrderedDict()

    shake = namedtuple('shake', 'name path category data')

    for root, categories, filenames in os.walk(directory):
        for category in categories:
            shake_files = []
            folder_fpn = os.path.join(directory, category)

            if not os.path.isdir(folder_fpn):
                return
            files = os.listdir(folder_fpn)

            for shake_file in files:
                name = os.path.splitext(shake_file)[0]
                path = os.path.join(folder_fpn, shake_file)
                data = read_data_from_file(path)
                shake_files.append(shake(name, path, category, data))

            shake_dict[category] = sorted(shake_files, key=lambda s: int(s.name.partition('_')[0].split('mm')[0]))

    return shake_dict


def read_data_from_file(path):
    with open(path) as f:
        content = f.read().splitlines()
    return tuple(tuple((float(y) for y in x.split(' '))) for x in content)


def get_new_filepath():
    shake_dir = get_directory()
    shake_files = get_shakes_files()

    last_file = shake_files[-1].name
    new = int(last_file) + 1
    new_file = os.path.join(shake_dir, (str(new).zfill(4))+ '.txt')
    return new_file


def write_shake_file(data):
    filepath = get_new_filepath()
    doc = open(filepath, 'w')
    doc.write(data)
    return doc

if __name__ == '__main__':
    print get_reformatted_shakes()