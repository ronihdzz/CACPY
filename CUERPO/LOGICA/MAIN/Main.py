from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox, QAction, QActionGroup, QWidget, QVBoxLayout, QTabWidget, QLabel, QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QCompleter

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal  # mandas senales a la otra ventana

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QApplication, QSpinBox, QActionGroup,
                             QLabel, QWidget, QPushButton, QVBoxLayout, QScrollArea, QMessageBox, QStackedWidget)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.Qt import QSizePolicy, Qt
from PyQt5 import QtCore

###############################################################
#  IMPORTACION DEL LOGICA...
##############################################################
from CUERPO.LOGICA.TAREA.TareaMain import TareaMain
from CUERPO.LOGICA.PERFIL.PerfilMain import PerfilMain
from CUERPO.LOGICA.CONFIGURACION.ConfiguracionMain import ConfiguracionMain
from CUERPO.LOGICA.ALUMNO.AlumnoMain import AlumnoMain

from CUERPO.LOGICA.API.ClassRoomControl import ClassRoomControl
from CUERPO.LOGICA.API.AdministradorProgramasClassRoom import AdministradorProgramasClassRoom
from CUERPO.LOGICA.API.CalificadorConfiguracion import CalificadorConfiguracion
from CUERPO.LOGICA.API.BaseDatosLocal import BaseDatos_ClassRoomProgramas

from CUERPO.LOGICA.MAIN.DatosCreador import Dialog_datosCreador

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.MAIN.Main_d import Ui_MainWindow
import recursos


