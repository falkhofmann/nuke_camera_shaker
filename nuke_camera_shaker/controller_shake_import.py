
# Import local modules
from nuke_camera_shaker import view_shake_import
# from nuke_camera_shaker import model_import
from nuke_camera_shaker import utils

reload(view_shake_import)
# reload(model_import)
reload(utils)


class Controller:

    def __init__(self, view):
        self.view = view
        self.set_up_signals()

    def set_up_signals(self):
        self.view.import_shake.connect(lambda details: self.import_shake(details))

    @staticmethod
    def import_shake(details):
        pass
        # model_import.create_transform(*details)


def start():
    """Start up function."""

    shakes = utils.get_reformatted_shakes()

    global VIEW  # pylint: disable=global-statement
    VIEW = view_shake_import.CameraShake(shakes=shakes)
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
    VIEW = view_shake_import.CameraShake(shakes=shakes)
    VIEW.raise_()
    VIEW.show()

    Controller(VIEW)
    app.exec_()


if __name__ == '__main__':
    start_from_main()
