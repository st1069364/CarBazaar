from ui import app_res_rc
import os
import sys
import time

import classes
from classes import *

from PyQt5 import QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
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
inspection_invoice: Invoice = None
inspection_transaction: Transaction = None
alt_flow_2: bool = False


def back_button_pressed():
    stack_widget.setCurrentIndex(stack_widget.currentIndex() - 1)  # move to the previous UI screen


class ScheduleCarInspectionScreen1(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen1, self).__init__()
        loadUi("ui/qt_ui/car_inspection_1.ui", self)

        classes.main()  # to add some test data

        self.screen_2 = ScheduleCarInspectionScreen2()

        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

    def continue_button_clicked(self):
        global car_inspection

        # split coordinates by comma into two values
        coordinates_list = self.location_box.toPlainText().split(",", 2)
        # strip() is used to remove excess whitespace
        entered_location = Location((float(coordinates_list[0].strip()), float(coordinates_list[1].strip())))

        if not entered_location.check_location_validity(): # Alternate Flow #1 (Invalid location)
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

            date = self.calendar_widget.selectedDate().toPyDate()  # convert QDate to datetime.date
            time = datetime.time(self.hour_box.time().hour(), self.minute_box.time().minute())
            date_and_time = datetime.datetime.combine(date, time)  # combine date and time into a datetime object

            car_inspection.set_car_inspection_info(check_type, date_and_time, entered_location)
            recommended_inspector = car_inspection.find_recommended_inspector()  # find recommended inspector

            inspector_info = recommended_inspector.get_inspector_info()
            inspector_reviews = recommended_inspector.get_reviews_list()

            self.fill_inspector_info_table(inspector_info, inspector_reviews)

            stack_widget.insertWidget(1, self.screen_2)
            stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen

    def fill_inspector_info_table(self, inspector_info, inspector_reviews):
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

    def calculate_review_positivity_percentage(self, inspector_reviews) -> float:
        positive_reviews_count = 0
        for review in inspector_reviews:
            if review.is_review_positive():
                positive_reviews_count += 1

        return positive_reviews_count / len(inspector_reviews)  # return the percetange of positive reviews


class ScheduleCarInspectionScreen2(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen2, self).__init__()
        loadUi("ui/qt_ui/car_inspection_2.ui", self)

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
        self.custom_inspector_check_box.stateChanged.connect(self.is_recommended_inspector_accepted)

    def is_recommended_inspector_accepted(self):
        check_box_status = self.custom_inspector_check_box.checkState()
        if check_box_status == 2:  # checked -> continue using a user specified Inspector
            global alt_flow_2
            alt_flow_2 = True  # set the alt_flow_2 flag to indicate that we will execute Alternate Flow #2 of the use case
            inspector_info_screen = EnterInspectorInfoScreen()
            stack_widget.insertWidget(2, inspector_info_screen)
        elif check_box_status == 0:  # unchecked -> continue using the recommended Inspector
            screen_3 = ScheduleCarInspectionScreen3()
            stack_widget.insertWidget(2, screen_3)

    def continue_button_clicked(self):
        self.is_recommended_inspector_accepted()
        stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)


