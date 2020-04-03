# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

from widgets.filelist_widget import Ui_Filelist
from poppler import Poppler
from model import Model, Delegate, Item

class Filelist(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Filelist, self).__init__(parent)
        self.ui = Ui_Filelist()
        self.ui.setupUi(self)
        
        self.model = Model(None, Item())
        self.model.insertColumns(0, ['Name', 'Page size'])
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setItemDelegate(Delegate())
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            suffixes = list(set( [Path(url.toLocalFile()).suffix.lower() for url in urls] ))
            suffixes.remove('.pdf')
            if len(suffixes) > 0:
                event.ignore()
                return
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        paths = [Path(url.toLocalFile()) for url in event.mimeData().urls()]
        self.open_files(paths)

    def open_files(self, paths):
        pdfinfo = Poppler().pdfinfo
        dicts = [ pdfinfo(path) for path in paths ]

        self.model.removeRows(0, self.model.rowCount())
        self.model.insertRows(0, len(paths))

        for r in range(self.model.rowCount()):
            item = self.model.index(r, 0, QtCore.QModelIndex()).internalPointer()
            item.set_dict(dicts[r])

    def tableViewClicked(self, index):
        # pdf to png and create scene from png
        p = Poppler().pdftocairo(index.internalPointer().data('Path'), Path('__temp__.png'), 300)
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap( QtGui.QPixmap(str(p)) )
        p.unlink()

        # set scene in graphicsView from mainwindow
        gv = self.find_mainwindow(self).ui.graphicsView
        gv.setScene(scene)
        gv.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        
    def find_mainwindow(self, parent):
        if parent is None:
            return None
        if parent.inherits('QMainWindow'):
            return parent
        return self.find_mainwindow(parent.parent())

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Filelist(app)
    window.show()
    app.exec()
 
if __name__ == '__main__':
    main()
