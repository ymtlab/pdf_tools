# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

if Path(__file__).parent.name == 'widgets':
    sys.path.append( str(Path(__file__).resolve().parent.parent) )

from widgets.filelist_widget import Ui_Filelist
from widgets.list_settings import ListSettings
from poppler import Poppler
from model import Model, Delegate, Item

class Filelist(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Filelist, self).__init__(parent)
        self.ui = Ui_Filelist()
        self.ui.setupUi(self)
        self.setObjectName('Filelist')
        
        self.model = Model(None, Item())
        self.model.insertColumns(0, ['Name', 'Page size'])
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setItemDelegate(Delegate())

        self.droppable_suffix = ['.pdf']
        self.menu = QtWidgets.QMenu(self)
        self.menu.addActions([self.ui.actionCopy, self.ui.actionDelete_data, self.ui.actionColumn_Settings])
        
    def column_settings(self):
        # create list
        keys_list = [ c.to_dict().keys() for c in self.model.root_item.children() ]
        left_list = []
        [left_list.extend(keys) for keys in keys_list]
        left_list = sorted( list(set(left_list)) )
        right_list = self.model.columns()
        
        # show window
        list_settings = ListSettings(self, left_list, right_list)
        list_settings.setWindowTitle('Columns settings')
        r = list_settings.exec()

        if r == 0:
            return
        
        # insert columns
        self.model.removeColumns(0, self.model.columnCount())
        columns = [c.data('C0') for c in list_settings.model_right.root_item.children()]
        self.model.insertColumns(0, columns)
        
    def context_menu(self, point):
        self.menu.exec( self.focusWidget().mapToGlobal(point) )

    def copy(self):
        indexes = self.ui.tableView.selectedIndexes()
        d = { index.row():[] for index in indexes }
        [ d[index.row()].append(self.model.data(index)) for index in indexes ]
        t = '\n'.join([ '\t'.join(d[row]) for row in d ])
        QtWidgets.QApplication.clipboard().setText(t)

    def delete_data(self):
        indexes = self.ui.tableView.selectedIndexes()
        for index in indexes:
            self.model.setData(index, '')
            self.model.dataChanged.emit(index, index)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            suffixes = list(set( [Path(url.toLocalFile()).suffix.lower() for url in urls] ))
            for s in self.droppable_suffix:
                if s in suffixes:
                    suffixes.remove(s)
            if len(suffixes) > 0:
                event.ignore()
                return
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # input tableview
        paths = [Path(url.toLocalFile()) for url in event.mimeData().urls()]
        print(paths)
        self.open_files(paths)

        # input draw shapes
        mainwindow = self.find_mainwindow(self)
        dock = mainwindow.findChild(QtWidgets.QDockWidget, 'dockWidgetDrawshapes')
        draw_shapes = dock.findChild(QtWidgets.QTreeView).parentWidget()
        draw_shapes.reset()

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
        if e.key() == QtCore.Qt.Key_Delete:
            self.delete_data()

    def open_files(self, paths):
        pdfinfo = Poppler().pdfinfo
        dicts = [ pdfinfo(path) for path in paths ]

        self.model.removeRows(0, self.model.rowCount())
        self.model.insertRows(0, len(paths))

        for r in range(self.model.rowCount()):
            item = self.model.index(r, 0, QtCore.QModelIndex()).internalPointer()
            item.set_dict(dicts[r])

    def tableViewClicked(self, index):
        # has parent or not index.column() = 0
        mainwindow = self.find_mainwindow(self)
        #if mainwindow is None or not index.column() == 0:
        #    return

        # pdf to png and create scene from png
        gv = mainwindow.ui.graphicsView
        item = index.internalPointer()
        pixmap = item.data('Pixmap')
        if pixmap is None:
            p = Poppler().pdftocairo(item.data('Path'), Path('__temp__.png'), 300)
            scene = QtWidgets.QGraphicsScene()
            pixmap = QtGui.QPixmap(str(p))
            item.set_data('Pixmap', pixmap)
            scene.addPixmap(pixmap)
            p.unlink()
            # set scene in graphicsView
            gv.setScene(scene)
            gv.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        else:
            # set scene in graphicsView
            scene = QtWidgets.QGraphicsScene()
            scene.addPixmap(pixmap)
            gv.setScene(scene)

        # reset pdfinfo dock
        pdfinfo_dock = mainwindow.findChild(QtWidgets.QDockWidget, 'dockWidgetPDFinfo')
        pdfinfo = pdfinfo_dock.findChild(QtWidgets.QTableView).parentWidget()
        pdfinfo.update_view()

        # add shapes in graphicsView
        mainwindow = self.find_mainwindow(self)
        dock = mainwindow.findChild(QtWidgets.QDockWidget, 'dockWidgetDrawshapes')
        draw_shapes = dock.findChild(QtWidgets.QTreeView).parentWidget()
        shapes, size, rot = None, item.data('Page size'), item.data('Page rot')
        for child in draw_shapes.model.root_item.children():
            if child.data('Page size') == size and child.data('Page rot') == rot:
                shapes = child
        if shapes is None:
            return
        for shape in shapes.children(): # add shapes in graphicsView
            c = [ float(s) for s in shape.data('Page size').split(',') ]
            pixmap = shape.data('Pixmap')
            if pixmap is None:
                continue
            pixmap_item = gv.scene().addPixmap(pixmap)
            pixmap_item.setPos( c[0], c[1] )

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Filelist(None)
    window.show()
    app.exec()
 
if __name__ == '__main__':
    main()
