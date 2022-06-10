import os.path
import time
from ui import app_res_rc
import types
import sys
import classes
from classes import *

import test_data_init
from test_data_init import main

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

# -------------------------------------------------
# For use case Post Car Listing
listing_car: Car = None
car_listing: CarListing = None
test_location: Location = Location((34.5, 35.5))
# -------------------------------------------------

# -------------------------------------------------
# For use case Schedule Car Inspection
car_inspection: CarInspection = None
car_listing: CarListing = None
inspection_invoice: Invoice = None
inspection_transaction: Transaction = None
alt_flow_2: bool = False


# -------------------------------------------------


def init_stack_widget():
    stack_widget.setFixedWidth(400)
    stack_widget.setFixedHeight(881)
    stack_widget.setStyleSheet("QMainWindow {background: 'white';}")

    # set up window icon to the CarBazaar logo and window title to that of the current Use Case
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/resources/resources/CarBazaar_logo_trans.png"), QtGui.QIcon.Normal,
                   QtGui.QIcon.Off)
    stack_widget.setWindowIcon(icon)
    stack_widget.setWindowTitle('CarBazaar')


def return_to_user_menu():
    # Remove all widgets from stack_widget
    for i in range(stack_widget.count()):
        stack_widget.setCurrentIndex(i)
        stack_widget.removeWidget(stack_widget.currentWidget())

    # Add user menu screen to stack widget and show the widget. Since, the only widget in the stack_widget,
    # is the menu screen, this effectively returns the user to the User Menu
    menu_screen = UserMenuScreen()
    stack_widget.addWidget(menu_screen)
    stack_widget.setWindowTitle('CarBazaar')
    stack_widget.show()


# needed to set the placeholder text for the QComboBox objects
def paintEvent(self, event):
    painter = QtWidgets.QStylePainter(self)
    painter.setPen(self.palette().color(QtGui.QPalette.Text))

    # draw the combobox frame, focusrect and selected etc.
    opt = QtWidgets.QStyleOptionComboBox()
    self.initStyleOption(opt)
    painter.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt)

    if self.currentIndex() < 0:
        opt.palette.setBrush(
            QtGui.QPalette.ButtonText,
            opt.palette.brush(QtGui.QPalette.ButtonText).color().lighter(),
        )
        if self.placeholderText():
            opt.currentText = self.placeholderText()

    # draw the icon and text
    painter.drawControl(QtWidgets.QStyle.CE_ComboBoxLabel, opt)


def back_button_pressed():
    stack_widget.setCurrentIndex(stack_widget.currentIndex() - 1)  # move to the previous UI screen


class UserMenuScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/qt_ui/user_menu.ui", self)  # load the .ui file

        # gray-out the non-implemented use cases
        self.spare_part_listing_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.test_drive_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.car_search_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.spare_part_search_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.nearby_dealerships_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.compare_cars_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.buy_car_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.car_exchange_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.insurance_plan_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.car_transportation_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.my_purchases_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.my_car_inspections_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.my_test_drives_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.my_car_transportations_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.my_listings_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.my_messages_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.wishlist_button.setStyleSheet("QPushButton {background-color: #919191}")
        self.contact_button.setStyleSheet("QPushButton {background-color: #919191}")

        self.car_listing_button.clicked.connect(self.post_car_listing)
        self.car_inspection_button.clicked.connect(self.schedule_car_inspection)

    def post_car_listing(self):
        screen_1 = PostCarListingScreen1()
        stack_widget.addWidget(screen_1)
        stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)

    def schedule_car_inspection(self):
        screen_1 = ScheduleCarInspectionScreen1()
        stack_widget.addWidget(screen_1)
        stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)


