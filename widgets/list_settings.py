# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

if Path(__file__).parent.name == 'widgets':
    sys.path.append( str(Path(__file__).resolve().parent.parent) )

from widgets.list_settings_dialog import Ui_Dialog_list_settings
from model import Model, Delegate, Item

class ListSettings(QtWidgets.QDialog):
    def __init__(self, parent=None, datas_left=[], datas_right=[]):
        super(ListSettings, self).__init__(parent)
        self.ui = Ui_Dialog_list_settings()
        self.ui.setupUi(self)

        self.model_left = Model(None, Item())
        self.model_right = Model(None, Item())

        for model, datas, view in [
            [self.model_left, datas_left, self.ui.listView],
            [self.model_right, datas_right, self.ui.listView_2]
        ]:
            view.setModel(model)
            view.setItemDelegate(Delegate())
            model.insertRows(0, len(datas))
            model.insertColumns(0, ['C0'])
            for r, data in enumerate(datas):
                index = model.index(r, 0, QtCore.QModelIndex())
                model.setData(index, data)
        
    def up(self):
        parent = QtCore.QModelIndex()
        rows = set([ index.row() for index in self.ui.listView_2.selectedIndexes() ])
        sourceRow = min(rows)
        count = max(rows) - min(rows) + 1
        destinationChild = sourceRow-1
        if destinationChild < 0:
            return
        self.model_right.moveRows(parent, sourceRow, count, parent, destinationChild)

    def down(self):
        parent = QtCore.QModelIndex()
        rows = set([ index.row() for index in self.ui.listView_2.selectedIndexes() ])
        if len(rows) == 0:
            return
        sourceRow = min(rows)
        count = max(rows) - min(rows) + 1
        destinationChild = max(rows)  + 2
        if destinationChild > self.model_right.rowCount():
            return
        self.model_right.moveRows(parent, sourceRow, count, parent, destinationChild)

    def left(self):
        for index in self.ui.listView_2.selectedIndexes()[::-1]:
            self.model_right.removeRows(index.row(), 1)

    def right(self):
        indexes = self.ui.listView.selectedIndexes()
        self.model_right.insertRows(self.model_right.rowCount(), len(indexes))
        for i, index in enumerate(indexes):
            d = self.model_left.data(index)
            r = self.model_right.rowCount() - len(indexes) + i
            index_right = self.model_right.index(r, 0, QtCore.QModelIndex())
            self.model_right.setData(index_right, d)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ListSettings(None, ['a', 'b', 'c', 'd', 'e'], ['a', 'b', 'c', 'd', 'e'])
    r = window.exec()
    #app.exec()

    print(r)
    print([item.data('C0') for item in window.model_left.root_item.children()])
    print([item.data('C0') for item in window.model_right.root_item.children()])

if __name__ == '__main__':
    main()
