import sys
import globalVariables
import websockets
import json
import asyncio

from StateHandler import States
from StateHandler import StateHandler
from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ChargerAvailable import Available_MainWindow
from ChargerNotAvailable import NotAvailable_MainWindow
from StartingUp import StartingUp_MainWindow

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result, call

globalVariables.chargerID = ['1','2','3','4','5','6']

state = StateHandler()
lastState = StateHandler()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = StartingUp_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.stateMachine)
        self.timer.start(5000)

        self.show()

    def changeToNotAvailable(self):
        self.ui = NotAvailable_MainWindow()
        self.ui.setupUi(self)

    def changeToAvailable(self):
        self.ui = Available_MainWindow()
        self.ui.setupUi(self)

    def changeToStartUp(self):
        self.ui = StartingUp_MainWindow()
        self.ui.setupUi(self)

    def stateMachine(self):
        if state.get_state() == States.S_STARTUP:
            state.set_state(States.S_AVAILABLE)
            self.changeToAvailable()
        elif state.get_state() == States.S_AVAILABLE:
            state.set_state(States.S_NOTAVAILABLE)
            self.changeToNotAvailable()
        elif state.get_state() == States.S_NOTAVAILABLE:
            state.set_state(States.S_STARTUP)
            self.changeToStartUp()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