class PostCarListingScreen1(QtWidgets.QMainWindow):
    def __init__(self):
        super(PostCarListingScreen1, self).__init__()
        loadUi("ui/qt_ui/post_lst_1.ui", self)  # load the .ui file for the first screen

        self.back_button.clicked.connect(return_to_user_menu)

        # set the placeholder text for all the QComboBox objects
        self.category_box.paintEvent = types.MethodType(paintEvent, self.category_box)
        self.company_box.paintEvent = types.MethodType(paintEvent, self.company_box)
        self.model_box.paintEvent = types.MethodType(paintEvent, self.model_box)
        self.condition_box.paintEvent = types.MethodType(paintEvent, self.condition_box)
        self.transmission_box.paintEvent = types.MethodType(paintEvent, self.transmission_box)
        self.fuel_box.paintEvent = types.MethodType(paintEvent, self.fuel_box)
        self.color_box.paintEvent = types.MethodType(paintEvent, self.color_box)
        self.int_color_box.paintEvent = types.MethodType(paintEvent, self.int_color_box)
        self.ndoors_box.paintEvent = types.MethodType(paintEvent, self.ndoors_box)

        test_data_init.main()  # load test data

        self.screen_2 = PostCarListingScreen2()

        stack_widget.setWindowTitle('Post Car Listing')

        # when the user selects a company on the company_box drop-down menu, call the
        # on_company_selection method, to populate the model_box with the corresponding
        # company's car models.
        self.company_box.activated[str].connect(self.on_company_selection)
        self.condition_box.activated[str].connect(self.on_condition_selection)

        # when the continue button gets clicked, we need to switch to the next UI screen,
        # so attach that functionality to the button by connecting to the corresponding method
        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

    # This would normally cause a data fetch from the DB, but here, we only support selecting 'Alfa Romeo'
    # and 'Citroen', at which point we se the available model selections, to just a few predetermined ones
    def on_company_selection(self):
        if self.company_box.currentText() == 'Alfa Romeo':
            self.model_box.addItem('Giulietta')
            self.model_box.addItem('Mito')
            self.model_box.addItem('156')
        if self.company_box.currentText() == 'Citroen':
            self.model_box.addItem('C3')
            self.model_box.addItem('C4')
            self.model_box.addItem('Xsara')

    # When the user selects the cars condition, check the mileage. If the user chose 'New' the car cannot
    # have a non-zero mileage, so show a warning message. Similarly, if the user chose 'Used', the car
    # cannot have a zero mileage, so show a corresponding warning message
    def on_condition_selection(self):
        if self.condition_box.currentText() == 'New' and self.mileage_box.toPlainText() != '':
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('A Car cannot be New and have a non-zero mileage!!')
            msg.exec()
        elif self.condition_box.currentText() == 'Used' and self.mileage_box.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('A Car cannot be Used and have a zero mileage')
            msg.exec()

    def continue_button_clicked(self):
        global car_listing
        global listing_car

        listing_car = Car()

        if self.mileage_box.toPlainText() == '':
            car_mileage = 0
        else:
            car_mileage = int(self.mileage_box.toPlainText())

        listing_car.set_car_info(self.category_box.currentText(),
                                 self.company_box.currentText(),
                                 self.model_box.currentText(), self.year_box.value(),
                                 car_mileage, int(self.engine_box.toPlainText()),
                                 int(self.power_box.toPlainText()), self.transmission_box.currentText(),
                                 self.fuel_box.currentText(), int(self.ccons_box.toPlainText()),
                                 int(self.mcons_box.toPlainText()), self.color_box.currentText(),
                                 self.int_color_box.currentText(), int(self.ndoors_box.currentText()),
                                 self.reg_plate_box.toPlainText())

        if listing_car.is_car_valid():
            car_listing = CarListing(self.condition_box.currentText())
            car_listing.set_car(listing_car)

            stack_widget.insertWidget(2, self.screen_2)
            stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('Non-existent car. Please check the data you entered again !!')
            msg.exec()


