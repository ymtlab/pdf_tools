# -*- coding: utf-8 -*-
import os
import sys
import shutil
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

if Path(__file__).parent.name == 'widgets':
    sys.path.append( str(Path(__file__).resolve().parent.parent) )

from widgets.unite_widget import Ui_Unite
from poppler import Poppler

class Unite(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Unite, self).__init__(parent)
        self.ui = Ui_Unite()
        self.ui.setupUi(self)

    def all(self):
        if self.find_mainwindow(self) is None:
            return
        p = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '\\Desktop\\united.pdf'
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', p, ('PDF (*.pdf)'))
        if not filename[0]:
            return
        model = self.filelist()
        paths = [ f.data('Path') for f in model.root_item.children() ]

        # file rename
        unite_paths = []
        for i, p in enumerate(paths):
            rename_path = Path('temp/' + str(i) + '.pdf')
            shutil.copy(p, rename_path)
            unite_paths.append(rename_path)
        
        # unite
        Poppler().pdfunite(unite_paths, Path(filename[0]))

        # rename file delete
        for path in unite_paths:
            path.unlink()

    def with_page_size(self):
        if self.find_mainwindow(self) is None:
            return
        p = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '\\Desktop'
        foldername = QtWidgets.QFileDialog.getExistingDirectory(self, 'Save folder', p)

        # get paths
        model = self.filelist()
        files = { f.data('Page size'):[] for f in model.root_item.children() }
        for f in model.root_item.children():
            files[f.data('Page size')].append( f.data('Path') )
        
        output_folder = Path(foldername)
        delete_paths = []
        for page_size in files:
            # file rename
            unite_paths = []
            for i, p in enumerate(files[page_size]):
                rename_path = Path('temp/' + str(i) + '.pdf')
                shutil.copy(p, rename_path)
                unite_paths.append(rename_path)
            
            # unite
            filename = output_folder / (page_size+'.pdf')
            Poppler().pdfunite( unite_paths, filename )
            delete_paths.append(len(unite_paths))
            
        # rename file delete
        for i in range(max(delete_paths)):
            Path('temp/' + str(i) + '.pdf').unlink()

    def filelist(self):
        mainwindow = self.find_mainwindow(self)
        dock = mainwindow.findChild(QtWidgets.QDockWidget, 'dockWidgetFile')
        tableView = dock.findChild(QtWidgets.QTableView)
        return tableView.model()
        
    def find_mainwindow(self, parent):
        if parent is None:
            return None
        if parent.inherits('QMainWindow'):
            return parent
        return self.find_mainwindow(parent.parent())

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Unite(None)
    window.show()
    app.exec()
 
if __name__ == '__main__':
    main()
