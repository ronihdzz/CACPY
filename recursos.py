import os
from PyQt5.QtWidgets import QMessageBox

class App_Principal():

    # Contiene los datos cada uno separado por un salto de linea
    # correo del profesor, nombre completo del profesor
    ARCHIVO_DATOS_PROFESOR="RECURSOS/PROFESOR_EN_CURSO/archivo_datos_profesor.txt"

    # Contiene los datos cada uno separado por un salto de linea
    # curso_id, topic_id
    ARCHIVO_TRABAJO_PROFESOR="RECURSOS/PROFESOR_EN_CURSO/archivo_trabajo_profesor.txt"

    FOTO_PERFIL_PROFESOR="RECURSOS/PROFESOR_EN_CURSO/fotoProfesor.jpg"

    NOMBRE_COMPLETO_BASE_DATOS='RECURSOS/baseDatos.db'

    NOMBRE_COMPLETO_TOKEN='RECURSOS/API/token.json'
    NOMBRE_COMPLETO_CREDENCIALES='RECURSOS/API/credentials.json'

    RUTA_NB_GRADER = "RECURSOS/NB_GRADER/"
    RUTA_CARPETA_RECURSOS="RECURSOS/"



    LEYENDA_SIN_CURSO_SELECCIONADO='Curso no seleccionado'
    COLOR_TOPIC_SELECCIONADO="#0DDEFF"
    COLOR_TOPIC_NO_SELECCIONADO="#EEF2F3"
    COLOR_TABLA_TOPICS="#F1DAF9"

    #self.COLOR_TABLA = "#EEF2F3"
    #self.COLOR_RESPUESTA = "#9AE5E0"
    COLOR_MALO = "#E22E1C"
    #self.COLOR_REGULAR = "#DCE21C"
    #self.COLOR_BUENO = "#1CE285"
    COLOR_EXCELENTE = "#0DDEFF"

    ICONO_APLICACION =":/main/IMAGENES/ICONO/RoniHernandez_CACPY_64.png"
    NOMBRE_APLICACION ="RoniHernandez99/CACPY"
    IMAGEN_SPLASH_SCREEN =":/main/IMAGENES/ICONO/RoniHernandez_CACPY_512.png"




    NOMBRE_ARCHIVO_LOG ='depuracionPrograma.log'


    @classmethod
    def actualizarUbicaciones(cls ,ubicacion):
        cls.RUTA_CARPETA_RECURSOS=ubicacion+'RECURSOS/'
        cls.ARCHIVO_DATOS_PROFESOR=ubicacion + cls.ARCHIVO_DATOS_PROFESOR
        cls.ARCHIVO_TRABAJO_PROFESOR=ubicacion+cls.ARCHIVO_TRABAJO_PROFESOR
        cls.FOTO_PERFIL_PROFESOR=ubicacion+ cls.FOTO_PERFIL_PROFESOR
        cls.RUTA_NB_GRADER=ubicacion+cls.RUTA_NB_GRADER
        cls.NOMBRE_COMPLETO_BASE_DATOS=ubicacion+cls.NOMBRE_COMPLETO_BASE_DATOS
        cls.NOMBRE_COMPLETO_TOKEN=ubicacion+cls.NOMBRE_COMPLETO_TOKEN
        cls.NOMBRE_COMPLETO_CREDENCIALES=ubicacion+cls.NOMBRE_COMPLETO_CREDENCIALES


    @classmethod
    def serciorarExistenciaCarpetaRecursos(cls):
        '''
        Si no existen las carpeta de los datos del profesor ni de los datos
        de la API, entonces se van a crear
        '''

        os.makedirs(cls.RUTA_CARPETA_RECURSOS+'PROFESOR_EN_CURSO/', exist_ok=True)
        os.makedirs(cls.RUTA_CARPETA_RECURSOS + 'API/', exist_ok=True)
        os.makedirs(cls.RUTA_CARPETA_RECURSOS + 'NB_GRADER/', exist_ok=True)

    @classmethod
    def borrarDatosSesionProfesor(cls):
        if os.path.isfile(cls.FOTO_PERFIL_PROFESOR):
            os.remove(cls.FOTO_PERFIL_PROFESOR)

        if os.path.isfile(cls.ARCHIVO_DATOS_PROFESOR):
            os.remove(cls.ARCHIVO_DATOS_PROFESOR)

        if os.path.isfile(cls.ARCHIVO_TRABAJO_PROFESOR):
            os.remove(cls.ARCHIVO_TRABAJO_PROFESOR)

        if os.path.isfile(cls.NOMBRE_COMPLETO_BASE_DATOS):
            os.remove(cls.NOMBRE_COMPLETO_BASE_DATOS)

        if os.path.isfile(cls.NOMBRE_COMPLETO_TOKEN):
            os.remove(cls.NOMBRE_COMPLETO_TOKEN)


class App_datosCreador():

    NOMBRE_PROGRAMADOR ="Roni Hernández"


    LIKEDIN_NOMBRE ="Roni Hernández"
    LIKEDIN_LINK ="https://www.linkedin.com/in/roni-hern%C3%A1ndez-613a62173/"

    GITHUB_NOMBRE ="RoniHernandez99"
    GITHUB_LINK ="https://github.com/RoniHernandez99"

    REPOSITORIO_PROYECTO_NOMBRE ="CACPY"
    REPOSITORIO_PROYECTO_LINK ="https://github.com/RoniHernandez99/CACPY"

    FOTO_PROGRAMADOR=":/main/IMAGENES/ICONO/programador.jpg"

    # Datos del mensaje que se mandaria al programador
    GMAILS=["roni.hernandez.1999@gmail.com"]
    GMAIL_SUBJECT=f"Comentarios acerca de: {REPOSITORIO_PROYECTO_NOMBRE}"
    GMAIL_CUERPO=f"Hola {NOMBRE_PROGRAMADOR} espero tengas un buen dia, el motivo del mensaje es:"

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
import textwrap

# class HuellaAplicacion(QtCore.QObject):
class HuellaAplicacion(QtCore.QObject):
    NOMBRE_APLICACION = App_Principal.NOMBRE_APLICACION
    ICONO_APLICACION = App_Principal.ICONO_APLICACION
    LONGITUD_ESTANDAR_MENSAJES_EMERGENTES=len('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')


    def __init__(self):
        # NO USAMOS EL CONSTRUCTOR DEL PADRE POR LO TANTO NO HACEMOS SUS CONFIGURACIONES DEFAULT
        self.dejarHuella()

    def dejarHuella(self):
        self.setWindowTitle(self.NOMBRE_APLICACION)
        self.setWindowIcon(QIcon(self.ICONO_APLICACION))

    def huellaAplicacion_ajustarMensajeEmergente(self,mensaje,extra=0):
        mensaje = textwrap.fill(mensaje, self.LONGITUD_ESTANDAR_MENSAJES_EMERGENTES+extra)
        return mensaje

    def ventanaEmergenteDe_pregunta(self,mensaje):

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton() == btn_yes:
            return True
        return False

    def ventanaEmergenteDe_informacion(self,mensaje):

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


    def ventanaEmergenteDe_advertencia(self,mensaje):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Warning)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()

    def ventanaEmergenteDe_error(self,mensaje):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Critical)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()









