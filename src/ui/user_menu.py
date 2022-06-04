import app_res_rc
import sys
from src import classes
from src.ui import post_car_listing

sys.path.append('../src')

from src.classes import *
from post_car_listing import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from PyQt5 import QtCore, QtGui, QtWidgets

BUTTON_STYLE = """QPushButton {
    background-color: #d3311b;
    border : none;
    color : white;
}"""


class UserMenuScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("qt_ui/user_menu.ui", self) # load the .ui file

        self.post_car_lst_button.clicked.connect(self.post_car_listing)

    def post_car_listing(self):
        print('in post car listing')
        stack_widget.addWidget(post_car_listing.MainWindow())



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(BUTTON_STYLE)
    stack_widget = QtWidgets.QStackedWidget()
    menu = UserMenuScreen()

    stack_widget.addWidget(menu)

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