class ScheduleCarInspectionScreen3(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen3, self).__init__()
        loadUi("ui/qt_ui/car_inspection_3.ui", self)

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

        self.screen_4 = ScheduleCarInspectionScreen4()

    def submit_button_clicked(self):
        global car_listing
        global car_inspection

        if self.listing_id_box.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('Please enter a Listing ID')
            msg.exec()
        else:
            listing_id = int(self.listing_id_box.toPlainText())

            for listing in system_posted_listings:  # find the CarListing instance with the given Listing ID
                if listing.get_listing_id() == listing_id:
                    car_listing = listing

            if car_listing is None:  # if a CarListing was not found
                msg = QMessageBox()
                msg.setWindowTitle('Error!!')
                msg.setText('Please enter a valid Listing ID')
                msg.exec()
            else:  # if a CarListing was found
                listing_car_info = car_listing.get_car().get_car_info()
                car_inspection.set_car_to_inspect(car_listing)
                self.fill_car_info_table(listing_car_info)

    def fill_car_info_table(self, listing_car_info):
        self.car_info_table.setItem(0, 0, QTableWidgetItem(listing_car_info[0]))
        self.car_info_table.setItem(0, 1, QTableWidgetItem(listing_car_info[1]))
        self.car_info_table.setItem(0, 2, QTableWidgetItem(listing_car_info[2]))
        self.car_info_table.setItem(0, 3, QTableWidgetItem(str(listing_car_info[3])))
        self.car_info_table.setItem(0, 4, QTableWidgetItem(str(listing_car_info[4])))

        if car_listing.get_car_condition() == ProductCondition.Used:
            self.car_info_table.setItem(0, 5, QTableWidgetItem('Used'))
        elif str(car_listing.get_car_condition()) == ProductCondition.New:
            self.car_info_table.setItem(0, 5, QTableWidgetItem('New'))

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
        global car_listing
        global alt_flow_2
        if car_listing is None:
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('Please enter a Listing ID in order to retrieve the car\'s details')
            msg.exec()
        else:
            self.screen_4.price_box.setText(str(random.randint(50, 150)) + ' €')  # random price for car inspection
            self.screen_4.duration_box.setText(str(random.randint(10, 90)) + ' minutes')  # random duration
            if alt_flow_2:
                stack_widget.insertWidget(4, self.screen_4)
            else:
                stack_widget.insertWidget(3, self.screen_4)
            stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)


class EnterInspectorInfoScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EnterInspectorInfoScreen, self).__init__()
        loadUi("ui/qt_ui/car_inspection_alt_2.ui", self)

        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

        self.submit_button.clicked.connect(self.submit_button_clicked)

    def submit_button_clicked(self):
        global car_inspection

        inspector_telephone = self.inspector_phone_box.toPlainText()
        inspector_email = self.inspector_email_box.toPlainText()
        # search for an Inspector with the given contact information
        chosen_inspector = car_inspection.find_inspector(inspector_telephone, inspector_email)
        if chosen_inspector is None:  # if such an Inspector was not found
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('The contact info you entered, does not correspond to a registered Inspector.\nExiting...')
            msg.exec()
            choice = QMessageBox.Ok
            if choice == QMessageBox.Ok:
                app.exit(-1)
        else:  # if the given Inspector was found
            car_inspection.set_car_inspection_inspector(chosen_inspector)
            screen_3 = ScheduleCarInspectionScreen3()
            stack_widget.insertWidget(3, screen_3)
            stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)


class ScheduleCarInspectionScreen4(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen4, self).__init__()
        loadUi("ui/qt_ui/car_inspection_4.ui", self)

        self.confirm_button.clicked.connect(self.confirm_button_clicked)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

    def confirm_button_clicked(self):
        global inspection_invoice
        global inspection_transaction
        global car_inspection

        # this Transaction would be normally created from the Payment Menu (payment use case)
        inspection_transaction = Transaction()
        # assume that the payment was made using Cash, and that the user paying for the transaction is
        # user "system_registered_users[0]", i.e the first User created in main() of classes.py file
        inspection_transaction.set_transaction_info(PaymentType.Cash, float(self.price_box.text().replace("€", "")),
                                                    TransactionType.Payment, system_registered_users[0],
                                                    car_inspection.get_inspector(), random.randint(1, 10))

        inspection_invoice = Invoice()
        inspection_invoice.set_invoice_info(inspection_transaction, "Invoice for Car Inspection of Citroen C3",
                                            system_registered_users[0].get_email())

        car_inspection.set_car_inspection_transaction(inspection_transaction)
        if car_inspection.register_car_inspection() and TransactionLog.register_transaction(inspection_transaction):
            time.sleep(2)  # sleep for 2 seconds, assume that the payment is made and that the emails were sent
            self.success_label.setText("You have successfully arranged an inspection\nappointment!")
            self.success_label.setStyleSheet("QLabel {color: #5cb85c}")
            self.success_label.adjustSize()
            self.success_label.setAlignment(Qt.AlignCenter)
            self.email_label.setText("The appointment's details have been sent\nto your email!")
            self.email_label.setStyleSheet("QLabel {color: #d3311b}")
            self.email_label.adjustSize()
            self.email_label.setAlignment(Qt.AlignCenter)


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
