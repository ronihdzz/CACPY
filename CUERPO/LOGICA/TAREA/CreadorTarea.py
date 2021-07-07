from PyQt5 import QtWidgets
import sys
from os import getcwd
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QThread  # hilos

from PyQt5.QtWidgets import QDialog, QCompleter
from functools import partial

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QDoubleValidator,QRegExpValidator


###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.TAREA.CreadorTarea_d import Ui_Dialog

###############################################################
#  IMPORTACIONES DE LAS DEMAS VENTANAS LOGICAS...
##############################################################


class CreadorTareas(QtWidgets.QDialog, Ui_Dialog):
    # las siguientes constantes almacenan los nombres de las imagenes que cambiaran en función
    # del comportamiento de cada boton...


    IMAGEN_MAL = '''QPushButton{border-image:url(:/main/IMAGENES/tache_off.png);}
                  QPushButton:hover{ border-image:url(:/main/IMAGENES/tache_on.png);}
                  QPushButton:pressed{border-image:url(:/main/IMAGENES/tache_off.png);}'''
    IMAGEN_BIEN = '''QPushButton{border-image:url(:/main/IMAGENES/paloma_off.png);}
                  QPushButton:hover{ border-image:url(:/main/IMAGENES/paloma_on.png);}
                  QPushButton:pressed{border-image:url(:/main/IMAGENES/paloma_off.png);}'''

    TUPLA_RESOLUCION_DUDAS = (

        '''Restricciones:
Cada campo tiene sus propias restricciones, 
para poder verlas debes dar click en el 
boton que tiene forma de tache o  paloma,
este boton se encuentra a lado derecho de
cada campo.''',

        '''El nombre de usuario:
    -Solo puede ser una palabra.
    -Solo puede estar conformado de
    letras minusculas y numeros.
    -No debe coincidir con los 
    nombres ya existentes:''',

        '''La edad:
    -La edad minima que debes tener
    son 4 años.''',

        '''La contraseña:
    -Su unica restricción es que no 
    debe tener espacios en blanco.''',

        '''La repetición de contraseña:
    -Debe ser exactamente la misma que 
    la contraseña.'''
    )

    senalUsuarioSoloCerroVentana=pyqtSignal(bool)
    senalUsuarioCreoTarea=pyqtSignal(list)



    def __init__(self,listaNombresTareasYaCreadas):

        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        self.listaNombresTareasYaCreadas = listaNombresTareasYaCreadas

        self.agruparVariablesInstancia()
        self.conectarObjetos_conMetodos()
        self.restringirLasEntradas()


        self.USUARIO_SE_REGISTRO=False