class Main(QtWidgets.QMainWindow, Ui_MainWindow, recursos.HuellaAplicacion):


    def __init__(self,baseDatosLocalClassRoom,classRoomControl,configuracionCalificador):
        '''
        Cuando un profesor abre la aplicación, se espera que ingrese los datos de los parametros, sin
        embargo pueden no ser obligatorios en caso de que sea la primera vez que el profesor abre
        la aplicacion.Una vez que el profesor abre la aplicacion este clase tiene como objetivo
        cargar todos los datos del classroom del profesor.

        Parametros:
            correo_profesor (str) : representa el correo electronico del profesor que quiere abrir
            el programa
            nombre_profesor (str): representa en nombre completo del profesor que quiere abrir
            el programa
            curso_id (str) : representa el id del ultimo curso que selecciono el profesor la ultima
            vez que cerro el programa
            topic_id (str): representan el id del ultimo topic que selecciono el profesor la ultima
            vez que cerro el programa
        '''


        QtWidgets.QMainWindow.__init__(self)
        recursos.HuellaAplicacion.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Se obtiene un objeto que permitira el manejo de la base de datos local
        # que almacenara los datos de classroom del profesor.
        self.baseDatosLocalClassRoomProgramas = baseDatosLocalClassRoom

        # Se obtiene un objeto que podra hacer consultas al classroom del profesor
        # que abrio la aplicacion
        self.elClassRoom_control = classRoomControl


        # esta instancia contiene todos los datos  que se necesitan para administrar la calificacion de  las tareas
        # de programación del profesor que inicia sesion en el programa
        self.configuracionCalificador = configuracionCalificador



        self.administradorProgramasClassRoom = AdministradorProgramasClassRoom(
            classroom_control=self.elClassRoom_control,
            configuracionCalificador=self.configuracionCalificador,
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoomProgramas
        )

        if self.configuracionCalificador.getIdApi_cursoClassroom()!=None:
            self.configuracionCalificador.curso_nombre=self.baseDatosLocalClassRoomProgramas.getNombre_curso(
                curso_id=self.configuracionCalificador.getIdApi_cursoClassroom()
            )

            if self.configuracionCalificador.getIdApi_topicClassroom()!=None:
                self.configuracionCalificador.topic_nombre =self.baseDatosLocalClassRoomProgramas.getNombre_topic(
                    curso_id=self.configuracionCalificador.getIdApi_cursoClassroom(),
                    topic_id=self.configuracionCalificador.getIdApi_topicClassroom()
                )


        # Creando la barra de navegacion
        self.crear_barraNavegacion()




        # Creando los diferentes apartados del programa:
        self.ventana_aplicacionPerfil = PerfilMain(profesor_correo=self.configuracionCalificador.getNombreProfesor(),
                                                   profesor_nombre=self.configuracionCalificador.getCorreoProfesor(),
                                                   profesor_imagenPerfil=recursos.App_Principal.FOTO_PERFIL_PROFESOR
                                                   )
        self.ventana_aplicacionPerfil.cargarPerfilProfesor()

        self.ventana_aplicacionConfiguracion = ConfiguracionMain(
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoomProgramas,
            classRoomControl=self.elClassRoom_control,
            configuracionCalificador=self.configuracionCalificador
        )

        self.ventana_aplicacionTareas = TareaMain(
            administradorProgramasClassRoom=self.administradorProgramasClassRoom,
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoomProgramas
        )
        self.ventana_aplicacionAlumnos = AlumnoMain(
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoomProgramas,
            classRoomControl=self.elClassRoom_control,
            configuracionCalificador=self.configuracionCalificador
        )

        self.ventanaDatosCreador = Dialog_datosCreador()


        # Agregando cada  apartados del programa a la list  widget
        self.listWidget.addWidget(self.ventana_aplicacionPerfil)
        self.listWidget.addWidget(self.ventana_aplicacionTareas)
        self.listWidget.addWidget(self.ventana_aplicacionAlumnos)
        self.listWidget.addWidget(self.ventana_aplicacionConfiguracion)

        # Conectando las QAction que creo la funcion 'crear_barraNavegacion()' con cada
        # respectiva parte de la aplicacion.

        self.accion_verApartadoPerfil.triggered.connect(self.mostrar_apartadoPerfil)
        self.accion_verApartadoTareas.triggered.connect(self.mostrar_apartadoTareas)
        self.accion_verApartadoAlumnos.triggered.connect(self.mostrar_apartadoAlumnos)
        self.accion_verApartadoConfiguracion.triggered.connect(self.mostrar_apartadoConfiguracion)
        self.accion_verInfoProgramador.triggered.connect(lambda: self.ventanaDatosCreador.show())

        # Contanto las señales de los diferentes apartados del programa
        self.ventana_aplicacionConfiguracion.senal_eligioTopic.connect(self.actuarAnteCambioTopic)
        self.ventana_aplicacionConfiguracion.senal_eligioUnCurso.connect(self.actuarAnteCambioCurso)
        self.ventana_aplicacionConfiguracion.senal_claseNbGrader_cambio.connect(self.actuarAnte_cambio_claseNbGrader)
        self.ventana_aplicacionTareas.senal_operacionCompleja.connect(self.actuarAnteEstado_operacionCompleja)

        self.ventana_aplicacionPerfil.senal_cerrarAplicacion.connect(self.cerrarPrograma)


        # Mostrando de forma default el el perfil del apartado del programa
        self.accion_verApartadoPerfil.trigger()
        self.ventana_aplicacionConfiguracion.cargarDatos()

        self.CERRAR_PROGRAMA=False

    def cerrarPrograma(self):
        self.CERRAR_PROGRAMA=True
        self.close()


    def actuarAnteEstado_operacionCompleja(self,estadoSenalCompleja):
        if estadoSenalCompleja==True:
            self.setEnabled(False)
        else:
            self.setEnabled(True)

    def actuarAnte_cambio_claseNbGrader(self):
        print("*"*100)
        print("CAMBIANDO CLASE NBGRADER...")
        self.administradorProgramasClassRoom.actualizar_nbGraderControl()


    def actuarAnteCambioCurso(self):
        print("ACTUANDO ANTE EL CAMBIO DE UNA CLASEEEEEEEE.................")
        self.ventana_aplicacionTareas.actuarCambioCurso()
        self.ventana_aplicacionAlumnos.actuarCambioCurso()





    def actuarAnteCambioTopic(self):
        self.ventana_aplicacionTareas.actuarCambioTopic()

    def mostrar_apartadoTareas(self):
        if self.configuracionCalificador.datosListosApartadoTareas():
            self.bel_nombreApartado.setText("Mis tareas")
            self.listWidget.setCurrentIndex(1)
        else:
            self.msg_elegirCurso_y_topic()
            self.accion_verApartadoConfiguracion.trigger()

    def mostrar_apartadoConfiguracion(self):
        self.bel_nombreApartado.setText("Mis configuraciones")
        self.listWidget.setCurrentIndex(3)

    def mostrar_apartadoPerfil(self):
        self.bel_nombreApartado.setText("Mi perfil")
        self.listWidget.setCurrentIndex(0)

    def mostrar_apartadoAlumnos(self):
        self.bel_nombreApartado.setText("Mis alumnos")
        self.listWidget.setCurrentIndex(2)

    def closeEvent(self, event):
        '''
        Cuando el usuario le de clic izquierdo sobre el boton de cerra el programa, el metodo
        que se llamara es este, el cual le preguntara al usuario si esta seguro de cerrar el
        programa, en caso de que su respuesta sea afirmativa se cerrara el programa.
        '''

        if self.CERRAR_PROGRAMA:
            event.accept()

        else:
            respuestaAfirmativa = self.msg_cerrarVentana()
            if respuestaAfirmativa:
                # respaldando los datos del  curso_id y topic_id de ser necesarios
                self.configuracionCalificador.respaldarDatosProfesor(recursos.App_Principal.ARCHIVO_DATOS_PROFESOR)
                self.configuracionCalificador.respaldarDatosSesion(recursos.App_Principal.ARCHIVO_TRABAJO_PROFESOR)
                event.accept()
            else:
                event.ignore()  # No saldremos del evento

