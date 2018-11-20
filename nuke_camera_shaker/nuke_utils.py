import nuke

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


def create_transform(shake_data, multiply, fps, shake, start_frame=1):
    transform = nuke.nodes.Transform()
    transform['label'].setValue('camera shake\n{}\n{}'.format(shake.cat, shake.name))
    tab = nuke.Tab_Knob('camshake', 'camera shake options')

    usr_speed = 1.0/(25.0/float(fps))
    speed = nuke.Double_Knob('speed')
    speed.setRange(0, 3)
    speed.setValue(usr_speed)

    mult = nuke.Double_Knob('multiply')
    mult.setRange(0, 10)
    mult.setValue(multiply)

    offset = nuke.Double_Knob('offset', 'timeoffset')
    offset.setRange(-200, 200)
    offset.setValue(0)

    transform.addKnob(tab)
    transform.addKnob(speed)
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
    translate.setExpression('curve(x*speed-(speed*first_frame)-offset)*multiply')


def is_number(usr_input):
    try:
        float(usr_input)
        return True
    except ValueError:
        return False
