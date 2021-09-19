from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt

from PyQt5 import QtWidgets

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5 import QtCore,QtGui

from CUERPO.DISENO.TAREA.AgregadorCourseWorks_d import Ui_Dialog
import recursos

class AgregadorCourseWorks(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):
    NO_COLUMNAS=2 # titulo,,fecha

    senal_regresar= pyqtSignal(bool)  # id de tarea
    senal_calificarDirecto=pyqtSignal(bool)

    senal_courseWork_selec=pyqtSignal(tuple) #id,nombre

    def __init__(self,administradorProgramasClassRoom):
        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)

        self.administradorProgramasClassRoom=administradorProgramasClassRoom

        self.dictCourseWorks = {}
        self.configurarTabla()


        self.tableWidget.doubleClicked.connect(self.courseWork_elegido)
        self.btn_refrescarCourseWorks.clicked.connect(self.refrescarCourseWorks)



    def courseWork_elegido(self,item):
        renglon=item.row()

        courseWorkSelec_id=tuple(self.dictCourseWorks.keys())[renglon]
        courseWorkSelec_nombre=self.dictCourseWorks[courseWorkSelec_id]
        courseWorkSelec_fecha=self.tableWidget.item(renglon,1).text()

        respuestaPositiva=self.msg_preguntarConfirmacionEleccionCourseWorks(
            nombreCourseWork=courseWorkSelec_nombre
        )
        if respuestaPositiva:
            tuplaDatosMandar=(courseWorkSelec_id,courseWorkSelec_nombre,courseWorkSelec_fecha)
            self.senal_courseWork_selec.emit(  tuplaDatosMandar  )
            self.administradorProgramasClassRoom.seleccionarBaseLocal_coursework(courseWorkSelec_id)
            self.close()



    def cargarDatos_courseWorks(self):
        '''
        Para que esto sea habra el apartado de tareas debe tener definido
        un curso y un topic asi que ya no seran necesarias validaciones
        en ese tema

        :param curso_id:
        :return:
        '''


        if self.administradorProgramasClassRoom.configuracionCalificador.datosListosApartadoTareas():
            tuplaDatosCourseWorks=self.administradorProgramasClassRoom.get_courseWorksLibres_baseDatosLocal()

            self.dictCourseWorks = {}
            self.tableWidget.setRowCount(0) # borrando la tabla

            tuplaDatosMostrar=[]
            self.dictCourseWorks={}
            if tuplaDatosCourseWorks != () and len(tuplaDatosCourseWorks) != 0:
                for courseWork_api_id,titulo,descripccion,fechaCreacion in tuplaDatosCourseWorks:
                    tuplaDatosMostrar.append( (titulo,fechaCreacion) )
                    self.dictCourseWorks[courseWork_api_id]=titulo

                self.cargarDatosEnTabla(tuplaDatos=tuplaDatosMostrar)




    def refrescarCourseWorks(self):

        if self.administradorProgramasClassRoom.configuracionCalificador.datosListosApartadoTareas():
            respuestaAfirmativa=self.msg_preguntarAcercaRefrescarCourseWorks()
            if respuestaAfirmativa:
                # Consultamos los datos en la API
                tuplaDatosCourseWorks = self.administradorProgramasClassRoom.get_dictTareasDejadas()
                print("TDODOS LOS TOPICS API: ", tuplaDatosCourseWorks)

                # Si hay datos vamos a descargarlos en la base de datos local
                if tuplaDatosCourseWorks!=() and len(tuplaDatosCourseWorks) != 0:
                    self.administradorProgramasClassRoom.agregarCourseWorks_baseDatosLocal(
                        tuplaDatos=tuplaDatosCourseWorks
                    )


                # Ya que se cargaron los datos regresaremos a los valores inciiales
                self.dictCourseWorks={}
                self.tableWidget.setRowCount(0)

                # Ahora consultaremos de la base de datos local para que nos de los nuevos courseworks
                tuplaDatosCourseWorks=self.administradorProgramasClassRoom.get_courseWorksLibres_baseDatosLocal()


                tuplaDatosMostrar=[]
                self.dictCourseWorks={}
                if tuplaDatosCourseWorks != () and len(tuplaDatosCourseWorks) != 0:
                    for courseWork_api_id,titulo,descripccion,fechaCreacion in tuplaDatosCourseWorks:
                        tuplaDatosMostrar.append( (titulo,fechaCreacion) )
                        self.dictCourseWorks[courseWork_api_id]=titulo

                    self.cargarDatosEnTabla(tuplaDatos=tuplaDatosMostrar)

                self.msg_exitoDescargarCourseWorks()

