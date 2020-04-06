# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets\list_settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_list_settings(object):
    def setupUi(self, Dialog_list_settings):
        Dialog_list_settings.setObjectName("Dialog_list_settings")
        Dialog_list_settings.resize(300, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog_list_settings)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listView = QtWidgets.QListView(Dialog_list_settings)
        self.listView.setObjectName("listView")
        self.horizontalLayout.addWidget(self.listView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.toolButton = QtWidgets.QToolButton(Dialog_list_settings)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/remixicon/arrow-up-s-line.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(24, 24))
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.verticalLayout.addWidget(self.toolButton)
        self.toolButton_2 = QtWidgets.QToolButton(Dialog_list_settings)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/remixicon/arrow-down-s-line.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_2.setIcon(icon1)
        self.toolButton_2.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setObjectName("toolButton_2")
        self.verticalLayout.addWidget(self.toolButton_2)
        self.toolButton_3 = QtWidgets.QToolButton(Dialog_list_settings)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/remixicon/arrow-right-s-line.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_3.setIcon(icon2)
        self.toolButton_3.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_3.setAutoRaise(True)
        self.toolButton_3.setObjectName("toolButton_3")
        self.verticalLayout.addWidget(self.toolButton_3)
        self.toolButton_4 = QtWidgets.QToolButton(Dialog_list_settings)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/remixicon/arrow-left-s-line.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_4.setIcon(icon3)
        self.toolButton_4.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_4.setAutoRaise(True)
        self.toolButton_4.setObjectName("toolButton_4")
        self.verticalLayout.addWidget(self.toolButton_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.listView_2 = QtWidgets.QListView(Dialog_list_settings)
        self.listView_2.setObjectName("listView_2")
        self.horizontalLayout.addWidget(self.listView_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_list_settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_list_settings)
        self.buttonBox.accepted.connect(Dialog_list_settings.accept)
        self.buttonBox.rejected.connect(Dialog_list_settings.reject)
        self.toolButton.clicked.connect(Dialog_list_settings.up)
        self.toolButton_2.clicked.connect(Dialog_list_settings.down)
        self.toolButton_3.clicked.connect(Dialog_list_settings.right)
        self.toolButton_4.clicked.connect(Dialog_list_settings.left)
        QtCore.QMetaObject.connectSlotsByName(Dialog_list_settings)

    def retranslateUi(self, Dialog_list_settings):
        _translate = QtCore.QCoreApplication.translate
        Dialog_list_settings.setWindowTitle(_translate("Dialog_list_settings", "Dialog"))
        self.toolButton.setText(_translate("Dialog_list_settings", "Up"))
        self.toolButton_2.setText(_translate("Dialog_list_settings", "Down"))
        self.toolButton_3.setText(_translate("Dialog_list_settings", "Right"))
        self.toolButton_4.setText(_translate("Dialog_list_settings", "Left"))
import resource_rc
