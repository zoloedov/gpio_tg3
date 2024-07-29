# coding: utf-8
import os
import sys
import string
import random
import csv
import sqlite3
from threading import Thread
from gpiozero import Button
from datetime import datetime
from report import Report

from matplotlib import pyplot
from matplotlib import dates
import matplotlib.animation as animation

import main_ui
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog
from PyQt5 import QtCore


PINS = (4, 17, 27, 22, 23, 24, 5, 6)
CHANNELS = [1,2,3,4,5,6,7,8]

# led = LED(17)
# connection = sqlite3.connect("gpio.db")
# cursor = connection.cursor()
class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.textEdit.append("Started at {}".format(datetime.now()))
        self.turbine = Turbine(PINS)
        self.report = Report()
        
        self.radioButton_1.toggled.connect(self.refresh_statuses)
        self.radioButton_2.toggled.connect(self.refresh_statuses)
        self.radioButton_3.toggled.connect(self.refresh_statuses)
        self.radioButton_4.toggled.connect(self.refresh_statuses)
        self.radioButton_5.toggled.connect(self.refresh_statuses)
        self.radioButton_6.toggled.connect(self.refresh_statuses)
        self.radioButton_7.toggled.connect(self.refresh_statuses)
        self.radioButton_8.toggled.connect(self.refresh_statuses)
        self.checkBox_theme.toggled.connect(self.changeTheme)
        
        # Connecting Signals
        self.turbine.querySignal.connect(self.on_query_appear, QtCore.Qt.QueuedConnection)
        self.turbine.buttonToggleSignal.connect(self.on_button_toggle, QtCore.Qt.QueuedConnection)
        #self.pushButton_graph.clicked.connect(self.make_graph, QtCore.Qt.QueuedConnection)
        self.pushButton_csv.clicked.connect(self.export_csv)

        self.pushButton_graph.clicked.connect(self.show_selectdate_window)
        # Initializing radio buttons states
        self.refresh_statuses()
        
        self.lightCSS = """
            QWidget {
                font-size: 15pt;
            }
            
            /*QTextEdit {
                border-radius: 4px;
            }*/
            
            QPushButton {
                font-size: 15pt;
                text-transform: uppercase;
            }
            
            QRadioButton::indicator:checked {
                background-color: #de2649;
                border-radius: 3px;
            }
            
            QRadioButton::indicator:unchecked {
                background-color: #0176f3;
                border-radius: 3px;
            }
        """   
        self.darkCSS = """
            QWidget {
                background-color: #142233; \*#142233 #343d46 #141821*\
                font-size: 15pt;
                color: white;
            }
            
            QTextEdit {
                background-color: #0e1621;
                border-radius: 4px;
            }
            
            
            QPushButton {
                border: none;
                border-radius: 2px;
                padding: 12px 18px;
                font-size: 16pc;
                text-transform: uppercase;
                color: white;
                background-color: #2b5282; \*#0176f3*\
                outline: none;
            }
            
            QPushButton:hover {
                background-color: #2196f3;
            }
           
            QPushButton:pressed {
                background-color: #de2649;
        
            }
            
            QRadioButton::indicator:checked {
                background-color: #de2649;
                border-radius: 3px;
            }
            
            QRadioButton::indicator:unchecked {
                background-color: #0176f3;
                border-radius: 3px;
            }
            
            QCheckBox {
                font-size: 15pt;
            }
        """    
        self.checkBox_theme.setChecked(True)
        
        
    def changeTheme(self):
        if self.checkBox_theme.isChecked():
            self.setStyleSheet(self.darkCSS)
        else:
            self.setStyleSheet("")
            self.setStyleSheet(self.lightCSS)
        
    def setDarkTheme(self):
        self.setStyleSheet(self.darkCSS)
        
        
    def show_selectdate_window(self):
        self.from_to_window = Report()
        self.from_to_window.makeGraphSignal.connect(self.make_graph, QtCore.Qt.QueuedConnection)
        #self.from_to_window.makeExportSignal.connect(self.export_csv, QtCore.Qt.QueuedConnection)
        self.from_to_window.show()
                    
    def on_query_appear(self, message):
        self.textEdit.append(message)
        
    def on_button_toggle(self, button_number, state):
        self.radio_button = self.__getattribute__('radioButton_%s'%button_number)
        self.radio_button.setChecked(state)
        self.radio_button.setText("Включен" if state else "Выключен")
        
    def refresh_statuses(self):
        self.radioButton_1.setChecked(self.turbine.buttons[0].is_pressed)
        self.radioButton_1.setText("Включен" if self.turbine.buttons[0].is_pressed else "Выключен")
        self.radioButton_2.setChecked(self.turbine.buttons[1].is_pressed)
        self.radioButton_2.setText("Включен" if self.turbine.buttons[1].is_pressed else "Выключен")
        self.radioButton_3.setChecked(self.turbine.buttons[2].is_pressed)
        self.radioButton_3.setText("Включен" if self.turbine.buttons[2].is_pressed else "Выключен")
        self.radioButton_4.setChecked(self.turbine.buttons[3].is_pressed)
        self.radioButton_4.setText("Включен" if self.turbine.buttons[3].is_pressed else "Выключен")
        self.radioButton_5.setChecked(self.turbine.buttons[4].is_pressed)
        self.radioButton_5.setText("Включен" if self.turbine.buttons[4].is_pressed else "Выключен")
        self.radioButton_6.setChecked(self.turbine.buttons[5].is_pressed)
        self.radioButton_6.setText("Включен" if self.turbine.buttons[5].is_pressed else "Выключен")
        self.radioButton_7.setChecked(self.turbine.buttons[6].is_pressed)
        self.radioButton_7.setText("Включен" if self.turbine.buttons[6].is_pressed else "Выключен")
        self.radioButton_8.setChecked(self.turbine.buttons[7].is_pressed)
        self.radioButton_8.setText("Включен" if self.turbine.buttons[7].is_pressed else "Выключен")
    
    def make_graph(self, from_date="", to_date=""):
        self.graph = Graph(from_date, to_date)
        self.graph.run()
        
    def export_csv(self, from_date="", to_date=""):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", self.generate_filename("csv"), "csv files (*.csv);;All Files (*.*);;txt files (*.txt)")
        if filename:
            self.textEdit.append("exporting CSV...")
            filename = filename.split(".csv")[0] + ".csv"
            print("Export csv to {}".format(filename))
            with open(filename, "w", newline = "") as export_file:
                writer = csv.writer(export_file)
                connection = sqlite3.connect("gpio.db")
                cursor = connection.cursor()
                result = cursor.execute("SELECT channel, timestamp, value FROM gpio_data")
                result = result.fetchall()
                writer.writerow([u"Канал", u"Время", u"Значение"])
                writer.writerows(result)
            self.textEdit.append("CSV exported successfully to {}".format(filename))    
        
    def generate_filename(self, extension="csv", salt=""):
        basedir = os.path.dirname(sys.argv[0])
        #exports_dir =  os.path.join(os.path.dirname(sys.argv[0]),"csv_export")
        #if not os.path.exists(exports_dir):
        #    os.mkdir(exports_dir)
        s = string.ascii_letters # + string.digits
        salt = salt if salt else "".join(random.choice(s) for i in range(10))
        date_time = datetime.now().strftime("%Y%m%d_%H%M")
        filename = os.path.join(basedir, "_".join([date_time, salt]))
        filename += ".{}".format(extension)
        return filename
        
        
