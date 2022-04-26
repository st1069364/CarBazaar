import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout
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

    def continue_button_clicked(self):
        stack_widget.setCurrentIndex(stack_widget.currentIndex() + 1)  # move to the next UI screen

    def back_button_pressed(self):
        stack_widget.setCurrentIndex(stack_widget.currentIndex() - 1)

    def file_upload(self):
        self.file_dialog.show()


class MainWindow(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("qt_ui/post_lst_1.ui", self)  # load the .ui file for the first screen

        # when the continue button gets clicked, we need to switch to the next UI screen,
        # so attach that functionality to the button by connecting to the corresponding method
        self.continue_button.clicked.connect(super().continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")


class Screen2(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("qt_ui/post_lst_2.ui", self)  # load the .ui file for the second screen
        self.continue_button.clicked.connect(super().continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")


class Screen3(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(Screen3, self).__init__()
        loadUi("qt_ui/post_lst_3.ui", self)  # load the .ui file for the third screen

        self.continue_button.clicked.connect(super().continue_button_clicked)
        self.skip_button.clicked.connect(super().continue_button_clicked)
        self.upload_button.clicked.connect(super().file_upload)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")


class Screen4(QtWidgets.QMainWindow, PostListingScreen):
    def __init__(self):
        super(Screen4, self).__init__()
        loadUi("qt_ui/post_lst_4.ui", self)  # load the .ui file for the fourth screen

        # here using some future code functionality, we will set the displayed vehicle price
        self.price_box.setText('12345 €')
        self.checkBox.setStyleSheet("QCheckBox {color: #d3311b;}")

        self.continue_button.clicked.connect(super().continue_button_clicked)
        self.back_button.clicked.connect(super().back_button_pressed)
        self.back_button.setStyleSheet("QPushButton {background-color: #ebebeb; color: #d3311b; border-style: outset; "
                                       "border-width: 2px; border-color: #d5d5d5; font: bold 11px}")


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

    # add the widgets to the StackedWidget
    stack_widget.addWidget(main_window)
    stack_widget.addWidget(screen_2)
    stack_widget.addWidget(screen_3)
    stack_widget.addWidget(screen_4)

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