####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################

    def msg_cerrarVentana(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Esta seguro que quieres\n"
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

    def msg_elegirCurso_y_topic(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Warning)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Para ver las tareas asignadas primero debes definir la clase de classroom,"
        mensaje += "el topic en donde se encuentran esas tareas, y la clase de NbGrader, para hacer ello "
        mensaje += "debes ir al apartado de 'configuracion' "
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()

################################################################################################################################
#  C R E A D O R E S :
################################################################################################################################
    def crear_barraNavegacion(self):
        '''
        Creara una toolbar la cual sera la barra de navegacion de la aplicacion.
        Este metodo creara 5 atributos de instancia:
            self.accion_VerApartadoPerfil
            self.accion_verApartadoTareas
            self.accion_verApartadoAlumnos
            self.accion_verApartadoConfiguracion
            self.accion_verInfoProgramador

        Cada una de ellas es un objeto de la clase 'QAction' y su funcion son ser
        el medio por el cual el profesor podra navegar por la aplicacion.
        '''


        toolbar = self.addToolBar('')


        # QtCore.Qt.BottomToolBarArea= toolbar ubicada abajo
        # Qt.LeftToolBarArea = toolbar ubicada en la parte izquierda
        self.addToolBar(QtCore.Qt.LeftToolBarArea, toolbar)


        toolbar.setStyleSheet(
            " *{background:#d8d8d8; border:none} QToolButton:checked {background-color:#94DCD3; border:none;  }"
        )

        # restringiendo  que la toolbar pueda ser movida por el usuario
        toolbar.setMovable(False)
        # establenciendo la horientacion de la tool bar
        toolbar.setOrientation(QtCore.Qt.Vertical)

        # restringiendo que el clic derecho sobre la toolbar pueda desaparecerla
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)


        toolbar.setIconSize(QtCore.QSize(35, 35))
        toolbar.setFixedWidth(60)

        # creando los QAction de la toolbar
        self.crear_acciones()


        toolbar.addWidget( self.get_separadorQAction() )

        toolbar.addAction(self.accion_verInfoProgramador)
        toolbar.addWidget(self.get_expansorWidget())

        toolbar.addAction(self.accion_verApartadoPerfil)
        toolbar.addSeparator()
        toolbar.addWidget(self.get_separadorQAction())

        toolbar.addAction(self.accion_verApartadoTareas)
        toolbar.addSeparator()
        toolbar.addWidget(self.get_separadorQAction())

        toolbar.addAction(self.accion_verApartadoAlumnos)
        toolbar.addSeparator()
        toolbar.addWidget(self.get_separadorQAction())

        toolbar.addAction(self.accion_verApartadoConfiguracion)
        toolbar.addSeparator()
        toolbar.addWidget(self.get_separadorQAction())

        toolbar.addWidget(self.get_expansorWidget())




    def crear_acciones(self):
        '''
        Creara 5 atributos de instancia que seran objetos de la clase 'QAction', el objetivo
        de estos 5 atributos de instancia es crear los medios por los cuales el profesor
        navegara por toda la interfaz grafica del programa

        '''

        # Creando los 'QAction' asi como asignandoles nombres y aparte iconos:
        self.accion_verApartadoPerfil = QAction(QIcon(":/main/IMAGENES/cuenta.png"), 'Perfil', self)
        self.accion_verApartadoTareas = QAction(QIcon(":/main/IMAGENES/tareas.png"), 'Tareas', self)
        self.accion_verApartadoAlumnos = QAction(QIcon(":/main/IMAGENES/estudiantes.png"), 'Alumnos', self)
        self.accion_verApartadoConfiguracion = QAction(QIcon(":/main/IMAGENES/configuraciones.png"), 'Configuraciones',
                                                       self)

        self.accion_verInfoProgramador = QAction(QIcon(":/main/IMAGENES/info_off.png"), 'Info programador', self)

        # Permitiendo que las 'QAction' puedan ser seleccionadas
        self.accion_verApartadoPerfil.setCheckable(True)
        self.accion_verApartadoTareas.setCheckable(True)
        self.accion_verApartadoAlumnos.setCheckable(True)
        self.accion_verApartadoConfiguracion.setCheckable(True)

        # Agrupando las acciones que permitiran al usuario alinear el texto de sus deberes,
        # con la finalidad de que solo una de las acciones  pueda ser seleccionada a la vez
        self.grupoAcciones = QActionGroup(self.accion_verApartadoPerfil)
        self.grupoAcciones.addAction(self.accion_verApartadoPerfil)
        self.grupoAcciones.addAction(self.accion_verApartadoTareas)
        self.grupoAcciones.addAction(self.accion_verApartadoAlumnos)
        self.grupoAcciones.addAction(self.accion_verApartadoConfiguracion)

    def get_separadorQAction(self):
        '''
        Retornara una instancia de la clase 'QLabel' con el objetivo de que este
        sirva como seperador entre los elementos que se colocan en la toolbar
        '''

        separadorQAction = QLabel()
        separadorQAction.setMinimumSize(10, 2)
        return separadorQAction

    def get_expansorWidget(self):
        '''
        Retornara una instancia de la clase 'QWidget' con la caracteristica
        peculiar de que este objeto donde se coloque ocupara todo el espacio
        horizontalmente, es decir si se coloca en la toolbar al principio,esto
        obligara a que todos los elementos de esta se recorran a la derecha,o
        si se coloca este objeto al ultimo en la toolbar este obligara que
        todos los elemento se recorran a la izquierda en la toolbar
        '''

        expansorWidget = QWidget()
        expansorWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return expansorWidget

