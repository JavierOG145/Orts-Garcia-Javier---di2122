import json
import os
import sqlite3
import sys
from sqlite3 import Error
from urllib.request import urlopen

from PySide6.QtCharts import (QChart, QChartView,
                              QLineSeries, QBarSet, QStackedBarSeries)
from PySide6.QtGui import QAction, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QComboBox,
    QListWidget, QToolBar, QCheckBox, QStatusBar

)

pueblos = "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=abebb88b-5867-42e3-a2f1-1202f3eda515&limit=542"

# Los enlaces de donde vamos a recojer los datos


directory_carpeta = os.path.dirname(__file__)
user_db = os.path.join(directory_carpeta, "user.db")
covid_comunidades = os.path.join("covid_ca.json")

try:
    sqliteConnection = sqlite3.connect(user_db)
    cursor = sqliteConnection.cursor()
except Error as error:
    print("Error conexion", error)


class AnotherWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QVBoxLayout()
        self.main = None
        self.user = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
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

    def exit(self):
        self.close()

    def toggle_window(self):

        usuario = self.user.text()  # User = user
        contrasenya = self.password.text()  # Password = 1234

        cursor.execute("""SELECT name,password FROM users
                        WHERE name=? AND password=?""", (usuario, contrasenya))

        result = cursor.fetchone()

        if result:
            self.error.setText("Credencials correctes")
            self.error.setStyleSheet("QLabel { color : red; }")
            print("Correct")
            self.main = MainWindow()
            self.main.show()
            self.close()
        else:
            self.error.setText("Credencials incorrectes")
            self.error.setStyleSheet("QLabel { color : red; }")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(700, 400)
        self.setWindowTitle("Aplicación COVID")

        # Layout General
        self.layout_general = QVBoxLayout()

        # Layout Botones cambiar tipos
        layout_botones = QHBoxLayout()

        # Layout Grafica + Lista
        layout_especifico = QHBoxLayout()

        # Layout Lista
        layout_list_totales = QVBoxLayout()

        # Creamos el menu
        self.menu = self.menuBar()
        option_menu = self.menu.addMenu("&Menu")

        # Creamos los QAction
        menu_button_logout = QAction("&Return", self)
        menu_button_logout.triggered.connect(self.logout_action)
        menu_button_logout.setStatusTip("Boton Return")

        menu_button_exit = QAction("&Exit", self)
        menu_button_exit.triggered.connect(self.exit)
        menu_button_exit.setStatusTip("Boton Exit")

        # Añadimos los QAction al Menu
        option_menu.addAction(menu_button_logout)
        option_menu.addAction(menu_button_exit)

        # Creamos los botones
        self.has_been_clicked = False  # Esta variable determinará si se ha pulsado algún botón, para así hacer una cosa u otra
        self.boton_totales_cv = QAction("Datos por Comunidad Autónoma")
        self.boton_totales_cv.triggered.connect(self.cambia_barras)
        self.boton_totales_cv.setStatusTip("Por CA")

        self.boton_evolucion_positivos = QAction("PCR+ totales")
        self.boton_evolucion_positivos.triggered.connect(self.condicion_1)
        self.boton_evolucion_positivos.triggered.connect(self.cambia_evo)
        self.boton_evolucion_positivos.setStatusTip("PCR+ por municipio")

        self.boton_evolucion_positivos_14 = QAction("PCR+ 14 días")
        self.boton_evolucion_positivos_14.triggered.connect(self.condicion_2)
        self.boton_evolucion_positivos_14.triggered.connect(self.cambia_evo)
        self.boton_evolucion_positivos_14.setStatusTip("PCR+ 14 dias por municipio")

        self.boton_evolucion_muertes = QAction("Defunciones")
        self.boton_evolucion_muertes.triggered.connect(self.condicion_3)
        self.boton_evolucion_muertes.triggered.connect(self.cambia_evo)
        self.boton_evolucion_muertes.setStatusTip("Muertes por municipio")

        # Creando el QChart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        # Creando el QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Creamos el comboBox de las provincias de la C.V.
        self.combo_ciudades = QComboBox()
        self.combo_ciudades.setVisible(False)
        self.combo_ciudades.setFixedWidth(200)
        self.combo_ciudades.addItem("Alacant")
        self.municipis_alacant = self.rellena_municipios_alacant()
        self.combo_ciudades.addItem("Castelló")
        self.municipis_castello = self.rellena_municipios_castello()
        self.combo_ciudades.addItem("València")
        self.municipis_valencia = self.rellena_municipios_valencia()

        self.combo_ciudades.currentIndexChanged.connect(self.index_changed)

        # Creamos la lista de los municipios
        self.lista_municipios = QListWidget()
        self.lista_municipios.addItems(self.municipis_alacant)
        self.lista_municipios.setMaximumHeight(800)
        self.lista_municipios.setFixedWidth(200)
        self.lista_municipios.setVisible(False)

        # CheckBox de inicio para C.Autonomas
        self.infectados_chx = QCheckBox("Infectados")
        self.vacunados_chx = QCheckBox("Vacunados")
        self.muertos_chx = QCheckBox("Defunciones")
        self.hosp_chx = QCheckBox("Hospitalizados")
        self.infectados_chx.setFixedWidth(200)
        self.vacunados_chx.setFixedWidth(200)
        self.muertos_chx.setFixedWidth(200)
        self.hosp_chx.setFixedWidth(200)

        # Lista de comunidades autónomas
        self.lista_ca = QListWidget()
        self.lista_ca.setMaximumHeight(800)
        self.lista_ca.setFixedWidth(200)
        # Añadimos elementos a la Lista
        self.anyade_ca()

        # Boton Submit
        self.boton_mostrar = QPushButton("Mostrar")
        self.boton_mostrar.setFixedWidth(200)
        self.boton_mostrar.clicked.connect(self.rellena_grafico)
        self.boton_mostrar.hide()

        self.boton_mostrar_ca = QPushButton("Mostrar CA")
        self.boton_mostrar_ca.setFixedWidth(200)
        self.boton_mostrar_ca.clicked.connect(self.grafico_barras)

        # Añadiendo los botones al layout de botones
        self.toolbar = QToolBar("Toolbar")
        self.addToolBar(self.toolbar)
        texto_ca = QLabel("Por comunidades: ")
        texto_ca.setStyleSheet("font: 15px; color: black; font-weight: bold")
        texto_pro = QLabel("Por provincias: ")
        texto_pro.setStyleSheet("font: 15px; color: black; font-weight: bold")
        self.toolbar.addWidget(texto_ca)
        self.toolbar.addAction(self.boton_totales_cv)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addWidget(texto_pro)
        self.toolbar.addAction(self.boton_evolucion_positivos)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_evolucion_positivos_14)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_evolucion_muertes)
        self.toolbar.addSeparator()

        # Añadimos los checkbox
        layout_list_totales.addWidget(self.infectados_chx)
        layout_list_totales.addWidget(self.vacunados_chx)
        layout_list_totales.addWidget(self.muertos_chx)
        layout_list_totales.addWidget(self.hosp_chx)

        # Añadimos la lista de provincias, la lista y los botones
        layout_list_totales.addWidget(self.combo_ciudades)
        layout_list_totales.addWidget(self.lista_municipios)
        layout_list_totales.addWidget(self.lista_ca)
        layout_list_totales.addWidget(self.boton_mostrar)
        layout_list_totales.addWidget(self.boton_mostrar_ca)

        # Añadimos la grafica y el layout list
        layout_especifico.addWidget(self.chart_view)

        self.text_infectados = QLabel("")
        self.text_infectados.setStyleSheet("font: 15px; color: black")
        self.text_vacunados = QLabel("")
        self.text_vacunados.setStyleSheet("font: 15px; color: black")
        self.text_bv = QLabel("Bienvenido")
        self.text_bv.setStyleSheet("font: 15px; color: black")
        self.text_morts = QLabel("")
        self.text_morts.setStyleSheet("font: 15px; color: black")
        self.text_hosp = QLabel("")
        self.text_hosp.setStyleSheet("font: 15px; color: black")
        self.layout_test = QVBoxLayout()
        self.layout_test.addWidget(self.text_infectados)
        self.layout_test.addWidget(self.text_vacunados)
        self.layout_test.addWidget(self.text_bv)
        self.layout_test.addWidget(self.text_morts)
        self.layout_test.addWidget(self.text_hosp)

        layout_especifico.addLayout(self.layout_test)
        layout_especifico.addLayout(layout_list_totales)
        self.setStatusBar(QStatusBar(self))

        self.setStatusBar(QStatusBar(self))
        self.mode = QLabel("Modo: Por comunidades")
        self.statusBar().addPermanentWidget(self.mode)

        self.grafico_barras_init()

        # Añadimos los layouts al layout general
        self.layout_general.addLayout(layout_botones)
        self.layout_general.addLayout(layout_especifico)

        widget = QWidget()
        widget.setLayout(self.layout_general)
        self.setCentralWidget(widget)

    def exit(self):
        self.close()

    def logout_action(self):
        self.w = AnotherWindow()
        self.w.show()
        self.close()

    # Función llamada cuando cambiamos la provincia
    def index_changed(self):
        if self.combo_ciudades.currentText() == "Alacant":
            self.lista_municipios.clear()
            self.lista_municipios.addItems(self.municipis_alacant)
        else:
            if self.combo_ciudades.currentText() == "Castelló":
                self.lista_municipios.clear()
                self.lista_municipios.addItems(self.municipis_castello)
            else:
                if self.combo_ciudades.currentText() == "València":
                    self.lista_municipios.clear()
                    self.lista_municipios.addItems(self.municipis_valencia)

    # Función que rellena los municipios de la provincia de Valencia
    def rellena_municipios_valencia(self):
        municipis_valencia = []
        response = urlopen(pueblos)
        data_json = json.loads(response.read())
        for i in data_json["result"]["records"]:
            if i.get('CodMunicipio') > 46000:
                municipis_valencia.append(i.get('Municipi'))
        return municipis_valencia

    # Función que rellena los municipios de la provincia de Valencia
    def rellena_municipios_castello(self):
        municipis_castello = []
        response = urlopen(pueblos)
        data_json = json.loads(response.read())
        for i in data_json["result"]["records"]:
            if i.get('CodMunicipio') in range(12000, 46000):
                municipis_castello.append(i.get('Municipi'))
        return municipis_castello

    # Función que rellena los municipios de la provincia de Valencia
    def rellena_municipios_alacant(self):
        municipis_alacant = []
        response = urlopen(pueblos)
        data_json = json.loads(response.read())
        for i in data_json["result"]["records"]:
            if i.get('CodMunicipio') in range(3000, 12000):
                municipis_alacant.append(i.get('Municipi'))
        return municipis_alacant

    def rellena_grafico(self):
        self.mode.setText("Modo: por municipios")
        url_04_01_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=c1f36903-bf2e-4a43-9cfd-5075b4a956c9&limit=542")
        url_28_01_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=6459ccbb-63e5-41f3-b99a-ae763f57303c&limit=542")
        url_25_02_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=bde095bb-05ff-42fe-8481-df133ca2281b&limit=542")
        url_25_03_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=d278e615-cc72-4494-8dcd-2fb59c6dd66d&limit=542")
        url_29_04_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=36d42040-b784-4559-931a-454807c802fa&limit=542")
        url_31_05_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=4829416f-4911-4a1f-88c1-75aa50581125&limit=542")
        url_28_06_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=217319b6-c7ae-4e2f-ac2f-a25d458e9b77&limit=542")
        url_29_07_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=3ce650d9-dc77-4cf2-b45b-9b1a709d7303&limit=542")
        url_30_08_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=93141f32-ef4e-416f-8a80-6b5f9f77aab8&limit=542")
        url_30_09_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=db85107c-cd9e-411f-bca9-4fe49ede079f&limit=542")
        url_28_10_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=e38e006f-0a5b-4c7b-b7e5-44c8bbaa79d7&limit=542")
        url_25_11_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=30d5e647-f5a6-4fd2-820c-b2819e4a6895&limit=542")
        url_30_12_2021 = urlopen(
            "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=14c5eb17-30cf-46e8-9564-7051a841c549&limit=542")
        # url_03_01_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=abebb88b-5867-42e3-a2f1-1202f3eda515&limit=542")
        # url_05_01_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=f4864e40-5268-459b-94fc-20318a7a246d&limit=542")
        # url_10_01_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=bfb666e8-db73-44b4-94ad-0bb79814bfe3&limit=542")
        # url_13_01_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=ebe4297b-2e7c-451f-b41d-98a706fb5039&limit=542")
        # url_17_01_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=ea02cc70-a2f0-4f8f-8d49-151c42f19437&limit=542")
        # url_20_01_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=9a00dd92-79b7-4f99-9355-c81764604a66&limit=542")
        # url_27_01_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=4729ab91-1004-46af-9d49-a4a775638125&limit=542")
        # url_31_01_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=5b53697f-4b2f-4e38-bffb-2786e2d04335&limit=542")
        # url_03_02_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=6dd17811-a4ac-41ab-8043-11b75168a1c8&limit=542")
        # url_07_02_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=fa7915b6-9df8-454d-96a9-c88d9c0be721&limit=542")
        # url_10_02_2022 = urlopen(
        #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=847815c9-27ab-4dbd-b935-087425488ffd&limit=542")
        # url_14_02_2022 = urlopen(
        #     "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=7fd9a2bf-ffee-4604-907e-643a8009b04e&limit=542")
        # url_17_02_2022 = urlopen(
        #     "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=7968883a-2329-4c26-8304-83f19ec54ab1&limit=542")
        # urls = [url_04_01_2021, url_28_01_2021, url_25_02_2021, url_25_03_2021, url_29_04_2021, url_31_05_2021,
        #         url_28_06_2021, url_29_07_2021, url_30_08_2021, url_30_09_2021, url_28_10_2021, url_25_11_2021,
        #         url_30_12_2021,
        #         url_03_01_2022, url_05_01_2022, url_10_01_2022, url_13_01_2022,
        #         url_17_01_2022,
        #         url_20_01_2022, url_27_01_2022, url_31_01_2022, url_03_02_2022,
        #         url_07_02_2022, url_10_02_2022, url_14_02_2022, url_17_02_2022]

        urls = [url_04_01_2021, url_28_01_2021, url_25_02_2021, url_25_03_2021, url_29_04_2021, url_31_05_2021,
                url_28_06_2021, url_29_07_2021, url_30_08_2021, url_30_09_2021, url_28_10_2021, url_25_11_2021,
                url_30_12_2021]
        municipi = self.lista_municipios.currentItem().text()

        self.chart.removeAllSeries()
        series = QLineSeries()
        z = 0
        for x in urls:
            data_json = json.loads(x.read())
            for url in data_json["result"]["records"]:
                if url.get('Municipi') == municipi:
                    caso = url.get(self.condicion)
                    z += 1
                    series.append(z, float(caso))
        self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        self.chart.setTitle(self.condicion + " de " + self.lista_municipios.currentItem().text())
        self.chart.legend().hide()

    def rellena_grafico_init(self):
        self.mode.setText("Modo: por municipios")
        if not self.has_been_clicked:
            url_04_01_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=c1f36903-bf2e-4a43-9cfd-5075b4a956c9&limit=542")
            url_28_01_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=6459ccbb-63e5-41f3-b99a-ae763f57303c&limit=542")
            url_25_02_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=bde095bb-05ff-42fe-8481-df133ca2281b&limit=542")
            url_25_03_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=d278e615-cc72-4494-8dcd-2fb59c6dd66d&limit=542")
            url_29_04_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=36d42040-b784-4559-931a-454807c802fa&limit=542")
            url_31_05_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=4829416f-4911-4a1f-88c1-75aa50581125&limit=542")
            url_28_06_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=217319b6-c7ae-4e2f-ac2f-a25d458e9b77&limit=542")
            url_29_07_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=3ce650d9-dc77-4cf2-b45b-9b1a709d7303&limit=542")
            url_30_08_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=93141f32-ef4e-416f-8a80-6b5f9f77aab8&limit=542")
            url_30_09_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=db85107c-cd9e-411f-bca9-4fe49ede079f&limit=542")
            url_28_10_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=e38e006f-0a5b-4c7b-b7e5-44c8bbaa79d7&limit=542")
            url_25_11_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=30d5e647-f5a6-4fd2-820c-b2819e4a6895&limit=542")
            url_30_12_2021 = urlopen(
                "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=14c5eb17-30cf-46e8-9564-7051a841c549&limit=542")
            # url_03_01_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=abebb88b-5867-42e3-a2f1-1202f3eda515&limit=542")
            # url_05_01_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=f4864e40-5268-459b-94fc-20318a7a246d&limit=542")
            # url_10_01_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=bfb666e8-db73-44b4-94ad-0bb79814bfe3&limit=542")
            # url_13_01_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=ebe4297b-2e7c-451f-b41d-98a706fb5039&limit=542")
            # url_17_01_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=ea02cc70-a2f0-4f8f-8d49-151c42f19437&limit=542")
            # url_20_01_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=9a00dd92-79b7-4f99-9355-c81764604a66&limit=542")
            # url_27_01_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=4729ab91-1004-46af-9d49-a4a775638125&limit=542")
            # url_31_01_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=5b53697f-4b2f-4e38-bffb-2786e2d04335&limit=542")
            # url_03_02_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=6dd17811-a4ac-41ab-8043-11b75168a1c8&limit=542")
            # url_07_02_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=fa7915b6-9df8-454d-96a9-c88d9c0be721&limit=542")
            # url_10_02_2022 = urlopen(
            #     "https://dadesobertes.gva.es/api/3/action/datastore_search?resource_id=847815c9-27ab-4dbd-b935-087425488ffd&limit=542")
            # url_14_02_2022 = urlopen(
            #     "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=7fd9a2bf-ffee-4604-907e-643a8009b04e&limit=542")
            # url_17_02_2022 = urlopen(
            #     "https://dadesobertes.gva.es/va/api/3/action/datastore_search?resource_id=7968883a-2329-4c26-8304-83f19ec54ab1&limit=542")
            # urls = [url_04_01_2021, url_28_01_2021, url_25_02_2021, url_25_03_2021, url_29_04_2021, url_31_05_2021,
            #         url_28_06_2021, url_29_07_2021, url_30_08_2021, url_30_09_2021, url_28_10_2021, url_25_11_2021,
            #         url_30_12_2021,
            #         url_03_01_2022, url_05_01_2022, url_10_01_2022, url_13_01_2022,
            #         url_17_01_2022,
            #         url_20_01_2022, url_27_01_2022, url_31_01_2022, url_03_02_2022,
            #         url_07_02_2022, url_10_02_2022, url_14_02_2022, url_17_02_2022]
            urls = [url_04_01_2021, url_28_01_2021, url_25_02_2021, url_25_03_2021, url_29_04_2021, url_31_05_2021,
                    url_28_06_2021, url_29_07_2021, url_30_08_2021, url_30_09_2021, url_28_10_2021, url_25_11_2021,
                    url_30_12_2021]

            self.chart.removeAllSeries()
            series = QLineSeries()
            z = 0
            for x in urls:
                data_json = json.loads(x.read())
                for url in data_json["result"]["records"]:
                    if url.get('Municipi') == "Adsubia":
                        caso = url.get(self.condicion)
                        z += 1
                        series.append(z, float(caso))
            self.chart.addSeries(series)
            self.chart.createDefaultAxes()
            self.chart.setTitle((self.condicion + " de Adsubia"))
            self.chart.legend().hide()
            self.has_been_clicked = True
        else:
            self.rellena_grafico()

    def grafico_barras(self):
        self.mode = QLabel("Modo: Por comunidades")
        self.chart.removeAllSeries()
        self.text_infectados.setText("")
        self.text_vacunados.setText("")
        self.text_bv.setText("")
        self.text_morts.setText("")
        self.text_hosp.setText("")

        self.info_municipio = ""
        self.info_infectados = ""
        self.info_vacunados = ""
        self.info_defunciones = ""
        self.info_hospitalizados = ""

        infectados_barra = QBarSet("Infectados")
        vacunados_barra = QBarSet("Vacunados")
        muertos_barra = QBarSet("Defunciones")
        hosp_barra = QBarSet("Hospitalizados")

        data = open(covid_comunidades)
        data_json = json.load(data)

        for i in data_json["comunidades"]:
            self.info_municipio = self.lista_ca.currentItem().text()
            if i.get('name') == self.lista_ca.currentItem().text():

                if self.infectados_chx.isChecked():
                    infectados_barra.append([i.get('infectados')])
                    self._bar_series = QStackedBarSeries()
                    self._bar_series.append(infectados_barra)
                    self.chart.addSeries(self._bar_series)
                    self.chart.createDefaultAxes()
                    self.info_infectados = i.get('infectados')
                    self.text_vacunados.setText("Infectados: " + str(self.info_infectados))
                if self.vacunados_chx.isChecked():
                    vacunados_barra.append([i.get('vacunados')])
                    self._bar_series = QStackedBarSeries()
                    self._bar_series.append(vacunados_barra)
                    self.chart.addSeries(self._bar_series)
                    self.chart.createDefaultAxes()
                    self.info_vacunados = i.get('vacunados')
                    self.text_bv.setText("Vacunados: " + str(self.info_vacunados))
                if self.muertos_chx.isChecked():
                    muertos_barra.append([i.get('defunciones')])
                    self._bar_series = QStackedBarSeries()
                    self._bar_series.append(muertos_barra)
                    self.chart.addSeries(self._bar_series)
                    self.chart.createDefaultAxes()
                    self.info_defunciones = i.get('defunciones')
                    self.text_morts.setText("Defunciones: " + str(self.info_defunciones))
                if self.hosp_chx.isChecked():
                    hosp_barra.append([i.get('hospitalizados')])
                    self._bar_series = QStackedBarSeries()
                    self._bar_series.append(hosp_barra)
                    self.chart.addSeries(self._bar_series)
                    self.chart.createDefaultAxes()
                    self.info_hospitalizados = i.get('hospitalizados')
                    self.text_hosp.setText("Hospitalizados: " + str(self.info_hospitalizados))
                self.text_infectados.setText("Ciudad: " + str(self.info_municipio))

        self.chart.setTitle("Total " + self.lista_ca.currentItem().text())

    def grafico_barras_init(self):
        self.mode.setText("Modo: por comunidades")
        self.chart.removeAllSeries()

        infectados_barra = QBarSet("Infectados")
        vacunados_barra = QBarSet("Vacunados")
        muertos_barra = QBarSet("Defunciones")
        hosp_barra = QBarSet("Hospitalizados")

        data = open(covid_comunidades)
        data_json = json.load(data)

        for i in data_json["comunidades"]:
            if i.get('name') == "Espanya":
                infectados_barra.append([i.get('infectados'), 0, 0, 0])
                positivos = i.get('infectados')
                self.texto_info = (str(positivos) + " Positivos")
                vacunados_barra.append([0, i.get('vacunados'), 0, 0])
                muertos_barra.append([0, 0, i.get('defunciones'), 0])
                hosp_barra.append([0, 0, 0, i.get('hospitalizados')])

        self._bar_series = QStackedBarSeries()
        self._bar_series.append(infectados_barra)
        self._bar_series.append(vacunados_barra)
        self._bar_series.append(muertos_barra)
        self._bar_series.append(hosp_barra)

        self.chart.addSeries(self._bar_series)
        self.chart.setTitle("Total España")

        self.chart.createDefaultAxes()

    # Función que añade las Comunidades Autónomas a la lista
    def anyade_ca(self):
        ca = []
        data = open(covid_comunidades)
        data_json = json.load(data)
        for i in data_json["comunidades"]:
            ca.append(i.get('name'))
            self.lista_ca.addItem(i.get('name'))

    def cambia_barras(self):
        self.grafico_barras()
        self.infectados_chx.show()
        self.vacunados_chx.show()
        self.muertos_chx.show()
        self.hosp_chx.show()
        self.lista_ca.show()
        self.boton_mostrar_ca.show()
        self.text_infectados.show()
        self.text_vacunados.show()
        self.text_bv.show()
        self.text_morts.show()
        self.text_hosp.show()
        self.combo_ciudades.hide()
        self.lista_municipios.hide()
        self.boton_mostrar.hide()

    def cambia_evo(self):
        self.mode.setText("Modo: por municipios")
        self.rellena_grafico_init()
        self.infectados_chx.hide()
        self.vacunados_chx.hide()
        self.muertos_chx.hide()
        self.hosp_chx.hide()
        self.lista_ca.hide()
        self.text_infectados.hide()
        self.text_vacunados.hide()
        self.text_bv.hide()
        self.text_morts.hide()
        self.text_hosp.hide()

        self.boton_mostrar_ca.hide()
        self.combo_ciudades.show()
        self.lista_municipios.show()
        self.boton_mostrar.show()

    def condicion_1(self):
        self.condicion = "Casos PCR+"

    def condicion_2(self):
        self.condicion = "Casos PCR+ 14 dies"

    def condicion_3(self):
        self.condicion = "Defuncions"


app = QApplication(sys.argv)
w = AnotherWindow()
w.show()
app.exec()
