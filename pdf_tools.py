# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

from mainwindow import Ui_MainWindow
from widgets import Filelist

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # add menu
        menu_view = self.ui.menubar.findChild(QtWidgets.QMenu, 'menuView')
        action_and_icon = [
            [self.ui.dockWidgetFile.toggleViewAction(), QtGui.QIcon('remixicon/edit-box-line.svg')],
            [self.ui.dockWidgetUnite.toggleViewAction(), QtGui.QIcon('remixicon/edit-box-line.svg')]
        ]
        for action, icon in action_and_icon:
            action.setIcon(icon)
            self.ui.toolBar.addAction(action)
            menu_view.addAction(action)
        
        self.ui.dockWidgetUnite.close()

    def open_pdfs(self):
        p = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '\\Desktop\\united.pdf'
        filenames = QtWidgets.QFileDialog.getOpenFileNames(
            self, 'Open PDF file', p, 'PDF File (*.pdf)'
        )
        if not filenames[0]:
            return
        filelist = self.ui.dockWidgetFile.findChild(Filelist)
        filelist.open_files([ Path(f) for f in filenames[0] ])

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
