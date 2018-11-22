# Import build-in modules
import csv
from collections import namedtuple

# Import third-party modules
import nuke

_KEYFRAME = namedtuple('keyframe', ['x', 'y'])



def export_animation_as_retime(shake_file_path, node_name, knob_name, export_from_range, first, last):

    knob = nuke.toNode(node_name)[knob_name]

    if export_from_range:
        keys = bake_and_convert_to_keyframes(knob, first, last)

    else:
        keys = convert_animation_to_keyframes(knob)

    with open(shake_file_path, 'w') as dst:
        writer = csv.writer(dst, delimiter=' ')

        for keyframe in keys:
            writer.writerow('{} {}'.format(keyframe.x, keyframe.y))


def convert_animation_to_keyframes(knob):

    animation_curve = knob.animation(0)
    return [_KEYFRAME(x=key.x, y=key.y) for key in animation_curve.keys()]


def bake_and_convert_to_keyframes(knob, first, last):
    return [_KEYFRAME(x=f, y=knob.valueAt(f)) for f in range(first, last+1)]