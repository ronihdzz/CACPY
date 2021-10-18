
'''
AgregadorCourseworks.py :
    Contine una sola  clase, la clase 'TareaMain.py :
    Contine una sola  clase, la clase 'TareaMain', la cual  a grosso ...
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import QtWidgets

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.DISENO.TAREA.AgregadorCourseWorks_d import Ui_Dialog
import recursos

class AgregadorCourseWorks(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):
    '''
    Se encarga de hacer posible que el usuario pueda agregar a la tabla de  tareas calificables
    las tareas que el  desee, por ello le muestra al usuario todas las tareas que no han sido
    agregadas aun a la tabla de tareas calificables y que pertenecen a la clase de classroom y topic de
    classroom que el usuario selecciono con anterioridad.Si el usuario agrega una tarea a la tabla
    de tareas calificables esta ventana emitira la señal respectiva y posteriormente se cerrara.
    '''

    senal_regresar= pyqtSignal(bool)  # unicamente emitira el valor de True, y esto sucedera cuando el
                                      # usuario de clic sobre el boton regresar para ver las otras tareas
                                      # calificables

    senal_courseWork_selec=pyqtSignal(tuple) # unicamente se emitira cuando el usuario haya decidido agregar una
                                             # tarea a la tabla de tareas calificables, y los datos que mandara de
                                             # de la tarea que se desea agregar son:
                                             # (courseWorkSelec_id,courseWorkSelec_nombre,courseWorkSelec_fecha)

    def __init__(self,administradorProgramasClassRoom):
        '''
        - administradorProgramasClassroom (objeto de la clase: AdministradorProgramasClassRoom): dicho
        objeto permite calificar tareas de los estudiantes  del classroom seleccionado por el usuario, este
        objeto tambien permite obtener informacion de una manera mas sencilla acerca de las tareas del classroom
        y topic seleccionadas por el usuario
        '''

        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)

        self.administradorProgramasClassRoom=administradorProgramasClassRoom

        # keys: las id que le asigna la API a cada tarea(coursework)
        # values: los nombres de tarea(coursework)
        self.dictCourseWorks = {}

        self.configurarTabla()

        self.tableWidget.doubleClicked.connect(self.courseWork_elegido)
        self.btn_refrescarCourseWorks.clicked.connect(self.refrescarCourseWorks)


    def cargarDatos_courseWorks(self):
        '''
        Cargara los datos de los nombres de las tareas(courseworks) que estan almacenadas en la
        base de datos local y que no han sido importados a la tabla de tareas calificables.
        '''


        # al obtener los datos de las tareas (courseworks) que estan almacenadas en la
        # base de datos local y que no han sido importados a la tabla de tareas calificables,
        # los datos se obtienen en el siguiente formato:
        # (
        #       (id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1),
        #       (id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2) ,
        #       ....
        #   )
        tuplaDatosCourseWorks=self.administradorProgramasClassRoom.get_courseWorksLibres_baseDatosLocal()

        # keys: las id que le asigna la API a cada tarea(coursework)
        # values: los nombres de tarea(coursework)
        self.dictCourseWorks = {}
        self.tableWidget.setRowCount(0) # borrando los datos de la tabla

        numeroCourseworks=len(tuplaDatosCourseWorks)
        if tuplaDatosCourseWorks != () and numeroCourseworks != 0:
            self.tableWidget.setRowCount(numeroCourseworks)
            for r,tuplaDatos_unCoursework in enumerate(tuplaDatosCourseWorks):
                courseWork_api_id, titulo, descripccion, fechaCreacion= tuplaDatos_unCoursework

                self.dictCourseWorks[courseWork_api_id]=titulo

                # Cargando datos de los coursworks en la tabla:

                # nombre de la tarea(coursework)
                a = QtWidgets.QTableWidgetItem(titulo)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(r, 0, a)

                # fecha de creacion de la tarea(coursework)
                a = QtWidgets.QTableWidgetItem(fechaCreacion)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(r, 1, a)


    def refrescarCourseWorks(self):
        '''
        El objetivo de este metodo es actualizar su contenido con respecto a las tareas
        de la clase de classroom seleccionada que se encuentran el topic de classroom
        seleccionado.

        Este metodo consultara a la API de google classroom para obtener todos los nombres,ids,
        fechaCreacion,descripccion de las tareas(coursewroks) que se en encuentran en el topic
        de classroom seleccionado de la clase de classroom seleccionada, posteriormente solo guardara
        los datos de las tareas(courseworks) que no esten en la base de datos local, y finalmente
        mostrara la en la tabla los datos de las tareas(courseworks) que el usuario aun no se agrega
        a la tabla de tareas seleccionables
        '''


        respuestaAfirmativa=self.msg_preguntarAcercaRefrescarCourseWorks()
        if respuestaAfirmativa:
            # Consultamos los datos en la API

            # Le pedimos a la API de google classroom que nos retorne todas las tareas(courseworks)
            # que pertencen al topic de classroom seleccionado de la clase de classroom seleccionada.
            # En caso de existir alguna  tarea  los datos de la tarea o tareas obtenidas vendran en
            # el siguiente formato:
            # (
            #       (id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1),
            #       (id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2) ,
            #       ....
            #   )
            tuplaDatosCourseWorks = self.administradorProgramasClassRoom.get_dictTareasDejadas()

            # ¿se obtuvo almenos los datos de una tarea?
            if tuplaDatosCourseWorks!=() and len(tuplaDatosCourseWorks) != 0:
                # guardando en la base de datos local los datos de las tareas obtenidas al
                # realizar la consulta a la API  de google classroom, sin embargo es importante
                # mencionar que solo se guardaran los datos de los topics nuevos que no esten ya
                # almacenados dentro de la base de datos local.
                self.administradorProgramasClassRoom.agregarCourseWorks_baseDatosLocal(
                    tuplaDatos=tuplaDatosCourseWorks
                )

            # voviendo a cargar los datos de las tareas desde la base de datos local
            self.cargarDatos_courseWorks()

            self.msg_exitoDescargarCourseWorks()


    def courseWork_elegido(self,item):
        '''
        Este metodo es llamado cuando el usuario haga doble clic izquierdo sobre el nombre de
        una tarea(courseWork), que desea agregar a la tabla de tareas calificables.

        ¿Que hara este metodo?
            - Preguntara si  a la tarea que se le dio doble clic izquierdo es la tarea que se desea
            agregar a la tabla de tareas calificables, si el usuario responde afirmativamente, entonces
            este metodo procedera a registrar esta tarea como tarea calificable en la base de datos local
            y posteriormente este metodo emitira una señal y  cerrara esta ventana
        '''

        # la tarea(coursework)  que se selecciono se encuentra dentro de un renglon de la tabla en donde
        # vienen las tareas que pueden ser agregadas a la tabla de tareas calificables, con lo siguiente
        # se obtiene dicho numero de renglon en donde se encuentra la tarea que se selecciono
        renglon=item.row()

        # obteniendo los datos de la tarea que se desea agregar a la tabla de tareas calificables
        courseWorkSelec_id=tuple(self.dictCourseWorks.keys())[renglon]
        courseWorkSelec_nombre=self.dictCourseWorks[courseWorkSelec_id]
        courseWorkSelec_fecha=self.tableWidget.item(renglon,1).text()

        # preguntandole al usuario si esta seguro de agregar la tarea que selecciono
        # a la tabla de tareas calificables
        respuestaPositiva=self.msg_preguntarConfirmacionEleccionCourseWorks(
            nombreCourseWork_deseaAgregar=courseWorkSelec_nombre
        )

        if respuestaPositiva:

            # mandando la señal para que: 'TareaMain' puede agregar la tarea que selecciono el
            # usuario a la tabla de tareas calificables
            tuplaDatosMandar=(courseWorkSelec_id,courseWorkSelec_nombre,courseWorkSelec_fecha)
            self.senal_courseWork_selec.emit(  tuplaDatosMandar  )

            # registrando en la base de datos local que la tarea que selecciono el usuario ya
            # forma parte de la tabla de tareas calificables
            self.administradorProgramasClassRoom.seleccionarBaseLocal_coursework(courseWorkSelec_id)
            self.close()

    def configurarTabla(self):
        '''
        Se encargara de darle un formato a la tabla de tareas(coursework) que el usuario
        puede agregar a la tabla de tareas calificables, es decir:
         - Se encargara de definir el numero de columnas de la tabla
         - Se encargara de definirla interaccion que se tendra con dicha tabla.
         - Se encargara de definir el diseño de la tabla(color de tabla, color de renglones,etc)
        '''

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        stylesheet = f"""QTableView{{ 
        selection-background-color:{recursos.App_Principal.COLOR_TOPIC_SELECCIONADO};
        background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }}; """
        self.tableWidget.setStyleSheet(stylesheet)

        self.tableWidget.verticalHeader().setDefaultSectionSize(40)

        # la tabla tiene 2 columnas
        # ("NOMBRE","FECHA CREACION")
        header = self.tableWidget.horizontalHeader()
        for columna in range(0,2):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)

####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################


    def msg_preguntarConfirmacionEleccionCourseWorks(self, nombreCourseWork_deseaAgregar):
        '''
        Mostrara un cuadro emergente de dialogo con la finalidad de preguntarle
        al usuario si en realidad esta seguro de querer importar la tarea con
        el nombre igual al valor que almacenara el parametro: 'nombreCoursework'

        Parámetros:
            - nombreCourseWork_deseaAgregar (str) : Nombre de la tarea(coursework)
            que el usuario desea agregar a la tabla de tareas calificables.

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si es la
            tarea que desea agregar
            - False (bool): Si el usuario dijo que NO es la tarea que desea
            agregar
        '''

        mensaje = f"¿El CourseWork que deseas agregar en verdad es:<<{nombreCourseWork_deseaAgregar}>>?"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado

    def msg_preguntarAcercaRefrescarCourseWorks(self):
        '''
        Mostrara un cuadro de dialogo al usuario para preguntarle si
        en realidad desea refrescar.

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si
            desea  refrescar
            - False (bool): Si el usuario dijo que NO desea refrescar
        '''

        mensaje = "Solo es recomendable refrescar cuando no vez el CourseWork o CourseWorks que deseas "
        mensaje+="¿en verdad los CourseWorks que deseas seleccionar no se encuentran en la lista? "
        mensaje+="¿en verdad necesitas refrescar?"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado


    def msg_exitoDescargarCourseWorks(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que se
        han actualizado y descargado con exito los courseworks
        '''

        mensaje = "Ya se descargaron los CourseWorks que faltaban por mostrar, sin embargo "
        mensaje+="es importante recalcar que si no vez ningun cambio es por que no  "
        mensaje+="se encontraron CourseWorks nuevos"

        self.ventanaEmergenteDe_informacion(mensaje)

if __name__ == '__main__':
    app = QApplication([])
    application = AgregadorCourseWorks()
    application.show()
    app.exit(app.exec())