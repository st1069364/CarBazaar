import app_res_rc
import types
import sys
from src import classes

sys.path.append('../src')

from src.classes import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

BUTTON_STYLE = """QPushButton {
    background-color: #d3311b;
    border : none;
    color : white;
}"""

# ----------------------------------------------------
# Driver code for the Schedule Car Inspection Use Case
# ----------------------------------------------------

# def continue_button_clicked():
#     stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen
#
#
# def back_button_pressed():
#     stack_widget.setCurrentIndex(stack_widget.currentIndex() - 1)  # move to the previous UI screen

class ScheduleCarInspectionScreen1(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen1, self).__init__()
        loadUi("qt_ui/car_inspection_1.ui", self)

        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # create Qt Application and pass the command-line args
    app.setStyleSheet(BUTTON_STYLE)  # set the button style to be used to the "CarBazaar" style

    # create the StackedWidget that will be used to transition from one Window to another
    stack_widget = QtWidgets.QStackedWidget()

    # create the screen to be added to the StackedWidget
    screen_1 = ScheduleCarInspectionScreen1()

    # add the widget to the StackedWidget
    stack_widget.addWidget(screen_1)

    # fix the dimensions
    stack_widget.setFixedWidth(400)
    stack_widget.setFixedHeight(881)
    stack_widget.setStyleSheet("QMainWindow {background: 'white';}")

    # set up window icon to the CarBazaar logo and window title to that of the current Use Case
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/resources/resources/CarBazaar_logo_trans.png"), QtGui.QIcon.Normal,
                   QtGui.QIcon.Off)
    stack_widget.setWindowIcon(icon)
    stack_widget.setWindowTitle('Schedule Car Inspection')
    stack_widget.show()  # show the widget
    sys.exit(app.exec_())  # program waits for window close, to end execution