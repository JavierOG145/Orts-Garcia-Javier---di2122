import sys
import argparse

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import QSize

parser = argparse.ArgumentParser()
parser.add_argument("-t TITLE","--title TITLE", help="Title of application")
parser.add_argument("-b BUTTON_TEXT", "--button-text BUTTON_TEXT",help="Button text")
parser.add_argument("-f","--fixed-size", help="Title of application")
parser.add_argument("-s SIZE SIZE","--size SIZE SIZE", help="Size of windows")
args = parser.parse_args()

class MainWindow(QMainWindow):
    def __init__(self, title="Title", button_text="Text", fixed=False):
        super().__init__()
        self.setWindowTitle(title)

        self.button = QPushButton(button_text)

        self.setCentralWidget(self.button)

        #self.setFixedSize(400,600)
        self.button.setMaximumSize(100,25)
        self.setMaximumSize(400,400)
        self.setMinimumSize(200,200)

        self.button.show()
        self.show()

app = QApplication(sys.argv)

window = MainWindow()

app.exec()