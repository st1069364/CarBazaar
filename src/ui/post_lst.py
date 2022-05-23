import sys

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

class PostListingScreen:
    def __init__(self):
        self.file_dialog = QFileDialog(self)
        self.files = []
        self.images = []

        self.call_screen5 = 0

    def continue_button_clicked(self):
        stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen

    def back_button_pressed(self):
        stack_widget.setCurrentIndex(stack_widget.currentIndex() - 1)  # move to the previous UI screen

    def file_upload(self):
        self.files = self.file_dialog.getOpenFileNames(self, "Select one or more files", "",
                                                       "PDF Documents (*.pdf)")

    def image_upload(self):
        file_names = self.file_dialog.getOpenFileNames(self, "Select one or more image files",
                                                       "", "Images (*.png *.jpg)")
        if self.images:
            self.images = file_names[0]

    def get_image_list(self):
        if self.images:
            return self.images


class MainWindow(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("qt_ui/post_lst_1.ui", self)  # load the .ui file for the first screen

        # when the continue button gets clicked, we need to switch to the next UI screen,
        # so attach that functionality to the button by connecting to the corresponding method
        # self.continue_button.clicked.connect(super().continue_button_clicked)
        self.continue_button.clicked.connect(self.continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

    def continue_button_clicked(self):
        screen_5.car_info_table.setItem(0,0, QTableWidgetItem(self.category_box.currentText()))
        screen_5.car_info_table.setItem(0,1, QTableWidgetItem(self.company_box.currentText()))
        screen_5.car_info_table.setItem(0,2, QTableWidgetItem(self.model_box.currentText()))

        screen_5.car_info_table.setItem(0, 4, QTableWidgetItem(self.year_box.value()))
        screen_5.car_info_table.setItem(0, 5, QTableWidgetItem(self.mileage_box.toPlainText()))
        screen_5.car_info_table.setItem(0, 6, QTableWidgetItem(self.condition_box.currentText()))
        screen_5.car_info_table.setItem(0, 7, QTableWidgetItem(self.engine_box.toPlainText()))
        screen_5.car_info_table.setItem(0, 8, QTableWidgetItem(self.power_box.toPlainText()))
        screen_5.car_info_table.setItem(0, 9, QTableWidgetItem(self.transmission_box.currentText()))
        screen_5.car_info_table.setItem(0, 10, QTableWidgetItem(self.fuel_box.currentText()))
        screen_5.car_info_table.setItem(0, 11, QTableWidgetItem(self.ccons_box.toPlainText()))
        screen_5.car_info_table.setItem(0, 12, QTableWidgetItem(self.mcons_box.toPlainText()))

        screen_5.car_info_table.setItem(0, 13, QTableWidgetItem(self.color_box.currentText()))
        screen_5.car_info_table.setItem(0, 14, QTableWidgetItem(self.int_color_box.currentText()))
        screen_5.car_info_table.setItem(0, 15, QTableWidgetItem(self.ndoors_box.currentText()))
        screen_5.car_info_table.setItem(0, 16, QTableWidgetItem(self.reg_plate_box.toPlainText()))

        print(self.reg_plate_box.toPlainText())



        super().continue_button_clicked()


class Screen2(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("qt_ui/post_lst_2.ui", self)  # load the .ui file for the second screen
        self.continue_button.clicked.connect(super().continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")
        self.skip_button.clicked.connect(super().continue_button_clicked)
        self.skip_button.setStyleSheet("QPushButton {background-color: #2d4b5a; color: white; border: none}")

        self.upload_button.clicked.connect(super().file_upload)
        self.image_upload_button.clicked.connect(self.image_upload)

        self.images = []

    def image_upload(self):
        file_names = self.file_dialog.getOpenFileNames(self, "Select one or more image files",
                                                       "", "Images (*.png *.jpg)")
        if file_names:
            self.images = file_names[0]
            screen_5.image_list = self.images
            screen_5.setup_images()


class Screen3(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(Screen3, self).__init__()
        loadUi("qt_ui/post_lst_3.ui", self)  # load the .ui file for the third screen

        self.continue_button.clicked.connect(super().continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

        # here using some future code functionality, we will set the displayed vehicle price
        self.price_box.setText('12345 €')
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

        self.post_button.clicked.connect(self.post_listing_button_pressed)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")

        self.view_3d_button.clicked.connect(self.view_3d_model)
        self.next_image_button.clicked.connect(self.show_next_image)
        self.prev_image_button.clicked.connect(self.show_prev_image)

        self.car_info_table.setColumnWidth(0, 80)
        # header = self.car_info_table.horizontalHeader()
        # header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
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
