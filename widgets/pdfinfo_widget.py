# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets\pdfinfo_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PDFinfo(object):
    def setupUi(self, PDFinfo):
        PDFinfo.setObjectName("PDFinfo")
        PDFinfo.resize(253, 124)
        self.verticalLayout = QtWidgets.QVBoxLayout(PDFinfo)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(PDFinfo)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)

        self.retranslateUi(PDFinfo)
        QtCore.QMetaObject.connectSlotsByName(PDFinfo)

    def retranslateUi(self, PDFinfo):
        _translate = QtCore.QCoreApplication.translate
        PDFinfo.setWindowTitle(_translate("PDFinfo", "Form"))
