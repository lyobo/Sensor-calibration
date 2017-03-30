# -*- coding: utf-8 -*-
# author: Joy Wang
#
# update time : 03/16/2017
#
# the module is to initalize the GUI

from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
import sys
import os
import xlrd
import xlwt
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas # matplotlib对PyQt4的支持
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import datetime

import new_window
import selectSheet
import cal
import combine

# 像ui转py学习字符转码
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

guiPath = os.getcwd()
sys.path.append(guiPath)


class UIWindow(QDialog,new_window.Ui_Calibration):
    def __init__(self):
        super(UIWindow,self).__init__()
        self.setupUi(self)
        self._createFigures()
        self._createLayouts()
        self._readConfig()
        self._starthour = ''
        self._startminute = ''
        self._endhour = ''
        self._endminute = ''
        self._column_index = None
        self.export_range = []
        self._select_sheets = []
        self.flag = 0
        self.para_path = u""

    def _createFigures(self):
        u'''
        创建绘图画布，设置背景标题坐标轴格式
        :return:
        '''
        self._fig = Figure(figsize=(8, 6), dpi=100, tight_layout=True)
        self._fig.set_facecolor("#F5F5F5")
        self._fig.subplots_adjust(left=0.08, top=0.92, right=0.95, bottom=0.1)
        self._canvas = FigureCanvas(self._fig)
        self._ax = self._fig.add_subplot(111)
        #self._ax.hold(True)
        self._initializeFigure()

    def _createLayouts(self):
        u'''
        给上面创建好的画布分配一个layout
        :return:
        '''
        layout = QHBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._canvas)

    def _initializeFigure(self):
        u'''
        对画布图像进行初始化——字体，坐标轴标题
        :return:
        '''
        Font = {'family': 'Tahoma',
                'weight': 'bold',
                'size': 8}
        self._ax.set_xlabel("time", fontdict=Font)
        self._ax.set_ylabel("intensity of illumination(Lx)", fontdict=Font)

    def openxlsx(self):
        u'''
        打开表格，交互操作
        :return:
        '''
        full_file = QFileDialog.getOpenFileName(self, u"打开表格", guiPath, "table(*.xls)")
        if full_file is not u"":
            self.fileEdit.setText(full_file)

    def setNodeBox(self):
        u'''
        对可选择结点进行初始化。
        :return:
        '''
        self.nodeBox.clear()
        self.nodeBox.addItem(u"--请选择结点")
        self.nodeBox.addItems(self._data.sheet_names())

    def setSensorBox(self):
        u'''
        对可选择传感器进行初始化
        :return:
        '''
        self.sensorBox.clear()
        self.sensorBox.addItem(u"--请选择传感器")
        node_name = self.nodeBox.currentText()
        if node_name.isdigit():
            self._table = self._data.sheet_by_name(node_name)
            if node_name in self.cir_2:
                column_list = range(1,self.column_2s_2 / 2 + 1)
                for i in column_list:
                    self.sensorBox.addItem(u'%s'%i)
            else:
                column_list = range(self.data_start,self.data_end + 1, 2)
                for i in column_list:
                    col_temp = self._table.col_values(i)
                    if col_temp.count(0) != len(col_temp):
                        self.sensorBox.addItem(u"%s"%((i - self.data_start + 2) / 2))

    def setChannelBox(self):
        u'''
        对可选通道初始化
        :return:
        '''
        node_index = self.nodeBox.currentText()
        sensor_name = self.sensorBox.currentText()
        self.groupBox_2.setEnabled(True)
        if sensor_name.isdigit():
            if node_index in self.rec_2:
                self.flag = 1
                self._column_index = self.data_start + int(str(sensor_name)) - 1
                self._time_list(0, self._table.nrows)
                self._illumination_list(0, self._table.nrows, 2)
                self._updateFigure(self.year_flag1, self.month_flag1, self.day_flag1, self.time_list_flag1,
                                   self.illumination_list_flag1, 7, 19)
                self.setTimeComboBox()
            elif node_index in self.cir_2:
                self.flag = 1
                self._column_index = self.data_start + int(str(sensor_name)) - 1
                self._time_list(0,self._table.nrows)
                self._illumination_list(0,self._table.nrows,2)
                self._updateFigure(self.year_flag1, self.month_flag1, self.day_flag1, self.time_list_flag1,
                                   self.illumination_list_flag1, 7, 19)
                self.setTimeComboBox()
            else:
                self.flag = 0
                self.getColumnIndex()

    def getColumnIndex(self):
        u'''
        获得可选列，并更新画布
        :return:
        '''
        sensor_index = self.sensorBox.currentText()
        channel_index = u"可见光"
        if sensor_index.isdigit():
            if channel_index == u"可见光":
                self.flag = 1
                self._column_index = 2 * int(str(sensor_index)) + self.data_start - 2
                self._time_list(0, self._table.nrows)
                self._illumination_list(0,self._table.nrows,1)
                self._updateFigure(self.year_flag1, self.month_flag1, self.day_flag1, self.time_list_flag1, self.illumination_list_flag1,7,19)
                self.setTimeComboBox()
            else:
                self.flag = 0


    def _updateFigure(self,year,month,day,time_list,illumination_list,min,max):
        u'''
        更新画布，设置默认时间为7到19点，后面若选择具体时间，则通过下面updateCanvas进行画布更新
        :return:
        '''
        min_date = datetime.datetime(year,month,day,min,0,0)
        max_date = datetime.datetime(year, month,day, max, 0, 0)
        Font = {'family': 'Tahoma',
                'weight': 'bold',
                'size': 8}
        self._ax.clear()
        self._ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
        self._ax.set_xlim([min_date,max_date])
        self._ax.plot(np.array(time_list),np.array(illumination_list),'r',label = "Data")
        self._ax.set_xlabel("time", fontdict=Font)
        self._ax.set_ylabel("intensity of illumination(Lx)", fontdict=Font)
        self._canvas.draw()

    def _time_list(self, start, end):
        column = self._column_index
        time_list = []
        range_temp = range(start,end)
        for i in range_temp:
            year = int(self._table.col(self.year_column)[i].value)
            month = int(self._table.col(self.month_column)[i].value)
            day = int(self._table.col(self.day_column)[i].value)
            hour = int(self._table.col(self.hour_column)[i].value)
            minute = int(self._table.col(self.minute_column)[i].value)
            second = int(self._table.col(self.second_column)[i].value)
            datetime_temp = datetime.datetime(year,month,day,hour,minute,second)
            time_list.append(datetime_temp)

        self.year_flag1 = year
        self.month_flag1 = month
        self.day_flag1 = day
        self.time_list_flag1 = time_list

    def _illumination_list(self,start,end,type):
        if type == 1:
            column = self._column_index
            illumination_list = self._table.col_values(column, start, end)
            self.illumination_list_flag1 = illumination_list
        if type == 2:
            col1 = self._column_index
            col_temp = self._table.col_values(col1 + self.column_2s_1,start,end)
            if col_temp.count(0) == len(col_temp):
                col2 = col1 + self.column_2s_2
            else:
                col2 = self._column_index + self.column_2s_1
            illumination_list1 = []
            illumination_list2 = []
            time1 = []
            time2 = []
            illumination_list_1 = self._table.col_values(col1, start, end)
            illumination_list_2 = self._table.col_values(col2, start, end)
            for i in range(len(illumination_list_1)):
                if illumination_list_1[i] >= illumination_list_2[i]:
                    illumination_list1.append(illumination_list_1[i])
                    time1.append(self.time_list_flag1[i])
                else:
                    illumination_list2.append(illumination_list_2[i])
                    time2.append(self.time_list_flag1[i])

            if len(illumination_list1) > len(illumination_list2):
                self.illumination_list_flag1 = illumination_list1
                self.time_list_flag1 = time1
            else:
                self.illumination_list_flag1 = illumination_list2
                self.time_list_flag1 = time2

    def setTimeComboBox(self):
        u'''
        设置可选初始时间
        :return:
        '''
        if self.flag == 1:
            self.starthourBox.clear()
            self.starthourBox.addItem(u"--开始（小时）")
            self._hourtemp = self._table.col_values(self.hour_column)
            self._hourlist = list(set(self._hourtemp))
            for i in range(len(self._hourlist)):
                self.starthourBox.addItem(u"%s" % int(self._hourlist[i]))
        elif self.flag == 2:
            self.starthourBox.clear()
            self.starthourBox.addItem(u"--开始（小时）")
            for i in range(len(self.hourstandard_list)):
                self.starthourBox.addItem(u"%s" % int(self.hourstandard_list[i]))

    def setStartminute(self):
        u'''
        初始化开始分钟数。
        :return:
        '''
        self.startminuteBox.clear()
        self.startminuteBox.addItem(u"--开始（分钟）")
        self._starthour = self.starthourBox.currentText()
        if self.flag == 1:
            if self._starthour.isdigit():
                self._minutetemp = self._table.col_values(self.minute_column)
                for i in range(len(self._minutetemp)):
                    if self._hourtemp[i] == int(self._starthour):
                        self.startminuteBox.addItem("%s" % int(self._minutetemp[i]))
        if self.flag == 2:
            if self._starthour.isdigit():
                for i in range(len(self.minutestandard_list)):
                    if self.hourstandard_temp[i] == int(self._starthour):
                        self.startminuteBox.addItem("%s"%int(self.minutestandard_list[i]))

    def setEndhour(self):
        u'''
        设置终止小时（小于等于开始小时）
        :return:
        '''
        self.endhourBox.clear()
        self.endhourBox.addItem(u"--结束（小时）")
        self._startminute = self.startminuteBox.currentText()
        if self._startminute.isdigit():
            if self.flag == 1:
                for i in range(len(self._hourlist)):
                    if int(self._hourlist[i]) >= int(self._starthour):
                        self.endhourBox.addItem(u"%s" % int(self._hourlist[i]))
            if self.flag  == 2:
                for i in range(len(self.hourstandard_list)):
                    if int(self.hourstandard_list[i]) > int(self._starthour):
                        self.endhourBox.addItem((u"%s"% int(self.hourstandard_list[i])))

    def setEndminute(self):
        u'''
        设置终止分钟，确保终止时间晚于开始时间。
        :return:
        '''
        self.endminuteBox.clear()
        self.endminuteBox.addItem(u"--结束（分钟）")
        self._endhour = self.endhourBox.currentText()
        if self._endhour.isdigit():
            if self.flag == 1:
                if int(self._endhour) == int(self._starthour):
                    for i in range(self._table.nrows):
                        if (self._hourtemp[i] == int(self._endhour)) and (int(self._minutetemp[i]) > int(self._startminute)):
                            self.endminuteBox.addItem("%s" % int(self._minutetemp[i]))
                else:
                    for i in range(len(self._minutetemp)):
                        if self._hourtemp[i] == int(self._endhour):
                            self.endminuteBox.addItem("%s" % int(self._minutetemp[i]))
            if self.flag == 2:
                if int(self._endhour) == int(self._starthour):
                    for i in range(self._table_standard.nrows):
                        if (self.hourstandard_temp[i] == int(self._endhour)) and (int(self.minutestandard_list[i]) > int(self._startminute)):
                            self.endminuteBox.addItem("%s"% int(self.minutestandard_list[i]))
                else:
                    for i in range(len(self.minutestandard_list)):
                        if self.hourstandard_temp[i] == int(self._endhour):
                            self.endminuteBox.addItem("%s"% int(self.minutestandard_list[i]))

    def updateCanvas(self):
        u'''
        在用户选择好标准列后更新画布
        :return:
        '''
        self._endminute = self.endminuteBox.currentText()
        if self._starthour.isdigit() and self._endhour.isdigit() and self._endminute.isdigit() and self._startminute.isdigit():
            start, end = self._getSliceColumn()
            if self.flag == 1:
                self._updateFigure(self.year_flag1, self.month_flag1, self.day_flag1, self.time_list_flag1, self.illumination_list_flag1, int(self._starthour),int(self._endhour))
            elif self.flag == 2:
                self._updateFigure(self.year_flag2, self.month_flag2, self.day_flag2, self.time_list_flag2, self.illumination_list_flag2,int(self._starthour),int(self._endhour))

    def _getSliceColumn(self):
        u'''
        获取标准列的起始和终止行数
        :return:
        '''
        column_start = 0
        if self.flag == 1:
            column_end = self._table.nrows
            if self._starthour.isdigit() and self._endhour.isdigit() and self._endminute.isdigit() and self._startminute.isdigit():
                for i in range(self._table.nrows):
                    if (int(self._hourtemp[i]) == int(self._starthour)) and (int(self._minutetemp[i]) == int(self._startminute)):
                        column_start = i
                    elif (int(self._hourtemp[i]) == int(self._endhour)) and (int(self._minutetemp[i]) == int(self._endminute)):
                        column_end = i
        elif self.flag == 2:
            column_end = self._table_standard.nrows
            if self._starthour.isdigit() and self._endhour.isdigit() and self._endminute.isdigit() and self._startminute.isdigit():
                for i in range(self._table_standard.nrows):
                    if (int(self.hourstandard_temp[i]) == int(self._starthour)) and (int(self.minutestandard_list[i]) == int(self._startminute)):
                        column_start = i
                    elif(int(self.hourstandard_temp[i]) == int(self._endhour)) and (int(self.minutestandard_list[i]) == int(self._endminute)):
                        column_end = i
        return column_start,column_end

    def getName(self):
        u'''
        获取用户选择的输出结点
        :return:
        '''
        name_temp = self._data.sheet_names()
        name_list = []
        for i in range(len(name_temp)):
            if name_temp[i].isdigit():
                name_list.append(name_temp[i])
        self.select = selectSheet.SelectWindow()
        self.select._get_namelist(name_list)
        self.select.enable_sheet(self._select_sheets)
        self.select.show()
        QtCore.QObject.connect(self.select.confirm, QtCore.SIGNAL(_fromUtf8("clicked()")), self.name_list)
        QtCore.QObject.connect(self.select.confirm, QtCore.SIGNAL(_fromUtf8("clicked()")), self.enableButton)

    def name_list(self):
        u'''
        获取select页面的用户选择
        :return:
        '''
        self._select_sheets = self.select.confirm_selection()

    def calculateLeastsq(self):
        u'''
        连接校准按钮，进行数据校准，由于显示时间较长，因此生成进度条对话框。
        :return:
        '''
        file_path = QFileDialog.getSaveFileName(self, 'save file', "saveFile", "excel files(*.xls)")
        if file_path is u'':
            return 0
        column = self._column_index
        channel_list_1side = range(self.data_start,self.data_end + 1)
        channel_list_2sides_rec = range(self.data_start,self.data_start + (self.data_end - self.data_start + 1) / 2)
        channel_list_2sides_cir_1 = range(self.data_start,self.data_start + self.column_2s_2*2)
        channel_list_2sides_cir_2 = range(self.data_start + self.column_2s_2 * 2 , self.data_end + 1)
        sheet_sort = sorted(self._select_sheets)
        oneside,rec,cir,index1,index2,index3 = self.splitSheet(sheet_sort)
        file = xlwt.Workbook()
        table_k = file.add_sheet("k",cell_overwrite_ok=True)
        table_b = file.add_sheet("b",cell_overwrite_ok=True)
        table_mse = file.add_sheet("MSE",cell_overwrite_ok=True)
        table_rsquare = file.add_sheet("RSQUARE",cell_overwrite_ok=True)

        prog_max = len(self._select_sheets) + len(oneside) * len(channel_list_1side) + len(rec) * len(channel_list_2sides_rec) + len(cir) * len(channel_list_1side) + 1
        progdialog = QtGui.QProgressDialog(u"计算中...",u"取消",0,prog_max,self)
        progdialog.setWindowTitle(u"计算进度")
        progdialog.setWindowModality(QtCore.Qt.WindowModal)
        progdialog.show()
        prog_id = 0

        for i in range(len(sheet_sort)):
            if self._select_sheets[i].isdigit():
                table_k.write(i, 0, int(sheet_sort[i]))
                table_b.write(i, 0, int(sheet_sort[i]))
                table_mse.write(i, 0, int(sheet_sort[i]))
                table_rsquare.write(i, 0, int(sheet_sort[i]))
                if progdialog.wasCanceled():
                    return
                progdialog.setValue(prog_id)
                prog_id = prog_id + 1

        if self.flag == 1:
            if self._column_index is not None:
                start, end = self._getSliceColumn()
            else:
                QMessageBox.critical(self, u"提示", u"请选择标准结点！")
                return 0
        elif self.flag == 2:
            start,end = self._getSliceColumn()

        for i in range(len(oneside)):
            for j in channel_list_1side:
                standard_array,temp_array = self.get_oneside_Array(start, end, oneside[i], j)
                if temp_array.tolist().count(0) == len(temp_array):
                    [k,b] = [u"None",u"None"]
                    mse = u'None'
                    r_square =u"None"
                elif (j - self.data_start + 1) % 2 == 0:
                    [k,b] = [u"None",u"None"]
                    mse = u'None'
                    r_square =u"None"
                else:
                    [k,b] = np.polyfit(temp_array, standard_array, 1)
                    calculation = temp_array * k + b
                    mse = self._mse(calculation, standard_array)
                    r_square = self._r_square(calculation, standard_array)
                table_k.write(int(index1[i]), j - self.data_start + 1, k)
                table_b.write(int(index1[i]), j - self.data_start + 1, b)
                table_mse.write(int(index1[i]), j - self.data_start + 1, mse)
                table_rsquare.write(int(index1[i]), j - self.data_start + 1, r_square)
                if progdialog.wasCanceled():
                    return 0
                progdialog.setValue(prog_id)
                prog_id = prog_id + 1

        for i in range(len(rec)):
            for j in channel_list_2sides_rec:
                if progdialog.wasCanceled():
                    return 0
                progdialog.setValue(prog_id)
                prog_id = prog_id + 1
                try:
                    (standard_array,temp_array,plus) = self.get_twosides_Array(start, end, rec[i], j)
                except:
                    continue
                if temp_array.tolist().count(0) == len(temp_array):
                    [k,b] = [u"None",u"None"]
                    mse = u'None'
                    r_square =u"None"
                else:
                    [k,b] = np.polyfit(temp_array, standard_array, 1)
                    calculation = temp_array * k + b
                    mse = self._mse(calculation, standard_array)
                    r_square = self._r_square(calculation, standard_array)
                table_k.write(int(index2[i]), j + 1 - self.data_start + plus, k)
                table_b.write(int(index2[i]), j + 1 - self.data_start + plus, b)
                table_mse.write(int(index2[i]), j + 1 - self.data_start + plus, mse)
                table_rsquare.write(int(index2[i]), j + 1 - self.data_start + plus, r_square)

        for i in range(len(cir)):
            for j in channel_list_2sides_cir_1:
                if progdialog.wasCanceled():
                    return 0
                progdialog.setValue(prog_id)
                prog_id = prog_id + 1
                try:
                    (standard_array, temp_array, plus) = self.get_twosides_Array(start, end, cir[i], j)
                except:
                    continue
                if temp_array.tolist().count(0) == len(temp_array):
                    [k,b] = [u"None",u"None"]
                    mse = u'None'
                    r_square =u"None"
                if (j-self.data_start + 1)% 2 == 0:
                    [k,b] = [u"None",u"None"]
                    mse = u'None'
                    r_square =u"None"
                else:
                    [k,b] = np.polyfit(temp_array, standard_array, 1)
                    calculation = temp_array * k + b
                    mse = self._mse(calculation, standard_array)
                    r_square = self._r_square(calculation, standard_array)
                table_k.write(int(index3[i]), j + 1 - self.data_start + plus, k)
                table_b.write(int(index3[i]), j + 1 - self.data_start + plus, b)
                table_mse.write(int(index3[i]), j + 1 - self.data_start + plus, mse)
                table_rsquare.write(int(index3[i]), j + 1 - self.data_start + plus, r_square)
            for j in channel_list_2sides_cir_2:
                if progdialog.wasCanceled():
                    return 0
                progdialog.setValue(prog_id)
                prog_id = prog_id + 1
                [k, b] = [u"None", u"None"]
                mse = u'None'
                r_square = u"None"
                table_k.write(int(index3[i]), j + 1 - self.data_start, k)
                table_b.write(int(index3[i]), j + 1 - self.data_start, b)
                table_mse.write(int(index3[i]), j + 1 - self.data_start, mse)
                table_rsquare.write(int(index3[i]), j + 1 - self.data_start, r_square)
        file.save(file_path)
        prog_id = prog_id + 1
        progdialog.setValue(prog_id)
        progdialog.accept()
        QMessageBox.information(self, u"提示", u"操作成功！")
        self.para_path = file_path
        self.combineButton.setEnabled(True)

    def _func(self, p, x):
        k, b = p
        return k * x + b

    def _error(self, p, x, y):
        return self._func(p, x) - y

    def splitSheet(self,sheet):
        sheet1 = []
        index1 = []
        sheet2 = []
        index2 = []
        sheet3 = []
        index3 = []
        for i in range(len(sheet)):
            if sheet[i] in self.rec_2:
                sheet2.append(sheet[i])
                index2.append(i)
            elif sheet[i] in self.cir_2:
                sheet3.append(sheet[i])
                index3.append(i)
            else:
                sheet1.append(sheet[i])
                index1.append(i)
        return sheet1,sheet2,sheet3,index1,index2,index3

    def get_oneside_Array(self, start, end, name, column_temp):
        u'''
        根据阈值进行交集计算，得到两个数列
        :param start:
        :param end:
        :param name:
        :param column_temp:
        :return:
        '''
        if self.flag == 1:
            standard_value_temp = self.illumination_list_flag1[start:end]
            standard_time_temp = self._table.col_values(self.time_column,start,end)
        if self.flag == 2:
            standard_value_temp = self.illumination_list_flag2
            standard_time_temp = self.time_change

        standard_list = []
        table_cal = self._data.sheet_by_name(name)
        calbration_value_temp = table_cal.col_values(column_temp)
        calbration_time_temp = table_cal.col_values(self.time_column)
        calbration_list = []

        for i in range(len(standard_time_temp)):
            for j in range(len(calbration_time_temp)):
                if calbration_time_temp[j] in range(int(standard_time_temp[i]) - self.threshold_start,int(standard_time_temp[i]) + self.threshold_end):
                    standard_list.append(standard_value_temp[i])
                    calbration_list.append(calbration_value_temp[j])
        standard_array = np.array(standard_list)
        calbration_array = np.array(calbration_list)
        return standard_array,calbration_array

    def get_twosides_Array(self, start, end, name, column_temp):
        if self.flag == 1:
            standard_value_temp = self.illumination_list_flag1[start:end]
            standard_time_temp = self._table.col_values(self.time_column,start,end)
        if self.flag == 2:
            standard_value_temp = self.illumination_list_flag2
            standard_time_temp = self.time_change
        col1_gt_count = 0
        col2_gt_count = 0
        index_flag = 0
        standard_list = []
        table_cal = self._data.sheet_by_name(name)
        calbration_value_temp_11 = []
        calbration_value_temp_12 = []
        time1 = []
        time2 = []
        calbration_value_temp_1 = table_cal.col_values(column_temp)
        calbration_value_temp_2 = table_cal.col_values(self.data_end)
        calbration_time_temp = table_cal.col_values(self.time_column)
        if calbration_value_temp_2.count(0) == len(calbration_value_temp_2):
            calbration_value_temp_2 = table_cal.col_values(column_temp + self.column_2s_2)
            index_flag = 0
            if calbration_value_temp_2.count(0) == len(calbration_value_temp_2):
                return np.array([]),np.array([])
        else:
            calbration_value_temp_2 = table_cal.col_values(column_temp + self.column_2s_1)
            index_flag = 1
        for i in range(len(calbration_value_temp_1)):
            if calbration_value_temp_1[i] > calbration_value_temp_2[i]:
                calbration_value_temp_11 .append(calbration_value_temp_1[i])
                time1.append(calbration_time_temp[i])
                col1_gt_count = col1_gt_count + 1
            else:
                calbration_value_temp_12.append(calbration_value_temp_2[i])
                time2.append(calbration_time_temp[i])
                col2_gt_count = col2_gt_count + 1

        calbration_list = []

        if col1_gt_count >= col2_gt_count:
            calbration_value_temp = calbration_value_temp_1
            calbration_time_temp = time1
            col_plus = 0
        else:
            calbration_value_temp = calbration_value_temp_2
            calbration_time_temp = time2
            if index_flag:
                col_plus = int(self.column_2s_1)
            else:
                col_plus = int(self.column_2s_2)

        for i in range(len(standard_time_temp)):
            for j in range(len(calbration_time_temp)):
                if calbration_time_temp[j] in range(int(standard_time_temp[i]) - self.threshold_start,int(standard_time_temp[i]) + self.threshold_end):
                    standard_list.append(standard_value_temp[i])
                    calbration_list.append(calbration_value_temp[j])
        standard_array = np.array(standard_list)
        calbration_array = np.array(calbration_list)

        return standard_array,calbration_array,col_plus

    def _mse(self, calculation, standard):
        u'''
        计算mean standard error，需要输入计算列和标准列
        :param calculation:
        :param standard:
        :return:
        '''
        error_2 = (calculation - standard) ** 2
        return error_2.mean()

    def _r_square(self, calculation, standard):
        u'''
        计算R方，需要两列数列的输入
        :param calculation:
        :param standard:
        :return:
        '''
        result = 1 - ((calculation - standard) ** 2).sum() / ((standard - standard.mean()) ** 2).sum()
        return result

    def enableGroup1(self):
        u'''
        激活标准列选项
        :return:
        '''
        if os.path.isfile(u"%s"%self.fileEdit.text()):
            self._data = xlrd.open_workbook(self.fileEdit.text())
            if self.twosidesnode_list != []:
                self.get_node_type()
                self.data_path = self.fileEdit.text()
                self.setNodeBox()
                self.groupBox.setEnabled(True)
                self.pushButton_2.setEnabled(True)
        else:
            self.groupBox.setEnabled(False)
            self.pushButton_2.setEnabled(False)

    def enableGroup2(self):
        u'''
        激活输出部分选项
        :return:
        '''
        if self.sensorBox.currentText().isdigit():
            self.groupBox_2.setEnabled(True)
        else:
            self.groupBox_2.setEnabled(False)

    def enableButton(self):
        u'''
        使得校准按钮可按
        :return:
        '''
        if self._select_sheets is not []:
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)


    def _readConfig(self):
        u'''
        读取配置文件，说明读取数据表格的格式
        :return:
        '''
        file = open("config\\data_config.txt", "r")
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
            if split[0].strip() == "TIME":
                self.time_column = int(split[1].strip()) - 1
            if split[0].strip() == "YEAR":
                self.year_column = int(split[1].strip()) - 1
            if split[0].strip() == "MONTH":
                self.month_column = int(split[1].strip()) - 1
            if split[0].strip() == "DAY":
                self.day_column = int(split[1].strip()) - 1
            if split[0].strip() == "HOUR":
                self.hour_column = int(split[1].strip()) - 1
            if split[0].strip() == "MINUTE":
                self.minute_column = int(split[1].strip()) - 1
            if split[0].strip() == "SECOND":
                self.second_column = int(split[1].strip()) - 1
            if split[0].strip() == "THRESHOLD_START":
                self.threshold_start = int(split[1].strip())
            if split[0].strip() == "THRESHOLD_END":
                self.threshold_end = int(split[1].strip())
            if split[0].strip() == "COLUMN_1S_1":
                self.column_1s_1 = int(split[1].strip())
            if split[0].strip() == 'COLUMN_1S_2':
                self.column_1s_2 = int(split[1].strip())
            if split[0].strip() == "COLUMN_2S_1":
                self.column_2s_1 = int(split[1].strip())
            if split[0].strip() == "COLUMN_2S_2":
                self.column_2s_2 = int(split[1].strip())
        file.close()

        file = open("config\\2sides_config.txt", "r")
        line = "start reading"
        while (1):
            if (line == ""):
                break
            line = file.readline()
            split = line.strip().upper().split("=")
            if split[0].strip() == "NODE_2S_1":
                temp = split[1].strip()
                self.twosidesnode_list = temp.strip().split(',')
        file.close()

    def openStandardDialog(self):
        standard_data = QFileDialog.getOpenFileName(self, u"打开参数表格", guiPath, "table(*.xlsx;*.xls)")
        if standard_data is not u"":
            self._data_standard = xlrd.open_workbook(u"%s"%standard_data)
            self.nodeEdit.setText(standard_data)

    def openStandard(self):
        if os.path.isfile(u"%s"%self.nodeEdit.text()):
            self._data_standard = xlrd.open_workbook(self.nodeEdit.text())
            self.groupBox_2.setEnabled(True)
            self.nodeBox.setEnabled(False)
            self.channelBox.setEnabled(False)
            self.sensorBox.setEnabled(False)
            self.flag = 2
            self._readConfig_standard()
        else:
            self.groupBox_2.setEnabled(False)
            self.nodeBox.setEnabled(True)
            self.channelBox.setEnabled(True)
            self.sensorBox.setEnabled(True)
            self.flag = 0

    def openCalDialog(self):
        self.cal_dialog = cal.CalWindow()
        self.cal_dialog.get_parapath(self.para_path,self.data_path)
        self.cal_dialog.show()


    def _readConfig_standard(self):
        file = open("config\\standard_config.txt", "r")
        line = "start reading"
        while(1):
            if line == "":
                break
            line = file.readline()
            split = line.strip().split("=")
            if split[0].strip().upper() == "SHEETNAME":
                sheetname = split[1].strip()
            if split[0].strip().upper() == "DATE_COLUMN":
                date_column = int(split[1].strip()) - 1
            if split[0].strip().upper() == "TIME_COLUMN":
                time_column = int(split[1].strip()) - 1
            if split[0].strip().upper() == "AVERAGE_COLUMN":
                standard_column = int(split[1].strip()) - 1
        file.close()
        self._init_Standard(sheetname,date_column,time_column,standard_column)
        self._updateFigure(self.year_flag2, self.month_flag2, self.day_flag2, self.time_list_flag2, self.illumination_list_flag2,7,19)

    def _init_Standard(self,sheetname,date_column,time_column,standard_column):
        u'''

        :param sheetname:
        :param date_column:
        :param time_column:
        :param standard_column:
        :return:
        '''
        self.hourstandard_list = []
        self.minutestandard_list = []
        self.hourstandard_temp = []
        self._table_standard = self._data_standard.sheet_by_name(sheetname)
        length = self._table_standard.nrows
        time_list = []
        illumination_list = self._table_standard.col_values(standard_column)
        self.time_change = []
        for i in range(length):
            year, month, day, hour1, minute1, second1 = xlrd.xldate.xldate_as_tuple(self._table_standard.cell(i,date_column).value, self._data.datemode)
            year1, month1, day1, hour, minute, second = xlrd.xldate.xldate_as_tuple(self._table_standard.cell_value(i, time_column), self._data.datemode)
            time = datetime.datetime(year, month, day, hour, minute, second)
            time_list.append(time)
            self.hourstandard_temp.append(hour)
            self.minutestandard_list.append(minute)
            change_temp = ((hour - 7)* 3600 + minute * 60 + second) / 10
            self.time_change.append(change_temp)

        self.hourstandard_list = list(set(self.hourstandard_temp))

        self.year_flag2 = year
        self.month_flag2 = month
        self.day_flag2 = day
        self.time_list_flag2 = time_list
        self.illumination_list_flag2 = illumination_list


    def openCombine(self):
        self.combine = combine.CombineWindow()
        self.combine.getPath(self.para_path)
        self.combine.show()

    def get_node_type(self):
        self.rec_2 = self.twosidesnode_list
        all_nodes = self._data.sheet_names()
        self.cir_2 = []
        for i in range(len(all_nodes)):
            if all_nodes[i].isdigit():
                table = self._data.sheet_by_name(all_nodes[i])
                count = 0
                for j in range(self.data_start,self.data_end + 1):
                    col = table.col_values(j)
                    if col.count(0) != len(col):
                        count = count + 1
                if count == self.column_2s_2 * 2:
                    self.cir_2.append(all_nodes[i])
            else:
                continue