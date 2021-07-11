from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt

from PyQt5 import QtCore,QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana


from CUERPO.DISENO.CONFIGURACION.AgregadorTopics_d import Ui_Dialog
import recursos


class AgregadorTopics(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):

    senal_ventanaFueCerrada= pyqtSignal(bool)  # id de tarea
    senal_operacionImportante=pyqtSignal(bool)
    senal_agregoUnTopic=pyqtSignal(tuple) # curso_api_id,  curso_nombre


    def __init__(self,baseDatosLocalClassRoom,classRoomControl):
        QtWidgets.QDialog.__init__(self)
        recursos.HuellaAplicacion.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)

        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.classRoomControl=classRoomControl


        self.dictTopics = {}


        self.btn_agregar.clicked.connect(self.agregarTopics)
        self.btn_actualizarTopcis.clicked.connect(self.refrescarClases)



    def cargarDatosTopics(self,curso_id):

        # Cuando se crean datos se crea el atributo curso_id
        self.curso_id=None
        if curso_id:
            self.curso_id=curso_id
            tuplaDatosTopics=self.baseDatosLocalClassRoom.get_topicsLibres(course_id_api=curso_id)
            print("TUPLA DESDE BASE LOCAL:",tuplaDatosTopics)

            #tuplaDatosClases=self.baseDatosLocalClassRoom.get_tuplaClases()
            #print("CLASES BASE DE DATOS:",tuplaDatosClases)
            self.dictTopics = {}
            self.listWidget_topicsTareasProgramas.clear()
            self.listWidget_topicsRetroalimentacion.clear()

            if tuplaDatosTopics==() or len(tuplaDatosTopics)==0:
                tuplaDatosTopics=self.classRoomControl.get_listaDatosTopicsCurso(self.curso_id)
                print("TEMAS DEL CURSO API: ",tuplaDatosTopics)
                if tuplaDatosTopics !=() and len(tuplaDatosTopics)!= 0:
                    self.baseDatosLocalClassRoom.agregar_soloNuevosTopics(
                        tuplaDatos=tuplaDatosTopics,
                        curso_api_id=self.curso_id
                    )

            if tuplaDatosTopics != () and len(tuplaDatosTopics) != 0:
                for topic_api_id,topic_nombre in tuplaDatosTopics:
                    self.dictTopics[topic_api_id]=topic_nombre

                self.listWidget_topicsRetroalimentacion.addItems(  tuple( self.dictTopics.values() ) )
                self.listWidget_topicsTareasProgramas.addItems(  tuple( self.dictTopics.values() )  )


    def refrescarClases(self):

        if self.curso_id!=None:
            respuestaAfirmativa=self.msg_preguntarAcercaRefrescarTopics()
            if respuestaAfirmativa:
                # eliminamos todas los elementos de la base de datos
                # consultamos y agregamos a la base de datos

                tuplaDatosTopics = self.classRoomControl.get_listaDatosTopicsCurso(self.curso_id)
                print("TDODOS LOS TOPICS API: ", tuplaDatosTopics)

                if tuplaDatosTopics!=() and len(tuplaDatosTopics) != 0:
                    self.baseDatosLocalClassRoom.agregar_soloNuevosTopics(
                        tuplaDatos=tuplaDatosTopics,
                        curso_api_id=self.curso_id
                    )


                # keys= api_id de cada curso  values= nombre de cada curso
                self.dictCursos={}
                self.listWidget_topicsTareasProgramas.clear()
                self.listWidget_topicsRetroalimentacion.clear()


                tuplaDatosTopics=self.baseDatosLocalClassRoom.get_topicsLibres(course_id_api=self.curso_id)
                self.dictTopics={}

                if tuplaDatosTopics!=() and len(tuplaDatosTopics)!=0:
                    for topic_api_id,topic_nombre in tuplaDatosTopics:
                        self.dictTopics[topic_api_id]=topic_nombre

                    self.listWidget_topicsRetroalimentacion.addItems(  tuple( self.dictTopics.values() ) )
                    self.listWidget_topicsTareasProgramas.addItems(  tuple( self.dictTopics.values() )  )

                self.msg_exitoDescargarTopics()




    def agregarTopics(self):
        if len(self.dictTopics)>0:
            #programas_topic,retroalimentacion_topic

            programa_topic_index=self.listWidget_topicsTareasProgramas.currentRow()
            retroalimentacion_topic_index=self.listWidget_topicsRetroalimentacion.currentRow()

            if (programa_topic_index!=retroalimentacion_topic_index):
                programa_topic_nombre = self.listWidget_topicsTareasProgramas.currentItem().text()
                retroalimentacion_topic_nombre = self.listWidget_topicsRetroalimentacion.currentItem().text()

                respuestaAfirmativa=self.msg_preguntarConfirmacionEleccionTopics(
                    programas_topic=programa_topic_nombre,
                    retroalimentacion_topic=retroalimentacion_topic_nombre
                )

                if respuestaAfirmativa:
                    programa_topic_api_id=tuple( self.dictTopics.keys() )[programa_topic_index]
                    retroalimentacion_topic_api_id=tuple( self.dictTopics.keys() )[retroalimentacion_topic_index]


                    tupla_topic_programas=(programa_topic_api_id,programa_topic_nombre)
                    tupla_topic_retroalimentacion=(retroalimentacion_topic_api_id,retroalimentacion_topic_nombre)

                    self.baseDatosLocalClassRoom.actualizarEstadoTopic(
                        programas_topic_id=programa_topic_api_id,
                        retro_topic_id=retroalimentacion_topic_api_id
                    )

                    self.senal_agregoUnTopic.emit(  ( tupla_topic_programas,tupla_topic_retroalimentacion ) )
                    self.limpiarDeDatos()
                    self.close()

            else:
                self.msg_noPuedesElegirTopics_iguales()
        else:
            # no se pueden elegir los mismos topics
            self.msg_noPuedesElegirTopics_siNoHay()

    def  limpiarDeDatos(self):
        '''
        Vacia las list widget para que no tengan datos que cargar
        :return:
        '''

        self.dictTopics={}
        self.listWidget_topicsRetroalimentacion.clear()
        self.listWidget_topicsTareasProgramas.clear()



