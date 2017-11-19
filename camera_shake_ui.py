import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtUiTools import *
from PySide.QtOpenGL import *

import camera_shake_core as core
import camera_shake_util as util

reload(core)
reload(util)


class Settings():
    WIDTH = 50
    HEIGHT = 30
    LINES_X = 10
    LINES_Y = 10
    default_fps = 25
    default_mult = 1


class OGLWidget(QGLWidget):

    def __init__(self, default_fps):
        super(OGLWidget, self).__init__()

        self.toggle = True
        self.elapsed = 0
        self.init_ui()
        self.fps = default_fps
        self.multiply = 1
        self.data = None
        self.c_idx = 0
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.animate)

    def start_timer(self):
        self.timer.start(self.fps)

    def stop_timer(self):
        self.timer.stop()

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()

    def init_ui(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('Points')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        pen = QPen(Qt.SolidLine)
        pen.setColor(Qt.red)
        pen.setWidth(1.5)
        qp.begin(self)
        qp.setPen(pen)
        self.draw_lines(qp)
        qp.end()

    def draw_lines(self, qp):

        if self.data:
            offset_x, offset_y = self.data[self.c_idx]

            space_x = int(self.width()/Settings.LINES_X)
            space_y = int(self.height()/Settings.LINES_Y)

            for x in range(1, Settings.LINES_X):
                s = QPointF(x * space_x + (offset_x * self.multiply), 0)
                e = QPointF(x * space_x + (offset_x * self.multiply), self.height())
                qp.drawLine(s, e)

            for y in range(1, Settings.LINES_Y):
                s = QPointF(0, y * space_y + offset_y * self.multiply)
                e = QPointF(self.width(), y * space_y + offset_y * self.multiply)
                qp.drawLine(s, e)

            if self.c_idx < len(self.data)-1:
                self.c_idx += 1
            else:
                self.c_idx = 0


class ShakeItem(QTreeWidgetItem):
    def __init__(self, cat, shake_tuple):
        super(ShakeItem, self).__init__()
        self.parentitem = cat
        self.cat = cat
        self.name = shake_tuple.name
        self.path = shake_tuple.path
        self.cat = shake_tuple.category
        self.setText(0, self.name)
        self.parentitem.addChild(self)


class ShakeBox(QWidget):
    cur_data, cur_shake = None, None
    multiply = Settings.default_mult

    def __init__(self):
        super(ShakeBox, self).__init__()
        self.fps = Settings.default_fps

        self.load_ui()
        self.setup_tree()
        self.setup_values()
        self.add_oglwidget()

        self.sb.tree_shakes.itemSelectionChanged.connect(self.update_oglwidget)
        self.sb.line_fps.textChanged.connect(self.update_fps)
        self.sb.slider_multiply.valueChanged.connect(self.slider_moved)
        self.sb.btn_cancel.clicked.connect(self.cancel)
        self.sb.btn_import.clicked.connect(self.start_import)

    def add_oglwidget(self):
        self.shaky = OGLWidget(self.fps)
        self.sb.screen_layout = QHBoxLayout()
        self.sb.widget_screen.setLayout(self.sb.screen_layout)
        self.sb.screen_layout.addWidget(self.shaky)

    def load_ui(self):
        loader = QUiLoader()
        ui_dir = os.path.dirname(os.path.realpath(__file__))
        ui_filepath = os.path.join(ui_dir, "camera_shaker_ui.ui")
        ui_file = QFile(ui_filepath)
        ui_file.open(QFile.ReadOnly)
        self.sb = loader.load(ui_file, self)
        ui_file.close()

    def setup_tree(self):
        shakes = core.get_shakes_files()
        header = QTreeWidgetItem(["camshake types"])
        self.sb.tree_shakes.setHeaderItem(header)  # Another alternative is setHeaderLabels(["Tree","First",...])
        root = QTreeWidgetItem(self.sb.tree_shakes, ['shakes'])
        root.setData(2, Qt.EditRole, 'Some hidden data here')
        root.setExpanded(True)

        for shake_type in shakes:
            cat = QTreeWidgetItem(root, [shake_type])
            cat.setData(2, Qt.EditRole,'Some hidden data here')
            for shake in shakes[shake_type]:
                _shake = ShakeItem(cat, shake)
                _shake.setData(2, Qt.EditRole, 'Some hidden data here')

    def setup_values(self):
        self.sb.line_fps.setText(str(Settings.default_fps))

    def update_oglwidget(self):
        self.cur_shake = self.sb.tree_shakes.currentItem()
        self.cur_data = core.read_data_from_file(self.cur_shake.path)
        self.shaky.data = self.cur_data
        self.shaky.start_timer()

    def update_fps(self, item):
        if util.is_number(item):
            self.shaky.fps = 1000.0/float(item)
            self.fps = item
            self.shaky.start_timer()

    def slider_moved(self, value):
        self.multiply = value/10.0
        self.sb.label_multiply_value.setText(str(self.multiply))
        self.shaky.multiply = self.multiply

    def start_import(self):
        if util.is_number(self.fps):
            util.create_transform(self.cur_data, self.multiply, self.fps, self.cur_shake)

        self.cancel()

    def cancel(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.cancel()


def start_from_nuke():
    global cam_shake_box
    cam_shake_box = ShakeBox()
    cam_shake_box.show()


def start_as_main():
    app = QApplication(sys.argv)
    shake = ShakeBox()
    shake.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_as_main()
