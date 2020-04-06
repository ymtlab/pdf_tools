# -*- coding: utf-8 -*-
import os
import sys
import shutil
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

if Path(__file__).parent.name == 'widgets':
    sys.path.append( str(Path(__file__).resolve().parent.parent) )

from widgets.convert_widget import Ui_Convert
from poppler import Poppler

class Convert(QtWidgets.QWidget):
    def __init__(self, parent, resolution=None):
        super(Convert, self).__init__(parent)
        self.ui = Ui_Convert()
        self.ui.setupUi(self)

    def to_png(self):
        paths = self.filepaths()
        if paths is None:
            return
        save_folder = self.save_folder_name()
        if save_folder == '':
            return
        self.excute(Path(save_folder + '/'), paths, '.png')
        
    def to_jpeg(self):
        paths = self.filepaths()
        if paths is None:
            return
        save_folder = self.save_folder_name()
        if save_folder == '':
            return
        self.excute(Path(save_folder + '/'), paths, '.jpg')
        
    def to_svg(self):
        paths = self.filepaths()
        if paths is None:
            return
        save_folder = self.save_folder_name()
        if save_folder == '':
            return
        self.excute(Path(save_folder + '/'), paths, '.svg')
        
    def excute(self, output_path, paths, suffix):
        # copy and rename
        rename_paths = [ Path('temp/' + str(i) + '.pdf') for i in range(len(paths)) ]
        for path, rename_path in zip(paths, rename_paths):
            shutil.copy(path, rename_path)
        
        # convert
        converted_paths = []
        for path in rename_paths:
            p = Poppler().pdftocairo(path, path.with_suffix(suffix), 300)
            converted_paths.append(p)
        
        # copy and rename
        for path, converted_path in zip(paths, converted_paths):
            copied = output_path / path.with_suffix(suffix).name
            shutil.copy(converted_path, copied)

        # delete temp files
        for p in rename_paths + converted_paths:
            p.unlink()

    def save_folder_name(self):
        p = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '\\Desktop'
        foldername = QtWidgets.QFileDialog.getExistingDirectory(self, 'Save folder', p)
        return foldername

    def filepaths(self):
        try:
            mainwindow = self.find_mainwindow(self)
            dock = mainwindow.findChild(QtWidgets.QDockWidget, 'dockWidgetFile')
            tableView = dock.findChild(QtWidgets.QTableView)
            model = tableView.model()
            paths = [ f.data('Path') for f in model.root_item.children() ]
            return paths
        except:
            return None
        
    def find_mainwindow(self, parent):
        if parent is None:
            return None
        if parent.inherits('QMainWindow'):
            return parent
        return self.find_mainwindow(parent.parent())

def main():
    app = QtWidgets.QApplication(sys.argv)
    convert = Convert(None)
    convert.show()
    app.exec()
 
if __name__ == '__main__':
    main()
