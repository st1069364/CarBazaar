import app_res_rc
import types
import sys
from src import classes
import os

sys.path.append('../src')

from src.classes import *

from PyQt5 import QtCore, QtGui, QtWidgets, QtQuick
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

car_inspection: CarInspection = None
car_listing: CarListing = None
test_location: Location = Location((34.5, 35.5))


#
# def back_button_pressed():
#     stack_widget.setCurrentIndex(stack_widget.currentIndex() - 1)  # move to the previous UI screen


class ScheduleCarInspectionScreen1(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen1, self).__init__()
        loadUi("qt_ui/car_inspection_1.ui", self)

        classes.main()  # to add a listing, an inspector

        self.screen_2 = ScheduleCarInspectionScreen2()

        self.continue_button.clicked.connect(self.continue_button_clicked)
        # self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

    def continue_button_clicked(self):
        global car_inspection
        global car_listing

        coordinates_list = self.location_box.toPlainText().split(",", 2)

        entered_location = Location((float(coordinates_list[0].strip()), float(coordinates_list[1].strip())))
        if not entered_location.check_location_validity():
            msg = QMessageBox()
            msg.setWindowTitle('Invalid Location!!')
            msg.setText('The location you entered is outside of Patras !')
            msg.exec()
        else:
            car_inspection = CarInspection()
            check_type: InspectionType = None

            if self.inspection_type_box.currentText() == 'Basic Check':
                check_type = InspectionType.Basic
            elif self.inspection_type_box.currentText() == 'Car Engine Check':
                check_type = InspectionType.CarEngine
            else:
                check_type = InspectionType.Thorough

            date = self.calendar_widget.selectedDate().toPyDate()
            time = datetime.time(self.hour_box.time().hour(), self.minute_box.time().minute())
            date_and_time = datetime.datetime.combine(date, time)

            car_inspection.set_car_inspection_info(check_type, date_and_time, entered_location)
            inspector_info = car_inspection.find_inspector()
            print(inspector_info)

            stack_widget.insertWidget(1, self.screen_2)
            stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen


class ScheduleCarInspectionScreen2(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen2, self).__init__()
        loadUi("qt_ui/car_inspection_2.ui", self)


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
