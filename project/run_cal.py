from qgis.core import *
from PyQt4.QtGui import *
import sys
import cal


app = QApplication([])
qgisPath = 'C:\\Program Files (x86)\\QGIS 2.16.0\\apps\\qgis'
QgsApplication.setPrefixPath(qgisPath, True)
QgsApplication.initQgis()
main_win = cal.CalWindow()
main_win.show()
sys.exit(app.exec_())