class PostCarListingScreen2(QtWidgets.QMainWindow):
    def __init__(self):
        super(PostCarListingScreen2, self).__init__()
        loadUi("ui/qt_ui/post_lst_2.ui", self)  # load the .ui file for the second screen
        self.car_docs: List[CarDocument] = []
        self.images = []
        self.file_dialog = QFileDialog(self)

        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

        self.skip_button.clicked.connect(self.continue_button_clicked)

        self.skip_button.setStyleSheet("QPushButton {background-color: #2d4b5a; color: white; border: none}")

        self.upload_button.clicked.connect(self.file_upload)
        self.image_upload_button.clicked.connect(self.image_upload)

        self.screen_3 = PostCarListingScreen3()

    def file_upload(self):
        global car_listing
        file_names = self.file_dialog.getOpenFileNames(self, "Select one or more files", "./ui/test_docs",
                                                       "PDF Documents (*.pdf)")
        if file_names:
            file_names = file_names[0]
            for file_name in file_names:
                doc = CarDocument()
                self.car_docs.append(doc)

    def image_upload(self):
        global car_listing
        file_names = self.file_dialog.getOpenFileNames(self, "Select one or more image files",
                                                       "./ui/test_img", "Images (*.png *.jpg)")
        if file_names:
            self.images = file_names[0]
            car_listing.set_photos(self.images)

    def continue_button_clicked(self):
        global car_listing

        for doc in self.car_docs:
            doc.set_doc_info(self.doc_issue_authority_combobox.currentText(), self.doc_id_box.toPlainText())

        car_listing.set_docs(self.car_docs)

        # set the estimated price only the first time, because if for some reason the user pressed the 'back' button
        # the next time that PostCarListingScreen3 would show up, it would have a different estimated price for
        # the listing's car
        if self.screen_3.price_set_flag == 0:
            car_price = car_listing.get_car_price()
            self.screen_3.price_set_flag = 1
            self.screen_3.price_box.setText(str(car_price) + ' €')

        stack_widget.insertWidget(3, self.screen_3)
        stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen


class PostCarListingScreen3(QtWidgets.QMainWindow):
    def __init__(self):
        super(PostCarListingScreen3, self).__init__()
        loadUi("ui/qt_ui/post_lst_3.ui", self)  # load the .ui file for the third screen

        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

        self.price_check_box.setStyleSheet("QCheckBox {color: #d3311b;}")
        self.price_check_box.stateChanged.connect(self.price_check_box_toggled)

        self.price_set_flag = 0
        self.recommended_price_accepted_flag = 0

        self.screen_4 = PostCarListingScreen4()

    def price_check_box_toggled(self):
        check_box_status = self.price_check_box.checkState()
        if check_box_status == 2:  # checked -> continue using the system's recommended price
            self.recommended_price_accepted_flag = 1
        elif check_box_status == 0:  # unchecked -> continue using the user's specified price (**if** it is a valid one)
            self.recommended_price_accepted_flag = 0

    def continue_button_clicked(self):
        global listing_car
        global car_listing

        stack_widget.insertWidget(4, self.screen_4)
        if self.recommended_price_accepted_flag == 1:
            stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen
        elif self.recommended_price_accepted_flag == 0 and self.custom_price_box.toPlainText() != '':
            if listing_car.compare_price(float(self.custom_price_box.toPlainText())):
                car_listing.set_car_price(float(self.custom_price_box.toPlainText()))
                stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen
            else:
                msg = QMessageBox()
                msg.setWindowTitle('Error!!')
                msg.setText('The price you entered varies greatly from the system\'s recommended price!'
                            ' Please pick a price closer to the recommended one or'
                            ' continue using the recommended price !!')
                msg.exec()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('Please either check the box to continue using the recommended price or enter you own price')
            msg.exec()


