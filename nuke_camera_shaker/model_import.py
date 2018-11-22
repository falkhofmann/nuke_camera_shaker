
# Import third party modules
import nuke

# Import local modules
from nuke_camera_shaker import utils


def read_data_from_node(node):
    keys_x = [key.y for key in node['translate'].animations()[0].keys()]
    keys_y = [key.y for key in node['translate'].animations()[1].keys()]
    export_string = ''.join([str(a) + ' ' + str(b) + '\n' for a, b in zip(keys_x, keys_y)])
    return export_string


def export_shake_from_node():

    node = nuke.selectedNode()
    if node.Class() == "Transform":
        data = read_data_from_node(node)
        shake_file = utils.write_shake_file(data)
        return shake_file


def create_transform(shake_data, multiply, fps, shake, start_frame=1001):
    transform = nuke.nodes.Transform()
    root_format = nuke.toNode('root')['format'].value()

    transform['center'].setValue((root_format.width()/2,
                                  root_format.height()/2))

    transform['label'].setValue('Imported shake\n{}\n{}'.format(shake.category,
                                                              shake.name))

    tab = nuke.Tab_Knob('camshake', 'camera shake')

    mult = nuke.Double_Knob('multiply')
    mult.setRange(0, 10)
    mult.setValue(multiply)

    offset = nuke.Double_Knob('offset', 'timeoffset')
    offset.setRange(-200, 200)
    offset.setValue(0)

    transform.addKnob(tab)
    transform.addKnob(mult)
    transform.addKnob(offset)

    translate = transform['translate']
    translate.setAnimated()

    frame = start_frame
    keys_x, keys_y = [], []

    for each in shake_data:
        keys_x.append((frame, each[0]))
        keys_y.append((frame, each[1]))
        frame += 1

    anim_x = translate.animations()[0]
    anim_y = translate.animations()[1]
    anim_x.addKey([nuke.AnimationKey(frame, value) for (frame, value) in keys_x])
    anim_y.addKey([nuke.AnimationKey(frame, value) for (frame, value) in keys_y])
    translate.setExpression('curve(x-offset)*multiply')
