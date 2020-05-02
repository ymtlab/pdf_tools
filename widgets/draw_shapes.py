# -*- coding: utf-8 -*-
import datetime
import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

if Path(__file__).parent.name == 'widgets':
    sys.path.append( str(Path(__file__).resolve().parent.parent) )

from widgets.draw_shapes_widget import Ui_DrawShapes
from stamp import Stamp, CircleStamp, Square
from poppler import Poppler
from model import Model, Delegate, Item

class DrawShapes(QtWidgets.QWidget):
    def __init__(self, parent):
        super(DrawShapes, self).__init__(parent)
        self.ui = Ui_DrawShapes()
        self.ui.setupUi(self)
        
        self.model = Model(self, Item())
        self.model.insertColumns(0, ['Page size', 'Page rot', 'Pixmap'])

        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setItemDelegate(Delegate(self.ui.treeView))
        self.ui.treeView.setStyleSheet("QTreeView::item { padding: 10px }")
        self.ui.treeView.setColumnWidth(0, 130)
        self.ui.treeView.setColumnWidth(1, 55)
        self.ui.treeView.setColumnWidth(2, 40)

        self.ui.lineEdit_2.setText( str(datetime.date.today()) )

    def add_shape(self):
        # split list with parents
        indexes = self.ui.treeView.selectedIndexes()
        items = list(set( [i.internalPointer() for i in indexes if i.parent() == QtCore.QModelIndex()] ))

        # insert rows
        for item in items:
            parent = self.model.index(item.row(), 0, QtCore.QModelIndex())
            self.model.insertRows(item.child_count(), 1, parent)
            last_child = item.children()[-1]
            last_child.set_data('Page size', '0,0,0,0')

    def data_to_item(self, item, stamp_type):
        item.set_data('type', stamp_type)
        item.set_data('size', [self.ui.doubleSpinBox_4.value(), self.ui.doubleSpinBox_5.value()])
        item.set_data('text0', self.ui.lineEdit.text())
        item.set_data('text1', self.ui.lineEdit_2.text())
        item.set_data('text2', self.ui.lineEdit_3.text())
        item.set_data('font0', Path('C:/Windows/Fonts/msgothic.ttc'))
        item.set_data('font1', Path('C:/Windows/Fonts/msgothic.ttc'))
        item.set_data('font2', Path('C:/Windows/Fonts/msgothic.ttc'))
        item.set_data('font_size0', self.ui.doubleSpinBox.value())
        item.set_data('font_size1', self.ui.doubleSpinBox_2.value())
        item.set_data('font_size2', self.ui.doubleSpinBox_3.value())
        item.set_data('stroke', 'Red')
        item.set_data('fill', 'Red')

    def delete_shape(self):
        # split list with parents
        indexes = self.ui.treeView.selectedIndexes()
        items = list(set( [i.internalPointer() for i in indexes if not i.parent() == QtCore.QModelIndex()] ))
        parent_splited = { item.parent():[] for item in items }
        for item in items:
            parent_splited[item.parent()].append(item)
        
        # delete shape
        for parent in parent_splited:
            for child in parent_splited[parent][::-1]:
                parent_index = self.model.index(parent.row(), 0, QtCore.QModelIndex())
                self.model.removeRows(child.row(), 1, parent_index)
        
    def draw_all(self):
        stamps = {}
        for item in self.model.root_item.children():
            # create stamp
            stamp = item.data('stamp')
            ps = item.data('Page size').strip().split()
            page_size = ( float(ps[0]), float(ps[2]) )
            page_rot = int(item.data('Page rot'))
            stamp.save(page_size, page_rot)

            # set dictionary
            stamps[item.data('Page size')] = stamp

        # stamp
        fileitems = self.fileitems_from_mainwindow()
        for item in fileitems:
            stamps[ item.data('Page size') ].to_pdf( item.data('Path'), Path('output/') )

        # delete stamp pdfs
        for key in stamps:
            Path(stamps[key].path).unlink()

    def find_mainwindow(self, parent):
        if parent is None:
            return None
        if parent.inherits('QMainWindow'):
            return parent
        return self.find_mainwindow( parent.parent() )

    def fileitems_from_mainwindow(self, is_selected=False):
        try:
            tableView = self.find_mainwindow(self).filelist.ui.tableView
            if is_selected:
                return [ index.internalPointer() for index in tableView.selectedIndexes() ]
            else:
                return [ child for child in tableView.model().root_item.children() ]
        except:
            return None

    def get_shapes(self, page_size):
        # get item
        shapes_items = { item.data('Page size'):item for item in self.model.root_item.children() }
        shapes_item = shapes_items[page_size]

        # shapes
        shapes = []
        for item in shapes_item.children():
            c = item.data('Page size').strip().split(',')
            shape = { 'Pixmap':item.data('Pixmap'), 'x':c[0], 'y':c[1], 'w':c[2], 'h':c[3] }
            shapes.append(shape)
        return shapes

    def graphics_view(self):
        # find graphics view
        mainwindow = self.find_mainwindow(self)
        for child in mainwindow.children():
            if child.inherits('QGraphicsView'):
                return child
        return None

    def preview_stamp(self):
        # create temp item
        item = Item()
        self.data_to_item(item, 'circle_stamp')

        # set pixmap from pdf
        temp_path = Path('temp/__temp__.pdf')
        CircleStamp(None, item).preview(temp_path)
        iamge_path = Poppler().pdftocairo(temp_path, temp_path.with_suffix('.png'), 300)
        pixmap = QtGui.QPixmap.fromImage( QtGui.QImage(str(iamge_path), 'png') )
        iamge_path.unlink()
        temp_path.unlink()
        
        # set pixmap to scene
        scene = QtWidgets.QGraphicsScene(self)
        scene.addPixmap(pixmap)
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.scale(1.0, 1.0)

    def resolution(self):
        return '300'

    def reset(self):
        def is_in_items(items, item):
            size = item.data('Page size')
            rot = item.data('Page rot')
            for i in items:
                if size == i.data('Page size') and rot == i.data('Page rot'):
                    return True
            return False

        # unique page size and page rot
        items = []
        for item in self.fileitems_from_mainwindow():
            if is_in_items(items, item):
                continue
            items.append(item)

        # reset table when reload files
        self.model.removeRows( 0, self.model.rowCount() )
        self.model.insertRows( 0, len(items) )
        index = self.model.index

        for r, item in enumerate(items):
            self.model.setData( index(r, 0, QtCore.QModelIndex()), item.data('Page size') )
            self.model.setData( index(r, 1, QtCore.QModelIndex()), item.data('Page rot') )
            item = index( r, 0, QtCore.QModelIndex() ).internalPointer()
            item.set_data( 'stamp', Stamp(Path('temp/'+item.data('Page size')+'.pdf'), self, item) )

    def set_coordinate(self):
        if self.parent().visibleRegion().isEmpty():
            return
        
        graphics_view = self.graphics_view()
        if graphics_view is None:
            return
        
        # set clicked coordinate to selected items
        indexes = self.ui.treeView.selectedIndexes()
        items = list(set([ i.internalPointer() for i in indexes if not i.parent() == QtCore.QModelIndex()]))
        for item in items:
            item.set_data( 'Page size', ','.join([str(i) for i in graphics_view.coordinates]) )
            parent = self.model.index(item.parent().row(), 0, QtCore.QModelIndex())
            i = self.model.index(item.row(), 0, parent)
            self.model.dataChanged.emit(i, i)
        
    def set_stamp(self):
        items = set([ index.internalPointer() for index in self.ui.treeView.selectedIndexes() ])
        for item in items:
            if item.parent() is self.model.root_item:
                continue
            # add stamp and set data
            item.parent().data('stamp').add_circle_stamp(item)
            self.data_to_item(item, 'circle_stamp')

            # create circle stamp
            temp_path = Path('temp/__temp__.pdf')
            CircleStamp(None, item).preview(temp_path)
            iamge_path = Poppler().pdftocairo(temp_path, temp_path.with_suffix('.png'), 300)
            qimage = QtGui.QImage(str(iamge_path), 'png')
            pixmap = QtGui.QPixmap.fromImage(qimage)
            item.set_data('Pixmap', pixmap)
            iamge_path.unlink()
            temp_path.unlink()
            
    def set_square(self):
        items = list(set([ index.internalPointer() for index in self.ui.treeView.selectedIndexes() ]))
        
        for item in items:
            if item.parent() is self.model.root_item:
                return
            # set data to item
            item.extend_dict({
                'type':'square','stroke':self.ui.comboBox.currentText(),
                'fill':self.ui.comboBox_2.currentText()
            })
            item.parent().data('stamp').add_square(item)

            # create square
            temp_path = Path('temp/__temp__.pdf')
            Square(None, item).preview(temp_path)
            iamge_path = Poppler().pdftocairo(temp_path, temp_path.with_suffix('.png'), 300)
            qimage = QtGui.QImage(str(iamge_path), 'png')
            pixmap = QtGui.QPixmap.fromImage(qimage)
            item.set_data('Pixmap', pixmap)
            iamge_path.unlink()
            temp_path.unlink()
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    drawShapes = DrawShapes(None)
    drawShapes.show()
    app.exec()
 
if __name__ == '__main__':
    main()
