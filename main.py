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
from CUERPO.LOGICA.API.ClassRoomControl import ClassRoomControl,AdministradorProgramasClassRoom
from CUERPO.LOGICA.API.BaseDatosLocal import BaseDatos_ClassRoomProgramas
from CUERPO.LOGICA.MAIN.DatosCreador import Dialog_datosCreador

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.MAIN.Main_d import Ui_MainWindow
import recursos

class Main(QtWidgets.QMainWindow,Ui_MainWindow,recursos.HuellaAplicacion):
    '''
    El objetivo de esta clase  sera mostrar todo el sistema que permite
    agregar deberes, eliminar los deberes cuando se cumplen,cambiar la posicion del texto de los deberes
    y cambiar el tamaño del texto de los deberes, por ello esta clase basicamente estara compuesta de
    una apartado en donde se mostraran todos los deberes a realizar  y unos botones que permitieran hacer
    lo mencionado anteriormente.
    '''


    def __init__(self,correo_profesor=None, nombre_profesor=None, curso_id=None, topic_id=None):

        QtWidgets.QMainWindow.__init__(self)
        recursos.HuellaAplicacion.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Obteniendo los permisos de la API...

        self.baseDatosLocalClassRoomProgramas=BaseDatos_ClassRoomProgramas('roni.db')
        self.baseDatosLocalClassRoomProgramas.crearBaseDatos()
        self.elClassRoom_control=ClassRoomControl()
        self.elClassRoom_control.obtenerValor_service_classroom_and_drive()



        self.profesor_correo = correo_profesor
        self.profesor_nombre=nombre_profesor
        if not(correo_profesor and nombre_profesor) :
            self.profesor_correo, self.profesor_nombre=self.elClassRoom_control.get_datosProfesor(recursos.App_Principal.FOTO_PERFIL_PROFESOR)
        self.curso_id=curso_id
        self.topic_id=topic_id


        self.administradorProgramasClassRoom=AdministradorProgramasClassRoom(
            classroom_control=self.elClassRoom_control,
            curso_id=curso_id,
            tareasProgramas_topic_id=topic_id,
            retroProgramas_topic_id=None
        )



        curso_id = '267287795258'
        tareasProgramas_topic_id = '369766123712'



        #c=self.elClassRoom_control.get_listaTareasTopic(curso_id=curso_id,
        #                                              topic_id=tareasProgramas_topic_id)
        #print(c)

        #self.baseDatosLocalClassRoomProgramas.add_courseWork(c[0])




        #a=self.elClassRoom_control.get_listaDatosCursos()
        #print(a)
        #self.baseDatosLocalClassRoomProgramas.add_curso(a[0])

        #b=self.elClassRoom_control.get_listaDatosTopicsCurso(curso_id=curso_id)
        #print(b)
        #self.baseDatosLocalClassRoomProgramas.add_topic(b[0])








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


        toolbar.addWidget(self.get_separadorQAction())  # agrendado widget entre cada objeto de la toobar para que tengan separacion entre si
        toolbar.addAction(self.accion_verInfoProgramador)

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




        # Creando los diferentes apartados del programa:
        self.ventana_aplicacionPerfil=PerfilMain(profesor_correo=self.profesor_correo,
                                                 profesor_nombre=self.profesor_nombre,
                                                 profesor_imagenPerfil=recursos.App_Principal.FOTO_PERFIL_PROFESOR
                                                 )
        self.ventana_aplicacionPerfil.cargarPerfilProfesor()

        # Si los datos del curso y topic no estan definidos...
        if not(self.curso_id and self.topic_id) :
            self.ventana_aplicacionTareas = TareaMain(administradorProgramasClassRoom=None)
            self.ventana_aplicacionConfiguracion=ConfiguracionMain()
            self.ventana_aplicacionAlumnos=AlumnoMain()

        # Si los datos del curso y topic si estan definidos...
        else:
            pass

        self.listWidget.addWidget(self.ventana_aplicacionPerfil)
        self.listWidget.addWidget(self.ventana_aplicacionTareas)
        self.listWidget.addWidget(self.ventana_aplicacionAlumnos)
        self.listWidget.addWidget(self.ventana_aplicacionConfiguracion)


        ##############################################################################################################
        # CONECTANDO LAS ACCIONES DE LOS OBJETOS:
        self.accion_VerApartadoPerfil.triggered.connect(self.mostrar_apartadoPerfil)
        self.accion_verApartadoTareas.triggered.connect(self.mostrar_apartadoTareas )
        self.accion_verApartadoAlumnos.triggered.connect(self.mostrar_apartadoAlumnos)
        self.accion_verApartadoConfiguracion.triggered.connect(self.mostrar_apartadoConfiguracion )

        self.accion_verInfoProgramador.triggered.connect(lambda : self.ventanaDatosCreador.show() )


        # Ventana defualt que se mostrara
        self.accion_VerApartadoPerfil.trigger()

        self.ventanaDatosCreador=Dialog_datosCreador()


    def mostrar_apartadoTareas(self):
        if self.curso_id and self.topic_id:
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

        respuesta=self.msg_cerrarVentana()

        if respuesta:
            if self.profesor_correo and self.profesor_nombre:
             with open(recursos.App_Principal.ARCHIVO_DATOS_PROFESOR,'w') as archivo:
                 archivo.write(  '\n'.join((self.profesor_correo, self.profesor_nombre)))
             event.accept()
        else:
            event.ignore()  # No saldremos del evento




