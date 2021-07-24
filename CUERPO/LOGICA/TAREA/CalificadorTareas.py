from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt


from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5 import QtGui


from CUERPO.DISENO.TAREA.CalificadorTareas_d import  Ui_Dialog
import recursos


class CalificadorTareas(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):

    NO_COLUMNAS=3

    senal_calificadorTareas_cerro=pyqtSignal( dict ) # se emitira un señal cuando se cierre
                                                   # el calificador para que se desbloque
                                                   # el programa


    def __init__(self,administradorProgramasClassRoom):

        QtWidgets.QDialog.__init__(self)
        recursos.HuellaAplicacion.__init__(self)
        Ui_Dialog.__init__(self)

        self.administradorProgramasClassRoom=administradorProgramasClassRoom
        self.setupUi(self)

        self.LISTA_CALIFICAR = True  # 0=> Se acaba de terminar de calificar
        # 1=> Esta lista para calificar nuevamente

        self.configurarTabla()

        self.spinBox_tareasACalificar.setMinimum(0)

        self.spinBox_tareasACalificar.valueChanged.connect(self.tareasDeseanCalificar_actualizar)



        self.administradorProgramasClassRoom.hiloCalificadorTarea.senal_unAlumnoCalificado.connect(self.mostrarDatosAlumnoCalificado)
        self.administradorProgramasClassRoom.hiloCalificadorTarea.senal_terminoCalificar.connect( self.avisarTerminoCalificar )
        self.administradorProgramasClassRoom.hiloCalificadorTarea.senal_errorRed.connect( self.mostrarErrorRed )

        self.btn_calificar.clicked.connect(self.calificarTarea_or_alistarParaCalificar)
        self.btn_detener.clicked.connect(self.detenerProcesoCalificar)
        self.btn_actualizarInfoCourseworks.clicked.connect(self.refrescarDatosCourseWork)

        self.tareasLogradasCalificar=0





    def mostrarErrorRed(self,tuplaDatos):
        tituloError,error=tuplaDatos

        self.msg_errorRed(
            tituloError=tituloError,
            error=error
        )


    def detenerProcesoCalificar(self):
        respuestaPositiva=self.msg_detenerCalificador()
        if respuestaPositiva:
            self.btn_detener.setEnabled(False)
            self.administradorProgramasClassRoom.hiloCalificadorTarea.terminarHilo()


    def avisarTerminoCalificar(self,terminoNaturalmente):
        '''
        Si se termino de calificar los valores de tareas a calificar pudieron cambiar...

        :param terminoNaturalmente:
        :return:
        '''

        self.spinBox_tareasACalificar.setMaximum(self.numeroTareasCalificar)

        self.ponerModoCalificando(False)
        if terminoNaturalmente:
            self.msg_calificadorTerminoCalificar()


    def ponerModoCalificando(self,modoCalificando):
        if modoCalificando:
            self.btn_calificar.setEnabled(False)
            self.btn_detener.setEnabled(True)
            self.spinBox_tareasACalificar.setEnabled(False)
            self.btn_actualizarInfoCourseworks.setEnabled(False)
        else:
            self.btn_calificar.setEnabled(True)
            self.btn_detener.setEnabled(False)
            self.btn_actualizarInfoCourseworks.setEnabled(True)


    def calificarTarea_or_alistarParaCalificar(self):
        '''
        Cuando se califica, los resultado aparecen una tabla, y el
        progressBar va avanzando en funcion del trabajo que vaya
        logrando, una vez terminado de calificar los datos se quedan asi
        por si el maestro los quiere revisar,

        :return:
        '''


        if self.LISTA_CALIFICAR:
            noTareasDeseanCalificar=self.spinBox_tareasACalificar.value()
            if noTareasDeseanCalificar>0:
                respuestaPositiva=self.msg_preguntarAcercaAccionCalificar(noTareasDeseanCalificar)
                if respuestaPositiva:
                    self.btn_calificar.setText('Calificar\nmas tareas')
                    self.ponerModoCalificando(True)
                    self.LISTA_CALIFICAR=False
                    self.administradorProgramasClassRoom.hiloCalificadorTarea.activarHiloParaCalificar()

                    self.tareasLogradasCalificar=0

                    self.administradorProgramasClassRoom.calificarEstudiantes(
                        courseWork_id=self.coursework_id,
                        courseWork_name=self.coursework_name,
                        noMaxEstudiantesCalificar=noTareasDeseanCalificar
                    )
            else:
                self.msg_minimoTareasCalificar()

        else:
            respuestaPositiva=self.msg_calificarMasTareas()
            if respuestaPositiva:
                self.LISTA_CALIFICAR=True
                self.tableWidget_alumnosCalif.setRowCount(0)
                self.btn_calificar.setText('Calificar')
                self.bel_noTareasCalificadas.setText('0')
                self.bel_noTareasAcalificar.setText('0')
                self.spinBox_tareasACalificar.setValue(0)
                self.spinBox_tareasACalificar.setMaximum(self.numeroTareasCalificar)
                self.spinBox_tareasACalificar.setEnabled(True)


    def cargarValoresEnElCalificador(self):

        self.tableWidget_alumnosCalif.setRowCount(0)

        self.bel_noTareasCalificadas.setText('0')
        self.bel_noTareasAcalificar.setText('0')
        self.btn_detener.setEnabled(False)

        self.LISTA_CALIFICAR = True
        self.btn_calificar.setText('Calificar')
        self.spinBox_tareasACalificar.setEnabled(True)


        self.spinBox_tareasACalificar.setMaximum(self.numeroTareasCalificar)
        self.spinBox_tareasACalificar.setValue(self.numeroTareasCalificar)

        self.bel_noTareasPorCalificar.setText( str(self.numeroTareasCalificar) )


        self.bel_noTareasCalificadasTotales.setText( str(self.numeroTareasCalificadasTotales) )
        self.bel_noTareasPorEntregar.setText( str(self.numeroTareasPorEntregar) )



    def mostrarDatosAlumnoCalificado(self,tuplaDatosAlumnoCalificado):
        noRenglones = self.tableWidget_alumnosCalif.rowCount()
        self.tableWidget_alumnosCalif.insertRow(noRenglones)
        #nombre,correo,califacion
        bienCalificado=tuplaDatosAlumnoCalificado[0]

        for noDato,dato in enumerate(tuplaDatosAlumnoCalificado[1:]):
            # el dato numero cero no cuenta
            celda=QtWidgets.QTableWidgetItem(str(dato))
            celda.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget_alumnosCalif.setItem(noRenglones,noDato,celda )

        if bienCalificado:
            colorRenglon=recursos.App_Principal.COLOR_EXCELENTE
        else:
            colorRenglon=recursos.App_Principal.COLOR_MALO

        self.colorearRenglon(noRenglon=noRenglones,
                            color=colorRenglon)

        self.tareasLogradasCalificar+=1
        self.numeroTareasCalificadasTotales+=1
        self.numeroTareasCalificar-=1

        self.bel_noTareasCalificadas.setText( str(self.tareasLogradasCalificar)  )
        self.bel_noTareasPorCalificar.setText( str(self.numeroTareasCalificar) )
        self.bel_noTareasCalificadasTotales.setText( str(self.numeroTareasCalificadasTotales) )


    def tareasDeseanCalificar_actualizar(self,numero):
        if numero!=None:
            self.bel_noTareasAcalificar.setText(str(numero))

    def refrescarDatosCourseWork(self):
        respuestaPositiva=self.msg_preguntar_refrescarDatosCourseWork()
        if respuestaPositiva:
            dictDatosEntrega=self.administradorProgramasClassRoom.getDatosCourseWork(
                courseWork_id=self.coursework_id
            )

            self.numeroTareasCalificar=dictDatosEntrega['porCalificar']
            self.numeroTareasCalificadasTotales=dictDatosEntrega['calificados']
            self.numeroTareasPorEntregar=dictDatosEntrega['porEntregar']

            self.cargarValoresEnElCalificador()
            self.msg_refrescoExitosamente()



    def cargarDatosTareaCalificar(self,cousework_id,coursework_name,coursework_fechaCreacion,dictDatosEntrega):
        self.coursework_id=cousework_id
        self.coursework_name=coursework_name

        self.bel_nombreCourseWork.setText(self.coursework_name)
        self.bel_fechaCreacion.setText(coursework_fechaCreacion)

        self.numeroTareasCalificar=dictDatosEntrega['porCalificar']
        self.numeroTareasCalificadasTotales=dictDatosEntrega['calificados']
        self.numeroTareasPorEntregar=dictDatosEntrega['porEntregar']

        self.cargarValoresEnElCalificador()









    def colorearRenglon(self,noRenglon,color):
        for c in range(self.NO_COLUMNAS):
            self.tableWidget_alumnosCalif.item(noRenglon,c).setBackground(QtGui.QColor(color))


    def configurarTabla(self):

        self.tableWidget_alumnosCalif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_alumnosCalif.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_alumnosCalif.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget_alumnosCalif.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)


        header = self.tableWidget_alumnosCalif.horizontalHeader()

        stylesheet = f"""QTableView{{ background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }}; """

        self.tableWidget_alumnosCalif.setStyleSheet(stylesheet)

        self.tableWidget_alumnosCalif.verticalHeader().setDefaultSectionSize(40)

        # la tabla tiene 3 columnas
        # ("NOMBRE","DATA_TIME", "PREGUNTAS")
        header = self.tableWidget_alumnosCalif.horizontalHeader()
        for columna in range(0,self.NO_COLUMNAS):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)
            #header.setSectionResizeMode(columna, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)




    def closeEvent(self, event):
        '''
        Cuando el usuario le de clic izquierdo sobre el boton de cerra el programa, el metodo
        que se llamara es este, el cual le preguntara al usuario si esta seguro de cerrar el
        programa, en caso de que su respuesta sea afirmativa se cerrara el programa.
        '''

        respuestaPositiva=self.msf_preguntarSalidaVentana()
        if respuestaPositiva:
            dictDatosEntrega={}
            dictDatosEntrega['porCalificar']=self.numeroTareasCalificar
            dictDatosEntrega['calificados']=self.numeroTareasCalificadasTotales
            dictDatosEntrega['porEntregar']=self.numeroTareasPorEntregar
            self.senal_calificadorTareas_cerro.emit( dictDatosEntrega )
            event.accept()
        else:
            event.ignore()  # No saldremos del evento

