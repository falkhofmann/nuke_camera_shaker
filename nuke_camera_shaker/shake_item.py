from PySide2 import QtWidgets


class ShakeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, cat, shake_tuple):

        super(ShakeItem, self).__init__()
        self.parentitem = cat
        self.cat = cat
        self.name = shake_tuple.name
        self.path = shake_tuple.path
        self.cat = shake_tuple.category
        self.setText(0, self.name)
        self.parentitem.addChild(self)
