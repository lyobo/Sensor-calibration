# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'combine_window.ui'
#
# Created: Sat Mar 25 15:40:39 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(393, 197)
        self.warningLabel1 = QtGui.QLabel(Dialog)
        self.warningLabel1.setGeometry(QtCore.QRect(20, 10, 351, 31))
        self.warningLabel1.setText(_fromUtf8(""))
        self.warningLabel1.setObjectName(_fromUtf8("warningLabel1"))
        self.warningLabel2 = QtGui.QLabel(Dialog)
        self.warningLabel2.setGeometry(QtCore.QRect(20, 40, 351, 31))
        self.warningLabel2.setText(_fromUtf8(""))
        self.warningLabel2.setObjectName(_fromUtf8("warningLabel2"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 160, 351, 25))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.combineButton = QtGui.QPushButton(self.widget)
        self.combineButton.setEnabled(False)
        self.combineButton.setObjectName(_fromUtf8("combineButton"))
        self.horizontalLayout_4.addWidget(self.combineButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.widget1 = QtGui.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(22, 77, 351, 58))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Day1Button = QtGui.QPushButton(self.widget1)
        self.Day1Button.setObjectName(_fromUtf8("Day1Button"))
        self.horizontalLayout_2.addWidget(self.Day1Button)
        self.day1Edit = QtGui.QLineEdit(self.widget1)
        self.day1Edit.setObjectName(_fromUtf8("day1Edit"))
        self.horizontalLayout_2.addWidget(self.day1Edit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Day2Button = QtGui.QPushButton(self.widget1)
        self.Day2Button.setObjectName(_fromUtf8("Day2Button"))
        self.horizontalLayout.addWidget(self.Day2Button)
        self.day2Edit = QtGui.QLineEdit(self.widget1)
        self.day2Edit.setObjectName(_fromUtf8("day2Edit"))
        self.horizontalLayout.addWidget(self.day2Edit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.Day1Button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.openday1)
        QtCore.QObject.connect(self.Day2Button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.openday2)
        QtCore.QObject.connect(self.combineButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.combine)
        QtCore.QObject.connect(self.day1Edit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Dialog.enable)
        QtCore.QObject.connect(self.day2Edit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Dialog.enable)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "combine_xls", None))
        self.combineButton.setText(_translate("Dialog", "开始合并", None))
        self.Day1Button.setText(_translate("Dialog", "打开基准数据", None))
        self.Day2Button.setText(_translate("Dialog", "打开补充数据", None))

