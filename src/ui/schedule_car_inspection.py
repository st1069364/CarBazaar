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


def back_button_pressed():
    stack_widget.setCurrentIndex(stack_widget.currentIndex() - 1)  # move to the previous UI screen


class ScheduleCarInspectionScreen1(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen1, self).__init__()
        loadUi("qt_ui/car_inspection_1.ui", self)

        classes.main()  # to add a listing, an inspector, reviews

        self.screen_2 = ScheduleCarInspectionScreen2()

        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

    def continue_button_clicked(self):
        global car_inspection

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
            recommended_inspector = car_inspection.find_inspector()

            inspector_info = recommended_inspector.get_inspector_info()
            print(inspector_info)

            inspector_reviews = recommended_inspector.get_reviews_list()

            self.screen_2.recomm_insp_info_table.setItem(0, 0, QTableWidgetItem(inspector_info[0]))
            self.screen_2.recomm_insp_info_table.setItem(0, 1, QTableWidgetItem(inspector_info[1]))
            self.screen_2.recomm_insp_info_table.setItem(0, 2, QTableWidgetItem(inspector_info[4]))
            self.screen_2.recomm_insp_info_table.setItem(0, 3, QTableWidgetItem(inspector_info[5]))
            self.screen_2.recomm_insp_info_table.setItem(0, 4, QTableWidgetItem(str(inspector_info[10])))
            # assume that the actual distance of the Inspector from the user, would be calculated in some way
            self.screen_2.recomm_insp_info_table.setItem(0, 5, QTableWidgetItem('3 Km Away'))
            self.screen_2.recomm_insp_info_table.setItem(0, 6, QTableWidgetItem(str(len(inspector_reviews))))
            self.screen_2.recomm_insp_info_table.setItem(0, 7, QTableWidgetItem(str(
                self.calculate_review_positivity_percentage(inspector_reviews) * 100) + ' % Positive'))

            stack_widget.insertWidget(1, self.screen_2)
            stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen

    def calculate_review_positivity_percentage(self, inspector_reviews) -> float:
        positive_reviews_count = 0
        for review in inspector_reviews:
            if review.is_review_positive():
                positive_reviews_count += 1

        return positive_reviews_count / len(inspector_reviews)


class ScheduleCarInspectionScreen2(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen2, self).__init__()
        loadUi("qt_ui/car_inspection_2.ui", self)

        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")
        self.continue_button.clicked.connect(self.continue_button_clicked)

        header = self.recomm_insp_info_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.recomm_insp_info_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)  # no edit on table cells

        self.custom_inspector_check_box.setStyleSheet("QCheckBox {color: #d3311b;}")
        self.custom_inspector_check_box.stateChanged.connect(self.custom_inspector_check_box_toggled)

    def custom_inspector_check_box_toggled(self):
        check_box_status = self.custom_inspector_check_box.checkState()
        print("in here, status : ", check_box_status)
        if check_box_status == 2:  # checked -> continue using a user specified Inspector
            pass
        elif check_box_status == 0:  # unchecked -> continue using the recommended Inspector
            screen_3 = ScheduleCarInspectionScreen3()
            stack_widget.insertWidget(2, screen_3)

    def continue_button_clicked(self):
        self.custom_inspector_check_box_toggled()
        stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)


class ScheduleCarInspectionScreen3(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen3, self).__init__()
        loadUi("qt_ui/car_inspection_3.ui", self)

        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

        self.submit_button.clicked.connect(self.submit_button_clicked)

        header = self.car_info_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.car_info_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)  # no edit on table cells

    def submit_button_clicked(self):
        global car_listing

        listing_id = int(self.listing_id_box.toPlainText())

        for listing in system_posted_listings:
            if listing.get_listing_id() == listing_id:
                car_listing = listing

        listing_car_info = car_listing.get_car().get_car_info()
        # print(listing_car_info)

        self.populate_car_info_table(listing_car_info)

    def populate_car_info_table(self, listing_car_info):
        self.car_info_table.setItem(0, 0, QTableWidgetItem(listing_car_info[0]))
        self.car_info_table.setItem(0, 1, QTableWidgetItem(listing_car_info[1]))
        self.car_info_table.setItem(0, 2, QTableWidgetItem(listing_car_info[2]))
        self.car_info_table.setItem(0, 3, QTableWidgetItem(str(listing_car_info[3])))
        self.car_info_table.setItem(0, 4, QTableWidgetItem(str(listing_car_info[4])))
        self.car_info_table.setItem(0, 5, QTableWidgetItem(str(car_listing.get_car_condition())))
        self.car_info_table.setItem(0, 6, QTableWidgetItem(str(listing_car_info[5])))
        self.car_info_table.setItem(0, 7, QTableWidgetItem(str(listing_car_info[6])))
        self.car_info_table.setItem(0, 8, QTableWidgetItem(str(listing_car_info[7])))
        self.car_info_table.setItem(0, 9, QTableWidgetItem(str(listing_car_info[8])))
        self.car_info_table.setItem(0, 10, QTableWidgetItem(str(listing_car_info[9])))
        self.car_info_table.setItem(0, 11, QTableWidgetItem(str(listing_car_info[10])))
        self.car_info_table.setItem(0, 12, QTableWidgetItem(str(listing_car_info[11])))
        self.car_info_table.setItem(0, 13, QTableWidgetItem(str(listing_car_info[12])))
        self.car_info_table.setItem(0, 14, QTableWidgetItem(str(listing_car_info[13])))
        self.car_info_table.setItem(0, 15, QTableWidgetItem(str(listing_car_info[14])))

    def continue_button_clicked(self):
        pass


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
