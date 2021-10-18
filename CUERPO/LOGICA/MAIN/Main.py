
'''
Main.py :   Contine una sola  clase, la clase 'Main', la cual  es la clase principal 
            ya que se encarga de unificar  todos los scripts de python que realice 
            para dar vida  a esta aplicacion, sin embargo es importante  aclarar 
            que a pesar de ello este script se encuentra en este  apartado por que 
            para hacer una instancia  de la  clase 'Main' se necesitan algunos objetos 
            y configuraciones  extras las cuales para hacer un  codigo mas  limpio se 
            efectuan en el script 'CACPY.py' el cual es la que  crea una  instancia de 
            esta clase  entre otras cosas, por tal motivo si se desea ejecutar todo el 
            sofware el script que debe ser ejecutado es el script : 'CACPY.py'
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QSizePolicy, Qt
from PyQt5.QtWidgets import QAction,QActionGroup,QLabel,QWidget,QMessageBox

###########################################################################################################################################
# fuente local
###########################################################################################################################################

# diseño de este apartado de la aplicación
from CUERPO.DISENO.MAIN.Main_d import Ui_MainWindow
import recursos
from CUERPO.LOGICA.TAREA.TareaMain import TareaMain
from CUERPO.LOGICA.PERFIL.PerfilMain import PerfilMain
from CUERPO.LOGICA.CONFIGURACION.ConfiguracionMain import ConfiguracionMain
from CUERPO.LOGICA.ALUMNO.AlumnoMain import AlumnoMain
from CUERPO.LOGICA.API.AdministradorProgramasClassRoom import AdministradorProgramasClassRoom
from CUERPO.LOGICA.MAIN.DatosCreador import Dialog_datosCreador


class Main(QtWidgets.QMainWindow, Ui_MainWindow, recursos.HuellaAplicacion):
    '''
    Es la clase principal ya  que se encarga de unificar todos los scripts 
    de python que realice para dar vida a esta  aplicacion, es decir 
    junta todos los diferentes apartados del programa en una seccion 
    respectiva de la aplicación.
    '''


    def __init__(self,baseDatosLocalClassRoom,classRoomControl,configuracionCalificador):
        ''' 
        Parametros:
            baseDatosLocalClassRoom (objeto de la clase: BaseDatos_ClassRoomProgramas): dicho
            objeto permitira acceder a la base de datos local, la cual almacena los datos de
            lo 'CourseWork' asi como los 'Topics' y 'Clases' del ClassRoom del profesor que ha
            iniciado sesión

            classRoomControl (objeto de la clase: ClassRoomControl): dicho objeto es una capa
            de abstracción para poder hacer algunas peticiones al ClassRoom del profesor, asi
            como al GoogleDrive del profesor

            configuracionCalificador (objeto de la clase: CalificadorConfiguracion): dicho objeto
            contiene ordenados los datos de configuracion que necesitara el programa, asi como tambien
            contiene metodos que serviran para obtener o editar dichos datos
        '''

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)

        # objeto que permitira el manejo de la base de datos local
        # que almacenara los datos de classroom del profesor.
        self.baseDatosLocalClassRoomProgramas = baseDatosLocalClassRoom

        # objeto que podra hacer consultas al classroom del profesor
        # que abrio la aplicacion
        self.elClassRoom_control = classRoomControl


        # esta instancia contiene todos los datos  que se necesitan 
        # para administrar la calificacion de  las tareas
        # de programación del profesor que inicia sesion en el programa
        self.configuracionCalificador = configuracionCalificador


        # el objeto de la clase: AdminitradorProgramasClassRoom sirve para poder 
        # calificar las tareas de programación de los alumnos, dicho objeto abstrae
        # la logica empleada para poder hacer eso
        self.administradorProgramasClassRoom = AdministradorProgramasClassRoom(
            classroom_control=self.elClassRoom_control,
            configuracionCalificador=self.configuracionCalificador,
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoomProgramas
        )


        # Creando los diferentes apartados del programa:

        # el apartado de 'Mi perfil' permitira al profesor ver su informacion personal asi como
        # tambien le permitira cerra sesión 
        self.ventana_aplicacionPerfil = PerfilMain(profesor_correo=self.configuracionCalificador.getCorreoProfesor(),
                                                   profesor_nombre=self.configuracionCalificador.getNombreProfesor(),
                                                   profesor_imagenPerfil=recursos.App_Principal.FOTO_PERFIL_PROFESOR
                                                   )
        self.ventana_aplicacionPerfil.cargarPerfilProfesor()


        # el apartado de 'Mis configuraciones' permitira al profesor elegir la clase de ClassRoom
        # asi como el topic entre otras mas configuraciones del programa.
        self.ventana_aplicacionConfiguracion = ConfiguracionMain(
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoomProgramas,
            classRoomControl=self.elClassRoom_control,
            configuracionCalificador=self.configuracionCalificador
        )

        # el apartado de 'Mis tareas' permitira al profesor seleccionar las tareas que quiere
        # calificar, asi como tambien permitira calificar las entregas correspondientes a una
        # tarea especifica
        self.ventana_aplicacionTareas = TareaMain(
            administradorProgramasClassRoom=self.administradorProgramasClassRoom,
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoomProgramas
        )

        # el apartado de 'Mis alumnos' permitira al profesor poder ver a los alumnos inscritos
        # a la clase de classroom seleccionada, asi como tambien permite ver las calificaciones
        # de cada uno de ellos en cada tarea.
        self.ventana_aplicacionAlumnos = AlumnoMain(
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoomProgramas,
            classRoomControl=self.elClassRoom_control,
            configuracionCalificador=self.configuracionCalificador
        )

        # este apartado contendra la información acerca del programador, es decir contendra
        # mis datos de contacto
        self.ventanaDatosCreador = Dialog_datosCreador()


        # Agregando cada  apartados del programa a la list  widget
        self.listWidget.addWidget(self.ventana_aplicacionPerfil)
        self.listWidget.addWidget(self.ventana_aplicacionTareas)
        self.listWidget.addWidget(self.ventana_aplicacionAlumnos)
        self.listWidget.addWidget(self.ventana_aplicacionConfiguracion)


        # Creando la barra de navegacion
        self.crear_barraNavegacion()


        # Conectando las QAction que creo la funcion 'crear_barraNavegacion()' con cada
        # respectiva parte de la aplicacion.
        self.accion_verApartadoPerfil.triggered.connect(self.mostrar_apartadoPerfil)
        self.accion_verApartadoTareas.triggered.connect(self.mostrar_apartadoTareas)
        self.accion_verApartadoAlumnos.triggered.connect(self.mostrar_apartadoAlumnos)
        self.accion_verApartadoConfiguracion.triggered.connect(self.mostrar_apartadoConfiguracion)
        self.accion_verInfoProgramador.triggered.connect(lambda: self.ventanaDatosCreador.show())


        # Contanto las señales de los diferentes apartados del programa
        self.ventana_aplicacionConfiguracion.senal_eligioTopic.connect(self.actuarAnteCambio_topicClassroom)
        self.ventana_aplicacionConfiguracion.senal_eligioUnCurso.connect(self.actuarAnteCambio_claseClassroom)
        self.ventana_aplicacionConfiguracion.senal_claseNbGrader_cambio.connect(self.actuarAnteCambio_claseNbGrader)
        self.ventana_aplicacionTareas.senal_operacionCompleja.connect(self.actuarAnteEstado_operacionCompleja)
        self.ventana_aplicacionPerfil.senal_cerrarAplicacion.connect(self.cerrarPrograma_sinConsultar)


        # Se cargan las configuraciones que el usuario realizo la ultima vez que cerro el programa
        self.ventana_aplicacionConfiguracion.cargarDatos_objetoConfigurador()

        # Mostrando de forma default el el perfil del apartado del programa
        self.accion_verApartadoPerfil.trigger()

        # variable de bandera que servira para que el programa sepa cuando
        # preguntar acerca de cerrar o no.
        self.CERRAR_PROGRAMA_SIN_CONSULTAR=False


    def cerrarPrograma_sinConsultar(self):
        '''
        Este metodo cerrara el programa sin consultar al profesor 
        la desición de cerrar el programa.
        '''

        self.CERRAR_PROGRAMA_SIN_CONSULTAR=True
        self.close()


    def actuarAnteEstado_operacionCompleja(self,estadoSenalCompleja):
        '''
        Este metodo se encargara de bloquear o desbloquear toda la aplicación,
        en función del valor que tome el parametro: 'estadoSenalCompleja', es 
        decir si:
            
            estadoSenalCompleja=False   eso hara que el metodo bloquee toda la
            aplicación con la finalidad de que el profesor no pueda interactuar
            con ningun elemento de la aplicación.

            estadoSenalCompleja=True    eso hara que el metodo desbloque toda 
            la aplicación con la finalidad de que el profesor de ser que no podia
            interactuar con la aplicación, ahora si ya pueda interactuar con toda
            la aplicación
        
        Parámetros:
            estadoSenalCompleja (bool): Servira para indicar si se desea bloquear
            o desbloquear toda la aplicacion
        '''

        if estadoSenalCompleja==True:
            self.setEnabled(False)
        else:
            self.setEnabled(True)

    def actuarAnteCambio_claseNbGrader(self):
        '''
        Cada vez que el profesor efectue un cambio en el apartado de:  'Mis configuraciones' 
        y dicho cambio haya sido un cambio en la seleccion de la clase NbGrader, es 
        indispensable llamar a este metodo por que este metodo se encarga de avisarle al 
        objeto 'self.administradorProgramasClassRoom' que se realizo un cambio en la clase
        NbGrader seleccionada, y que por lo tanto que se  actue en consecuencia.
        Es importante resaltar que el objeto: 'self.administradorProgramasClassRoom' es el
        encargado de calificar las tareas de programación, por lo que se le siempre se le debe avisar
        cuando se realice un cambio en la eleccion de la clase NbGrader ya que esta juega un papel
        importante en calificación de las tareas.
        '''

        self.administradorProgramasClassRoom.actualizar_nbGraderControl()
        self.ventana_aplicacionTareas.regresarMenu()


    def actuarAnteCambio_claseClassroom(self):
        '''
        Cada vez que el profesor efectue un cambio en el apartado de:  'Mis configuraciones' 
        y dicho cambio haya sido un cambio en la seleccion de la clase de Classroom, es 
        indispensable llamar a este metodo por que este metodo se encarga de avisarle a los
        demas apartados del programa que la clase de Classroom ha sido cambiado, y estos 
        apartados actuaran en consecuencia, por ejemplo:
            * El apartado de 'Mis alumnos' lo que hara es limpiar la pantalla ya que
            al elegirse otra clase asume que son otros los  alumnos, asi que limpia
            la pantalla
            * El apartado de 'Mis tareas' debera ahora cargar los datos de la clase de classroom
            seleccionada
        '''

        self.ventana_aplicacionTareas.actuarCambioCurso()
        self.ventana_aplicacionAlumnos.actuarAnteCambio_claseClassroom()


    def actuarAnteCambio_topicClassroom(self):
        '''
        Cada vez que el profesor efectue un cambio en el apartado de:  'Mis configuraciones' 
        y dicho cambio haya sido un cambio en la seleccion de la clase de Topic, es 
        indispensable llamar a este metodo por que este metodo se encarga de avisarle al apartado
        de 'Mis tareas' que el Topic seleccionado ahora es una diferente y que actue en consecuencia.
        '''

        self.ventana_aplicacionTareas.actuarCambioTopic()


    def mostrar_apartadoTareas(self):
        '''
        Este metodo se encargara de mostrar el apartado del programaga cuyo nombre es: 'Mis tareas', 
        sin embargo solo mostrara dicho apartado si el profesor cumple con los requisitos, en caso 
        contrario le mostrara un cuadro de dialogo explicandole las razones de por que no puede acceder
        al apartado de 'Mis tareas' y posteriormente se le direccionara al apartado de:
        'Mis configuraciones'
        '''

        if self.configuracionCalificador.datosListosApartadoTareas():
            self.bel_nombreApartado.setText("Mis tareas")
            self.listWidget.setCurrentIndex(1)
        else:
            self.msg_faltanDatosParaApartadoTareas()
            self.accion_verApartadoConfiguracion.trigger()

    def mostrar_apartadoAlumnos(self):
        '''
        Este metodo se encargara de mostrar el apartado del programaga cuyo nombre es: 'Mis alumnos', 
        sin embargo solo mostrara dicho apartado si el profesor cumple con los requisitos, en caso 
        contrario le mostrara un cuadro de dialogo explicandole las razones de por que no puede acceder
        al apartado de 'Mis alumnos' y posteriormente se le direccionara al apartado de:
        'Mis configuraciones'
        '''

        if self.configuracionCalificador.datosListosApartadoAlumnos():
            self.bel_nombreApartado.setText("Mis alumnos")
            self.listWidget.setCurrentIndex(2)
        else:
            self.msg_faltanDatosParaApartadoAlumnos()
            self.accion_verApartadoConfiguracion.trigger()



    def mostrar_apartadoConfiguracion(self):
        '''
        Este metodo se encargara de mostrar el apartado de 'Mis configuraciones'
        '''

        self.bel_nombreApartado.setText("Mis configuraciones")
        self.listWidget.setCurrentIndex(3)

    def mostrar_apartadoPerfil(self):
        '''
        Este metodo se encargara de mostrar el apartado de 'Mi perfil'
        '''

        self.bel_nombreApartado.setText("Mi perfil")
        self.listWidget.setCurrentIndex(0)



    def closeEvent(self, event):
        '''
        Este metodo es llamado de distintas formas unas de ellas son:
            * Cuando el usuario le de clic izquierdo sobre el boton de cerrar programa 
            * Cuando se llama al metodo 'self.close()'
            
        Sin embargo este metodo se sobreescribio para que tenga dos comportamientos diferentes
        que dependenran del valor de atributo de instancia: 'self.CERRAR_PROGRAMA_SIN_CONSULTAR'.

        Los comportamientos son los siguientes:
            * Si se manda a llamar este metodo y la variable de instancia: 
            'self.CERRAR_PROGRAMA_SIN_CONSULTAR' es igual a True, se cerrara
            el programa sin consultarse
            * Si se manda a llamar este metodo y la variable de instancia: 
            'self.CERRAR_PROGRAMA_SIN_CONSULTAR' es igual a False, se preguntara
            al usuario si en verdad esta seguro de querer cerrar el programa y solo 
            en caso de que la respuesta sea afirmativa, el programa hara un respaldo 
            de la información que inicio sesión y posteriormente cerrara el programa.
        '''

        if self.CERRAR_PROGRAMA_SIN_CONSULTAR:
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
        '''
        Mostrara un cuadro de dialogo con el objetivo de: preguntarle el profesor
        si en realidad desea cerrar la aplicacion

        Returns:
            True : En caso de que el profesor presione el boton de 'Si'
            False: En caso de que el profesor presione el boton de 'No'
        '''

        mensaje = "¿Esta seguro que deseas salir de la aplicacion?"
        respuesta=self.ventanaEmergenteDe_pregunta(mensaje)

        return respuesta


    def msg_faltanDatosParaApartadoAlumnos(self):
        '''
        Mostrara un cuadro de dialogo con el objetivo de: informarle al
        profesor la razon por la cual no puede acceder al apartado de
        alumnos.
        '''


        mensaje = "Para acceder al apartado 'Mis alumnos' primero debes seleccionar una de tus clases de classroom "
        mensaje+= "y la carpeta de google drive en donde se almacenaran todas las retroalimentaciones de tus cursos "
        mensaje+=" y todo ello podras hacerlo en el apartado de 'Mis configuraciones' "

        self.ventanaEmergenteDe_error(mensaje)



    def msg_faltanDatosParaApartadoTareas(self):
        '''
        Mostrara un cuadro de dialogo con el objetivo de: informarle al
        profesor la razon por la cual no puede acceder al apartado de
        tareas
        '''

        mensaje = "Para ver las tareas asignadas primero debes seleccionar una de tus clases de classroom,"
        mensaje+= "el topic en donde se encuentran las tareas que deseas calificar, la clase de NbGrader "
        mensaje+= "y la carpeta de google drive en donde se almacenaran todas las retroalimentaciones de tus cursos "
        mensaje+=" y todo ello podras hacerlo en el apartado de 'Mis configuraciones' "

        self.ventanaEmergenteDe_error(mensaje)

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


        # QtCore.Qt.BottomToolBarArea => toolbar ubicada abajo
        # Qt.LeftToolBarArea => toolbar ubicada en la parte izquierda
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

        # Agrupando las acciones que permitiran al maestro solo seleccionara una a la vez.
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