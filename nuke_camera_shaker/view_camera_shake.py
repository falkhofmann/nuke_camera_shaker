from PySide2 import QtCore
from PySide2 import QtGui
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


class SliderGroup(QtWidgets.QWidget):

    value_changed = QtCore.Signal(object)

    def __init__(self, label, value=10):
        super(SliderGroup, self).__init__()
        self._value = value
        self._build_widgets(label, value)
        self._build_layouts()
        self._set_up_signals()

    def _set_up_signals(self):
        self.slider.valueChanged.connect(self._update_label)

    def _build_widgets(self, label, value):
        self.label = QtWidgets.QLabel('{}: '.format(label))
        self.label_value = QtWidgets.QLabel(str(value/10.0))

        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(value)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(10)

    def _build_layouts(self):
        layout = QtWidgets.QVBoxLayout()
        label_layout = QtWidgets.QHBoxLayout()
        label_layout.addWidget(self.label)
        label_layout.addWidget(self.label_value)

        layout.addLayout(label_layout)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def _update_label(self, value):
        self.label_value.setText(str(value/10.0))
        self.value_changed.emit(value)

    @property
    def value(self):
        return self._value


class Draw(QtWidgets.QWidget):

    def __init__(self, fps=25):
        super(Draw, self).__init__()
        self.fps = fps

        self.toggle = True
        self.elapsed = 0

        self.multiply = 1
        self.data = None
        self.c_idx = 0

        self.timer = QtCore.QTimer(self)

        self.set_window_properties()
        self.set_up_signal()

        self.start_timer()

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

        self.fps = None
        self.current_shake = None
        self.current_data = None

        self._build_widgets()
        self._build_layouts()
        self._set_window_properties()
        self._set_up_signals()

        self._setup_tree()

    def _set_window_properties(self):
        self.setMinimumSize(1000, 500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def _build_widgets(self):
        self.shake_tree = QtWidgets.QTreeWidget()

        self.multiply = SliderGroup('Multiply', 10)

        self.fps_label = QtWidgets.QLabel('FPS: ')
        self.fps_input = QtWidgets.QLineEdit('25')
        self.fps_input.setValidator(QtGui.QIntValidator(0, 200))

        self.draw_widget = Draw()

        self.cancel_button = BasicButton('cancel')
        self.import_button = BasicButton('import')

    def _build_layouts(self):

        fps_layout = QtWidgets.QHBoxLayout()
        fps_layout.addWidget(self.fps_label)
        fps_layout.addWidget(self.fps_input)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.shake_tree)
        left_layout.addWidget(self.multiply)
        left_layout.addWidget(self.multiply)
        left_layout.addLayout(fps_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.import_button)

        grid = QtWidgets.QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 4)

        grid.addLayout(left_layout, 0, 0)
        grid.addWidget(self.draw_widget, 0, 1)
        grid.addLayout(button_layout, 1, 1)

        self.setLayout(grid)

    def _set_up_signals(self):
        self.shake_tree.itemSelectionChanged.connect(self._update_draw_widget)
        self.fps_input.textChanged.connect(self._update_fps)
        self.multiply.value_changed.connect(self._update_multiply)

        self.cancel_button.clicked.connect(self.close)
        self.import_button.clicked.connect(self.start_import)

    def _update_draw_widget(self):
        self.current_shake = self.shake_tree.currentItem()
        self.current_data = utils.read_data_from_file(self.current_shake.path)
        self.draw_widget.data = self.current_data
        self.draw_widget.start_timer()

    def start_import(self):

        self.import_shake.emit((self.current_data,
                                self.multiply,
                                self.fps,
                                self.current_shake))

        self.close()

    def _update_fps(self, item):
        self.draw_widget.fps = 1000.0/float(int(item))
        self.fps = item
        self.draw_widget.start_timer()

    def _update_multiply(self, value):
        self.draw_widget.multiply = value/10.0

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
        for shake_type in self.shakes:
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
