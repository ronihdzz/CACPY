
class App_Principal():

    # Contiene los datos cada uno separado por un salto de linea
    # correo del profesor, nombre completo del profesor
    ARCHIVO_DATOS_PROFESOR="CUERPO/RECURSOS/PROFESOR_EN_CURSO/archivo_datos_profesor.txt"

    # Contiene los datos cada uno separado por un salto de linea
    # curso_id, topic_id
    ARCHIVO_TRABAJO_PROFESOR="CUERPO/RECURSOS/PROFESOR_EN_CURSO/archivo_trabajo_profesor.txt"

    FOTO_PERFIL_PROFESOR="CUERPO/RECURSOS/PROFESOR_EN_CURSO/fotoProfesor.png"


    ICONO_APLICACION =":/main/IMAGENES/ICONO/RoniHernandez_CalificadorAutomatico_64.png"
    NOMBRE_APLICACION ="RoniHernandez99/CalificadorAutomatico"
    IMAGEN_SPLASH_SCREEN =":/main/IMAGENES/ICONO/RoniHernandez_CalificadorAutomatico_512.png"


    NOMBRE_ARCHIVO_LOG ='depuracionPrograma.log'

    @classmethod
    def actualizarUbicaciones(cls ,ubicacion):
        cls.ARCHIVO_DATOS_PROFESOR=ubicacion + cls.ARCHIVO_DATOS_PROFESOR
        cls.ARCHIVO_TRABAJO_PROFESOR=ubicacion+cls.ARCHIVO_TRABAJO_PROFESOR
        cls.FOTO_PERFIL_PROFESOR=ubicacion+ cls.FOTO_PERFIL_PROFESOR


class App_datosCreador():

    NOMBRE_PROGRAMADOR ="Roni Hernández"


    LIKEDIN_NOMBRE ="Roni Hernández"
    LIKEDIN_LINK ="https://www.linkedin.com/in/roni-hern%C3%A1ndez-613a62173/"

    GITHUB_NOMBRE ="RoniHernandez99"
    GITHUB_LINK ="https://github.com/RoniHernandez99"

    REPOSITORIO_PROYECTO_NOMBRE ="CalificadorAutomatico"
    REPOSITORIO_PROYECTO_LINK ="https://github.com/RoniHernandez99"

    FOTO_PROGRAMADOR=":/main/IMAGENES/ICONO/programador.jpg"

    # Datos del mensaje que se mandaria al programador
    GMAILS=["ronaldo.runing.r@gmail.com","ronaldo.runing_@hotmail.com"]
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


