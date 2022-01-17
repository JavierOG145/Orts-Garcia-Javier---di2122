import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QStatusBar
)

class AnotherWindow(QWidget):
    """
    Esta finestra és un QWidget, si no té parent,
    es mostrarà com una finestra flotant.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.user = QLineEdit("user")
        self.password = QLineEdit("password")
        self.aceptar_button = QPushButton("Aceptar")
        self.aceptar_button.clicked.connect(self.toggle_window)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.exit)
        self.error = QLabel("")

        
        layout.addWidget(self.user)
        layout.addWidget(self.password)
        layout.addWidget(self.aceptar_button)
        layout.addWidget(self.close_button)
        layout.addWidget(self.error)
        self.setLayout(layout)

    def exit(self,s):
        self.close()  
    def toggle_window(self, checked):
            
            account = self.user.text()
            password = self.password.text()

            self.w = MainWindow1()
            self.w2 = MainWindow2()

            if account=="user":
                if password == "1234":
                    if self.w.isVisible():
                        self.w.hide()
                    else:
                        self.w.show()
                        self.hide()
                else:
                    self.error.setText("ERROR Contraseña")
                    
            elif account=="admin":
                if password == "1234":
                    if self.w2.isVisible():
                        self.w2.hide()
                    else:
                        self.w2.show()
                        self.hide()
                else:
                    self.error.setText("ERROR Contraseña")
            else:
                self.error.setText("ERROR Usuario")


class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("USER")
        layout = QVBoxLayout()
        self.label = QLabel("WELCOME USER")
        
        layout.addWidget(self.label)
        
        self.menu = self.menuBar()
        option_menu = self.menu.addMenu("&Menu")
        
        menu_button_logout = QAction("&Return", self)
        menu_button_logout.setStatusTip("Return")
        menu_button_logout.triggered.connect(self.logout_action)
        menu_button_logout.setStatusTip("Boton Return")
        menu_button_exit = QAction("&Exit", self)
        menu_button_exit.setStatusTip("Exit")
        menu_button_exit.triggered.connect(self.exit)

        option_menu.addAction(menu_button_logout)
        option_menu.addAction(menu_button_exit)

        self.setStatusBar(QStatusBar(self))

        self.window_mode = QLabel("Mode: User")
        self.window_mode.setScaledContents(True)
        self.statusBar().addPermanentWidget(self.window_mode)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def exit(self,s):
        self.close()     
    def logout_action(self, checked):
        self.w = AnotherWindow()

        if self.w.isVisible():
            self.w.hide()

        else:
            self.hide()
            self.w.show()
    
            
class MainWindow2(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ADMIN")
        layout = QVBoxLayout()
        self.label = QLabel("WELCOME ADMIN")

        layout.addWidget(self.label)
        
        self.menu = self.menuBar()
        option_menu = self.menu.addMenu("&Menu")
        
        menu_button_logout = QAction("&Return", self)
        menu_button_logout.setStatusTip("Return")
        menu_button_logout.triggered.connect(self.logout_action)

        menu_button_logout.setStatusTip("Boton Return")
        menu_button_exit = QAction("&Exit", self)
        menu_button_exit.setStatusTip("Exit")
        menu_button_exit.triggered.connect(self.exit)

        option_menu.addAction(menu_button_logout)
        option_menu.addAction(menu_button_exit)


        self.setStatusBar(QStatusBar(self))

        self.window_mode = QLabel("mode: Admin")
        self.window_mode.setScaledContents(True)
        self.statusBar().addPermanentWidget(self.window_mode)


        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def exit(self,s):
        self.close()     
    def logout_action(self, checked):
        self.w = AnotherWindow()

        if self.w.isVisible():
            self.w.hide()

        else:
            self.hide()
            self.w.show()
         

    
        
app = QApplication(sys.argv)
w = AnotherWindow()
w.show()
app.exec()