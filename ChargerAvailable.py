# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerHWskwD.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5 import QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc
import globalVariables   

class Available_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 480, 800))
        self.widget.setStyleSheet(u"background-image: url(:/ChargerAvailableScreen/Pictures/chargerid.png);")

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(58, 703, 55, 61))
        self.label.setFont(QFont('Tw Cen MT Condensed Extra Bold', 25, QtGui.QFont.Bold))
        self.label.setStyleSheet("QLabel { color : white; }")

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(127, 703, 55, 61))
        self.label_2.setFont(QFont('Tw Cen MT Condensed Extra Bold', 25, QtGui.QFont.Bold))
        self.label_2.setStyleSheet("QLabel { color : white; }")

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(196, 703, 55, 61))
        self.label_3.setFont(QFont('Tw Cen MT Condensed Extra Bold', 25, QtGui.QFont.Bold))
        self.label_3.setStyleSheet("QLabel { color : white; }")

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(265, 703, 55, 61))
        self.label_4.setFont(QFont('Tw Cen MT Condensed Extra Bold', 25, QtGui.QFont.Bold))
        self.label_4.setStyleSheet("QLabel { color : white; }")

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(334, 703, 55, 61))
        self.label_5.setFont(QFont('Tw Cen MT Condensed Extra Bold', 25, QtGui.QFont.Bold))
        self.label_5.setStyleSheet("QLabel { color : white; }")

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(403, 703, 55, 61))
        self.label_6.setFont(QFont('Tw Cen MT Condensed Extra Bold', 25, QtGui.QFont.Bold))
        self.label_6.setStyleSheet("QLabel { color : white; }")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", globalVariables.chargerID[0], None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", globalVariables.chargerID[1], None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", globalVariables.chargerID[2], None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", globalVariables.chargerID[3], None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", globalVariables.chargerID[4], None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", globalVariables.chargerID[5], None))
    # retranslateUi