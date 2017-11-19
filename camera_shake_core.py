import os
from collections import namedtuple
import pprint
try:
    import nuke
except:
    pass


def get_directory():
    return '/home/falcon/development/dummy_data/shakebox'


def get_shakes_files():
    directory = get_directory()
    shake_dict = {}
    shake = namedtuple('shake', 'name path category')
    for root, subdirs, filenames in os.walk(directory):
        for folder in subdirs:
            shake_files = []

            folder_fpn = os.path.join(directory, folder)
            if os.path.isdir(folder_fpn):
                files = os.listdir(folder_fpn)
                for each in files:
                    _shake = shake(each.split('.')[0], os.path.join(folder_fpn, each), folder)
                    shake_files.append(_shake)
            shake_files.sort()
            shake_dict[folder] = shake_files

    return shake_dict


def read_data_from_file(path):
    with open(path) as f:
        content = f.read().splitlines()
    return [[float(y) for y in x.split(' ')] for x in content]


def read_data_from_node(node):
    keys_x = [key.y for key in node['translate'].animations()[0].keys()]
    keys_y = [key.y for key in node['translate'].animations()[1].keys()]
    export_string = ''.join([str(a) + ' ' + str(b) + '\n' for a, b in zip(keys_x, keys_y)])
    return export_string


def get_new_filepath():
    shake_dir = get_directory()
    shake_files = get_shakes_files()

    last_file = shake_files[-1].name
    new = int(last_file) + 1
    new_file = os.path.join(shake_dir, (str(new).zfill(4))+ '.txt')
    return new_file


def export_shake_from_node():

    node = nuke.selectedNode()
    if node.Class() == "Transform":
        data = read_data_from_node(node)
        shake_file = write_shake_file(data)
        return shake_file


def write_shake_file(data):
    filepath = get_new_filepath()
    doc = open(filepath, 'w')
    doc.write(data)
    return doc


def get_test_shake():
    filepath = '/home/falcon/development/dummy_data/shakebox/002.txt'
    buffer = ""
    buffer += open(filepath, 'rU').read()
    return buffer


def test():
    shakes = get_shakes_files()
    pprint.pprint( shakes)
    tst = '/home/falcon/development/dummy_data/shakebox/floating/0001.txt'
    string = read_data_from_file(tst)
    print string