class PostCarListingScreen4(QtWidgets.QMainWindow):
    def __init__(self):
        super(PostCarListingScreen4, self).__init__()
        loadUi("ui/qt_ui/post_lst_4.ui", self)  # load the .ui file for the fourth screen

        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

        self.screen_5 = PostCarListingScreen5()

    def get_listing_title(self):
        return self.listing_title_box.toPlainText()

    def continue_button_clicked(self):
        global car_listing
        global test_location
        if self.description_box.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('No description added! Please fill the description box')
            msg.exec()
        if self.listing_title_box.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('No listing title added! Please fill the Listing Title box')
            msg.exec()
        else:
            self.screen_5.car_descr_box.setText(self.description_box.toPlainText())

            if self.listing_title_box.toPlainText():
                self.screen_5.listing_title_bar.move(115, self.screen_5.listing_title_bar.y())
                self.screen_5.listing_title_bar.setAlignment(Qt.AlignCenter)
                self.screen_5.listing_title_bar.setStyleSheet("color: #d3311b")
                self.screen_5.listing_title_bar.setText(self.listing_title_box.toPlainText())
                self.screen_5.listing_title_bar.adjustSize()

            car_listing.set_listing_info(self.listing_title_box.toPlainText(), classes.system_registered_users[0],
                                         test_location)
            car_listing.set_description(self.description_box.toPlainText())
            car_listing.create_3D_model()

            self.screen_5.update_car_details_table()
            self.screen_5.image_list = car_listing.get_photos()
            self.screen_5.setup_images()
            stack_widget.insertWidget(5, self.screen_5)
            stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen


class PostCarListingScreen5(QtWidgets.QMainWindow):
    def __init__(self):
        super(PostCarListingScreen5, self).__init__()
        loadUi("ui/qt_ui/post_lst_5.ui", self)

        self.image_list = []
        self.image = None
        self.current_image_index = 0

        self.label = QLabel(self)
        self.label.setGeometry(55, 150, 290, 100)
        self.label.setScaledContents(True)

        self.label.setText('No images were added')
        self.label.setAlignment(Qt.AlignCenter)

        self.post_button.clicked.connect(self.post_listing_button_pressed)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

        self.view_3d_button.clicked.connect(self.view_3d_model)
        self.next_image_button.clicked.connect(self.show_next_image)
        self.prev_image_button.clicked.connect(self.show_prev_image)

        header = self.car_info_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.car_info_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # no editing on table cells

    def setup_images(self):
        if self.image_list:
            self.image = QPixmap(self.image_list[self.current_image_index])
            self.image.scaled(140, 50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
            self.label.setPixmap(self.image)

    def show_next_image(self):
        if self.image_list:
            if self.current_image_index == len(self.image_list) - 1:
                self.current_image_index = 0
            else:
                self.current_image_index += 1

            file = self.image_list[self.current_image_index]
            self.label.setPixmap(QPixmap(file))

    def show_prev_image(self):
        if self.image_list:
            if self.current_image_index == 0:
                self.current_image_index = len(self.image_list) - 1
            else:
                self.current_image_index -= 1

            file = self.image_list[self.current_image_index]
            self.label.setPixmap(QPixmap(file))

    def view_3d_model(self):
        msg = QMessageBox()
        msg.setWindowTitle('Unavailable Feature !!')
        msg.setText('This feature has not been implemented yet !!')
        msg.exec()

    def post_listing_button_pressed(self):
        global car_listing
        global stack_widget
        if car_listing.post_listing():
            msg = QMessageBox()
            msg.setWindowTitle('Success !!')
            msg.setText('Your Car Listing has been successfully posted!!\nClick OK to return to User Menu')
            msg.exec()
            return_to_user_menu()

    def update_car_details_table(self):
        global listing_car
        global car_listing
        car_details = listing_car.get_car_info()

        self.car_info_table.setItem(0, 0, QTableWidgetItem(car_details[0]))
        self.car_info_table.setItem(0, 1, QTableWidgetItem(car_details[1]))
        self.car_info_table.setItem(0, 2, QTableWidgetItem(car_details[2]))
        self.car_info_table.setItem(0, 3, QTableWidgetItem(str(car_details[3])))
        self.car_info_table.setItem(0, 4, QTableWidgetItem(str(car_details[4])))
        self.car_info_table.setItem(0, 5, QTableWidgetItem(car_listing.get_car_condition()))
        self.car_info_table.setItem(0, 6, QTableWidgetItem(str(car_details[5])))
        self.car_info_table.setItem(0, 7, QTableWidgetItem(str(car_details[6])))
        self.car_info_table.setItem(0, 8, QTableWidgetItem(car_details[7]))
        self.car_info_table.setItem(0, 9, QTableWidgetItem(car_details[8]))
        self.car_info_table.setItem(0, 10, QTableWidgetItem(str(car_details[9])))
        self.car_info_table.setItem(0, 11, QTableWidgetItem(str(car_details[10])))
        self.car_info_table.setItem(0, 12, QTableWidgetItem(car_details[11]))
        self.car_info_table.setItem(0, 13, QTableWidgetItem(car_details[12]))
        self.car_info_table.setItem(0, 14, QTableWidgetItem(str(car_details[13])))
        self.car_info_table.setItem(0, 15, QTableWidgetItem(car_details[14]))
        self.car_info_table.setItem(0, 16, QTableWidgetItem(str(car_listing.get_car_price()) + ' €'))


class ScheduleCarInspectionScreen1(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScheduleCarInspectionScreen1, self).__init__()
        loadUi("ui/qt_ui/car_inspection_1.ui", self)

        test_data_init.main()  # load test data

        self.back_button.clicked.connect(return_to_user_menu)

        self.screen_2 = ScheduleCarInspectionScreen2()

        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")
        stack_widget.setWindowTitle('Schedule Car Inspection')

    def continue_button_clicked(self):
        global car_inspection

        # split coordinates by comma into two values
        coordinates_list = self.location_box.toPlainText().split(",", 2)
        # strip() is used to remove excess whitespace
        entered_location = Location((float(coordinates_list[0].strip()), float(coordinates_list[1].strip())))

        if not entered_location.check_location_validity():  # Alternate Flow #1 (Invalid location)
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

            stack_widget.insertWidget(2, self.screen_2)
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
            QtWidgets.QAbstractItemView.NoEditTriggers)  # no editing on table cells

        self.custom_inspector_check_box.setStyleSheet("QCheckBox {color: #d3311b;}")
        self.custom_inspector_check_box.stateChanged.connect(self.is_recommended_inspector_accepted)

    def is_recommended_inspector_accepted(self):
        check_box_status = self.custom_inspector_check_box.checkState()
        if check_box_status == 2:  # checked -> continue using a user specified Inspector
            global alt_flow_2
            alt_flow_2 = True  # set the alt_flow_2 flag to indicate that we will execute Alternate Flow #2 of the use case
            inspector_info_screen = EnterInspectorInfoScreen()
            stack_widget.insertWidget(4, inspector_info_screen)
        elif check_box_status == 0:  # unchecked -> continue using the recommended Inspector
            screen_3 = ScheduleCarInspectionScreen3()
            stack_widget.insertWidget(3, screen_3)

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
            QtWidgets.QAbstractItemView.NoEditTriggers)  # no editing on table cells

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
                stack_widget.insertWidget(5, self.screen_4)
            else:
                stack_widget.insertWidget(4, self.screen_4)
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
            msg.setText(
                'The contact info you entered, does not correspond to a registered Inspector.\nReturning to main menu...')
            msg.exec()
            choice = QMessageBox.Ok
            if choice == QMessageBox.Ok:
                return_to_user_menu()
        else:  # if the given Inspector was found
            car_inspection.set_car_inspection_inspector(chosen_inspector)
            screen_3 = ScheduleCarInspectionScreen3()
            stack_widget.insertWidget(4, screen_3)
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
        global stack_widget

        # this Transaction would be normally created from the Payment Menu (payment use case)
        inspection_transaction = Transaction()
        # assume that the payment was made using Cash, and that the user paying for the transaction is
        # user "system_registered_users[0]", i.e the first User created in main() of test_data_init.py file
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

            msg = QMessageBox()
            msg.setWindowTitle('Return to User Menu')
            msg.setText('Click OK to return to User Menu')
            msg.exec()
            return_to_user_menu()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(BUTTON_STYLE)

    stack_widget = QtWidgets.QStackedWidget()
    menu = UserMenuScreen()
    stack_widget.addWidget(menu)

    init_stack_widget()
    stack_widget.show()  # show the widget

    msg = QMessageBox()
    msg.setWindowTitle('Welcome to CarBazaar !!!')
    msg.setText('The grey buttons correspond to features not implemented yet,\nsince this is a demo')
    msg.exec()

    sys.exit(app.exec_())  # program waits for window close, to end execution