####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################
    def msf_preguntarSalidaVentana(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Seguro que quieres salir?"
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


    def msg_preguntarAcercaAccionCalificar(self,noTareasCalificar):

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿En verdad quieres calificar {} tareas?".format(noTareasCalificar)
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


    def msg_minimoTareasCalificar(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "No se pueden calificar cero tareas"
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


    def msg_refrescoExitosamente(self):

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Se ha refrescado exitosamente los datos de courseworks "
        mensaje+="si no vez nuevos courseworks por calificar es porque no "
        mensaje+="hay nuevas entregas hechas por tus alumnos"
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)


        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


    def msg_preguntar_refrescarDatosCourseWork(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Solo es recomendable refrescar si deseas ver si ya no hay mas tareas por calificar "
        mensaje+="¿en realidad deseas refrescar?"
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



    def msg_detenerCalificador(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿En verdad deseas detener el proceso de calificacion? "
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

    def msg_calificarMasTareas(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Recuerda que si deseas calificar mas tareas aparte de las que ya calificaste "
        mensaje+="se limpiaran los datos ocacionados por la calificacion previa ¿en realidad deseas "
        mensaje+="calificar nuevamente"
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

    def msg_errorRed(self,tituloError,error):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Critical)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Al calificar las tareas se ha presentado un error de conexion "
        mensaje+= "el cual es el siguiente: <<{}:    {}>>".format(tituloError,error)

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)


        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()




    def msg_calificadorTerminoCalificar(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Se ha terminado de calificar con exito, recuerda que si "
        mensaje+="deseas calificar mas tareas da clic izquierdo sobre el boton "
        mensaje+="con la leyenda <<Calificar mas tareas>> "
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)


        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


if __name__ == '__main__':
    app = QApplication([])
    application = CalificadorEnDirecto()
    application.show()
    app.exit(app.exec())