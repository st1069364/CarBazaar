import sys

from src import classes

sys.path.append('../src')

from src.classes import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import app_res_rc

BUTTON_STYLE = """QPushButton {
    background-color: #d3311b;
    border : none;
    color : white;
}"""

# ---------------------------------------------
# Driver code for the Post Car Listing Use Case
# ---------------------------------------------

listing_car: Car = None
car_listing: CarListing = None


class PostListingScreen:
    def __init__(self):
        self.file_dialog = QFileDialog(self)
        self.files = []
        self.images = []

    def continue_button_clicked(self):
        stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen

    def back_button_pressed(self):
        stack_widget.setCurrentIndex(stack_widget.currentIndex() - 1)  # move to the previous UI screen

    def file_upload(self):
        file_names = self.file_dialog.getOpenFileNames(self, "Select one or more files", "",
                                                       "PDF Documents (*.pdf)")
        if file_names:
            self.files = file_names[0]
            car_listing.set_docs(self.files)

    def image_upload(self):
        file_names = self.file_dialog.getOpenFileNames(self, "Select one or more image files",
                                                       "", "Images (*.png *.jpg)")
        if file_names:
            self.images = file_names[0]
            car_listing.set_photos(self.images)

    def get_image_list(self):
        if self.images:
            return self.images


