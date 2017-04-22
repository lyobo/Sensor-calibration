
# -*- coding: utf-8 -*-
from qgis.gui import *
from PyQt4.Qt import *

import selectSheet_window


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class SelectWindow(QDialog, selectSheet_window.Ui_selectSheets):
    def __init__(self):
        super(SelectWindow,self).__init__()
        self.setupUi(self)
        self.checkbox_none = None

    def _get_namelist(self, list):
        u'''
        获取主文件中的结点列表
        :param list:
        :return:
        '''
        self._name_list = list
        self._initialize_checkbox(self._name_list)

    def _initialize_checkbox(self, list):
        u'''
        对checkbox进行初始化，使其平均分布在三行。
        :param list:
        :return:
        '''
        self.checkbox_all = QCheckBox("select all",self)
        self.layout1.addWidget(self.checkbox_all)
        QtCore.QObject.connect(self.checkbox_all, QtCore.SIGNAL(_fromUtf8("clicked()")), self.select_all)
        self.box_list = []
        self._all_box_list = []
        for i in range(len(list)):
            checkbox=QCheckBox(list[i],self)
            checkbox.id = i
            checkbox.stateChanged.connect(self.checks)
            self._all_box_list.append(checkbox)
            self.layout1.addWidget(checkbox)

    def confirm_selection(self):
        u'''
        用户确认选择后，将所选的结点列表传回主文件内
        :return:
        '''
        self.accept()
        return self.box_list

    def checks(self,start):
        u'''
        检查checkbox是否被选中，并时刻扩充box列表
        :param start:
        :return:
        '''
        checkbox = self.sender()
        if start == Qt.Checked:
            self.box_list.append(checkbox.text())
            self.box_list = list(set(self.box_list))
            if self.checkbox_none is not None:
                self.checkbox_none.setChecked(False)
                if -1 in self.box_list:
                    self.box_list.remove(-1)
        elif start == Qt.Unchecked:
            self.box_list.remove(checkbox.text())

    def select_all(self):
        u'''
        全选的实现
        :return:
        '''
        if self.checkbox_all.isChecked():
            for c in self._all_box_list:
                c.setChecked(True)
            if self.checkbox_none is not None:
                self.checkbox_none.setChecked(False)
        else:
            for c in self._all_box_list:
                c.setChecked(False)

    def enable_sheet(self,namelist):
        u'''
        记住用户上次选择，使得下次出现该页面时用户的选择已经被选中
        :param namelist:
        :return:
        '''
        for c in self._all_box_list:
            if c.text() in namelist:
                c.setChecked(True)
        if -1 in namelist:
            self.checkbox_none.setChecked(True)
            self.box_list.append(-1)

    def init_None(self):
        self.checkbox_none = QCheckBox("No two sides Node",self)
        self.layout1.addWidget(self.checkbox_none)
        QtCore.QObject.connect(self.checkbox_none, QtCore.SIGNAL(_fromUtf8("clicked()")), self.select_none)

    def select_none(self):
        u'''
        全选的实现
        :return:
        '''
        if self.checkbox_none.isChecked():
            for c in self._all_box_list:
                c.setChecked(False)
            self.box_list.append(-1)
            self.checkbox_all.setChecked(False)
        else:
            self.box_list.remove(-1)