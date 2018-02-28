from Qt import QtCore
from Qt import QtGui
from Qt import QtOpenGL


from nuke_camera_shaker.constants import LINE_WIDTH


class OGLWidget(QtOpenGL.QGLWidget):

    def __init__(self, fps=25):
        super(OGLWidget, self).__init__()

        self.toggle = True
        self.elapsed = 0
        self.init_ui()
        self.fps = fps
        self.multiply = 1
        self.data = None
        self.c_idx = 0

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animate)

    def start_timer(self):
        self.timer.start(self.fps)

    def stop_timer(self):
        self.timer.stop()

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()

    def init_ui(self):
        self.setMinimumSize(500, 400)
        self.setWindowTitle('Points')

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