class MainWindow(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("qt_ui/post_lst_1.ui", self)  # load the .ui file for the first screen

        classes.main()

        # when the user selects a company on the company_box drop-down menu, call the
        # on_company_selection method, to populate the model_box with the corresponding
        # company's car models.
        self.company_box.activated[str].connect(self.on_company_selection)
        self.condition_box.activated[str].connect(self.on_condition_selection)

        # when the continue button gets clicked, we need to switch to the next UI screen,
        # so attach that functionality to the button by connecting to the corresponding method
        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
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
        if self.condition_box.currentText() == 'New' and int(self.mileage_box.toPlainText()) != 0:
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

        listing_car.set_car_info(self.category_box.currentText(),
                                 self.company_box.currentText(),
                                 self.model_box.currentText(), self.year_box.value(),
                                 int(self.mileage_box.toPlainText()), int(self.engine_box.toPlainText()),
                                 int(self.power_box.toPlainText()), self.transmission_box.currentText(),
                                 self.fuel_box.currentText(), int(self.ccons_box.toPlainText()),
                                 int(self.mcons_box.toPlainText()), self.color_box.currentText(),
                                 self.int_color_box.currentText(), int(self.ndoors_box.currentText()),
                                 self.reg_plate_box.toPlainText())

        if listing_car.is_car_valid():
            car_listing = CarListing(self.condition_box.currentText())
            car_listing.set_car(listing_car)
            self.update_car_details_table()
            super().continue_button_clicked()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error!!')
            msg.setText('Non-existent car. Please check the data you entered again !!')
            msg.exec()

    def update_car_details_table(self):
        screen_5.car_info_table.setItem(0, 0, QTableWidgetItem(self.category_box.currentText()))
        screen_5.car_info_table.setItem(0, 1, QTableWidgetItem(self.company_box.currentText()))
        screen_5.car_info_table.setItem(0, 2, QTableWidgetItem(self.model_box.currentText()))

        screen_5.car_info_table.setItem(0, 3, QTableWidgetItem(str(self.year_box.value())))
        screen_5.car_info_table.setItem(0, 4, QTableWidgetItem(self.mileage_box.toPlainText()))
        screen_5.car_info_table.setItem(0, 5, QTableWidgetItem(self.condition_box.currentText()))
        screen_5.car_info_table.setItem(0, 6, QTableWidgetItem(self.engine_box.toPlainText()))
        screen_5.car_info_table.setItem(0, 7, QTableWidgetItem(self.power_box.toPlainText()))
        screen_5.car_info_table.setItem(0, 8, QTableWidgetItem(self.transmission_box.currentText()))
        screen_5.car_info_table.setItem(0, 9, QTableWidgetItem(self.fuel_box.currentText()))
        screen_5.car_info_table.setItem(0, 10, QTableWidgetItem(self.ccons_box.toPlainText()))
        screen_5.car_info_table.setItem(0, 11, QTableWidgetItem(self.mcons_box.toPlainText()))

        screen_5.car_info_table.setItem(0, 12, QTableWidgetItem(self.color_box.currentText()))
        screen_5.car_info_table.setItem(0, 13, QTableWidgetItem(self.int_color_box.currentText()))
        screen_5.car_info_table.setItem(0, 14, QTableWidgetItem(self.ndoors_box.currentText()))
        screen_5.car_info_table.setItem(0, 15, QTableWidgetItem(self.reg_plate_box.toPlainText()))


class Screen2(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("qt_ui/post_lst_2.ui", self)  # load the .ui file for the second screen
        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")
        self.skip_button.clicked.connect(self.continue_button_clicked)
        self.skip_button.setStyleSheet("QPushButton {background-color: #2d4b5a; color: white; border: none}")

        self.upload_button.clicked.connect(super().file_upload)
        self.image_upload_button.clicked.connect(super().image_upload)
        # self.image_upload_button.clicked.connect(self.image_upload)

        # self.screen_3 = Screen3()

        # self.images = []

    # def image_upload(self):
    #     file_names = self.file_dialog.getOpenFileNames(self, "Select one or more image files",
    #                                                    "", "Images (*.png *.jpg)")
    #     if file_names:
    #         self.images = file_names[0]
    #         super().car_listing.set_photos(self.images)
    #
    #         screen_5.image_list = self.images
    #         screen_5.setup_images()

    def continue_button_clicked(self):
        global listing_car
        car_price = listing_car.calculate_car_price()
        # self.screen_3.price_box.setText(car_price)
        # self.screen_3.show()


class Screen3(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(Screen3, self).__init__()
        loadUi("qt_ui/post_lst_3.ui", self)  # load the .ui file for the third screen

        self.continue_button.clicked.connect(super().continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

        # here using some future code functionality, we will set the displayed vehicle price
        # self.price_box.setText('12345 €')
        self.checkBox.setStyleSheet("QCheckBox {color: #d3311b;}")


class Screen4(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(Screen4, self).__init__()
        loadUi("qt_ui/post_lst_4.ui", self)  # load the .ui file for the fourth screen

        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

    def get_listing_title(self):
        return self.listing_title_box.toPlainText()

    def continue_button_clicked(self):
        screen_5.car_descr_box.setText(self.description_box.toPlainText())

        if self.listing_title_box.toPlainText():
            screen_5.listing_title_bar.move(115, screen_5.listing_title_bar.y())
            screen_5.listing_title_bar.setAlignment(Qt.AlignCenter)
            screen_5.listing_title_bar.setStyleSheet("color: #d3311b")
            screen_5.listing_title_bar.setText(self.listing_title_box.toPlainText())
            screen_5.listing_title_bar.adjustSize()

        super(Screen4, self).continue_button_clicked()
    # listing_title = self.get_listing_title()
    # lst = Listing()
    # print('Initial listing title: ' + lst.get_listing_title())
    # lst.set_listing_title(listing_title)
    # print('New listing title: ' + lst.get_listing_title())


class Screen5(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(Screen5, self).__init__()
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
        self.back_button.clicked.connect(super().back_button_pressed)
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
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # create Qt Application and pass the command-line args
    app.setStyleSheet(BUTTON_STYLE)  # set the button style to be used to the "CarBazaar" style

    # create the StackedWidget that will be used to transition from one Window to another
    stack_widget = QtWidgets.QStackedWidget()

    # create the screen to be added to the StackedWidget
    main_window = MainWindow()
    screen_2 = Screen2()
    screen_3 = Screen3()
    screen_4 = Screen4()
    screen_5 = Screen5()

    # add the widgets to the StackedWidget
    stack_widget.addWidget(main_window)
    stack_widget.addWidget(screen_2)
    stack_widget.addWidget(screen_3)
    stack_widget.addWidget(screen_4)
    stack_widget.addWidget(screen_5)

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
