import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout
from PySide6.QtCore import *
import config

class MainWindow(QMainWindow):
    
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.setFixedSize(QSize(config.NORM_SCREEN_WIDTH, config.NORM_SCREEN_HEIGHT))
        self.setWindowTitle("Exemple signals-slots 1")
        
        

        self.MaxButton = QPushButton('Maximitza', self)
        self.MaxButton.setFixedSize(config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
        
        self.NorButton = QPushButton('Normalitza',self)
        self.NorButton.setFixedSize(config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
        
        self.MinButton = QPushButton('Minimitza',self)
        self.MinButton.setFixedSize(config.BUTTON_WIDTH, config.BUTTON_HEIGHT)   
        
        self.MaxButton.move((config.NORM_SCREEN_WIDTH/2)-(config.BUTTON_WIDTH*1.5),(config.NORM_SCREEN_HEIGHT/2)-(config.BUTTON_HEIGHT/2))
        self.NorButton.move((config.NORM_SCREEN_WIDTH/2)-(config.BUTTON_WIDTH/2),(config.NORM_SCREEN_HEIGHT/2)-(config.BUTTON_HEIGHT/2))
        self.MinButton.move((config.NORM_SCREEN_WIDTH/2)+(config.BUTTON_WIDTH/2),((config.NORM_SCREEN_HEIGHT/2)-(config.BUTTON_HEIGHT/2)))
        
        #Connectem la senyal clicked a la ranura button_pressed
        self.MaxButton.clicked.connect(self.Maxbutton_pressed) 
        self.NorButton.clicked.connect(self.Norbutton_pressed) 
        self.MinButton.clicked.connect(self.Minbutton_pressed) 

    def Maxbutton_pressed(self):
        print('Max Button Clicked')
        self.setFixedSize(QSize(config.MAX_SCREEN_WIDTH,config.MAX_SCREEN_HEIGHT))
        
        print(config.MAX_SCREEN_WIDTH)
        print(config.MAX_SCREEN_HEIGHT)
        self.MaxButton.setEnabled(False)
        self.NorButton.setEnabled(True)
        self.MinButton.setEnabled(True)
        self.MaxButton.move((config.MAX_SCREEN_WIDTH/2)-(config.BUTTON_WIDTH*1.5),(config.MAX_SCREEN_HEIGHT/2)-(config.BUTTON_HEIGHT/2))
        self.NorButton.move((config.MAX_SCREEN_WIDTH/2)-(config.BUTTON_WIDTH/2),(config.MAX_SCREEN_HEIGHT/2)-(config.BUTTON_HEIGHT/2))
        self.MinButton.move((config.MAX_SCREEN_WIDTH/2)+(config.BUTTON_WIDTH/2),(config.MAX_SCREEN_HEIGHT/2)-(config.BUTTON_HEIGHT/2))
        
        
    def Norbutton_pressed(self):
        print('Norm Button Clicked')
        self.setFixedSize(QSize(config.NORM_SCREEN_WIDTH,config.NORM_SCREEN_HEIGHT))
        
        print(config.NORM_SCREEN_WIDTH)
        print(config.NORM_SCREEN_HEIGHT)
        self.MaxButton.setEnabled(True)
        self.NorButton.setEnabled(False)
        self.MinButton.setEnabled(True)
        self.MaxButton.move((config.NORM_SCREEN_WIDTH/2)-(config.BUTTON_WIDTH*1.5),(config.NORM_SCREEN_HEIGHT/2)-(config.BUTTON_HEIGHT/2))
        self.NorButton.move((config.NORM_SCREEN_WIDTH/2)-(config.BUTTON_WIDTH/2),(config.NORM_SCREEN_HEIGHT/2)-(config.BUTTON_HEIGHT/2))
        self.MinButton.move((config.NORM_SCREEN_WIDTH/2)+(config.BUTTON_WIDTH/2),((config.NORM_SCREEN_HEIGHT/2)-(config.BUTTON_HEIGHT/2)))
        
    def Minbutton_pressed(self):
        print('Min Button Clicked')
        self.setFixedSize(QSize(config.MIN_SCREEN_WIDTH,config.MIN_SCREEN_HEIGHT))
        self.MaxButton.setEnabled(True)
        self.NorButton.setEnabled(True)
        self.MinButton.setEnabled(False)
                    
        self.MaxButton.move(0, 0)
        self.NorButton.move(120, 0)
        self.MinButton.move(240,0)
            
        #self.MaxButton.move((config.MIN_SCREEN_WIDTH/2)-180,(config.MIN_SCREEN_WIDTH/2)-50)
        #self.NorButton.move((config.MIN_SCREEN_WIDTH/2)-60,(config.MIN_SCREEN_WIDTH/2)-50)
        #self.MinButton.move((config.MIN_SCREEN_WIDTH/2)+60,(config.MIN_SCREEN_WIDTH/2)-50)

if __name__ == "__main__":
    app = QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec()