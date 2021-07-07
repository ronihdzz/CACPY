from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel,QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana





import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QApplication,QSpinBox,QActionGroup,
                             QLabel,QWidget,QPushButton, QVBoxLayout,QScrollArea,QMessageBox,QStackedWidget)
from PyQt5.QtGui import QIcon,QFont
from PyQt5.Qt import QSizePolicy,Qt
from PyQt5 import QtCore



###############################################################
#  IMPORTACION DEL LOGICA...
##############################################################
from CUERPO.LOGICA.TAREA.TareaMain import TareaMain
from CUERPO.LOGICA.PERFIL.PerfilMain import PerfilMain
from CUERPO.LOGICA.CONFIGURACION.ConfiguracionMain import ConfiguracionMain
from CUERPO.LOGICA.ALUMNO.AlumnoMain import AlumnoMain



###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.MAIN.Main_d import Ui_MainWindow


class Main(QtWidgets.QMainWindow,Ui_MainWindow):
    '''
    El objetivo de esta clase  sera mostrar todo el sistema que permite
    agregar deberes, eliminar los deberes cuando se cumplen,cambiar la posicion del texto de los deberes
    y cambiar el tamaño del texto de los deberes, por ello esta clase basicamente estara compuesta de
    una apartado en donde se mostraran todos los deberes a realizar  y unos botones que permitieran hacer
    lo mencionado anteriormente.
    '''

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)



        ##############################################################################################################
        # CONFIGURACIONES DE LA TOOL BAR
        toolbar = self.addToolBar('')

        #self.addToolBar(QtCore.Qt.Lef,toolbar)  # ubicando a la toolbar en la posicion  inferior de la widget
        self.addToolBar(QtCore.Qt.LeftToolBarArea,toolbar)

        #self.addToolBar(QtCore.Qt.BottomToolBarArea,toolbar) # ubicando a la toolbar en la posicion  inferior de la widget
        toolbar.setStyleSheet(" *{background:#d8d8d8; border:none} QToolButton:checked {background-color:#94DCD3; border:none;  } ")
        toolbar.setMovable(False) # restringir que la toolbar pueda ser movida por el usuario
        toolbar.setOrientation(QtCore.Qt.Vertical) # posicion horizontal tool bar
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu) # restringir el clic derecho sobre la toolbar para evitar que
                                                            # el usuario pueda desaparecerla

        toolbar.setIconSize(QtCore.QSize(35, 35))
        toolbar.setFixedWidth(60)

        self.crear_accionesParaPosiciones() # crear los atributos 'self.alineacion_izquierda','self.alineacion_centro'
                                            # 'self.alineacion_derecha' los cuales son acciones que serviran para
                                            #editar las posicion del texto de los deberes

        toolbar.addWidget(self.get_expansorWidget())  # agregando una widget con tal anchura que hara el todos
        # los iconos de la toolbar esten alineados a la izquierda

        toolbar.addAction(self.accion_VerApartadoPerfil)
        toolbar.addSeparator()
        toolbar.addWidget( self.get_separadorQAction() ) # agrendado widget entre cada objeto de la toobar para que tengan separacion entre si

        toolbar.addAction(self.accion_verApartadoTareas)
        toolbar.addSeparator()
        toolbar.addWidget( self.get_separadorQAction() )

        toolbar.addAction(self.accion_verApartadoAlumnos)
        toolbar.addSeparator()
        toolbar.addWidget( self.get_separadorQAction() )

        toolbar.addAction(self.accion_verApartadoConfiguracion)
        toolbar.addSeparator()
        toolbar.addWidget(self.get_separadorQAction())

        toolbar.addWidget( self.get_separadorQAction() )

        toolbar.addWidget(self.get_expansorWidget())  # agregando una widget con tal anchura que hara el todos
        # los iconos de la toolbar esten alineados a la izquierda



        ##############################################################################################################
        # CONECTANDO LAS ACCIONES DE LOS OBJETOS:

        self.accion_VerApartadoPerfil.triggered.connect( lambda : self.listWidget.setCurrentIndex(0) )
        self.accion_verApartadoTareas.triggered.connect(lambda : self.listWidget.setCurrentIndex(1) )
        self.accion_verApartadoAlumnos.triggered.connect( lambda : self.listWidget.setCurrentIndex(2) )
        self.accion_verApartadoConfiguracion.triggered.connect( lambda : self.listWidget.setCurrentIndex(3) )

        #self.stkwVentanas.addWidget(self.ventanaTestDelphia)


        #Ventana con la que se inicia por default
        #self.stkwVentanas.setCurrentIndex(0)
        #self.stkwVentanas.showFullScreen()

        self.ventana_aplicacionPerfil=PerfilMain()
        self.ventana_aplicacionTareas = TareaMain()
        self.ventana_aplicacionConfiguracion=ConfiguracionMain()
        self.ventana_aplicacionAlumnos=AlumnoMain()

        self.listWidget.addWidget(self.ventana_aplicacionPerfil)
        self.listWidget.addWidget(self.ventana_aplicacionTareas)
        self.listWidget.addWidget(self.ventana_aplicacionAlumnos)
        self.listWidget.addWidget(self.ventana_aplicacionConfiguracion)
        self.accion_verApartadoTareas.trigger()




################################################################################################################################
#  C R E A D O R E S :
################################################################################################################################
    def crear_accionesParaPosiciones(self):
        '''
        Creara 3 atributos de instancia que seran objetos de la clase 'QAction', el objetivo
        de estos 3 atributos de instancia es permitir al usuario modificar la posición del texto
        de los deberes, aparte esta metodo tambien les asigna una imagen como icono a las 'QAction'
        y tambien los agrupa de tal manera  que solo una de las 'QAction' puedo estar seleccionado
        a la vez.
        Los atributos de instancia que se crean y que son objetos de tipo 'QAction' son los siguientes:
            A) self.alineacion_izquierda
            B) self.alineacion_centro
            C) sel.alineacion_derecha

        Estos atributos de instancia en el metodo contructor  se anexaran  a la toolbar y se vincularan algunas
        señales de estos con los metodos correspondientes.

        border-image: url(:/main/IMAGENES/cuenta.png);
border-image: url(:/main/IMAGENES/estudiantes.png);
border-image: url(:/main/IMAGENES/configuraciones.png);
border-image: url(:/main/IMAGENES/tareas.png);
        '''


        # Creando los 'QAction' asi como asignandoles nombres y aparte iconos:
        self.accion_VerApartadoPerfil = QAction(QIcon(":/main/IMAGENES/cuenta.png"), 'Perfil', self)
        self.accion_verApartadoTareas= QAction(QIcon(":/main/IMAGENES/tareas.png"), 'Tareas', self)
        self.accion_verApartadoAlumnos= QAction(QIcon(":/main/IMAGENES/estudiantes.png"), 'Alumnos', self)
        self.accion_verApartadoConfiguracion = QAction(QIcon(":/main/IMAGENES/configuraciones.png"),'Configuraciones', self)


        # Permitiendo que las 'QAction' puedan ser seleccionadas
        self.accion_VerApartadoPerfil.setCheckable(True)
        self.accion_verApartadoTareas.setCheckable(True)
        self.accion_verApartadoAlumnos.setCheckable(True)
        self.accion_verApartadoConfiguracion.setCheckable(True)

        # Agrupando las acciones que permitiran al usuario alinear el texto de sus deberes,
        # con la finalidad de que solo una de las acciones  pueda ser seleccionada a la vez
        self.grupoAcciones = QActionGroup(self.accion_VerApartadoPerfil)
        self.grupoAcciones.addAction(self.accion_VerApartadoPerfil)
        self.grupoAcciones.addAction(self.accion_verApartadoTareas)
        self.grupoAcciones.addAction(self.accion_verApartadoAlumnos)
        self.grupoAcciones.addAction(self.accion_verApartadoConfiguracion)

    def get_separadorQAction(self):
        '''
        Retornara una instancia de la clase 'QLabel' con el objetivo de que este
        sirva como seperador entre los elementos que se colocan en la toolbar
        '''

        separadorQAction=QLabel()
        separadorQAction.setMinimumSize(10,2)
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

        expansorWidget=QWidget()
        expansorWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        return expansorWidget



if __name__ == '__main__':
    app = QApplication([])
    application = Main()
    application.show()
    app.exit(app.exec())