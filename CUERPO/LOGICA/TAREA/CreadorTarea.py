

'''
CreadorTarea.py :
    Esta clase sirve para calificar las entregas que han realizado los alumnos del usuario
    y que pertenecen a la tarea seleccionada..
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# librerias estandar
###########################################################################################################################################

import sys


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal,QRegExp
from PyQt5.QtGui import QRegExpValidator
from functools import partial

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.DISENO.TAREA.CreadorTarea_d import Ui_Dialog
import recursos


class CreadorTareas(QtWidgets.QDialog, Ui_Dialog,recursos.HuellaAplicacion):
    # las siguientes constantes almacenan los nombres de las imagenes que cambiaran en función
    # del comportamiento de cada boton...


    IMAGEN_MAL = '''QPushButton{border-image:url(:/main/IMAGENES/tache_off.png);}
                  QPushButton:hover{ border-image:url(:/main/IMAGENES/tache_on.png);}
                  QPushButton:pressed{border-image:url(:/main/IMAGENES/tache_off.png);}'''
    IMAGEN_BIEN = '''QPushButton{border-image:url(:/main/IMAGENES/paloma_off.png);}
                  QPushButton:hover{ border-image:url(:/main/IMAGENES/paloma_on.png);}
                  QPushButton:pressed{border-image:url(:/main/IMAGENES/paloma_off.png);}'''

    TUPLA_RESOLUCION_DUDAS = (

        "Restricciones: cada campo tiene sus propias restricciones "
        "para poder verlas debes dar click en el  boton que tiene forma " 
        "de tache o  paloma, este boton se encuentra a lado derecho de "
        "cada campo.",

        "Recuerda que el nombre de la tarea: solo puede ser una palabra, "
        "solo puede estar conformado de letras minusculas y numeros y no debe " 
        "tener espacios en blanco",

        "Aqui debes inscrustar el link que se te adjunta cuando se desea "
        "compartir un google colab, cabe  mencionar que no importa que tipo " 
        "de permisos tenga el google colab, solo debes adjuntar el link.",

        "Aqui debes inscrutar el id del google colab, es importante mencionar "
        "que el id se encuentra dentro del link que incrustate en el apartado "
        "anterior.",

        "Por lo menos debes escribir una instruccion breve acerca de lo que lo " 
        "que trata la tarea que deseas adjuntar."
    )

    senalUsuarioSoloCerroVentana=pyqtSignal(bool)
    senalUsuarioCreoTarea=pyqtSignal(tuple)


    def __init__(self,administradorProgramasClassRoom):

        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)


        self.agruparVariablesInstancia()
        self.conectarObjetos_conMetodos()
        self.restringirLasEntradas()

        self.administradorProgramasClassRoom=administradorProgramasClassRoom
        self.USUARIO_SE_REGISTRO=False

#############################################################################################################################################
#        A C C I O N E S    F R E  C U E N  T E S :
#############################################################################################################################################


    def validarEntradas(self, id_le):
        '''
        Lo que hara el siguiente metodo es validar los datos que el usuario ingresa
        cuando esta escribiendo, si los datos son correctos lo indicaremos con un
        booleano
        '''


        # ¿Lo que se modifico almenos tiene un dato?  ¿o.o?
        if self.dict_datosPediremos[id_le][0].text() != "":
            self.dict_datosPediremos[id_le][1] = True

        else:
            self.dict_datosPediremos[id_le][1] = False


        if self.dict_datosPediremos[id_le][1]:
            self.dict_btnEstadoAviso[id_le].setStyleSheet(self.IMAGEN_BIEN)
        else:
            self.dict_btnEstadoAviso[id_le].setStyleSheet(self.IMAGEN_MAL)


#############################################################################################################################################
#         A G R U P A C I O  N  E S     D  E    L O S    A T R I B U T O S    Y   C O N E X I O  N  E S    :
#############################################################################################################################################
    def agruparVariablesInstancia(self):
        # La siguiente tupla almacena los mensajes de las restricciones de cada
        # campo:


        # El siguiente diccionario almacena los punteros de los objetos botones
        # que se encuentran a lado de cada seccion,esos botones son los
        # tienen imagen de tache o palomo. La finalidad del diccionario
        # es conectar todos los botones de una manera mas sencilla:
        self.dict_btnEstadoAviso = {
            0: self.btn_infoDudas,
            1: self.btn_info_nombre,
            2: self.btn_info_urlSoloLectura,
            3: self.btn_info_id_archivo,
            4: self.btn_info_indicaciones
        }

        # El siguiente diccionario almacena los line edit en donde el usuario
        # tiene que ingresar sus datos, y donde este puede tener una mal
        # sintaxis, por tal motivo cada value es una lista de un objeto line edit
        # y un booleano que indicara si es buena o mala su sintaxis
        # otra cosa que aclara es que su keys coincide con la key del su boton estado
        self.dict_datosPediremos = {1: [self.lineEdit_nombreTarea, False],
                                    2: [self.plainText_urlSoloLectura, False],
                                    3: [self.lineEdit_idArchivo, False],
                                    4: [self.textEdit_indicaciones, False]
                                    }


    def conectarObjetos_conMetodos(self):
        # Si detecta algun cambio en el texto veremos si ya es el correcto...
        for x in tuple(self.dict_datosPediremos.keys()):
            self.dict_datosPediremos[x][0].textChanged.connect(partial(self.validarEntradas, x))

        # en funcion del boton estado que se presione mostraremos su respectivo mensaje...
        for x in tuple(self.dict_btnEstadoAviso.keys()):
            self.dict_btnEstadoAviso[x].clicked.connect(partial(self.msg_informar, x))

        self.btn_asignarTarea.clicked.connect(self.terminarRegistro)


    def restringirLasEntradas(self):

        # validacion del nombre de la tarea...
        validator = QRegExpValidator(QRegExp("[0-9a-zA-Z_-]{1,30}"))  # maximo solo 20 caracteres
        self.lineEdit_nombreTarea.setValidator(validator)


        self.textEdit_indicaciones.text=self.textEdit_indicaciones.toPlainText
        self.plainText_urlSoloLectura.text=self.plainText_urlSoloLectura.toPlainText

 

#############################################################################################################################################
#      A C C I O N E S     F I N A L E S :
#############################################################################################################################################

    def terminarRegistro(self):
            datosCorrectos = True

            # Con que haya uno malo el resultado sera false...
            print("\n" * 4)
            for x in tuple(self.dict_datosPediremos.keys()):
                datosCorrectos *= self.dict_datosPediremos[x][1]
                print(f"{x} = {self.dict_datosPediremos[x][1]}")

            if datosCorrectos:
                resultado=self.msg_confirmacionDatosTarea()
                if resultado == True:
                    #################################################################
                    # CREANDO TRABAJO
                    ################################################################


                    titulo=self.lineEdit_nombreTarea.text()
                    descripccion=self.textEdit_indicaciones.toPlainText()
                    idTarea,fechaCreacion=self.administradorProgramasClassRoom.crearTarea(
                        titulo=titulo,
                        descripccion=descripccion,
                        colab_link=self.plainText_urlSoloLectura.toPlainText(),
                        colab_id=self.lineEdit_idArchivo.text(),
                    )

                    tuplaDatosMandar = (idTarea,titulo,fechaCreacion)
                    self.senalUsuarioCreoTarea.emit(tuplaDatosMandar)

                    self.msg_exitoCrearTarea()
                    self.USUARIO_SE_REGISTRO=True
                    self.close()

            else:
                self.msg_errorCrearTarea()

    def borrarTodo(self):
        self.lineEdit_nombreTarea.setText("")
        self.lineEdit_idArchivo.setText("")
        self.plainText_urlSoloLectura.setPlainText("")
        self.textEdit_indicaciones.setPlainText("")


    def closeEvent(self, event):

        if self.USUARIO_SE_REGISTRO:
            nombreTarea=self.lineEdit_nombreTarea.text()
            urlSoloLectura=self.plainText_urlSoloLectura.toPlainText()
            idArchivoDrive=self.lineEdit_idArchivo.text()
            indicacionesTarea=self.textEdit_indicaciones.toPlainText()
            self.borrarTodo()
            event.accept()

        else:
            
            resultado = self.msg_cerrarVentana()
            if resultado:
                event.accept()
                self.senalUsuarioSoloCerroVentana.emit(True)
            else:
                event.ignore()  # No saldremos del evento


##################################################################################################################################################
# MENSAJES
##################################################################################################################################################

    def msg_confirmacionDatosTarea(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Seguro que los datos proporcionados son los datos correctos?"
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


    def msg_cerrarVentana(self):
        '''
        Mostrara un cuadro de dialogo con el objetivo de: preguntarle el profesor
        si en realidad desea cerrar la aplicacion

        Returns:
            True : En caso de que el profesor presione el boton de 'Si'
            False: En caso de que el profesor presione el boton de 'No'
        '''
        
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Esta seguro que deseas salir de la aplicacion?"
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





    def msg_informar(self,idDuda):
        '''
        Lo que hace esta funcion es que en funcion del boton de estado que
        se oprima se mostrara la restriccion de su apartado...
        '''

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = self.TUPLA_RESOLUCION_DUDAS[idDuda]
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()

    def msg_exitoCrearTarea(self):
        
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje= "Felicidades, tu tarea ha sido registrada correctamente."
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()



    def msg_errorCrearTarea(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Critical)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje="El registro no se puede realizar porque:tienes "
        mensaje+="errores en los datos requeridos. Por favor respeta las "
        mensaje+="restricciones de  cada campo,si tienes dudas acerca de "
        mensaje+="cuales son, da click en el boton que tiene forma de tache " 
        mensaje+=" o paloma, el cual se encuentra al lado derecho de cada campo."

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()



if __name__ == "__main__":
    # Cambiando de direcciones sus carpetas u archivos...
    app = QtWidgets.QApplication([])
    application = CreadorTareas()
    application.show()
    sys.exit(app.exec())