class Graph(QtCore.QObject):
        def __init__(self, from_datetime="", to_datetime=""):
            super(Graph, self).__init__()
            self.from_datetime = from_datetime
            self.to_datetime = to_datetime
           
        def run(self):
            print("making graph...")
            print("from {} to {}".format(self.from_datetime, self.to_datetime))
            self.channels = [1,2,3,4,5,6,7,8]
            # self.figure = pyplot.figure()
            self.connection = sqlite3.connect("gpio.db")
            self.cursor = self.connection.cursor()
            for channel in self.channels:
                self.result = self.cursor.execute("SELECT timestamp, value FROM gpio_data WHERE channel = '%s'\
                                                    AND timestamp > datetime('%s') AND timestamp < datetime('%s')"%(channel, self.from_datetime, self.to_datetime))
                self.result = self.result.fetchall()
                times = [datetime.strptime(el[0], "%Y-%m-%d %H:%M:%S.%f") for el in self.result]
                values = [el[1] + channel for el in self.result]
                pyplot.xticks(rotation=45, ha='right')
                pyplot.subplots_adjust(bottom=0.30)
                pyplot.step(times, values, where="post", label = str(channel))

            self.connection.close()
            pyplot.legend(title = "Channels")
            pyplot.subplots_adjust(bottom=0.30)
            pyplot.show()
            print("done making graph")
            
            
