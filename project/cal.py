# -*- coding: utf-8 -*-
# author: Joy Wang
#
# update time : 03/16/2017
#
# the module is to initalize the cal_window

import os
import sys
from PyQt4.Qt import *
from qgis.gui import *
from PyQt4 import QtGui
import xlrd
import xlwt
import numpy as np
import cal_window
import selectSheet
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

guiPath = os.getcwd()
sys.path.append(guiPath)


class CalWindow(QDialog, cal_window.Ui_Dialog):
    def __init__(self):
        super(CalWindow,self).__init__()
        self.setupUi(self)
        self._select_sheets = []
        self._readConfig()
        self.column_1s = None
        self.column_2s_1 = None
        self.column_2s_2 = None
        self.element = self.read_file()

    def openPara(self):
        u'''
        打开参数表格，同时连接到lineedit
        :return:
        '''
        para_path = QFileDialog.getOpenFileName(self, u"打开参数表格", guiPath, "table(*.xls)")
        self.lineEdit.setText(para_path)

    def openData(self):
        u'''
        打开待校准文件
        :return:
        '''
        data_path = QFileDialog.getOpenFileName(self, u"打开待校准数据表格", guiPath, "table(*.xls)")
        self.lineEdit_2.setText(data_path)

    def openparafile(self):
        u'''
        读取参数文件,同时设置下面输出按钮的able性
        :return:
        '''
        para_path = self.lineEdit.text()
        if os.path.isfile(para_path):
            self._para_data = xlrd.open_workbook(para_path)
            element_para = self._para_data.sheet_names()
            for i in self.element:
                if not i in element_para:
                    QMessageBox.critical(self,u'error',u'输入参数文件表名不匹配')
                    return 0
            self.node_split()
        self._check_enable()

    def opendatafile(self):
        u'''
        读取数据文件，同时配合参数文件共同设置输出属性的able
        :return:
        '''
        data_path = self.lineEdit_2.text()
        self._check_enable()

    def _check_enable(self):
        u'''
        检查输入框的文件是否存在，如果存在，则激活输出文件选项
        :return:
        '''
        data_path = self.lineEdit_2.text()
        if os.path.isfile(data_path):
            self._data_data = xlrd.open_workbook(data_path)
            if os.path.isfile(self.lineEdit.text()):
                self.pushButton_4.setEnabled(True)
        else:
            self.pushButton_4.setEnabled(False)

    def openSelect(self):
        u'''
        打开selectSheet窗口，（与UI里面类似），并传递参数。
        :return:
        '''
        self.k_sheet = self._para_data.sheet_by_index(0)
        self.b_sheet = self._para_data.sheet_by_index(1)
        self.data_node_list = self._data_data.sheet_names()
        para_node_list_temp = self.k_sheet.col_values(0)
        para_node_list_temp2 = map(int,para_node_list_temp)
        self.para_node_list = map(str,para_node_list_temp2)
        node_list = [val for val in self.data_node_list if val in  self.para_node_list]
        self.select = selectSheet.SelectWindow()
        self.select._get_namelist(node_list)
        self.select.enable_sheet(self._select_sheets)
        self.select.show()
        QtCore.QObject.connect(self.select.confirm, QtCore.SIGNAL(_fromUtf8("clicked()")), self.name_list)

    def name_list(self):
        u'''
        获取select页面的用户选择
        :return:
        '''
        self._select_sheets = self.select.confirm_selection()
        if self._select_sheets != []:
            self._get_range()
            self.pushButton_2.setEnabled(True)

    def enableButton(self):
        u'''
        判断输出选项是否选择完全，如果是，则激活使得最下面的校准按钮
        :return:
        '''
        if self._select_sheets != []:
            self._get_range()
            self.pushButton_2.setEnabled(True)

    def _get_range(self):
        u'''
        获得用户选择的输出通道
        :return:
        '''
        self.export_range = range(self.data_start, self.data_end + 1)

    def cal(self):
        u'''
        计算每一列，将其存储在新文件中（存储各个列的相对位置，第一列在最开头）
        :return:
        '''
        file_path = QFileDialog.getSaveFileName(self, 'save file', "saveFile", "excel files(*.xls)")
        if file_path is u'':
            return 0
        channel_list = self.export_range

        prog_max = len(self._select_sheets) * len(channel_list) * self._data_data.sheet_by_name(u"%s"%self._select_sheets[0]).nrows + 10
        progdialog = QtGui.QProgressDialog(u"计算中...",u"取消",0,prog_max,self)
        progdialog.setWindowTitle(u"计算进度")
        progdialog.setWindowModality(QtCore.Qt.WindowModal)
        progdialog.show()
        prog_id = 0

        file = xlwt.Workbook()
        for i in range(len(self._select_sheets)):
            table = file.add_sheet("%s"%self._select_sheets[i],cell_overwrite_ok=True)
            for j in channel_list:
                k,b = self.getPara(self._select_sheets[i],j)
                if k == u"None":
                    break
                if k == '':
                    continue
                ori_array = self.get_oriarray(self._select_sheets[i], j)
                cal_array = k * ori_array + b
                cal_list = cal_array.tolist()
                for k in range(len(cal_list)):
                    table.write(k,j-self.data_start,cal_list[k])
                    progdialog.setValue(prog_id)
                    prog_id = prog_id + 1

        file.save(file_path)
        prog_id = prog_id + 10
        progdialog.setRange(0,prog_id)
        progdialog.setValue(prog_id)
        progdialog.accept()
        QMessageBox.information(self, u"提示", u"操作成功！")


    def getPara(self,node_name,range_j):
        u'''
        读取相应结点相应通道和传感器的计算参数k和b
        :param node_name:
        :param range_j:
        :return:
        '''
        table_k = self._para_data.sheet_by_index(0)
        table_b = self._para_data.sheet_by_index(1)
        index = self.para_node_list.index(node_name)
        k = table_k.cell_value(index,range_j + 1 - self.data_start)
        b = table_b.cell_value(index,range_j + 1 - self.data_start)
        return k,b

    def get_oriarray(self,node_name,range_j):
        u'''
        获取计算前数列
        :param node_name:
        :param range_j:
        :return:
        '''
        table = self._data_data.sheet_by_name(u"%s"%node_name)
        if int(node_name) in self.node_1:
            ori_list = table.col_values(range_j)
        elif int(node_name) in self.node_2_1:
            ori_1 = table.col_values(range_j)
            if range_j > self.column_2s_1:
                ori_2 = table.col_values(range_j - self.column_2s_1)
            else:
                ori_2 = table.col_values(range_j + self.column_2s_1)
            ori_list = self.getmax(ori_1,ori_2)
        elif int(node_name) in self.node_2_2:
            ori_1 = table.col_values(range_j)
            if range_j > self.column_2s_2:
                ori_2 = table.col_values(range_j - self.column_2s_1)
            else:
                ori_2 = table.col_values(range_j + self.column_2s_2)
            ori_list = self.getmax(ori_1,ori_2)
        ori_array = np.array(ori_list)
        return ori_array

    def getmax(self,list1,list2):
        list = []
        for i in range(len(list1)):
            if list1[i] > list2[i]:
                list.append(list1[i])
            else:
                list.append(list2[i])
        return list

    def get_parapath(self, para_path,data_path):
        u'''
        如果该窗口通过UI窗口被调用，则运行该函数，获得UI窗口中用户已经输入的文件路径
        :param para_path:
        :param data_path:
        :return:
        '''
        if para_path is not u"":
            self.lineEdit.setText(u"%s" % para_path)
            self.openparafile()
        self.lineEdit_2.setText(u"%s" % data_path)
        self.opendatafile()

    def _readConfig(self):
        u'''
        读取配置文件，说明读取数据表格的格式
        :return:
        '''
        file = open("config\config_cal.txt", "r")
        line = "start reading"
        while (1):
            if (line == ""):
                break
            line = file.readline()
            split = line.strip().upper().split("=")
            if split[0].strip() == "DATA_START":
                self.data_start = int(split[1].strip()) - 1
            if split[0].strip() == "DATA_END":
                self.data_end = int(split[1].strip()) - 1
        file.close()

    def node_split(self):
        k = self._para_data.sheet_by_name(self.element[1])
        node_1s = []
        node_2s_1 = []
        node_2s_2 = []
        r = k.nrows
        for i in range(r):
            nodename = k.cell_value(i,0)
            row = k.row_values(i)
            # print row.count('')
            if row.count('') == self.column_1s - self.column_1s:
                node_1s.append(nodename)
            elif row.count('') == self.column_1s - self.column_2s_1:
                node_2s_1.append(nodename)
            elif row.count('') == self.column_1s - self.column_2s_2:
                node_2s_2.append(nodename)

        self.node_1 = node_1s
        self.node_2_1 = node_2s_1
        self.node_2_2 = node_2s_2

    def read_file(self):
        element = []
        file = open("config\config_combine.txt", "r")
        line = "start reading"
        while (1):
            if (line == ""):
                break
            line = file.readline()
            split = line.strip().split("=")
            if split[0].strip().upper() == "K":
                element.append(split[1].strip())
            if split[0].strip().upper() == "B":
                element.append(split[1].strip())
            if split[0].strip().upper() == 'MSE':
                element.append(split[1].strip())
            if split[0].strip().upper() == 'R2':
                element.append(split[1].strip())
            if split[0].strip().upper() == "COLUMN_1S":
                self.column_1s = int(split[1].strip())
            if split[0].strip().upper() == "COLUMN_2S_1":
                self.column_2s_1 = int(split[1].strip())
            if split[0].strip().upper() == "COLUMN_2S_2":
                self.column_2s_2 = int(split[1].strip())
        file.close()
        if len(element) is not 0:
            return element
        else:
            QMessageBox.critical(u'error', u'error in reading the config')
