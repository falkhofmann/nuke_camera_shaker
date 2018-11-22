
# Import third party modules
from PySide2 import QtWidgets


class ShakeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, cat, shake):

        super(ShakeItem, self).__init__()
        self.parentitem = cat
        self.name = shake.name
        self.path = shake.path
        self.category = shake.category
        self.setText(0, self.name)
        self.parentitem.addChild(self)
