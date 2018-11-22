
# import third party modules
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

# Import local modules
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
        layout.setContentsMargins(0, 0, 0, 0)
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


class HorizontalLine(QtWidgets.QFrame):
    def __init__(self):
        super(HorizontalLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class Draw(QtWidgets.QWidget):

    def __init__(self, hue=1.0, pen_width=2, grid_size=10, fps=25):
        super(Draw, self).__init__()
        self.fps = fps
        self.pen_width = pen_width
        self.grid_size = grid_size
        self.hue = hue

        self.multiply = 1
        self.data = None
        self.index = 0
        self.pen = None

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
        # self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()

    def paintEvent(self, e):

        size = int(self.grid_size)

        painter = QtGui.QPainter()
        self.pen = QtGui.QPen()
        self.pen.setWidth(self.pen_width)

        self.pen.setColor(QtGui.QColor.fromHsvF(self.hue, 0.5, 0.75))
        painter.begin(self)
        painter.setPen(self.pen)
        self.draw_lines(painter, size)
        painter.end()

    def draw_lines(self, painter, size):

        if self.data:
            offset_x, offset_y = self.data[self.index]

            try:
                space_x = int(self.width()/size)
            except ZeroDivisionError:
                space_x = 1

            try:
                space_y = int(self.height()/size)
            except ZeroDivisionError:
                space_y = 1

            for x in range(1, size):
                start_x = QtCore.QPointF(x * space_x + (offset_x * self.multiply), 0)
                end_x = QtCore.QPointF(x * space_x + (offset_x * self.multiply), self.height())
                painter.drawLine(start_x, end_x)

            for y in range(1, size):
                start_y = QtCore.QPointF(0, y * space_y + offset_y * self.multiply)
                end_y = QtCore.QPointF(self.width(), y * space_y + offset_y * self.multiply)
                painter.drawLine(start_y, end_y)

            if self.index < len(self.data)-1:
                self.index += 1
            else:
                self.index = 0


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
        self.setMinimumSize(1000, 600)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Import Camera Shake file.')

    def _build_widgets(self):
        self.shake_tree = QtWidgets.QTreeWidget()

        self.multiply = SliderGroup('Multiply', 10)
        self.line_width = SliderGroup('Line width', 10)
        self.color = SliderGroup('Color', 0)
        self.grid_size = SliderGroup('Grid size', 50)

        self.fps_label = QtWidgets.QLabel('FPS: ')
        self.fps_input = QtWidgets.QSpinBox()
        self.fps_input.setValue(25)

        self.start_label = QtWidgets.QLabel('Start at: ')
        self.start_input = QtWidgets.QSpinBox()
        self.start_input.setRange(0, 10000)
        self.start_input.setValue(1001)

        self.draw_widget = Draw()

        self.cancel_button = BasicButton('cancel')
        self.import_button = BasicButton('import')

    def _build_layouts(self):

        fps_layout = QtWidgets.QHBoxLayout()
        fps_layout.addWidget(self.fps_label)
        fps_layout.addWidget(self.fps_input)

        start_layout = QtWidgets.QHBoxLayout()
        start_layout.addWidget(self.start_label)
        start_layout.addWidget(self.start_input)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.shake_tree)
        left_layout.addWidget(self.multiply)
        left_layout.addLayout(fps_layout)
        left_layout.addLayout(start_layout)

        left_layout.addWidget(HorizontalLine())

        left_layout.addWidget(self.grid_size)
        left_layout.addWidget(self.line_width)
        left_layout.addWidget(self.color)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addSpacerItem(QtWidgets.QSpacerItem(500, 50))
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
        self.fps_input.valueChanged.connect(self._update_fps)
        self.multiply.value_changed.connect(self._update_multiply)
        self.line_width.value_changed.connect(self._update_line_width)
        self.color.value_changed.connect(self._update_line_color)
        self.grid_size.value_changed.connect(self._update_grid_size)

        self.cancel_button.clicked.connect(self.close)
        self.import_button.clicked.connect(self.start_import)

    def _update_draw_widget(self):
        if not isinstance(self.shake_tree.currentItem(), ShakeItem):
            return
        self.current_shake = self.shake_tree.currentItem()
        self.current_data = utils.read_data_from_file(self.current_shake.path)
        self.draw_widget.data = self.current_data
        self.draw_widget.start_timer()

    def _update_fps(self, item):

        self.draw_widget.fps = 1000.0/float(int(item))
        self.fps = item
        self.draw_widget.start_timer()

    def _update_multiply(self, value):
        self.draw_widget.multiply = value/10.0

    def _update_line_width(self, value):
        self.draw_widget.pen_width = value/10.0

    def _update_line_color(self, value):
        self.draw_widget.hue = value/100.0

    def _update_grid_size(self, value):
        try:
            self.draw_widget.grid_size = value/5
        except ZeroDivisionError:
            self.draw_widget.grid_size = 1

    def _setup_tree(self):
        self.shake_tree.setHeaderItem(QtWidgets.QTreeWidgetItem(["shakes"]))
        self.shake_tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        for shake_type in self.shakes:
            cat = QtWidgets.QTreeWidgetItem(self.shake_tree, [shake_type])
            for shake in self.shakes[shake_type]:
                ShakeItem(cat, shake)

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Catch user key events.

        Args:
            event: (QtGui.event)

        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def start_import(self):

        self.import_shake.emit((self.current_data,
                                self.multiply.value/10.0,
                                self.fps_input.value(),
                                self.current_shake))

        self.close()
