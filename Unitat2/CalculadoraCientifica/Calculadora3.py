import sys
import os
from exitDialog import exitDialog
import fileDialog

from functools import partial
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QApplication, QGridLayout,
                               QLineEdit,QPushButton, QVBoxLayout, QWidget,
                               QStackedLayout, QStatusBar, QLabel )


ERROR_MSG = "ERROR"

directory_carpeta = os.path.dirname(__file__)
ruta_save = os.path.join(directory_carpeta,"operaciones.txt")

class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Calculadora Normal")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #6e7d8a;")
        
        
        self.widget = QWidget()
        self.setCentralWidget(self.widget)


        # Modo Normal
        self.Norm = QWidget()
        self.layout_estandar = QVBoxLayout(self.Norm)
        self.Norm.setLayout(self.layout_estandar)

        # Modo Cientifica
        self.Cient = QWidget()
        self.layout_cientifica = QVBoxLayout(self.Cient)
        self.Cient.setLayout(self.layout_cientifica)

        # StackedLayout para añadir ambos modos
        self.stackedLayout = QStackedLayout(self.widget)
        self.stackedLayout.addWidget(self.Norm)
        self.stackedLayout.addWidget(self.Cient)

        #QAction para cambiar a Normal
        button_norm = QAction("&Normal", self)
        button_norm.setShortcut('Ctrl+n')
        button_norm.setStatusTip("Boton Normal")
        button_norm.triggered.connect(self.mode_norm)
        
        #QAction para cambiar a Cientifica
        button_cient = QAction("&Cientifica", self)
        button_cient.setShortcut('Ctrl+c')
        button_cient.setStatusTip("Boton Cientifica")
        button_cient.triggered.connect(self.mode_cient)
        
        #QAction checkable para alternar entre modo guardado o no
        self.button_save = QAction("&Save", self)
        self.button_save.setShortcut('Ctrl+s')
        self.button_save.setStatusTip("Boton save")
        self.button_save.setCheckable(True)
        self.button_save.triggered.connect(self.buttonHistorial)
        
        #QAction para cerrar aplicacion
        button_quit = QAction("Quit", self)
        button_quit.setShortcut('Ctrl+q')
        button_quit.setStatusTip("Boton quit")
        button_quit.triggered.connect(self.quitApp)
        
        #QAction para navegar por los archivos
        '''
        self.button_archivos = QAction("Files", self)
        self.button_archivos.setShortcut('Ctrl+h')
        self.button_archivos.setCheckable(True)
        self.button_archivos.triggered.connect(self.buttonHistorial)
        '''

        
        #Menu
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&Menu")
        
        #SubMenu donde se añadiran los QActions modo Normal y Cientifica
        file_submenu = file_menu.addMenu("&Tipos")
        file_submenu.addAction(button_norm)
        file_submenu.addAction(button_cient)
        
        #Añadir el QAction Quit y Save al menu
        file_menu.addAction(self.button_save)
        file_menu.addAction(button_quit)
        #file_menu.addAction(self.button_archivos)
        
        # Status Bar        
        self.setStatusBar(QStatusBar(self))
        # Status Bar Widget para guardar el estado de la calculadora
        self.calc_mode = QLabel("Calc. Normal")
        self.calc_mode.setScaledContents(True)
        self.statusBar().addPermanentWidget(self.calc_mode)
        self.statusBar().addPermanentWidget(QLabel("|"))
        
        # Status Bar Widget para saber el estado del save
        self.files = QLabel("OFF")
        self.files.setScaledContents(True)
        self.statusBar().addPermanentWidget(self.files)

        # Variables
        self.guardados = ""
        self.result = ""
        self.total = ""

        # NORMAL --------------
        self.display_norm = QLineEdit()
        self.display_norm.setAlignment(Qt.AlignRight)
        self.display_norm.setFixedHeight(100)
        self.display_norm.setStyleSheet("font: 30px; background-color: #192733; color: white")
        self.display_norm.setReadOnly(True)
        self.layout_estandar.addWidget(self.display_norm)
        
        self.keyboards_norm= {}

        teclas_layout_norm = QGridLayout()
        
        keyboards_norm = {
            '√': (0, 0),'π': (0, 1),'**': (0, 2),'<-': (0, 3),
            '(': (1, 0),')': (1, 1),'%': (1, 2),'/': (1, 3),
            '7': (2, 0),'8': (2, 1),'9': (2, 2),'x': (2, 3),
            '4': (3, 0),'5': (3, 1),'6': (3, 2),'+': (3, 3),
            '1': (4, 0),'2': (4, 1),'3': (4, 2),'-': (4, 3),
            '0': (5, 0),'.': (5, 1),'C': (5, 2),'=': (5, 3),
        }
        
        for boton, posicion in keyboards_norm.items():
            self.keyboards_norm[boton] = QPushButton(boton)
            self.keyboards_norm[boton].setStyleSheet("background-color: #192733; color: white")
            self.keyboards_norm[boton].setFixedSize(60, 38)
            self.keyboards_norm[boton].setShortcut(boton)
            self.keyboards_norm[boton].setStatusTip(boton)

            teclas_layout_norm.addWidget(self.keyboards_norm[boton],posicion[0], posicion[1])
            self.keyboards_norm[boton].clicked.connect(self.operacion)
            
        self.layout_estandar.addLayout(teclas_layout_norm)
        self.keyboards_norm['='].clicked.connect(self.calculateResult)
        
        # CIENTIFICA -------------
        
        self.display_cient = QLineEdit()
        self.display_cient.setAlignment(Qt.AlignRight)
        self.display_cient.setFixedHeight(100)
        self.display_cient.setStyleSheet("font: 30px; background-color: #192733; color: white")
        self.display_cient.setReadOnly(True)
        self.layout_cientifica.addWidget(self.display_cient)

        self.keyboards_cient = {}
        
        teclas_layout_cient = QGridLayout()

        keyboards_cient = {
            '√': (0, 0),'π': (0, 1),'**': (0, 2),'<-': (0, 3), 'log': (0, 4),
            '(': (1, 0),')': (1, 1),'%': (1, 2),'/': (1, 3), 'ln': (1, 4),
            '7': (2, 0),'8': (2, 1),'9': (2, 2),'x': (2, 3), 'n!': (2, 4),
            '4': (3, 0),'5': (3, 1),'6': (3, 2),'+': (3, 3), 'e': (3, 4),
            '1': (4, 0),'2': (4, 1),'3': (4, 2),'-': (4, 3), 'x/y': (4, 4),
            '0': (5, 0),'.': (5, 1),'C': (5, 2),'=': (5, 3), '|x|': (5, 4),
        }

        for boton_c, posicion_c in keyboards_cient.items():
            self.keyboards_cient[boton_c] = QPushButton(boton_c)
            self.keyboards_cient[boton_c].setFixedSize(55, 35)
            self.keyboards_cient[boton_c].setStyleSheet("background-color: #192733; color: white")
            self.keyboards_cient[boton_c].setShortcut(boton_c)
            self.keyboards_cient[boton_c].setStatusTip(boton_c)
            teclas_layout_cient.addWidget(self.keyboards_cient[boton_c],posicion_c[0], posicion_c[1])
            self.keyboards_cient[boton_c].clicked.connect(self.operacion)
            
        self.layout_cientifica.addLayout(teclas_layout_cient)
        self.keyboards_cient['='].clicked.connect(self.calculateResult)

    # Cambia a modo normal
    def mode_norm(self):
        self.stackedLayout.setCurrentWidget(self.Norm)
        self.calc_mode.setText("Calculadora Normal")

    # Cambia a modo cientifica
    def mode_cient(self):
        self.stackedLayout.setCurrentWidget(self.Cient)
        self.calc_mode.setText("Calculadora Cientifica")
    
    def operacion(self):
        if (self.sender().text() == "="):
            pass
        elif (self.sender().text() == "<-"):
            self.refresh_display(self.guardados[:-1])
            self.guardados = self.guardados[:-1]
        elif (self.sender().text() == "C"):
            self.clearDisplay()
        elif (self.sender().text() == "x"):
            self.guardados += "*"
            self.refresh_display(self.guardados)
        else:
            self.guardados += self.sender().text()
            self.refresh_display(self.guardados)

    # Borra el String/Texto que se muestra en la ventana
    def clearDisplay(self):
        self.refresh_display("")
        self.guardados = ""

    # Calcula la operacion, si el QAction save esta True guardara la operacion en un .txt
    def calculateResult(self):
        try:
            self.result = str(eval(self.guardados))
            total = self.guardados + "=" + self.result
            self.refresh_display(total)
            with open (ruta_save, "a") as f:
                if self.status_save():  
                    f.write(total)
                    f.write("\n")
        except:
            self.refresh_display("ERROR")

    # Actualiza el display
    def refresh_display(self, text):
        self.display_norm.setText(text)
        self.display_cient.setText(text)

    # Cierra la aplicacion
    def quitApp(self,s):
        
        dlg = exitDialog()
        if dlg.exec():
            self.close()
        else:
            print("Cancelada la salida")
    
    def buttonHistorial(self):
        print("Historial")
        if self.button_save.isChecked():
            save_dlg = fileDialog.fileDialog(self)
            if save_dlg.exec():
                self.files.setText("ON")
            else:
                self.button_save.setChecked(False)

        else:
            self.files.setText("OFF")

    # Devuelve el estado del QAction save
    def status_save(self):
        return self.button_save.isChecked()

app = QApplication(sys.argv)
window = Calculadora()
window.show()
app.exec()