# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectSheet_window.ui'
#
# Created: Tue Mar 07 16:53:06 2017
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

class Ui_selectSheets(object):
    def setupUi(self, selectSheets):
        selectSheets.setObjectName(_fromUtf8("selectSheets"))
        selectSheets.resize(514, 528)
        self.confirm = QtGui.QPushButton(selectSheets)
        self.confirm.setGeometry(QtCore.QRect(210, 460, 91, 23))
        self.confirm.setObjectName(_fromUtf8("confirm"))
        self.verticalLayoutWidget = QtGui.QWidget(selectSheets)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 151, 441))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.layout1 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.layout1.setMargin(0)
        self.layout1.setObjectName(_fromUtf8("layout1"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(selectSheets)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(180, 20, 151, 441))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.layout2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.layout2.setMargin(0)
        self.layout2.setObjectName(_fromUtf8("layout2"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(selectSheets)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(340, 20, 151, 441))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.layout3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.layout3.setMargin(0)
        self.layout3.setObjectName(_fromUtf8("layout3"))

        self.retranslateUi(selectSheets)
        QtCore.QObject.connect(self.confirm, QtCore.SIGNAL(_fromUtf8("clicked()")), selectSheets.confirm_selection)
        QtCore.QMetaObject.connectSlotsByName(selectSheets)

    def retranslateUi(self, selectSheets):
        selectSheets.setWindowTitle(_translate("selectSheets", "selectSheets", None))
        self.confirm.setText(_translate("selectSheets", "确认", None))

