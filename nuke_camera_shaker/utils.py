from collections import namedtuple
from collections import OrderedDict
from collections import defaultdict

import os
import re

from nuke_camera_shaker.constants import FILE_EXTENSION


def set_style_sheet(widget):

    styles_file = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                                "stylesheet.css"))

    with open(styles_file, "r") as file_:
        style = file_.read()
        widget.setStyleSheet(style)


def get_directory():

    return os.path.join(os.path.normpath(os.path.dirname(__file__)), '..', 'data')


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
            ordered_files = _reorder_shakes(files)
            for shake_file in ordered_files:
                name = os.path.splitext(shake_file)[0]
                path = os.path.join(folder_fpn, shake_file)
                data = read_data_from_file(path)
                shake_files.append(shake(name, path, category, data))

            shake_dict[category] = sorted(shake_files, key=lambda s: int(s.name.partition('_')[0].split('mm')[0]))

    return shake_dict


def _reorder_shakes(shakes):
    regex = r'(?P<focal>[\d]+)mm_(?P<distance>[\d.]+)m_(?P<counter>[A-Z]).{}'.format(FILE_EXTENSION)
    ordered = []
    temp = defaultdict(list)
    for shake in shakes:
        match = re.match(regex, shake).groupdict()
        temp[match['focal']].append(shake)

    for focal, shake in sorted(temp.items(), key=lambda s: int(s[0])):
        ordered += sorted(shake)
    return ordered


def read_data_from_file(path):
    with open(path) as f:
        content = f.read().splitlines()
    return tuple(tuple((float(y) for y in x.split(' '))) for x in content)
