# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets\convert_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Convert(object):
    def setupUi(self, Convert):
        Convert.setObjectName("Convert")
        Convert.resize(137, 259)
        self.verticalLayout = QtWidgets.QVBoxLayout(Convert)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolButton = QtWidgets.QToolButton(Convert)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/remixicon/save-3-line.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(24, 24))
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.verticalLayout.addWidget(self.toolButton)
        self.toolButton_2 = QtWidgets.QToolButton(Convert)
        self.toolButton_2.setIcon(icon)
        self.toolButton_2.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setObjectName("toolButton_2")
        self.verticalLayout.addWidget(self.toolButton_2)
        self.toolButton_3 = QtWidgets.QToolButton(Convert)
        self.toolButton_3.setIcon(icon)
        self.toolButton_3.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_3.setAutoRaise(True)
        self.toolButton_3.setObjectName("toolButton_3")
        self.verticalLayout.addWidget(self.toolButton_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Convert)
        self.toolButton.clicked.connect(Convert.to_png)
        self.toolButton_2.clicked.connect(Convert.to_jpeg)
        self.toolButton_3.clicked.connect(Convert.to_svg)
        QtCore.QMetaObject.connectSlotsByName(Convert)

    def retranslateUi(self, Convert):
        _translate = QtCore.QCoreApplication.translate
        Convert.setWindowTitle(_translate("Convert", "Form"))
        self.toolButton.setText(_translate("Convert", "PNG"))
        self.toolButton_2.setText(_translate("Convert", "JPEG"))
        self.toolButton_3.setText(_translate("Convert", "SVG"))
import resource_rc