####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################

    def msg_preguntarConfirmacionEleccionTopics(self,programas_topic,retroalimentacion_topic):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = f"¿Los ejercicios de programacion que asignes se adjuntaran en el topic:<<{programas_topic}>> "
        mensaje += f"y las retroalimentaciones de dichos ejercicios se adjuntaran en el topic:<<{retroalimentacion_topic}>> "
        mensaje+="¿eso es correcto?"
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


    def msg_exitoDescargarTopics(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Ya se descargaron los topics que faltaban por mostrar, sin embargo "
        mensaje+="es importante recalcar que si no vez ningun cambio es por que no  "
        mensaje+="se encountraron topics nuevos"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


    def msg_noPuedesElegirTopics_iguales(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "El topic donde se adjuntaran los ejercicios de programacion "
        mensaje+="no puede ser el mismo topic en donde se adjuntaran las retroalimentaciones "
        mensaje+="de los ejercicios de programacion"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


    def msg_noPuedesElegirTopics_siNoHay(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Warning)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "No hay ningun conjunto de topics que seleccionar, sin embargo la solucion "
        mensaje += "consiste en que vayas a ClassRoom y crees dos topics y despues regreses  "
        mensaje += "al programa y le des clic sobre el boton con la leyenda igual a refrescar  "

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


    def msg_preguntarAcercaRefrescarTopics(self):
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Question)
            ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            mensaje = "Solo es recomendable refrescar cuando no vez los topics que deseas "
            mensaje+="¿en verdad los topcis que deseas seleccionar no se encuentra en la lista? "
            mensaje+="¿en verdad necesitas refrescar?"
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


    def msg_ningunaClaseRegistrada(self):
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Warning)
            ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            mensaje = "No tienes ninguna clase asignada, por favor crear una clase "
            mensaje+=" en classroom y despues da nuevamente da clic sobre el icono "
            mensaje+=" de refrescar "

            mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()





if __name__ == '__main__':
    app = QApplication([])
    application = AgregadorTopics()
    application.show()
    app.exit(app.exec())