# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets\filelist_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Filelist(object):
    def setupUi(self, Filelist):
        Filelist.setObjectName("Filelist")
        Filelist.resize(253, 92)
        Filelist.setAcceptDrops(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Filelist)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(Filelist)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)

        self.retranslateUi(Filelist)
        self.tableView.clicked['QModelIndex'].connect(Filelist.tableViewClicked)
        QtCore.QMetaObject.connectSlotsByName(Filelist)

    def retranslateUi(self, Filelist):
        _translate = QtCore.QCoreApplication.translate
        Filelist.setWindowTitle(_translate("Filelist", "Form"))
