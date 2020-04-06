# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

if Path(__file__).parent.name == 'widgets':
    sys.path.append( str(Path(__file__).resolve().parent.parent) )

from widgets.pdfinfo_widget import Ui_PDFinfo
from model import Model, Delegate, Item

class PDFinfo(QtWidgets.QWidget):
    def __init__(self, parent):
        super(PDFinfo, self).__init__(parent)
        self.ui = Ui_PDFinfo()
        self.ui.setupUi(self)

        self.model = Model(self, Item())
        self.model.insertColumns(0, ['title', 'data'])
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setItemDelegate(Delegate())

    def copy(self):
        indexes = self.ui.tableView.selectedIndexes()
        d = { index.row():[] for index in indexes }
        [ d[index.row()].append(self.model.data(index)) for index in indexes ]
        t = '\n'.join([ '\t'.join(d[row]) for row in d ])
        QtWidgets.QApplication.clipboard().setText(t)

    def find_mainwindow(self, parent):
        if parent is None:
            return None
        if parent.inherits('QMainWindow'):
            return parent
        return self.find_mainwindow(parent.parent())

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_C: #copy
                self.copy()

    def pdfitem_from_mainwindow(self):
        try:
            mainwindow = self.find_mainwindow(self)
            dock = mainwindow.findChild(QtWidgets.QDockWidget, 'dockWidgetFile')
            tableView = dock.findChild(QtWidgets.QTableView)
            pdfitem = tableView.selectedIndexes()[0].internalPointer()
            _dict = pdfitem.to_dict()
            return _dict
        except:
            return None

    def update_view(self):
        # delete all row
        self.model.removeRows(0, self.model.rowCount())

        # get dictionaly from filelist tableview
        _dict = self.pdfitem_from_mainwindow()
        if _dict is None:
            return

        # insert rows in my model
        self.model.insertRows(0, len(_dict.keys()))

        index = self.model.index
        parent = QtCore.QModelIndex()

        # set datas from dictionaly
        for r, key in enumerate(_dict):
            self.model.setData( index(r, 0, parent), key )
            self.model.setData( index(r, 1, parent), _dict[key] )
        
        # model dataChanged emit
        self.model.dataChanged.emit( index(0, 0, parent), index(self.model.rowCount(), 1, parent) )

def main():
    app = QtWidgets.QApplication(sys.argv)
    pdfinfo = PDFinfo(None)
    pdfinfo.show()
    app.exec()
 
if __name__ == '__main__':
    main()
