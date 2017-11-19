import sys
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from PySide import QtOpenGL
import numpy
from operator import add

class Settings():

    WIDTH = 50
    HEIGHT = 30
    NUM_BLOCKS_X = 10
    NUM_BLOCKS_Y = 10

class hans (QtGui.QLabel):
    def __init__(self, parent = None):
        super(hans, self).__init__(parent)
        self.setText('peter')

    def move(self, pos_x, pos_y):
        self.setPos(pos_x, pos_y)

    def transform(self, mtx):
        self.setTransform(mtx)


class Grid (QtGui.QGraphicsItem):
    def __init__(self, scene, parent = None):
        self.lines = []
        QtGui.QGraphicsItem.__init__(self,parent)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

        width = Settings.NUM_BLOCKS_X * Settings.WIDTH
        height = Settings.NUM_BLOCKS_Y * Settings.HEIGHT

        pen = QtGui.QPen(QtGui.QColor(255, 0, 100), 1)

        for x in range(0,Settings.NUM_BLOCKS_X+1):
            xc = x * Settings.WIDTH
            self.lines.append(scene.addLine(xc,0,xc,height,pen))

        for y in range(0,Settings.NUM_BLOCKS_Y+1):
            yc = y * Settings.HEIGHT
            self.lines.append(scene.addLine(0,yc,width,yc,pen))

    def move(self, pos_x, pos_y):
        self.setPos(pos_x, pos_y)

    def transform(self, mtx):
        self.setTransform(mtx)

class Griddy (QtGui.QGraphicsItem):

    def __init__(self, scene):
        super(Griddy, self).__init__(None, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsMovable)
        self.rect = QtCore.QRectF(0, 0, 15, 15)
        self._scene = scene
        self._scene.clearSelection()
        self.lines = []

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(1)
        painter.setPen(pen)
        self.draw_grid()

    def draw_grid(self):
        width = Settings.NUM_BLOCKS_X * Settings.WIDTH
        height = Settings.NUM_BLOCKS_Y * Settings.HEIGHT
        pen = QtGui.QPen(QtGui.QColor(255, 0, 100), 1)

        for x in range(0,Settings.NUM_BLOCKS_X+1):
            xc = x * Settings.WIDTH
            self.lines.append(self._scene.addLine(xc,0,xc,height,pen))

        for y in range(0,Settings.NUM_BLOCKS_Y+1):
            yc = y * Settings.HEIGHT
            self.lines.append(self._scene.addLine(0,yc,width,yc,pen))

    def move(self, pos_x, pos_y):
        self.setPos(pos_x, pos_y)

    def transform(self, mtx):
        self.setTransform(mtx)

class ShakeView(QtGui.QGraphicsView):
    def __init__(self, scene, parent):
        super(ShakeView, self).__init__(parent)
        self._zoom = 0
        self._scene = scene
        self.setScene(self._scene)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtGui.QFrame.NoFrame)

class window(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(window, self).__init__()
        self.setWindowFlags(QtCore.Qt.Window)
        # make sure the widget is deleted when closed, so nuke doesn't crash on exit
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # make view
        self.view = QtGui.QGraphicsView(self)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setViewport(QtOpenGL.QGLWidget())
        # make view fit the widget size
        self.viewYoffset = 325  # 225
        self.view.setGeometry(0, 50, 500, 200)

        # make scene
        self.scene = QtGui.QGraphicsScene(self)
        # make scene fit the view size
        self.scene.setSceneRect(QtCore.QRect(0, 0, self.view.width(), self.view.height()))
        # set scene background colour
        self.scene.setBackgroundBrush(QtGui.QColor(50, 50, 50))
        # add scene to the view
        self.view.setScene(self.scene)


        #self.grid = Grid(self.scene)
        self.griddy = Griddy(self.scene)


        # set up timer
        self.rectangle = QtGui.QGraphicsRectItem(60,60,60,60)
        self.scene.addItem(self.rectangle)
        self.timer = QtCore.QBasicTimer()
        self.frameCounter = 0
        self.pos = [50,50]
        self.toggle = True
        self.zoom = 1.0
        self.rotate = 0

        self.timer.start(100, self)



    def timerEvent(self, e):
        old_pos = self.pos
        matrix = QtGui.QTransform()


        if self.toggle:
            offset = [20, 20]
            #self.rotate = 10
            self.toggle = not self.toggle
        else:
            offset = [-20, -20]
            #self.rotate = -10
            self.toggle = not self.toggle

        new_pos = map(add, old_pos, offset)


        matrix.translate(new_pos[0], new_pos[1])
        matrix.rotate(self.rotate)
        matrix.scale(1, 1.0)


        for item in self.scene.items():
            item.setTransform(matrix)


        #self.grid.move(new_pos[0], new_pos[1])
        #self.griddy.move(new_pos[0], new_pos[1])
        #self.rectangle.setPos(new_pos[0], new_pos[1])

        self.griddy.transform(matrix)
        #self.frameCounter += 1
        #print self.view.matrix()



    def startHead(self):
        # start animation head
        self.timerState = "head"
        self.slidingBall.setParticleColour(*self.alt_colour)
        self.slidingBall.move([self.slidingBall_xMin, self.slidingBall_yMin])
        self.growingBall.setParticleColour(*self.alt_colour)
        self.growingBall.scale(self.growingBall_rMin)
        self.flashingBall.setParticleColour(0.0, 0.0, 0.0)
        self.flashingBall.fade(self.flashingBall_aMin)

        self.timer.start(500, self)

    def startTail(self):
        # start animation tail
        self.timerState = "tail"
        self.slidingBall.move([self.slidingBall_xMax, self.slidingBall_yMax])
        self.growingBall.scale(self.growingBall_rMax)
        self.flashingBall.fade(self.flashingBall_aMax)

        self.timer.start(500, self)

    def beginAnimations(self):
        if self.timer.isActive():
            self.timer.stop()

        self.frameCounter = int(self.startFrameOld)
        self.duration = 1 + int(self.endFrameOld) - int(self.startFrameOld)  # in fps
        self.timer.start(self.GRAPHICS_RATE, self)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = window()
    # b.resize(800,600)
    win.show()
    sys.exit(app.exec_())