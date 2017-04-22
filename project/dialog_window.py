# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Thu Apr 13 20:47:09 2017
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
        Dialog.resize(331, 294)
        self.sheettext = QtGui.QLabel(Dialog)
        self.sheettext.setGeometry(QtCore.QRect(10, 200, 301, 71))
        self.sheettext.setText(_fromUtf8(""))
        self.sheettext.setWordWrap(True)
        self.sheettext.setObjectName(_fromUtf8("sheettext"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(12, 12, 301, 171))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.openButton = QtGui.QPushButton(self.widget)
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.horizontalLayout.addWidget(self.openButton)
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox = QtGui.QComboBox(self.widget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.exportButton = QtGui.QPushButton(self.widget)
        self.exportButton.setEnabled(False)
        self.exportButton.setObjectName(_fromUtf8("exportButton"))
        self.horizontalLayout_3.addWidget(self.exportButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pathButton = QtGui.QPushButton(self.widget)
        self.pathButton.setEnabled(False)
        self.pathButton.setObjectName(_fromUtf8("pathButton"))
        self.horizontalLayout_3.addWidget(self.pathButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.startButton = QtGui.QPushButton(self.widget)
        self.startButton.setEnabled(False)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout_4.addWidget(self.startButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.openButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.open_xlsx)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Dialog.combo_change)
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), Dialog.text_change)
        QtCore.QObject.connect(self.exportButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.date_selection)
        QtCore.QObject.connect(self.pathButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.export_path)
        QtCore.QObject.connect(self.startButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.split)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "node-segmentation", None))
        self.openButton.setText(_translate("Dialog", "打开文件", None))
        self.label_2.setText(_translate("Dialog", "请选择数据所在sheet:", None))
        self.exportButton.setText(_translate("Dialog", "输出天数选择", None))
        self.pathButton.setText(_translate("Dialog", "输出路径选择", None))
        self.startButton.setText(_translate("Dialog", "开始计算", None))

