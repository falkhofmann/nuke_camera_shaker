# Import build-in modules
import csv
from collections import namedtuple

# Import third-party modules
import nuke

_KEYFRAME = namedtuple('keyframe', ['x', 'y'])


def validate_node(node):

    return node.Class() in ('Transform',)


def message(message):
    nuke.message(message)


def export_animation_as_retime(node, shake_file_path, export_from_range, first, last):

    knob = node['translate']

    if export_from_range:
        keys = bake_and_convert_to_keyframes(knob, first, last)

    else:
        keys = convert_animation_to_keyframes(knob)

    with open(shake_file_path, 'w') as dst:
        writer = csv.writer(dst)

        for keyframe in keys:
            writer.writerow(keyframe)


def convert_animation_to_keyframes(knob):
    axis = [get_keyframes_from_animation(knob, axis) for axis in xrange(2)]
    return zip(axis[0], axis[1])


def get_keyframes_from_animation(knob, axis):
    return [key.y for key in knob.animation(axis).keys()]


def get_keyframes_from_frame(axis, first, last):
    return [axis.valueAt(f) for f in range(first, last+1)]


def bake_and_convert_to_keyframes(knob, first, last):
    return [knob.valueAt(f) for f in range(first, last+1)]