##########################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################

    def msg_cerrarVentana(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje="¿Esta seguro que quieres\n"
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton()  ==  btn_yes:
            return True
        return False

    def msg_elegirCurso_y_topic(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Warning)
        ventanaDialogo.setWindowIcon( QIcon(self.ICONO_APLICACION)  )
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje="Para ver las tareas asignadas primero debes definir la clase "
        mensaje+="y el topic en donde se encuentran esas tareas, para hacer ello "
        mensaje+="debes ir al apartado de 'configuracion' "
        mensaje=self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()









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

        self.accion_verInfoProgramador = QAction(QIcon(":/main/IMAGENES/info_off.png"), 'Info programador',self)

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

    from PyQt5.QtCore import QCoreApplication,Qt
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtWidgets import QSplashScreen
    import sys, time,os
    import recursos


    direccionTotal=sys.argv[0]
    direccionPartes=os.path.normpath(direccionTotal)
    direccionPartes=direccionPartes.split(os.sep)
    ruta_direccionTotal = os.sep.join( direccionPartes[:-1] )
    if len(direccionPartes)>1:
        ruta_direccionTotal+=os.sep
    recursos.App_Principal.actualizarUbicaciones(ruta_direccionTotal)


    correo_profesor=None
    nombre_profesor=None
    curso_id=None
    topic_id=None
    if os.path.isfile(recursos.App_Principal.ARCHIVO_DATOS_PROFESOR):
        # Contiene los datos cada uno separado por un salto de linea
        # correo del profesor, nombre completo del profesor
        with open(recursos.App_Principal.ARCHIVO_DATOS_PROFESOR) as archivo:
            datos=archivo.read()
        correo_profesor, nombre_profesor=datos.split('\n')


    if os.path.isfile(recursos.App_Principal.ARCHIVO_TRABAJO_PROFESOR):
        # Contiene los datos cada uno separado por un salto de linea
        # curso_id, topic_id
        with open(recursos.App_Principal.ARCHIVO_TRABAJO_PROFESOR) as archivo:
            datos=archivo.read()
        curso_id, topic_id=datos.split('\n')


    app = QApplication(sys.argv)
    splash_pix = QPixmap(recursos.App_Principal.IMAGEN_SPLASH_SCREEN)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    time.sleep(1)
    form = Main(
        correo_profesor=correo_profesor,
        nombre_profesor=nombre_profesor,
        curso_id=curso_id,
        topic_id=topic_id
    )
    form.show()
    splash.finish(form)
    app.exec_()


    #app = QApplication([])
    #application = Main()
    #application.show()
    #app.exit(app.exec())
