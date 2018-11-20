import sys


from PySide2 import QtCore
from PySide2 import QtWidgets

from nuke_camera_shaker.basic_button import BasicButton
from nuke_camera_shaker.opengl_widget import OGLWidget
from nuke_camera_shaker.shake_item import ShakeItem
import nuke_camera_shaker.nuke_utils as utils


class ShakeBox(QtWidgets.QWidget):
    cur_data, cur_shake = None, None

    def __init__(self):
        super(ShakeBox, self).__init__()
        self.shakes = utils.get_shakes_files()
        self.fps = 24
        self.build_ui()

        self.shake_tree.itemSelectionChanged.connect(self.update_oglwidget)
        self.multiply.valueChanged.connect(self.slider_moved)
        self.fps_input.textChanged.connect(self.update_fps)
        self.cancel_button.clicked.connect(self.cancel)
        self.import_button.clicked.connect(self.start_import)

    def build_ui(self):
        grid = QtWidgets.QGridLayout()
        left_layout = QtWidgets.QVBoxLayout()

        self.setMinimumSize(1000, 500)
        self.shake_tree = QtWidgets.QTreeWidget()

        multiply_label = QtWidgets.QLabel('Mutiply: ')
        self.multiply_label_value = QtWidgets.QLabel('1.0')
        multiply_layout = QtWidgets.QHBoxLayout()
        multiply_layout.addWidget(multiply_label)
        multiply_layout.addWidget(self.multiply_label_value)

        self.multiply = QtWidgets.QSlider()
        self.multiply.setOrientation(QtCore.Qt.Horizontal)
        self.multiply.setRange(0, 100)
        self.multiply.setValue(50)
        self.multiply.setTickInterval(10)
        self.multiply.setSingleStep(10)

        fps_label = QtWidgets.QLabel('FPS: ')
        self.fps_input = QtWidgets.QLineEdit()
        self.fps_input.setText('25')
        self.fps_input.setMaximumWidth(50)
        fps_layout = QtWidgets.QHBoxLayout()
        fps_layout.addWidget(fps_label)
        fps_layout.addWidget(self.fps_input)

        left_layout.addWidget(self.shake_tree)
        left_layout.addLayout(multiply_layout)
        left_layout.addWidget(self.multiply)
        left_layout.addLayout(fps_layout)

        self.cancel_button = BasicButton('cancel')
        self.import_button = BasicButton('import')
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.import_button)

        self.setup_tree()
        self.ogl_widget = OGLWidget()

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 4)

        grid.addLayout(left_layout, 0, 0)
        grid.addWidget(self.ogl_widget, 0, 1)
        grid.addLayout(button_layout, 1, 1)

        self.setLayout(grid)

    def setup_tree(self):

        self.shake_tree.setHeaderItem(QtWidgets.QTreeWidgetItem(["shakes"]))
        self.shake_tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        for shake_type in self.shakes:
            cat = QtWidgets.QTreeWidgetItem(self.shake_tree, [shake_type])
            for shake in self.shakes[shake_type]:
                ShakeItem(cat, shake)

    def update_oglwidget(self):
        self.cur_shake = self.shake_tree.currentItem()
        self.cur_data = utils.read_data_from_file(self.cur_shake.path)
        self.ogl_widget.data = self.cur_data
        self.ogl_widget.start_timer()

    def slider_moved(self, value):
        multiply = value/10.0
        self.multiply_label_value.setText(str(multiply))
        self.ogl_widget.multiply = multiply

    def update_fps(self, item):
        if utils.is_number(item):
            self.ogl_widget.fps = 1000.0/float(item)
            self.fps = item
            self.ogl_widget.start_timer()

    def start_import(self):
        if utils.is_number(self.fps):
            utils.create_transform(self.cur_data, self.multiply, self.fps, self.cur_shake)
        self.cancel()

    def cancel(self):
        self.close()


def start_from_nuke():
    global cam_shake_box
    cam_shake_box = ShakeBox()
    cam_shake_box.show()


def start_as_main():
    app = QtWidgets.QApplication(sys.argv)
    shake = ShakeBox()
    shake.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_as_main()