####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################


    def msg_preguntarConfirmacionEleccionCourseWorks(self,nombreCourseWork):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = f"¿El CourseWork que deseas agregar en verdad es:<<{nombreCourseWork}>>?"
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


    def msg_preguntarAcercaRefrescarCourseWorks(self):
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Question)
            ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            mensaje = "Solo es recomendable refrescar cuando no vez el CourseWork o CourseWorks que deseas "
            mensaje+="¿en verdad los CourseWorks que deseas seleccionar no se encuentran en la lista? "
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


    def msg_exitoDescargarCourseWorks(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Ya se descargaron los CourseWorks que faltaban por mostrar, sin embargo "
        mensaje+="es importante recalcar que si no vez ningun cambio es por que no  "
        mensaje+="se encontraron CourseWorks nuevos"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


##################################################################################################################################################
# OTRAS COSAS
##################################################################################################################################################


    def configurarTabla(self):

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        header = self.tableWidget.horizontalHeader()

        #stylesheet = f"""
        #QTableView{{selection-background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS};
        #background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }};
        #"""

        stylesheet = f"""QTableView{{ 
        selection-background-color:{recursos.App_Principal.COLOR_TOPIC_SELECCIONADO};
        background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }}; """

        # stylesheet += "background-color:" + self.COLOR_TABLA + ";}"
        self.tableWidget.setStyleSheet(stylesheet)

        self.tableWidget.verticalHeader().setDefaultSectionSize(40)

        # la tabla tiene 3 columnas
        # ("NOMBRE","DATA_TIME", "PREGUNTAS")
        header = self.tableWidget.horizontalHeader()
        for columna in range(0,self.NO_COLUMNAS):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)
            #header.setSectionResizeMode(columna, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)




    def cargarDatosEnTabla(self,tuplaDatos):
        '''
        Cargara los datos de los cuestionarios en la tabla, los datos que cargara
        son los que  vienen en el parametro cuyo nombre es: 'tuplaDatos'

        :param tuplaDatos:
         ¿Como vendran los datos?
         (
            ( Nombre,Calificadas,Por calificar,Fecha emision,Promedio ),
            ( Nombre,Calificadas,Por calificar,Fecha emision,Promedio ),
                                    .
                                    .
                                    .
            ( Nombre,Calificadas,Por calificar,Fecha emision,Promedio )
        )

        :return:
        '''

        # Si tan siquiera hay un dato...

        if len(tuplaDatos)>0:

            # Nombre,Calificadas,Por calificar,Fecha emision,Promedio
            FILAS = len(tuplaDatos)
            COLUMNAS = self.NO_COLUMNAS

            self.noCuestionarios = FILAS
            self.tableWidget.setRowCount(FILAS)

            for f in range(FILAS):
                for c in range(COLUMNAS):
                    dato_celda_string = str(tuplaDatos[f][c])
                    a = QtWidgets.QTableWidgetItem(dato_celda_string)
                    a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                    self.tableWidget.setItem(f, c, a)





if __name__ == '__main__':
    app = QApplication([])
    application = AgregadorCourseWorks()
    application.show()
    app.exit(app.exec())