
# Import local modules
from nuke_camera_shaker import view_camera_shake
from nuke_camera_shaker import utils

reload(view_camera_shake)


class Controller:

    def __init__(self, view):
        self.view = view
        self.set_up_signals()

    def set_up_signals(self):
        self.view.import_shake.connect(lambda details: self.import_shake(details))

    def import_shake(self, details):
        print details


def start():
    """Start up function."""

    shakes = utils.get_shakes_files()

    global VIEW
    VIEW = view_camera_shake.CameraShake(shakes=shakes)
    VIEW.raise_()
    VIEW.show()

    Controller(VIEW)


def start_from_main():
    """Start up function."""
    import sys
    from PySide2 import QtWidgets

    shakes = utils.get_reformatted_shakes()
    app = QtWidgets.QApplication(sys.argv)

    global VIEW  # pylint: disable=global-statement
    VIEW = view_camera_shake.CameraShake(shakes=shakes)
    VIEW.raise_()
    VIEW.show()

    Controller(VIEW)
    app.exec_()


if __name__ == '__main__':
    start_from_main()