#############################################################################################################################################
#        A C C I O N E S    F R E  C U E N  T E S :
#############################################################################################################################################

    def informar(self,idDuda):
        '''
        Lo que hace esta funcion es que en funcion del boton de estado que
        se oprima se mostrara la restriccion de su apartado...
        '''
        mensaje = self.TUPLA_RESOLUCION_DUDAS[idDuda]
        if idDuda==1: #si el id de la duda es del nombre de usuario
           mensaje+= ( "\n\t-" + "\n\t-".join(self.listaNombresTareasYaCreadas) )

        QMessageBox.information(self, 'bla bla bla ',mensaje,
                             QMessageBox.Ok)

    def validarEntradas(self, id_le):
        '''
        Lo que hara el siguiente metodo es validar los datos que el usuario ingresa
        cuando esta escribiendo, si los datos son correctos lo indicaremos con un
        booleano
        '''


        # ¿Lo que se modifico almenos tiene un dato?  ¿o.o?
        if self.dict_datosPediremos[id_le][0].text() != "":
            self.dict_datosPediremos[id_le][1] = True

            # Si el dato que se modifico fue el nombre pero ese nombre ya existe..
            # entonces...
            if self.dict_datosPediremos[id_le][0] == self.lineEdit_nombreTarea:  # si el dato que se esta modificando
                # es el nombre de usuario debemos preguntar
                # lo siguiente...
                if self.lineEdit_nombreTarea.text() in self.listaNombresTareasYaCreadas:
                    self.dict_datosPediremos[id_le][1] = False
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
                                    2: [self.lineEdit_urlSoloLectura, False],
                                    3: [self.lineEdit_idArchivo, False],
                                    4: [self.textEdit_indicaciones, False]
                                    }


    def conectarObjetos_conMetodos(self):
        # Si detecta algun cambio en el texto veremos si ya es el correcto...
        for x in tuple(self.dict_datosPediremos.keys()):
            self.dict_datosPediremos[x][0].textChanged.connect(partial(self.validarEntradas, x))

        # en funcion del boton estado que se presione mostraremos su respectivo mensaje...
        for x in tuple(self.dict_btnEstadoAviso.keys()):
            self.dict_btnEstadoAviso[x].clicked.connect(partial(self.informar, x))

        self.btn_asignarTarea.clicked.connect(self.terminarRegistro)


    def restringirLasEntradas(self):

        # validacion del nombre de la tarea...
        validator = QRegExpValidator(QRegExp("[0-9a-zA-Z_-]{1,20}"))  # maximo solo 20 caracteres
        self.lineEdit_nombreTarea.setValidator(validator)

        # validacion del link de acceso solo lectura..
        validator = QRegExpValidator(QRegExp("[^ ]{1,500}"))
        self.lineEdit_urlSoloLectura.setValidator(validator)
        self.lineEdit_idArchivo.setValidator(validator)


        self.textEdit_indicaciones.text=self.textEdit_indicaciones.toPlainText

        completer = QCompleter(self.listaNombresTareasYaCreadas)
        self.lineEdit_nombreTarea.setCompleter(completer)





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
                resultado = QMessageBox.question(self,'BLA BLA BLA ',
                                                 "¿Seguro que los datos proporcionados\n"
                                                 "son los datos correctos?",
                                                 QMessageBox.Yes | QMessageBox.No)
                if resultado == QMessageBox.Yes:
                    mensajeBienvenida = '''
    Felicidades, tu tarea ha sido registrada correctamente.'''
                    QMessageBox.information(self,'BLA BLA BLA ',
                                            mensajeBienvenida,
                                            QMessageBox.Ok)
                    self.USUARIO_SE_REGISTRO=True
                    self.close()

            else:
                mensajeError = '''El registro no se puede realizar porque:
    tienes errores en los datos requeridos.
    Por favor respeta las restricciones de 
    cada campo,si tienes dudas acerca de 
    cuales son, da click en el boton que
    tiene forma de tache o paloma, el cual
    se encuentra al lado derecho de cada 
    campo.'''
                QMessageBox.critical(self,'BLA BLA BLA',
                                     mensajeError,
                                     QMessageBox.Ok)


    def closeEvent(self, event):

        if self.USUARIO_SE_REGISTRO:
            nombreTarea=self.lineEdit_nombreTarea.text()
            urlSoloLectura=self.lineEdit_urlSoloLectura.text()
            idArchivoDrive=self.lineEdit_idArchivo.text()
            indicacionesTarea=self.textEdit_indicaciones.toPlainText()
            self.senalUsuarioCreoTarea.emit([nombreTarea,urlSoloLectura,idArchivoDrive,idArchivoDrive,indicacionesTarea])
            event.accept()

        else:

            mensage='''¿En verdad deseas salir?
Si sales tus datos ingresados 
se perderan'''
            resultado = QMessageBox.question(self,'BLA BLA BLA ',
                                             mensage,
                                             QMessageBox.Yes | QMessageBox.No)
            if resultado == QMessageBox.Yes:
                event.accept()
                self.senalUsuarioSoloCerroVentana.emit(True)
            else:
                event.ignore()  # No saldremos del evento


if __name__ == "__main__":
    # Cambiando de direcciones sus carpetas u archivos...
    app = QtWidgets.QApplication([])
    application = CreadorTareas(listaNombresTareasYaCreadas=["roni99","jorge","dilan"])
    application.show()
    sys.exit(app.exec())




