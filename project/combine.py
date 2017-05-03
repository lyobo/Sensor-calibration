# -*- coding: utf-8 -*-
# author: Joy Wang
#
# update time : 03/22/2017
#
# the module is to initalize the combine window

import os
import sys
from PyQt4.Qt import *
from qgis.gui import *
import xlrd
import xlwt
import combine_window

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

guiPath = os.getcwd()
sys.path.append(guiPath)

class CombineWindow(QDialog, combine_window.Ui_Dialog):
    def __init__(self):
        super(CombineWindow,self).__init__()
        self.setupUi(self)
        self.element = self.readConfig_combine()
        self.warning_text = [u'',u'']
        self.node_1 = []
        self.node_2 = []
        self.select_1 = []
        self.select_2 = []

    def openday1(self):
        u'''
        获得day1数据
        :return:
        '''
        full_file = QFileDialog.getOpenFileName(self, u"打开表格", guiPath, "table(*.xls)")
        if full_file is not u"":
            self.day1Edit.setText(full_file)

    def openday2(self):
        u'''
        获取day2数据
        :return:
        '''
        full_file = QFileDialog.getOpenFileName(self, u"打开表格", guiPath, "table(*.xls)")
        if full_file is not u"":
            self.day2Edit.setText(full_file)

    def combine(self):
        u'''
        结合两个文件
        :return:
        '''
        file_path = QFileDialog.getSaveFileName(self, 'save file', "saveFile", "excel files(*.xls)")
        if file_path is u'':
            return 0
        file = xlwt.Workbook()
        for i in self.element:
            table_k = file.add_sheet(i, cell_overwrite_ok=True)
            table_1 = self.data_day1.sheet_by_name(i)
            table_2 = self.data_day2.sheet_by_name(i)
            rows = table_1.nrows
            cols = table_1.ncols
            for i in range(rows):
                table_k.write(i,0,table_1.cell_value(i,0))
                for j in range(1,cols):
                    if table_1.cell_value(i,j) == u'':
                        data = self.get_data(table_1,table_2,i,j)
                        table_k.write(i,j,data)
                    else:
                        try:
                            data1 = float(table_1.cell_value(i,j))
                            data2 = float(self.get_data(table_1,table_2,i,j))
                            data = (data1 + data2)/2
                            table_k.write(i,j,data)
                        except:
                            data = table_1.cell_value(i,j)
                            table_k.write(i,j,data)

        file.save(file_path)
        QMessageBox.information(self,u'提示',u"操作成功")

    def get_data(self,table1,table2,i,j):
        u'''
        获取数据
        :param table1:
        :param table2:
        :param i:
        :param j:
        :return:
        '''
        nodes = table1.cell_value(i,0)
        data = u''
        for m in range(len(self.common_node)):
            if nodes == self.common_node[m]:
                index = self.common_node_index[m]
                data = table2.cell_value(index,j)
        return data

    def enable(self):
        u'''
        激活exportnode选项
        :return:
        '''
        if os.path.isfile(self.day1Edit.text()) and os.path.isfile(self.day2Edit.text()):
            self.warningLabel1.setText(u'')
            self.combineButton.setEnabled(True)
            self.openfile(1)
            self.openfile(2)
            self.getnode_array()
        else:
            self.combineButton.setEnabled(False)
            if self.day1Edit.text() is not u'':
                if not os.path.isfile(self.day1Edit.text()):
                    self.warningLabel1.setText(u'正面数据表路径无效')
            else:
                self.warningLabel1.setText(u'')
            if self.day2Edit.text() is not u'':
                if not os.path.isfile(self.day2Edit.text()):
                    self.warningLabel2.setText(u'反面数据表路径无效')
            else:
                self.warningLabel2.setText(u'')

    def openfile(self,day_index):
        u'''
        打开文件
        :param day_index:
        :return:
        '''
        if day_index == 1:
            self.data_day1 = xlrd.open_workbook(self.day1Edit.text())
            element_day1 = self.data_day1.sheet_names()
            str = ''
            for i in self.element:
                if i not in element_day1:
                    str = str + ' ' + '%s'%i
            warning1 = u'正面数据表中,' + u'%s'%str + u" sheet不存在！" + '\n'
            if str != '':
                self.warningLabel1.setText(warning1)
                return 0
            else:
                self.warningLabel1.setText(u'')
                return 1
        if day_index == 2:
            self.data_day2 = xlrd.open_workbook(self.day2Edit.text())
            element_day2 = self.data_day2.sheet_names()
            str = ''
            for i in self.element:
                if i not in element_day2:
                    str = str + ' ' + '%s'%i
            warning2 =  u'反面数据表中,' + u'%s'%str + u" sheet不存在！" + '\n'
            if str != '':
                self.warningLabel2.setText(warning2)
                return 0
            else:
                self.warningLabel2.setText(u'')
                return 1

    def getnode_array(self):
        u'''
        获取公共结点
        :return:
        '''
        node_2s_1 = []
        node_2s_2 = []
        table_day1_k = self.data_day1.sheet_by_name(self.element[1])
        table_day2_k = self.data_day2.sheet_by_name(self.element[1])
        node_1 = table_day1_k.col_values(0)
        node_2 = table_day2_k.col_values(0)
        self.common_node = [val for val in node_2 if val in node_1]
        self.common_node_index = [node_2.index(val) for val in node_2 if val in node_1]
        if self.common_node == []:
            QMessageBox.critical(self,'error!',u'两个文件没有相同结点！')

    def readConfig_combine(self):
        u'''
        读取配置文件，说明读取数据表格的格式
        :return:
        '''
        element = []
        file = open("config\export_config.txt", "r")
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
            if split[0].strip().upper()  == 'MSE':
                element.append(split[1].strip())
            if split[0].strip().upper() == 'R2':
                element.append(split[1].strip())
        file.close()

        file = open("config\data_config.txt", "r")
        line = "start reading"
        while (1):
            if (line == ""):
                break
            line = file.readline()
            split = line.strip().split("=")
            if split[0].strip().upper() == 'COLUMN_1S_1':
                self.column_1s = int(split[1].strip())
            if split[0].strip().upper() == 'COLUMN_2S_1':
                self.column_2s_1 = int(split[1].strip())
            if split[0].strip().upper() == 'COLUMN_2S_2':
                self.column_2s_2 = int(split[1].strip())
        file.close()
        if len(element) is not 0:
            return element
        else:
            QMessageBox.critical(u'error',u'error in reading the config')

    def getPath(self,path):
        self.day1Edit.setText(path)