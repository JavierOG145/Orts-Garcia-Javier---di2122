import sys

from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget


ERROR_MSG = "ERROR"

class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Calculadora")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #6e7d8a;")
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        self._createDisplay()
        self._createButtons()
        self.parentesis = False

    def _createDisplay(self):

        self.display = QLineEdit()
        self.display.setStyleSheet("font: 30px; background-color: #192733; color: white")
        self.display.setFixedHeight(100)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        
        self.buttons = {}
        buttonsLayout = QGridLayout()
                
        buttons = {
            '√': (0, 0),
            'π': (0, 1),
            '^': (0, 2),
            '<-': (0, 3),
            '(': (1, 0),
            ')': (1, 1),
            '%': (1, 2),
            '/': (1, 3),
            '7': (2, 0),
            '8': (2, 1),
            '9': (2, 2),
            'x': (2, 3),
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
        
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(65, 46)
            self.buttons[btnText].setStyleSheet("background-color: #192733; color: white")
            
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):   
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):   
        self.setDisplayText("")
    
    def deleteOneChar(self):       
        line = self.display.text()     
        self.setDisplayText(line[:-1])
    
    #No esta conectado, por si el usuario quiere hacer parentesis dentro de otro
    def  parenthesis(self):
        line = self.display.text()
        if self.parentesis == False:
            self.setDisplayText(line+"(")
            self.parentesis = True

        elif self.parentesis == True:
            self.setDisplayText(line+")")
            self.parentesis = False
                
def evaluateExpression(expression):
    """Evaluate an expression."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG

    return result


# Create a Controller class to connect the GUI and the model
class PyCalcCtrl:
    """PyCalc's Controller."""

    def __init__(self, model, view):
        """Controller initializer."""
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    def _calculateResult(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        """Build expression."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {"=", "C","<-"}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons["C"].clicked.connect(self._view.clearDisplay)
        self._view.buttons["<-"].clicked.connect(self._view.deleteOneChar)
        #self._view.buttons["()"].clicked.connect(self._view.parenthesis)


# Client code
def main():
    """Main function."""
    # Create an instance of `QApplication`
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = Calculadora()
    view.show()
    # Create instances of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)
    # Execute calculator's main loop
    sys.exit(pycalc.exec_())


if __name__ == "__main__":
    main()