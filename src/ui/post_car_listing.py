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


# ---------------------------------------------
# Driver code for the Post Car Listing Use Case
# ---------------------------------------------

listing_car: Car = None
car_listing: CarListing = None
test_location: Location = Location((34.5, 35.5))


def continue_button_clicked():
    stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen


def back_button_pressed():
    stack_widget.setCurrentIndex(stack_widget.currentIndex() - 1)  # move to the previous UI screen


class PostCarListingScreen1(QtWidgets.QMainWindow):
    def __init__(self):
        super(PostCarListingScreen1, self).__init__()
        loadUi("qt_ui/post_lst_1.ui", self)  # load the .ui file for the first screen

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

        classes.main()

        self.screen_2 = PostCarListingScreen2()

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

            stack_widget.insertWidget(1, self.screen_2)
            continue_button_clicked()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('Non-existent car. Please check the data you entered again !!')
            msg.exec()


class PostCarListingScreen2(QtWidgets.QMainWindow):
    def __init__(self):
        super(PostCarListingScreen2, self).__init__()
        loadUi("qt_ui/post_lst_2.ui", self)  # load the .ui file for the second screen
        self.files = []
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
        file_names = self.file_dialog.getOpenFileNames(self, "Select one or more files", "./test_docs",
                                                       "PDF Documents (*.pdf)")
        if file_names:
            self.files = file_names[0]
            car_listing.set_docs(self.files)

    def image_upload(self):
        global car_listing
        file_names = self.file_dialog.getOpenFileNames(self, "Select one or more image files",
                                                       "./test_img", "Images (*.png *.jpg)")
        if file_names:
            self.images = file_names[0]
            car_listing.set_photos(self.images)

    def continue_button_clicked(self):
        global car_listing
        # set the estimated price only the first time, because if for some reason the user pressed the 'back' button
        # the next time that PostCarListingScreen3 would show up, it would have a different estimated price for
        # the listing's car
        if self.screen_3.price_set_flag == 0:
            car_price = car_listing.get_car_price()
            self.screen_3.price_set_flag = 1
            self.screen_3.price_box.setText(str(car_price) + ' €')

        stack_widget.insertWidget(2, self.screen_3)
        continue_button_clicked()


class PostCarListingScreen3(QtWidgets.QMainWindow):
    def __init__(self):
        super(PostCarListingScreen3, self).__init__()
        loadUi("qt_ui/post_lst_3.ui", self)  # load the .ui file for the third screen

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

        stack_widget.insertWidget(3, self.screen_4)
        if self.recommended_price_accepted_flag == 1:
            continue_button_clicked()
        elif self.recommended_price_accepted_flag == 0 and self.custom_price_box.toPlainText() != '':
            if listing_car.compare_price(float(self.custom_price_box.toPlainText())):
                car_listing.set_car_price(float(self.custom_price_box.toPlainText()))
                continue_button_clicked()
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
        loadUi("qt_ui/post_lst_4.ui", self)  # load the .ui file for the fourth screen

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
            stack_widget.insertWidget(4, self.screen_5)
            continue_button_clicked()


class PostCarListingScreen5(QtWidgets.QMainWindow):
    def __init__(self):
        super(PostCarListingScreen5, self).__init__()
        loadUi("qt_ui/post_lst_5.ui", self)

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
        self.car_info_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # no edit on table cells

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
        if car_listing.post_listing():
            msg = QMessageBox()
            msg.setWindowTitle('Success !!')
            msg.setText('Your Car Listing has been successfully posted\nYou may now exit this screen !!')
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Failure !!')
            msg.setText('You have already posted a listing for this car !!')
            msg.exec()

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # create Qt Application and pass the command-line args
    app.setStyleSheet(BUTTON_STYLE)  # set the button style to be used to the "CarBazaar" style

    # create the StackedWidget that will be used to transition from one Window to another
    stack_widget = QtWidgets.QStackedWidget()

    # create the screen to be added to the StackedWidget
    screen_1 = PostCarListingScreen1()

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
    stack_widget.setWindowTitle('Post Car Listing')
    stack_widget.show()  # show the widget
    sys.exit(app.exec_())  # program waits for window close, to end execution
