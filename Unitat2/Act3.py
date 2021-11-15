import sys
import argparse

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-t","--title", help="Title of application")
group.add_argument("-b", "--button-text",help="Button text")
group.add_argument("-f","--fixed-size", action="store_true",help="Window fixed size")
group.add_argument("-s","--size", nargs=2, metavar=("SIZE_X", "SIZE_Y"), type=int, help="Window's size")
args = parser.parse_args()

class MainWindow(QMainWindow):
    def _init_(self, title="Title"):
        super()._init_()
        title, text, fixed, size_x, size_y = "La meua aplicació", "Aceptar", False, 300, 200
        if args.title:
            title = args.title
        if args.button_text:
            text = args.button_text
        if args.fixed_size:
            fixed = args.fixed_size
        if args.size:
            size_x,size_y = args.size

        self.setWindowTitle(title)
        self.setGeometry(600,400,size_x,size_y)
        if (fixed):
            self.setFixedSize(size_x,size_y)

        self.button = QPushButton(text)
        self.setCentralWidget(self.button)
        self.button.clicked.connect(QApplication.instance().quit)


        self.setCentralWidget(self.button)

        # self.setFixedSize(400,600)
        self.button.setMaximumSize(100, 25)
        self.setMaximumSize(400, 400)
        self.setMinimumSize(200, 200)

        self.button.show()
        self.show()


app = QApplication(sys.argv)

window = MainWindow()

app.exec()