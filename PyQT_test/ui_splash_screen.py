# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash_screenhdfjjc.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

import res

class Ui_Splashscreen(object):
    def setupUi(self, Splashscreen):
        if Splashscreen.objectName():
            Splashscreen.setObjectName(u"Splashscreen")
        Splashscreen.resize(480, 800)
        self.centralwidget = QWidget(Splashscreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"image: url(:/newPrefix/StartingUp.png);")
        self.progressBar = QProgressBar(self.widget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(28, 560, 411, 23))
        self.progressBar.setStyleSheet(u"QProgressBar{\n"
"	\n"
"	background-color: rgb(0, 0, 0);\n"
"	color: rgb(229, 229, 229);\n"
"	border-style: none;\n"
"	border-radius: 10px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.506, stop:0 rgba(240, 224, 7, 255), stop:1 rgba(64, 156, 104, 255));\n"
"	border-radius: 10px;\n"
"}")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.widget)

        Splashscreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(Splashscreen)

        QMetaObject.connectSlotsByName(Splashscreen)
    # setupUi

    def retranslateUi(self, Splashscreen):
        Splashscreen.setWindowTitle(QCoreApplication.translate("Splashscreen", u"MainWindow", None))
    # retranslateUi

