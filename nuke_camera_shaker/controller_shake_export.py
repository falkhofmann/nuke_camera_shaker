
# Import local modules
from nuke_camera_shaker import view_shake_export
from nuke_camera_shaker import model_export
from nuke_camera_shaker import utils


reload(view_shake_export)
reload(model_export)


class Controller:

    def __init__(self, view):
        self.view = view
        self.set_up_signals()

    def set_up_signals(self):
        self.view.save_file.connect(lambda file_path: self.verify_file_path(file_path))
        self.view.export.connect(lambda details: self.export_shake(details))

    def verify_file_path(self, file_path):
        updated_file_path = utils.combine_path_and_extension(file_path)
        self.view.update_field(updated_file_path)

    def export_file(self, details):
        model_export.export_animation_as_retime(*details)
        self.view.close()



    def export_shake(self, details):
        print details


def start():
    """Start up function."""

    global VIEW
    VIEW = view_shake_export.ViewExport()
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
    VIEW = view_shake_export.ViewExport()
    VIEW.raise_()
    VIEW.show()

    Controller(VIEW)
    app.exec_()


if __name__ == '__main__':
    start_from_main()
