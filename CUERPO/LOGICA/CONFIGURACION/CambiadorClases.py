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


from CUERPO.DISENO.CONFIGURACION.CambiadorClases_d import Ui_Dialog
import recursos


class CambiadorClases(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):

    senal_ventanaFueCerrada= pyqtSignal(bool)  # id de tarea
    senal_operacionImportante=pyqtSignal(bool)
    senal_eligioUnCurso=pyqtSignal(tuple) # curso_api_id,  curso_nombre

    def __init__(self,baseDatosLocalClassRoom,classRoomControl):
        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)


        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.classRoomControl=classRoomControl


        self.dictCursos = {}
        self.cargarDatosClase()
        self.btn_refrescarLasClases.clicked.connect(self.refrescarClases)
        self.btn_realizarCambio.clicked.connect(self.realizarCambioClase)




    def prepararMostrar(self,curso_tuplaDatos):
        '''

        :param curso_tuplaDatos:
            - primer elemento: id del curso
            - segundo elemetno: nombre dle curso
        :return:
        '''

        api_id,nombre=curso_tuplaDatos

        self.bel_nombreClaseActual.setText(nombre)
        self.comboBox_clases.setCurrentText(nombre)

    def cargarDatosClase(self):

        tuplaDatosClases=self.baseDatosLocalClassRoom.get_tuplaClases()
        print("CLASES BASE DE DATOS:",tuplaDatosClases)

        if tuplaDatosClases==() or len(tuplaDatosClases)==0:
            tuplaDatosClases=self.classRoomControl.get_listaDatosCursos()
            print("CLASE DE LA API: ",tuplaDatosClases)
            self.baseDatosLocalClassRoom.add_tuplaCursos(tuplaDatos=tuplaDatosClases)

        self.dictCursos={}

        for curso_api_id,curso_nombre in tuplaDatosClases:
            self.dictCursos[curso_api_id]=curso_nombre

        self.comboBox_clases.clear()
        self.comboBox_clases.addItems( tuple( self.dictCursos.values() ) )


    def refrescarClases(self):

        respuestaAfirmativa=self.msg_preguntarAcercaRefrescarClases()
        if respuestaAfirmativa:
            # eliminamos todas los elementos de la base de datos
            # consultamos y agregamos a la base de datos

            print("Eliminando los cursos registrados")
            self.baseDatosLocalClassRoom.eliminarCursosRegistrados()
            tuplaDatosClases = self.classRoomControl.get_listaDatosCursos()
            print("Cursos obtenidos con la api",tuplaDatosClases)


            # keys= api_id de cada curso  values= nombre de cada curso
            self.dictCursos={}

            if len(tuplaDatosClases)>0:
                self.baseDatosLocalClassRoom.add_tuplaCursos(tuplaDatos=tuplaDatosClases)
                for curso_api_id, curso_nombre in tuplaDatosClases:
                    self.dictCursos[curso_api_id]=curso_nombre
            else:
                self.msg_ningunaClaseRegistrada()

            self.comboBox_clases.clear()
            self.comboBox_clases.addItems( tuple( self.dictCursos.values() ) )
            self.msg_exitoDescargarClasesClassroom()




    def realizarCambioClase(self):
        if len(self.dictCursos)>0:
            cursoElegido_index=self.comboBox_clases.currentIndex()
            cursoElegido_nombre=self.comboBox_clases.currentText()
            respuestaPositiva=self.msg_preguntarConfirmacionEleccionCurso(nombreCursoSeleccionado=cursoElegido_nombre)
            if respuestaPositiva:
                cursoElegido_api_id=tuple(self.dictCursos.keys())[cursoElegido_index]
                cursoElegido_tuplaDatos=(cursoElegido_api_id,cursoElegido_nombre)
                print("curso seleccionado:",cursoElegido_tuplaDatos)

                self.senal_eligioUnCurso.emit(cursoElegido_tuplaDatos)
                self.close()


        # no puedes elegir cuando no hay ningun curso disponible
        else:
            self.msg_noPuedesElegirCurso_siNoHay()





##########################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################

    def msg_preguntarConfirmacionEleccionCurso(self,nombreCursoSeleccionado):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = f"¿En verdad el curso con el nombre de: <<{nombreCursoSeleccionado}>> "
        mensaje += " es el curso que deseas elegir? "
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


    def msg_exitoDescargarClasesClassroom(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Ya se descargaron las clases de classroom que faltaban por mostrar, sin embargo "
        mensaje+="es importante recalcar que si no vez ningun cambio es por que no  "
        mensaje+="se encountraron clases de classroom  nuevas"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()



    def msg_noPuedesElegirCurso_siNoHay(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Warning)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "No puedes seleccionar ningun curso, si no tienes ningun curso registrado, "
        mensaje += "en caso de que si tengas un curso registrado y no se visualice aqui,  "
        mensaje += "por favor da clic sobre el boton refrescar para que aparesca entre los  "
        mensaje += "cursos elegibles "

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()



    def msg_preguntarAcercaRefrescarClases(self):
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Question)
            ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            mensaje = "Solo es recomendable refrescar cuando no vez la clase que deseas "
            mensaje+="¿en verdad la clase que deseas no se encuentra en la lista? de ser "
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


    #def closeEvent(self, event):

        #event.accept()
        #event.ignore()  # No saldremos del evento


if __name__ == '__main__':
    app = QApplication([])
    application = CambiadorClases()
    application.show()
    app.exit(app.exec())