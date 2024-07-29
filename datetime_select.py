# coding: utf-8
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtWidgets import *
from datetime_ui import Ui_selectDateTime

class DateTimeSelect(QWidget, Ui_selectDateTime):
    datetimeSignal = QtCore.pyqtSignal(dict)
    def __init__(self, parent=None, date=QtCore.QDate, time=QtCore.QTime):
        super(DateTimeSelect, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint |
                            QtCore.Qt.Dialog |
                            QtCore.Qt.WindowCloseButtonHint)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.calendar = QCalendarWidget(self)
        self.calendar.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.dateEdit.setCalendarWidget(self.calendar)

        self.date = date
        self.time = time
        # print self.date
        # print self.time

        self.dateEdit.setDate(self.date)
        self.timeEdit.setTime(self.time)

        self.okButton.clicked.connect(self.send_datetime)
        self.cancelButton.clicked.connect(self.close)
      
    def send_datetime(self):
        # print self.dateEdit.date().toString("dd.MM.yyyy")
        # print self.timeEdit.time().toString("hh:mm:ss")
        self.datetimeSignal.emit({"date": self.dateEdit.date(), "time": self.timeEdit.time()})
        self.close()


def main():

    app = QApplication(sys.argv)
    datetime_select = DateTimeSelect(date=QtCore.QDate.currentDate(), time=QtCore.QTime.currentTime())
    datetime_select.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
