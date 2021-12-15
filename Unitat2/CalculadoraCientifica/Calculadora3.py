import sys
import os

from functools import partial
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QCheckBox, QMainWindow, QApplication, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget, QToolBar


ERROR_MSG = "ERROR"


'''
Shortcuts:

Ctrl+ñ = Quit
Ctrl+p = Change

'''

directory_carpeta = os.path.dirname(__file__)
ruta_save = os.path.join(directory_carpeta,"operaciones.txt")

class Calculadora(QMainWindow):
    def __init__(self, window2=None):
        super().__init__()
        
        self.setWindowTitle("Calculadora Normal")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #6e7d8a;")
        
        #Layout General
        self.generalLayout = QVBoxLayout()
        
        self._window2 = window2
    
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        #Toolbar para añadir el checkbox
        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        self.addToolBar(toolbar)
        
        #Alterna entre "Change_Cient" y "Change_Norm" para cambiar entre las dos calculadoras
        button_action = QAction("&Change_Cient", self)
        button_action.setShortcut('Ctrl+p')
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.changeWindow)
        
        #Si se presiona, se sale
        button_quit = QAction("Quit", self)
        button_quit.setShortcut('Ctrl+s')
        button_quit.setStatusTip("This is your button quit")
        button_quit.triggered.connect(self.quitApp)  
        #Menu
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&Calculadora")
        
        #SubMenu donde se añadira el QAction para cambiar entre calculadoras
        file_submenu = file_menu.addMenu("&Submenu")
        file_submenu.addAction(button_action)
        #Añadir el QAction Quit
        file_menu.addAction(button_quit)
        
        #CheckBox, si esta True entonces al presionar "=" guardara la operacion en un .txt
        self.save_check = QCheckBox("Checkbox")
        self.save_check.setStatusTip("Checkbox")
        toolbar.addWidget(self.save_check)
        #QLineEdit
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(100)
        self.display.setStyleSheet("font: 30px; background-color: #192733; color: white")
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)
        
        self.createButtons()
        self.connectButtons()

    def createButtons(self):
        self.buttons = {}
        layout_buttons = QGridLayout()
        # Creamos un diccionario con el texto y las coordenadas del Layout
        buttons_temp = {
            '√': (0, 0),
            'π': (0, 1),
            '**': (0, 2),
            'DELETE': (0, 3),
            '(': (1, 0),
            ')': (1, 1),
            '%': (1, 2),
            '/': (1, 3),
            '7': (2, 0),
            '8': (2, 1),
            '9': (2, 2),
            '*': (2, 3),
            '4': (3, 0),
            '5': (3, 1),
            '6': (3, 2),
            '+': (3, 3),
            '1': (4, 0),
            '2': (4, 1),
            '3': (4, 2),
            '-': (4, 3),
            '0': (5, 0),
            '.': (5, 1),
            'C': (5, 2),
            '=': (5, 3),
        }

        # Recorrer el diccionario de botones
        # Creando un boton en cada posición asignada
        for btn, pos in buttons_temp.items():
            self.buttons[btn] = QPushButton(btn)
            self.buttons[btn].setFixedSize(60, 38)
            self.buttons[btn].setStyleSheet("background-color: #192733; color: white")
            self.buttons[btn].setShortcut(btn)
            layout_buttons.addWidget(self.buttons[btn], pos[0], pos[1])  # Añadimos el boton con su posición

        # Añadimos el layout de botones al layout principal
        self.generalLayout.addLayout(layout_buttons)
        
    def connectButtons(self):
        # Recorre dict y utiliza la señal connect
        for text, boto in self.buttons.items():
            if text not in {"=", "C", "DELETE"}:
                boto.clicked.connect(partial(self.evaluateExpression, text))
        # Excepciones
        self.buttons["="].clicked.connect(self.calculateResult)
        self.display.returnPressed.connect(self.calculateResult)
        self.buttons["C"].clicked.connect(self.clearDisplay)
        self.buttons["DELETE"].clicked.connect(self.deleteOneChar)
    
    # Deja pantalla en blanco
    def clearDisplay(self):
        self.display.setText("")

    # Elimina carácter
    def deleteOneChar(self):
        self.display.setText(self.display.text()[:-1])

    # El boton que pulsemos se añade a la linea con el anterior
    def evaluateExpression(self, prev):
        if self.display.text() == "ERROR":
            self.clearDisplay()
        exp = self.display.text() + prev
        self.display.setText(exp)
        
    #Devuelve el estado del checkbox
    def saveStatus(self):
        return self.save_check.isChecked()
    
    # Envía el texto a la funcion evaluate y el resultado se muestra por pantalla
    def calculateResult(self):
        result = self.evaluate(self.display.text())
        total = self.display.text()+"="+result
        self.display.setText(total)
        with open (ruta_save, "a") as f:
            if self.saveStatus():  
                f.write(total)
                f.write("\n")
    # Pasado el parámetro hace un eval de este
    def evaluate(self, expression):
        try:
            res = str(eval(expression))
        except Exception:
            res = "ERROR"
        return res
    
    def quitApp(self):
        self.close()

    def changeWindow(self):
        self.hide()
        if self._window2 is None:
            self._window2 = CalculadoraCient(self)
        self._window2.show()
                 
    
