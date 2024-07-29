# coding: utf-8
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from report_ui import Ui_Report_Form
from datetime_select import DateTimeSelect

class Report(QWidget, Ui_Report_Form):
    makeGraphSignal = QtCore.pyqtSignal(str, str)
    #makeExportSignal = QtCore.pyqtSignal(str,str)
    def __init__(self, parent=None):
        super(Report, self).__init__(parent)
        # UI
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Dialog |
                            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.parent = parent        
        self.titles = {u"old_" : u"Отчёт по старому узлу учёта",
                        u"new_" : u"Отчёт по новому узлу учёта",
                        u"sn_" : u"Отчёт по собственным нуждам"}
        # определяем, кто вызвал форму, и в зависимости от этого выводим надпись, по кому отчет
        if self.parent is not None:
            self.title = self.titles[str(self.parent.objectName())]
            self.label_Title.setText(self.title)

        self.curdate_string = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
        self.from_datetime_string = self.curdate_string + " 00:00:00"
        self.to_datetime_string   = self.curdate_string + " 23:59:59"
        self.fromDateButton.setText(self.from_datetime_string)
        self.toDateButton.setText(self.to_datetime_string)

        self.fromDateButton.clicked.connect(self.from_date_select)
        self.toDateButton.clicked.connect(self.to_date_select)
        self.reportButton_graph.clicked.connect(self.make_graph)
        #self.reportButton_export.clicked.connect(self.make_export)

        self.from_date = QtCore.QDate.currentDate()
        self.to_date   = QtCore.QDate.currentDate()
        self.from_time = QtCore.QTime.fromString("00:00:00", "HH:mm:ss")
        self.to_time   = QtCore.QTime.fromString("23:59:59", "HH:mm:ss")

    def from_date_select(self):
        self.from_datetime_select = DateTimeSelect(self, self.from_date, self.from_time)
        self.from_datetime_select.datetimeSignal.connect(self.update_from_date)
        self.from_datetime_select.show()
        
    def to_date_select(self):
        self.to_datetime_select = DateTimeSelect(self, self.to_date, self.to_time)
        self.to_datetime_select.datetimeSignal.connect(self.update_to_date)
        self.to_datetime_select.show()

    def update_from_date(self, datetime):
        self.from_date = datetime["date"]
        self.from_time = datetime["time"]
        self.from_datetime_string = "{} {}".format(self.from_date.toString("yyyy-MM-dd"),
                                                   self.from_time.toString("HH:mm:ss"))
        self.fromDateButton.setText(self.from_datetime_string)

    def update_to_date(self, datetime):
        self.to_date = datetime["date"]
        self.to_time = datetime["time"]
        self.to_datetime_string = "{} {}".format(self.to_date.toString("yyyy-MM-dd"),
                                                 self.to_time.toString("HH:mm:ss"))
        self.toDateButton.setText(self.to_datetime_string)

    def make_graph(self):
        # from_to_tab_dic = {"from" : self.from_datetime_string, "to" : self.to_datetime_string,\
        #                 "tab" : str(self.parent.objectName()) if self.parent is not None else "None"}
        self.makeGraphSignal.emit(self.from_datetime_string, self.to_datetime_string)
        self.close()

    #def make_export(self):
    #    # from_to_tab_dic = {"from" : self.from_datetime_string, "to" : self.to_datetime_string,\
    #    #                 "tab" : str(self.parent.objectName()) if self.parent is not None else "None"}
    #    self.makeExportSignal.emit(self.from_datetime_string , self.to_datetime_string) # from_to_tab_dic)
    #    self.close()

def main():
    app = QApplication(sys.argv)
    report = Report()
    report.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
