# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets\filelist_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Filelist(object):
    def setupUi(self, Filelist):
        Filelist.setObjectName("Filelist")
        Filelist.resize(300, 300)
        Filelist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        Filelist.setAcceptDrops(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Filelist)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(Filelist)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)
        self.actionCopy = QtWidgets.QAction(Filelist)
        self.actionCopy.setObjectName("actionCopy")
        self.actionDelete_data = QtWidgets.QAction(Filelist)
        self.actionDelete_data.setObjectName("actionDelete_data")
        self.actionColumn_Settings = QtWidgets.QAction(Filelist)
        self.actionColumn_Settings.setObjectName("actionColumn_Settings")

        self.retranslateUi(Filelist)
        self.tableView.clicked['QModelIndex'].connect(Filelist.tableViewClicked)
        self.tableView.customContextMenuRequested['QPoint'].connect(Filelist.context_menu)
        self.actionCopy.triggered.connect(Filelist.copy)
        self.actionDelete_data.triggered.connect(Filelist.delete_data)
        self.actionColumn_Settings.triggered.connect(Filelist.column_settings)
        QtCore.QMetaObject.connectSlotsByName(Filelist)

    def retranslateUi(self, Filelist):
        _translate = QtCore.QCoreApplication.translate
        Filelist.setWindowTitle(_translate("Filelist", "File list"))
        self.actionCopy.setText(_translate("Filelist", "Copy"))
        self.actionCopy.setShortcut(_translate("Filelist", "Ctrl+C"))
        self.actionDelete_data.setText(_translate("Filelist", "Delete data"))
        self.actionDelete_data.setShortcut(_translate("Filelist", "Del"))
        self.actionColumn_Settings.setText(_translate("Filelist", "Column Settings"))
