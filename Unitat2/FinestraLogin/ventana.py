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

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QVBoxLayout()
        self.main = None
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

            if account=="user":
                if password == "1234":
                    self.main = MainWindow("user")
                    self.main.show()
                    self.close()
                else:
                    self.error.setText("ERROR Contraseña")
                    
            elif account=="admin":
                if password == "1234":
                    self.main = MainWindow("admin")
                    self.main.show()
                    self.close()
                else:
                    self.error.setText("ERROR Contraseña")
            else:
                self.error.setText("ERROR Usuario")
                
class MainWindow(QMainWindow):
    def __init__(self,user):
        super().__init__()
        
        self.setWindowTitle("Logeado")
        layout = QVBoxLayout()
        self.label = QLabel(f"Welcome {user}")
        
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

        self.window_mode = QLabel(f"Mode: {user}")
        self.window_mode.setScaledContents(True)
        self.statusBar().addPermanentWidget(self.window_mode)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def exit(self,s):
        self.close()     
    def logout_action(self, checked):
        self.w = AnotherWindow()
        self.w.show()
        self.close()

app = QApplication(sys.argv)
w = AnotherWindow()
w.show()
app.exec()