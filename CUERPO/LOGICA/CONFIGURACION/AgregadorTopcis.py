
'''
AgregadorTopcis.py :    Contine una sola  clase, la clase 'AgregarTopics', la cual  es una clase
                        que a grosso modo se encarga de hacer posible que el usuario pueda agregar
                        a la tabla de topics seleccionables el topic que desee de los topics de la
                        clase de classroom que se selecciono.
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"

###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.DISENO.CONFIGURACION.AgregadorTopics_d import Ui_Dialog
import recursos


class AgregadorTopics(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):
    '''
    Se encarga de hacer posible que el usuario pueda agregar a la tabla de topics seleccionables
    los topics de la clase de classrom que se selecciono, por ello le muestra al usuario los
    topics que pertenecen a la clase de classroom seleccionada y que aun no han sido agregados
    a la tabla de topics seleccionables.Tambien permite al usuario actualizar los topics mostrados
    ya que puede que recien haya creado un topic en su clase de classroom pero este aun no se haya
    visto reflejado en la ventana.
    Si el usuario decide agregar un topic esta clase emitira la señal respectiva.

    '''


    senal_agregoUnTopic=pyqtSignal(tuple)  # (idApi_topicAgregara,nombre_topicAgregara)


    def __init__(self,configuracionCalificador,baseDatosLocalClassRoom,classRoomControl):
        '''
        Parámetros:
            - configuracionCalificador (objeto de la clase: CalificadorConfiguracion): dicho objeto
            contiene ordenados los datos de configuracion que necesitara el programa, asi como tambien
            contiene metodos que serviran para obtener o editar dichos datos


            - baseDatosLocalClassRoom (objeto de la clase: BaseDatos_ClassRoomProgramas): dicho
            objeto permitira acceder a la base de datos local, la cual almacena los datos de
            los 'CourseWork' asi como los 'Topics' y 'Clases' del ClassRoom del profesor que ha
            iniciado sesión

            - classRoomControl (objeto de la clase: ClassRoomControl): dicho objeto es una capa
            de abstracción para poder hacer algunas peticiones al ClassRoom del profesor, asi
            como al GoogleDrive del profesor
        '''


        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)
        

        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.classRoomControl=classRoomControl
        self.configuracionCalificador=configuracionCalificador


        self.dictTopics = {} # keys: las id que le asigna la API a cada topic
                             # values: los nombres de cada topic


        self.btn_agregar.clicked.connect(self.agregarTopics)
        self.btn_actualizarTopcis.clicked.connect(self.refrescarTopics)


    def prepararParaMostrar(self):
        '''
        Cargara los topics que estan almacenados en la base de datos local y
        que no hayan sido importados a la tabla de topics seleccionables.
        '''


        cursoClassroom_id, _ = self.configuracionCalificador.get_id_nombre_cursoClassroom()

        # si hay un curso de classroom seleccionado se mostraran los topic almacenados en la
        # base de datos local y que no hayan sido importados a la tabla de topics seleccionables.
        if cursoClassroom_id:

            # la base de datos local retornara una tupla con el siguiente formato:
            # (   (idApi_topic_1,nombre_topic_1), (idApi_topic_2,nombre_topic_2) ...  )
            topics_tuplaDatos=self.baseDatosLocalClassRoom.get_topicsLibres(course_id_api=cursoClassroom_id)

            self.dictTopics = {}
            self.listWidget_topicsTareasProgramas.clear()

            # ¿la base de datos local retorno por lo menos los datos de un topic?
            if topics_tuplaDatos != () and len(topics_tuplaDatos) != 0:
                # keys: las id que le asigna la API a cada topic
                # values: los nombres de cada topic
                self.dictTopics=dict(topics_tuplaDatos)

                # agregando los nombres de los topics en la 'listWidget'
                self.listWidget_topicsTareasProgramas.addItems(  tuple( self.dictTopics.values() )  )


    def refrescarTopics(self):
        '''
        El objetivo de este metodo es actualizar su contenido con respecto a los topics
        de la clase de classroom seleccionada.

        Consultara a la API de google classroom para obtener todos los nombres y ids de los
        topics de la clase de classroom seleccionada, posteriormente solo guardara los datos
        de los topics que no esten en la base de datos local, y finalmente mostrara la lista
        de los topics que el aun no se agregan a la tabla de topics seleccionables.
        '''

        cursoClassroom_id, _ = self.configuracionCalificador.get_id_nombre_cursoClassroom()

        # si hay un curso de classroom seleccionado se mostraran los topic almacenados en la
        # base de datos local y que no hayan sido importados a la tabla de topics seleccionables.
        if cursoClassroom_id!=None:

            respuestaAfirmativa=self.msg_preguntarAcercaRefrescarTopics()

            if respuestaAfirmativa:

                # Le pedimos a la API de google classroom que nos retorne todos los topics de la
                # clase de classroom seleccionada.En caso de existir topics en la clase de classroom
                # los datos los retornara de los topics los retornara en el siguiente formato:
                # (   (idApi_topic_1,nombre_topic_1), (idApi_topic_2,nombre_topic_2) ...  )
                tuplaDatosTopics = self.classRoomControl.get_listaDatosTopicsCurso(cursoClassroom_id)

                # ¿habia tan siquiera un topic en la clase de classroom seleccionada?
                if tuplaDatosTopics!=() and len(tuplaDatosTopics) != 0:
                    # guardando los datos de todos los topics de la clase de classroom seleccionada,
                    # sin embargo solo se guardaran los datos de los topics nuevos que no esten ya
                    # almacenados dentro de la base de datos local.
                    self.baseDatosLocalClassRoom.agregar_soloNuevosTopics(
                        tuplaDatos=tuplaDatosTopics,
                        curso_api_id=cursoClassroom_id
                    )

                self.listWidget_topicsTareasProgramas.clear()

                # obteniendo de la base de datos local los datos de los topics que no
                # hayan sido importados a la tabla de topics seleccionables.La base de
                # datos local retornara una tupla con el siguiente formato:
                # (   (idApi_topic_1,nombre_topic_1), (idApi_topic_2,nombre_topic_2) ...  )
                tuplaDatosTopics=self.baseDatosLocalClassRoom.get_topicsLibres(course_id_api=cursoClassroom_id)

                self.dictTopics={} # keys: las id que le asigna la API a cada topic
                                   # values: los nombres de cada topic

                # ¿hay almenos un topic que  no hayan sido importados a la tabla
                # de topics seleccionables?
                if tuplaDatosTopics!=() and len(tuplaDatosTopics)!=0:
                    for topic_api_id,topic_nombre in tuplaDatosTopics:
                        self.dictTopics[topic_api_id]=topic_nombre

                    # agregando los nombres de los topics en la 'listWidget'
                    self.listWidget_topicsTareasProgramas.addItems(  tuple( self.dictTopics.values() )  )

                self.msg_exitoDescargarTopics()


    def agregarTopics(self):
        '''
        Cuando el usuario haya seleccionado el topic que desea agregar a la tabla de
        topics seleccionables y posteriormente le de en el boton de agregar, se llamara
        a este metodo, y lo que hara este metodo es:
            - Preguntarle al usuario si en realidad ese es el topic que desea agregar, y
            de ser afirmativa la respuesta:
                - obtendra los datos del topic que se desea agregar
                - registrara en la base de datos local que ese topic se configuro como
                topic perteneciente a la tabla de topics seleccionables
                - mandara una señal a la otra parte del programa para que este
                actue en consecuente del que el usuario haya decidido agregar un
                topic a la tabla de topics seleccionables.
        '''


        if len(self.dictTopics)>0:

            # datos del topic que se selecciono por que se desea agregar a la tabla
            # de topics seleccionables
            indice_topicSeDeseaAgregar=self.listWidget_topicsTareasProgramas.currentRow()
            nombre_topicSeDeseaAgregar = self.listWidget_topicsTareasProgramas.currentItem().text()


            respuestaAfirmativa=self.msg_preguntarConfirmacionEleccionTopics(
                nombreTopicSeDeseaAgregar=nombre_topicSeDeseaAgregar
            )

            if respuestaAfirmativa:
                idApi_topicSeDeseaAgregar=tuple( self.dictTopics.keys() )[indice_topicSeDeseaAgregar]

                tuplaDatosTopicAgregara=(idApi_topicSeDeseaAgregar,nombre_topicSeDeseaAgregar)

                cursoClassroom_id, _ = self.configuracionCalificador.get_id_nombre_cursoClassroom()

                self.baseDatosLocalClassRoom.registrarSelecciono_topic(
                    curso_id=cursoClassroom_id,
                    topic_id=idApi_topicSeDeseaAgregar
                )

                self.senal_agregoUnTopic.emit(  tuplaDatosTopicAgregara  )
                self.limpiarDeDatos()
                self.close()

        else:
            self.msg_noPuedesElegirTopics_siNoHay()


    def  limpiarDeDatos(self):
        '''
        Vacia las list widget en donde se visualizan todos los topics que se pueden
        agregar a la tabla de topics seleccionablees
        '''

        self.dictTopics={}
        self.listWidget_topicsTareasProgramas.clear()


####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################


    def msg_exitoDescargarTopics(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que se
        han actualizado y descargado con exito los topics de la clase de classroom
        '''

        mensaje = "Ya se descargaron los topics que faltaban por mostrar, sin embargo "
        mensaje+="es importante recalcar que si no vez ningun cambio es por que no  "
        mensaje+="se encountraron topics nuevos"

        self.ventanaEmergenteDe_informacion(mensaje)


    def msg_noPuedesElegirTopics_siNoHay(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de informarle
        que no puede agregar ningun topic por que no hay ningun topic registrado
        que se pueda agregar.
        '''

        mensaje = "No hay ningun  de topic que seleccionar, sin embargo la solucion "
        mensaje += "consiste en que vayas a ClassRoom y crees  topics y despues regreses  "
        mensaje += "al programa y le des clic sobre el boton con la leyenda igual a refrescar  "

        self.ventanaEmergenteDe_error(mensaje)


    def msg_preguntarConfirmacionEleccionTopics(self, nombreTopicSeDeseaAgregar):
        '''
        Mostrara un cuadro emergente de dialogo con la finalidad de preguntarle
        al usuario si en realidad esta seguro de querer elegir ese topic

        Parámetros:
            - nombreTopicSeDeseaAgregar (str) : Nombre del topic que se desea
            agregar

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si es el
            topic que desea agregar
            - False (bool): Si el usuario dijo que NO es el topic que desea
            agregar
        '''

        mensaje = f"¿Estas seguro de querer agregar al topic cuyo nombre es: <<{nombreTopicSeDeseaAgregar}>> "
        mensaje += "a la tabla de topics seleccionables? "

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado


    def msg_preguntarAcercaRefrescarTopics(self):
        '''
        Mostrara un cuadro de dialogo al usuario para preguntarle si
        en realidad desea refrescar.

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si
            desea  refrescar
            - False (bool): Si el usuario dijo que NO desea refrescar
        '''

        mensaje = "Solo es recomendable refrescar cuando no vez los topics que deseas "
        mensaje+="¿en verdad los topcis que deseas seleccionar no se encuentra en la lista? "
        mensaje+="¿en verdad necesitas refrescar?"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado


if __name__ == '__main__':
    app = QApplication([])
    application = AgregadorTopics()
    application.show()
    app.exit(app.exec())
