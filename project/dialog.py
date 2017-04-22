# -*- coding: utf-8 -*-
# author: Joy Wang

import os
import sys
from PyQt4.Qt import *
from qgis.gui import *
from PyQt4 import QtGui
import xlrd
import xlwt
import numpy as np
import datetime
import dialog_window
import selectDate
import solar_location

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

guiPath = os.getcwd()
sys.path.append(guiPath)

class MainWindow(QDialog, dialog_window.Ui_Dialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.readConfig()
        self._select_sheets = []
        self.dir_path = ''
        self.str0 = u''
        self.str1 = u""

    def open_xlsx(self):
        para_path = QFileDialog.getOpenFileName(self, u"打开结点数据表格", guiPath, "table(*.xls)")
        self.lineEdit.setText(para_path)

    def combo_change(self):
        self.comboBox.clear()
        self.comboBox.addItem(u'--请选择存储相应数据的表格')
        path = self.lineEdit.text()
        if os.path.isfile(path):
            self.data = xlrd.open_workbook(path)
            sheetnamelist = self.data.sheet_names()
            for i in sheetnamelist:
                self.comboBox.addItem(u'%s'%i)

    def text_change(self):
        select_sheet = self.comboBox.currentText()
        if select_sheet == u"--请选择存储相应数据的表格":
            self.sheettext.setText(u'未选择表格')
            return
        else:
            str = u'已选中表格：%s'%select_sheet
            self.sheettext.setText(str)
            i = self.judge(select_sheet)
            if i:
                self.date_str_list = []
                datelist = self.getdate()
                ISOFORMAT = '%Y%m%d'
                str2 = u"表格中包含日期为："
                for i in datelist:
                    str0 = i.strftime(ISOFORMAT)
                    self.date_str_list.append(str0)
                    str2 = str2 + ' ' + i.strftime(ISOFORMAT)
                self.str = u'已选中表格：%s' % select_sheet + '\n' + str2
                self.sheettext.setText(self.str)
                self.pathButton.setEnabled(True)
                self.exportButton.setEnabled(True)
            else:
                self.pathButton.setEnabled(False)
                self.exportButton.setEnabled(False)
                self.str = self.str = u'已选中表格：%s'%select_sheet + '\n' + u'请检查配置文件或数据表'
                self.sheettext.setText(self.str)

    def date_selection(self):
        self.select = selectDate.SelectWindow()
        self.select._get_namelist(self.date_str_list)
        self.select.enable_sheet(self._select_sheets)
        self.select.show()
        QtCore.QObject.connect(self.select.confirm, QtCore.SIGNAL(_fromUtf8("clicked()")), self.name_list)

    def name_list(self):
        self._select_sheets = self.select.confirm_selection()
        if len(self._select_sheets) > 0:
            self.str0 = u'已选择的输出日期为：'
            for i in self._select_sheets:
                self.str0 = self.str0 + u" %s"%i
            self.sheettext.setText(self.str + '\n' + self.str0 + '\n' + self.str1)
            self.enable()
        else:
            self.str0 = u"请至少选择一个输出日期"
            self.sheettext.setText(self.str + '\n' + self.str0 + '\n' + self.str1)
            self.enable()

    def export_path(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, "choose directory",guiPath)
        self.str1 = u'当前输出文件夹：' + u"%s"%self.dir_path
        self.sheettext.setText(self.str + '\n' + self.str0 + '\n' +self.str1)
        self.enable()
    def enable(self):
        if self._select_sheets is not [] and self.dir_path is not '':
            self.startButton.setEnabled(True)
        else:
            self.startButton.setEnabled(False)

    def split(self):
        table_name_list = []
        for i in range(len(self._select_sheets)):
            table_name_list.append(self._select_sheets[i] + 'nodeData.xls')
        node_list = self.table.col_values(self.node)
        node_list = list(set(node_list))
        node_list.remove('')
        file_list = []
        table_list = []
        count_list = []
        for i in range(len(table_name_list)):
            file_list.append(xlwt.Workbook())
            temp_list = []
            temp_count = []
            for j in range(len(node_list)):
                if node_list[j] is not '':
                    temp_list.append(file_list[-1].add_sheet('%s'%int(node_list[j]),cell_overwrite_ok=True))
                    temp_count.append(0)
            table_list.append(temp_list)
            count_list.append(temp_count)

        prog_max = self.table.nrows + len(file_list)
        progdialog = QtGui.QProgressDialog(u"计算中...",u"取消",0,prog_max,self)
        progdialog.setWindowTitle(u"计算进度")
        progdialog.setWindowModality(QtCore.Qt.WindowModal)
        progdialog.show()
        prog_id = 0
        nrows = self.table.nrows
        for i in range(nrows):
            if progdialog.wasCanceled():
                return
            progdialog.setValue(prog_id)
            prog_id = prog_id + 1
            data = self.table.row_values(i)
            if data.count('') > 0:
                continue
            aggregation = data[self.aggregation]
            year = data[self.year]
            if int(year) - 100 < 0:
                year = int(year) + 2000
            month = data[self.month]
            day = data[self.day]
            hour = data[self.hour]
            minute = data[self.minute]
            second = data[self.second]
            node_name = data[self.node]
            data_slice = data[self.data_start:self.data_end + 1]
            combine = str(int(year)*10000 + int(month)*100 + int(day))
            time_conversion = (int(hour) - self.standard_hour)*3600 + (int(minute) - self.standard_minute)*60 + (int(second) - self.standard_second)
            time_conversion = time_conversion/self.times
            solar_ele,solar_azi = solar_location.solar_location_cal(year,month,day,hour,minute,self.lon,self.lat)

            if combine in self.date_str_list:
                date_index = self.date_str_list.index(combine)
                node_index = node_list.index(node_name)

            table = table_list[date_index][node_index]
            row = count_list[date_index][node_index]
            table.write(row,self.ex_aggregation,aggregation)
            table.write(row,self.ex_year,year)
            table.write(row,self.ex_month,month)
            table.write(row,self.ex_day,day)
            table.write(row,self.ex_hour,hour)
            table.write(row,self.ex_minute,minute)
            table.write(row,self.ex_second,second)
            table.write(row,self.ex_44column,data[self.column44])
            for i in range(self.ex_data_start,self.ex_data_end + 1):
                table.write(row,i,data_slice[i - self.ex_data_start])
            table.write(row,self.ex_node,node_name)
            table.write(row,self.ex_solar_ele,solar_ele)
            table.write(row,self.ex_solar_azi,solar_azi)
            table.write(row,self.ex_time_convertion,time_conversion)
            count_list[date_index][node_index] = count_list[date_index][node_index] + 1

        for i in range(len(file_list)):
            path = self.dir_path +'\\'+ table_name_list[i]
            file_list[i].save(path)
            if progdialog.wasCanceled():
                return
            progdialog.setValue(prog_id)
            prog_id = prog_id + 1

        progdialog.setValue(prog_id)
        progdialog.accept()
        QMessageBox.information(self, u"提示", u"操作成功！")

    def readConfig(self):
        file = open("config\\pre_basic_config.txt", "r")
        line = "start reading"
        while (1):
            if (line == ""):
                break
            line = file.readline()
            split = line.strip().upper().split("=")
            if split[0].strip() == "AGGREGATION":
                self.aggregation = int(split[1].strip()) - 1
            if split[0].strip() == "DATA_START":
                self.data_start = int(split[1].strip()) - 1
            if split[0].strip() == "DATA_END":
                self.data_end = int(split[1].strip()) - 1
            if split[0].strip().upper() == "YEAR":
                self.year = int(split[1].strip()) - 1
            if split[0].strip().upper() == "MONTH":
                self.month = int(split[1].strip()) - 1
            if split[0].strip().upper() == "DAY":
                self.day = int(split[1].strip()) - 1
            if split[0].strip().upper() == "HOUR":
                self.hour = int(split[1].strip()) - 1
            if split[0].strip().upper() == "MINUTE":
                self.minute = int(split[1].strip()) - 1
            if split[0].strip().upper() == "SECOND":
                self.second = int(split[1].strip()) - 1
            if split[0].strip().upper() == "VOLTAGE":
                self.voltage = int(split[1].strip()) - 1
            if split[0].strip().upper() == "44COLUMN":
                self.column44 = int(split[1].strip()) - 1
            if split[0].strip().upper() == "NODE":
                self.node = int(split[1].strip()) - 1

            if split[0].strip().upper() == "TOTALCOLUMN":
                self.total_column = int(split[1].strip())

            if split[0].strip().upper() == "STANDARD_HOUR":
                self.standard_hour = int(split[1].strip())
            if split[0].strip().upper() == "STANDARD_SECOND":
                self.standard_second = int(split[1].strip())
            if split[0].strip().upper() == "STANDARD_MINUTE":
                self.standard_minute = int(split[1].strip())
                self.standard_second = int(split[1].strip())
            if split[0].strip().upper() == "TIMES":
                self.times = int(split[1].strip())
            if split[0].strip().upper() == "LON":
                self.lon = float(split[1].strip())
            if split[0].strip().upper() == "LAT":
                self.lat = float(split[1].strip())
        file.close()

        file = open("config\\pre_export_config.txt", "r")
        line = "start reading"
        while (1):
            if (line == ""):
                break
            line = file.readline()
            split = line.strip().upper().split("=")
            if split[0].strip() == "AGGREGATION":
                self.ex_aggregation = int(split[1].strip()) - 1
            if split[0].strip() == "DATA_START":
                self.ex_data_start = int(split[1].strip()) - 1
            if split[0].strip() == "DATA_END":
                self.ex_data_end = int(split[1].strip()) - 1
            if split[0].strip().upper() == "YEAR":
                self.ex_year = int(split[1].strip()) - 1
            if split[0].strip().upper() == "MONTH":
                self.ex_month = int(split[1].strip()) - 1
            if split[0].strip().upper() == "DAY":
                self.ex_day = int(split[1].strip()) - 1
            if split[0].strip().upper() == "HOUR":
                self.ex_hour = int(split[1].strip()) - 1
            if split[0].strip().upper() == "MINUTE":
                self.ex_minute = int(split[1].strip()) - 1
            if split[0].strip().upper() == "SECOND":
                self.ex_second = int(split[1].strip()) - 1
            if split[0].strip().upper() == "44COLUMN":
                self.ex_44column = int(split[1].strip()) - 1
            if split[0].strip().upper() == "NODE":
                self.ex_node = int(split[1].strip()) - 1
            if split[0].strip().upper() == "SOLAR_ELE":
                self.ex_solar_ele = int(split[1].strip()) - 1
            if split[0].strip().upper() == "SOLAR_AZI":
                self.ex_solar_azi = int(split[1].strip()) - 1
            if split[0].strip().upper() == "TIME_CONVERTION":
                self.ex_time_convertion = int(split[1].strip()) - 1

            if split[0].strip().upper() == "TOTALCOLUMN":
                self.ex_total_column = int(split[1].strip()) - 1

    def judge(self,sheet_name):
        table = self.data.sheet_by_name(u'%s'%sheet_name)
        cols = table.ncols
        rows = table.nrows
        if cols is not self.total_column:
            return 0
        else:
            self.table = table
            return 1

    def getdate(self):
        date_list = []
        year_list = self.table.col_values(self.year)
        for i in range(len(year_list)):
            if year_list[i] == '':
                continue
            if int(year_list[i]/10) < 10:
                year_list[i] = int(year_list[i]) + 2000
        month_list = self.table.col_values(self.month)
        day_list = self.table.col_values(self.day)
        rows = self.table.nrows
        for i in range(rows):
            if year_list[i] == '' or month_list[i] == '' or day_list[i] == '':
                continue
            date = datetime.date(int(year_list[i]),int(month_list[i]),int(day_list[i]))
            date_list.append(date)
        date_list = list(set(date_list))
        return date_list