class Turbine(QtCore.QObject):
    querySignal = QtCore.pyqtSignal(str)
    buttonToggleSignal = QtCore.pyqtSignal(int, bool)
    def __init__(self, pins):
        super(Turbine, self).__init__()
        self.pins = pins
        self.test_mode = 0
        print("Started at {}".format(datetime.now()))
        
        # creating list of Button objects
        self.buttons = [Button(pin) for pin in self.pins] # , bounce_time = 0.05
       
        self.enum = enumerate(self.buttons, start = 1)
        self.button_numbers = dict((but, num) for num, but in self.enum)
        #print(button_numbers)
        
        for bt in self.buttons:
            bt.when_pressed  = self.pressed
            bt.when_released = self.released
            # print(button_numbers[bt],bt.is_pressed)

    def pressed(self, button):
        # print(button)
        self.connection = sqlite3.connect("gpio.db")
        self.cursor = self.connection.cursor()
        self.information = {"pin" : button.pin,\
                        "channel" : self.button_numbers[button],\
                        "timestamp" : datetime.now(),\
                        "value" : 1,\
                        "test" : self.test_mode\
                        }
        # print("button pressed", information.values())
        # print("{pin}, {channel}, {timestamp}, {value}, {test}"%list(information.values()))
        self.query = "INSERT INTO gpio_data (pin, channel, timestamp, value, test) VAlUES ('%s', '%s', '%s', '%s', '%s')"%(self.information["pin"],\
                                                                                                                        self.information["channel"],\
                                                                                                                        self.information["timestamp"],\
                                                                                                                        self.information["value"],\
                                                                                                                        self.information["test"]\
                                                                                                                        )
        print(self.query)
        self.message = u"%s | Канал %s | Значение %s"%(self.information["timestamp"], self.information["channel"], self.information["value"])
        self.querySignal.emit(self.message)
        self.buttonToggleSignal.emit(self.information["channel"], bool(self.information["value"]))
        self.cursor.execute(self.query)
        self.connection.commit()

    def released(self, button):
        # print(button)
        self.connection = sqlite3.connect("gpio.db")
        self.cursor = self.connection.cursor()
        self.information = {"pin" : button.pin,\
                        "channel" : self.button_numbers[button],\
                        "timestamp" : datetime.now(),\
                        "value" : 0,\
                        "test" : self.test_mode\
                        }
        self.query = "INSERT INTO gpio_data (pin, channel, timestamp, value, test) VAlUES ('%s', '%s', '%s', '%s', '%s')"%(self.information["pin"],\
                                                                                                                        self.information["channel"],\
                                                                                                                        self.information["timestamp"],\
                                                                                                                        self.information["value"],\
                                                                                                                        self.information["test"]\
                                                                                                                        )
        
        
        self.message = u"%s | Канал %s | Значение %s"%(self.information["timestamp"], self.information["channel"], self.information["value"])
        self.querySignal.emit(self.message)
        self.buttonToggleSignal.emit(self.information["channel"], bool(self.information["value"]))
        print(self.query)
        self.cursor.execute(self.query)
        self.connection.commit()
        
        
def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    #pass
    main()














