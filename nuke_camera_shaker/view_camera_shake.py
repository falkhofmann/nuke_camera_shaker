from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtOpenGL
from PySide2 import QtWidgets


from nuke_camera_shaker.constants import LINE_WIDTH
from nuke_camera_shaker import utils
from nuke_camera_shaker.shake_item import ShakeItem


class BasicButton(QtWidgets.QPushButton):
    """Button class for changing colors during hovering."""

    def __init__(self, name, parent=None, enabled=True):
        super(BasicButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.setText(name)
        self.setMaximumWidth(150)
        utils.set_style_sheet(self)


class OGLWidget(QtOpenGL.QGLWidget):

    def __init__(self, fps=25):
        super(OGLWidget, self).__init__()
        self.fps = fps

        self.toggle = True
        self.elapsed = 0
        self.set_window_properties()

        self.multiply = 1
        self.data = None
        self.c_idx = 0

        self.timer = QtCore.QTimer(self)

    def set_window_properties(self):
        self.setMinimumSize(700, 400)

    def set_up_signal(self):
        self.timer.timeout.connect(self.animate)

    def start_timer(self):
        self.timer.start(self.fps)

    def stop_timer(self):
        self.timer.stop()

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        pen = QtGui.QPen()
        pen.setWidth(1.5)
        qp.begin(self)
        qp.setPen(pen)
        self.draw_lines(qp)
        qp.end()

    def draw_lines(self, qp):

        if self.data:
            offset_x, offset_y = self.data[self.c_idx]

            space_x = int(self.width()/LINE_WIDTH)
            space_y = int(self.height()/LINE_WIDTH)

            for x in range(1, LINE_WIDTH):
                s = QtCore.QPointF(x * space_x + (offset_x * self.multiply), 0)
                e = QtCore.QPointF(x * space_x + (offset_x * self.multiply), self.height())
                qp.drawLine(s, e)

            for y in range(1, LINE_WIDTH):
                s = QtCore.QPointF(0, y * space_y + offset_y * self.multiply)
                e = QtCore.QPointF(self.width(), y * space_y + offset_y * self.multiply)
                qp.drawLine(s, e)

            if self.c_idx < len(self.data)-1:
                self.c_idx += 1
            else:
                self.c_idx = 0


class CameraShake(QtWidgets.QWidget):

    import_shake = QtCore.Signal(object)

    def __init__(self, shakes=[]):
        super(CameraShake, self).__init__()
        self.shakes = shakes

        self.build_widgets()
        self.build_layouts()
        self.set_window_properties()
        self.set_up_signals()

        self._setup_tree()

    def set_window_properties(self):
        self.setMinimumSize(1000, 500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def build_widgets(self):
        self.shake_tree = QtWidgets.QTreeWidget()

        self.multiply_label = QtWidgets.QLabel('Mutiply: ')
        self.multiply_label_value = QtWidgets.QLabel('1.0')

        self.multiply = QtWidgets.QSlider()
        self.multiply.setOrientation(QtCore.Qt.Horizontal)
        self.multiply.setRange(0, 100)
        self.multiply.setValue(50)
        self.multiply.setTickInterval(10)
        self.multiply.setSingleStep(10)

        self.fps_label = QtWidgets.QLabel('FPS: ')
        self.fps_input = QtWidgets.QLineEdit('25')

        self.ogl_widget = OGLWidget()

        self.cancel_button = BasicButton('cancel')
        self.import_button = BasicButton('import')

    def build_layouts(self):
        multiply_layout = QtWidgets.QHBoxLayout()
        multiply_layout.addWidget(self.multiply_label)
        multiply_layout.addWidget(self.multiply_label_value)

        fps_layout = QtWidgets.QHBoxLayout()
        fps_layout.addWidget(self.fps_label)
        fps_layout.addWidget(self.fps_input)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.shake_tree)
        left_layout.addLayout(multiply_layout)
        left_layout.addWidget(self.multiply)
        left_layout.addLayout(fps_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.import_button)

        grid = QtWidgets.QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 4)

        grid.addLayout(left_layout, 0, 0)
        grid.addWidget(self.ogl_widget, 0, 1)
        grid.addLayout(button_layout, 1, 1)

        self.setLayout(grid)

    def set_up_signals(self):
        self.multiply.valueChanged.connect(self.slider_moved)
        # self.fps_input.textChanged.connect(self.update_fps)
        self.cancel_button.clicked.connect(self.close)
        self.import_button.clicked.connect(self.start_import)

    def slider_moved(self, value):
        multiply = value/10.0
        self.multiply_label_value.setText(str(multiply))
        self.ogl_widget.multiply = multiply

    def start_import(self):

        self.import_shake.emit((self.cur_data,
                                self.multiply,
                                self.fps,
                                self.cur_shake))

        self.close()

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Catch user key events.

        Args:
            event: (QtGui.event)

        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def _setup_tree(self):
        self.shake_tree.setHeaderItem(QtWidgets.QTreeWidgetItem(["shakes"]))
        self.shake_tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        print self.shakes
        for shake_type in self.shakes:
            print shake_type
            cat = QtWidgets.QTreeWidgetItem(self.shake_tree, [shake_type])
            for shake in self.shakes[shake_type]:
                ShakeItem(cat, shake)


def start():
    """Start up function."""
    global interface  # pylint: disable=global-statement
    interface = CameraShake()
    interface.show()


def start_from_main():
    app = QtWidgets.QApplication()
    global interface  # pylint: disable=global-statement
    interface = CameraShake()
    interface.show()
    app.exec_()


if __name__ == '__main__':
    start_from_main()
