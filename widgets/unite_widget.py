# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets\unite_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Unite(object):
    def setupUi(self, Unite):
        Unite.setObjectName("Unite")
        Unite.resize(181, 83)
        self.verticalLayout = QtWidgets.QVBoxLayout(Unite)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolButton = QtWidgets.QToolButton(Unite)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/remixicon/save-3-line.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(24, 24))
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.verticalLayout.addWidget(self.toolButton)
        self.toolButton_2 = QtWidgets.QToolButton(Unite)
        self.toolButton_2.setIcon(icon)
        self.toolButton_2.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setObjectName("toolButton_2")
        self.verticalLayout.addWidget(self.toolButton_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Unite)
        self.toolButton.clicked.connect(Unite.all)
        self.toolButton_2.clicked.connect(Unite.with_page_size)
        QtCore.QMetaObject.connectSlotsByName(Unite)

    def retranslateUi(self, Unite):
        _translate = QtCore.QCoreApplication.translate
        Unite.setWindowTitle(_translate("Unite", "Unite"))
        self.toolButton.setText(_translate("Unite", "Unite all"))
        self.toolButton_2.setText(_translate("Unite", "Unite with page size"))
import resource_rc
