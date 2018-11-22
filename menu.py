
import nuke

# Out of the Box Set
from nuke_camera_shaker import controller_shake_import
from nuke_camera_shaker import controller_shake_export


menubar = nuke.menu('Nuke')

nuke_hotboxes = menubar.addMenu("fhofmann")

nuke_hotboxes.addCommand("Camera Shake/Import Shake...", 'import_shake()')
nuke_hotboxes.addCommand("Camera Shake/Export Shake...", 'export_shake()')


def import_shake():
    reload(controller_shake_import)
    controller_shake_import.start()


def export_shake():
    reload(controller_shake_export)
    controller_shake_export.start()
