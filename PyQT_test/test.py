# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_splash_screenTWIRek.ui'
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

class Ui_id_splash_screen(object):
    def setupUi(self, id_splash_screen):
        if id_splash_screen.objectName():
            id_splash_screen.setObjectName(u"id_splash_screen")
        id_splash_screen.resize(480, 800)
        self.centralwidget = QWidget(id_splash_screen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"image: url(:/newPrefix/Charging.png);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.frame)

        id_splash_screen.setCentralWidget(self.centralwidget)

        self.retranslateUi(id_splash_screen)

        QMetaObject.connectSlotsByName(id_splash_screen)
    # setupUi

    def retranslateUi(self, id_splash_screen):
        id_splash_screen.setWindowTitle(QCoreApplication.translate("id_splash_screen", u"MainWindow", None))
    # retranslateUi

