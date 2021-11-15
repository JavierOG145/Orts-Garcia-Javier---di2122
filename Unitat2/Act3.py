import sys
import argparse

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import QSize

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-t","--title", help="Title of application")
group.add_argument("-b", "--button-text",help="Button text")
group.add_argument("-f","--fixed-size", action="store_true",help="Window fixed size")
group.add_argument("-s","--size", nargs=2, metavar=("SIZE_X", "SIZE_Y"), type=int, help="Window's size")
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