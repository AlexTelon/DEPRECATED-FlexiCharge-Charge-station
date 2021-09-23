import sys
import platform
from typing import Counter
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


## ==> start splash screen
from ui_splash_screen import Ui_Splashscreen

## ==> MAIN WINDOW
from ui_main import Ui_MainWindow

## ==> chagre splash screen
from test import Ui_id_splash_screen

## ==> Globals
counter_start = 0
#counter_charger = 20

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

class ChargeScreen(MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_id_splash_screen()
        self.ui.setupUi(self)

        ## remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

     #   self.timer = QtCore.QTimer()
     #   self.timer.timeout.connect(self.progress)
     #   self.timer.start(35)
     #   self.co

        self.show()

    #def chargeProgress(self):
     #   global counter_charger




class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Splashscreen()
        self.ui.setupUi(self)

        ## remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)



        self.show()

    def progress(self):
        global counter_start

        #set value to progress bar
        self.ui.progressBar.setValue(counter_start)

        if counter_start > 100:
            self.timer.stop()
            self.close()
            self.main = ChargeScreen()
            self.main.show()

        counter_start += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())