def evaluateExpression(expression):
    """Evaluate an expression."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result

class CalculadoraCient(QMainWindow):
    def __init__(self, window1=None):
        super().__init__()
        
        self.setWindowTitle("Calculadora Normal")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #6e7d8a;")
        
        #Layout General
        self.generalLayout = QVBoxLayout()
        
        self._window1 = window1
    
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        #Toolbar para añadir el checkbox
        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        self.addToolBar(toolbar)
        
        #Alterna entre "Change_Cient" y "Change_Norm" para cambiar entre las dos calculadoras
        button_action = QAction("&Change_Cient", self)
        button_action.setShortcut('Ctrl+p')
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.changeWindow)
        #Si se presiona, se sale
        button_quit = QAction("Quit", self)
        button_quit.setShortcut('Ctrl+s')
        button_quit.setStatusTip("This is your button quit")
        button_quit.triggered.connect(self.quitApp)  
        #Menu
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&Calculadora")
        
        #SubMenu donde se añadira el QAction para cambiar entre calculadoras
        file_submenu = file_menu.addMenu("Submenu")
        file_submenu.addAction(button_action)
        #Añadir el QAction Quit
        file_menu.addAction(button_quit)
        
        #CheckBox, si esta True entonces al presionar "=" guardara la operacion en un .txt
        self.save_check = QCheckBox("Checkbox")
        self.save_check.setStatusTip("Checkbox")
        toolbar.addWidget(self.save_check)
        #QLineEdit
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(100)
        self.display.setStyleSheet("font: 30px; background-color: #192733; color: white")
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)
        
        self.createButtons()
        self.connectButtons()

    def createButtons(self):
        self.buttons = {}
        layout_buttons = QGridLayout()
        # Creamos un diccionario con el texto y las coordenadas del Layout
        buttons_temp = {
            '√': (0, 0),
            'π': (0, 1),
            '**': (0, 2),
            'DELETE': (0, 3),
            'log': (0, 4),
            '(': (1, 0),
            ')': (1, 1),
            '%': (1, 2),
            '/': (1, 3),
            'ln': (1, 4),
            '7': (2, 0),
            '8': (2, 1),
            '9': (2, 2),
            '*': (2, 3),
            'n!': (2, 4),
            '4': (3, 0),
            '5': (3, 1),
            '6': (3, 2),
            '+': (3, 3),
            'e': (3, 4),
            '1': (4, 0),
            '2': (4, 1),
            '3': (4, 2),
            '-': (4, 3),
            'x/y': (4, 4),
            '0': (5, 0),
            '.': (5, 1),
            'C': (5, 2),
            '=': (5, 3),
            '|x|': (5, 4),
        }

        # Recorrer el diccionario de botones
        # Creando un boton en cada posición asignada
        for btn, pos in buttons_temp.items():
            self.buttons[btn] = QPushButton(btn)
            self.buttons[btn].setFixedSize(55, 35)
            self.buttons[btn].setStyleSheet("background-color: #192733; color: white")
            self.buttons[btn].setShortcut(btn)
            layout_buttons.addWidget(self.buttons[btn], pos[0], pos[1])  # Añadimos el boton con su posición

        # Añadimos el layout de botones al layout principal
        self.generalLayout.addLayout(layout_buttons)
        
    def connectButtons(self):
        # Recorre dict y utiliza la señal connect
        for text, boto in self.buttons.items():
            if text not in {"=", "C", "DELETE"}:
                boto.clicked.connect(partial(self.evaluateExpression, text))
        # Excepciones
        self.buttons["="].clicked.connect(self.calculateResult)
        self.display.returnPressed.connect(self.calculateResult)
        self.buttons["C"].clicked.connect(self.clearDisplay)
        self.buttons["DELETE"].clicked.connect(self.deleteOneChar)
    
    # Deja pantalla en blanco
    def clearDisplay(self):
        self.display.setText("")

    # Elimina carácter
    def deleteOneChar(self):
        self.display.setText(self.display.text()[:-1])

    # El boton que pulsemos se añade a la linea con el anterior
    def evaluateExpression(self, prev):
        if self.display.text() == "ERROR":
            self.clearDisplay()
        exp = self.display.text() + prev
        self.display.setText(exp)

    def saveStatus(self):
        return self.save_check.isChecked()
    # Envía el texto a la funcion evaluate y el resultado se muestra por pantalla
    def calculateResult(self):
        result = self.evaluate(self.display.text())
        total = self.display.text()+"="+result
        self.display.setText(total)
        with open (ruta_save, "a") as f:
            if self.saveStatus():  
                f.write(total)
                f.write("\n")
                

    # Pasado el parámetro hace un eval de este
    def evaluate(self, expression):
        try:
            res = str(eval(expression))
        except Exception:
            res = "ERROR"
        return res
    
    def quitApp(self):
        self.close()

    def changeWindow(self):
        self.hide()
        if self._window1 is None:
            self._window1 = Calculadora(self)
        self._window1.show()


app = QApplication(sys.argv)
window = Calculadora()
window.show()
app.exec()