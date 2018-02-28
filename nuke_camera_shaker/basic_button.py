from Qt import QtWidgets

from nuke_camera_shaker.constants import STYLES


class BasicButton(QtWidgets.QPushButton):
    """Button class for changing colors during hovering."""

    def __init__(self, name, parent=None, enabled=True):
        super(BasicButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.setText(name)
        self.setStyleSheet(STYLES['regular'])
        self.setMaximumWidth(150)

    def enterEvent(self, event):  # pylint: disable=invalid-name,unused-argument
        """Catch mouse enter event on widget.

        Args:
            event (QtGui.QWidget.event): Qt Event

        """
        if self.isEnabled():
            self.setStyleSheet(STYLES['orange'])

    def leaveEvent(self, event):  # pylint: disable=invalid-name,unused-argument
        """Catch mouse leave event on widget.

        Args:
            event (QtGui.QWidget.event): Qt Event

        """
        if self.isEnabled():
            self.setStyleSheet(STYLES['regular'])
