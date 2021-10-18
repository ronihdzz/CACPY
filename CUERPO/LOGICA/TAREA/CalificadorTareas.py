
'''
CalificadorTareas.py :
    Esta clase sirve para calificar las entregas que han realizado los alumnos del usuario
    y que pertenecen a la tarea seleccionada..
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import Qt,pyqtSignal

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.DISENO.TAREA.CalificadorTareas_d import  Ui_Dialog
import recursos


class CalificadorTareas(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):
    '''
    Esta clase sirve para calificar las entregas que han realizado los alumnos del usuario
    y que pertenecen a la tarea seleccionada.
    '''


    senal_calificadorTareas_cerro=pyqtSignal( dict ) # se emitira esta señal cuando se cierre
                                                     # la clase, el diccionario que se emitira
                                                     # contentra las siguientes llaves:
                                                     # 'porCalificar','calificados' y 'porEnntregar'


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


        self.LISTA_CALIFICAR = True  # False => Se acaba de terminar de calificar
                                     # True => Esta lista para calificar nuevamente

        self.configurarTabla()

        self.spinBox_tareasACalificar.setMinimum(0)

        self.spinBox_tareasACalificar.valueChanged.connect(self.tareasDeseanCalificar_actualizar)



        self.administradorProgramasClassRoom.hiloCalificadorTarea.senal_unAlumnoCalificado.connect(self.mostrarDatosAlumnoCalificado_enTablaAlumnosCalificados)
        self.administradorProgramasClassRoom.hiloCalificadorTarea.senal_terminoCalificar.connect( self.avisarTerminoCalificar )
        self.administradorProgramasClassRoom.hiloCalificadorTarea.senal_errorRed.connect( self.mostrarErrorRed )

        self.btn_calificar.clicked.connect(self.calificarTarea_or_alistarParaCalificar)
        self.btn_detener.clicked.connect(self.detenerProcesoCalificar)
        self.btn_actualizarInfoCourseworks.clicked.connect(self.refrescarDatosCourseWork)

        self.tareasLogradasCalificar=0


    def cargarDatosTareaCalificar(self,cousework_id,coursework_name,coursework_fechaCreacion,dictDatosEntrega):
        '''
        Cargara los datos de las entregas de la tarea que el usuario selecciono, por tal motivo hara las modificaciones
        respectivas en las label de la GUI
        '''

        self.coursework_id=cousework_id
        self.coursework_name=coursework_name

        self.bel_nombreCourseWork.setText(self.coursework_name)
        self.bel_fechaCreacion.setText(coursework_fechaCreacion)

        self.numeroTareasCalificar=dictDatosEntrega['porCalificar']
        self.numeroTareasCalificadasTotales=dictDatosEntrega['calificados']
        self.numeroTareasPorEntregar=dictDatosEntrega['porEntregar']

        self.cargarValoresEnElCalificador()

    def cargarValoresEnElCalificador(self):
        '''
        Este metodo esta pensado para llamarse despues de que se refrescaron
        las entregas de las tareas, ya que cuando esto sucede puede que
        se registren mas entregas de tareas de las que se habian registrado
        anteriormente y esto puede pasar por que los alumnos pueden subir su
        tarea en cualquier instante.

        Lo que hara este metodo es:
            * Prepara a la clase para calificar tareas por tal motivo cambia
            el valor de la variable bandera: self.LISTA_CALIFICAR a un valor
            de True, entre otras cosas mas
            * Cambia el valor maximo del spinBox al valor de: self.numeroTarreasCalificar,
            ya que este pudo cambiar al refrescarse los datos que se tenian de las
            entregas de las tareas.
            * Actualiza otros valores de la GUI que pudieron cambiar al actualizar los
            datos que se tenian acerca de las entregas de las tareas
        '''


        # se limpia la tabla
        self.tableWidget_alumnosCalif.setRowCount(0)


        self.bel_noTareasCalificadas.setText('0')
        self.bel_noTareasAcalificar.setText('0')

        self.LISTA_CALIFICAR = True
        self.btn_calificar.setText('Calificar')

        self.spinBox_tareasACalificar.setEnabled(True)
        self.btn_detener.setEnabled(False)

        self.spinBox_tareasACalificar.setMaximum(self.numeroTareasCalificar)
        self.spinBox_tareasACalificar.setValue(self.numeroTareasCalificar)

        self.bel_noTareasPorCalificar.setText( str(self.numeroTareasCalificar) )


        self.bel_noTareasCalificadasTotales.setText( str(self.numeroTareasCalificadasTotales) )
        self.bel_noTareasPorEntregar.setText( str(self.numeroTareasPorEntregar) )


    def mostrarErrorRed(self,tuplaDatos):
        '''
        Este metodo se encargar


        a de mostrar el error que se presento
        a la hora de calificar las tareas de programacion

        Parámetros:
            tuplaDatos (tuple): Es una tupla de dos elementos en donde:
                * El primer elemento (str) :Es el  titulo del error que
                se presento
                * El segundo elemento (str): Es la excepccion que
                se presento
        '''


        tituloError,error=tuplaDatos

        self.msg_errorRed(
            tituloError=tituloError,
            error=error
        )

    def detenerProcesoCalificar(self):
        '''
        Este metodo se encargara de detener el proceso de calificacion
        de tareas de programación
        '''

        # preguntando si en realidad se desea detener el proceso de calificacion
        # de tareas
        respuestaPositiva=self.msg_detenerCalificador()
        if respuestaPositiva:
            self.btn_detener.setEnabled(False)
            self.administradorProgramasClassRoom.hiloCalificadorTarea.terminarHilo()


    def avisarTerminoCalificar(self,terminoNaturalmente):
        '''
        Este metodo se llamara cuando se termine de calificar las entregas de
        la tarea de programacion, y lo que hara este metodo es lo siguiente:
            * Si no ocurrio ningun error al calificar las entregas de la tarea,o si
            no se interrumpio la calificacion de las entregas de la tarea, entonces
            le mostrara un mensaje al usuario para informarle que se termino de
            calificar exitosamente todas las entregas que se pidieron calificar de
            la tarea
            * Restablecera la a la clase en el modo de: YA NO CALIFICANDO, ya que
            la clase se comporta de diferente forma cuando se esta calificando
            a cuando no se esta calificando.

        Parámetros:
            terminoNaturalmente (bool): Si el valor de dicho parametro es igual a
            False, significa que  se presento un error al calificar las entregas de
            la tarea o significa que el usuario interrumpio el proceso de calificacion
            de tareas.Si el valor de dicho parametro es igual a True: significa que se
            calificaron exitosamente el numero de entregas que el usuario puso.
        '''

        # Por medio del spinBox el usuario puede elegir la cantidad de tareas
        # que desea calificar por tal motivo cuando se deja de calificar tareas
        # se actualiza al valor maximo del 'spinBox' ya que al califcar tareas,
        # reducio el numero de tareas que restan por calificar.
        self.spinBox_tareasACalificar.setMaximum(self.numeroTareasCalificar)

        # Haciendo las configuraciones respectivas a la clase, cuando esta esta
        # en modo de NO CALIFICANDO
        self.ponerModoCalificando(False)

        # Si no ocurrio a calificar ningun errro al calificar las entregas de la tarea
        # o si no se detuvo la calificacion de las tareas.
        if terminoNaturalmente:
            self.msg_calificadorTerminoCalificar()


    def ponerModoCalificando(self,modoCalificando):
        '''
        Esta clase tiene dos modos diferentes de actuar, en funcion de
        si se esta calificando entregas de tareas o no. El parametro:
        'modoCalificando' si vale True significa que se esta calificando
        entregas de tareas, si vale False significa que no se esta calificando
        entregas de tareas.

        * Si se estan calificando entregas de tareas de programacion
        este metodo:
            Desabilitara:
                -  El boton de calificar
                -  El spinBox  en donde se indican cuantas entregas se
                desean calificar
                -  El boton de actualizar entrega de tareas
            Habilitara: unicamente el boton de detener proceso de
            calificacion de tareas

        * Si NO SE estan calificando entregas de tareas de programacion
        este metodo:
            Habilitara:
                -  El boton de calificar
                -  El spinBox  en donde se indican cuantas entregas se
                desean calificar
                -  El boton de actualizar entregaS de tareas
            Desabilitara: unicamente el boton de detener proceso de
            calificacion de tareas

        Parámetros:
            modoCalficando (bool):
                - Si vale True significa que se esta calificando
                entregas de tareas
                - Si vale False significa que no se esta calificando
                entregas de tareas.
        '''

        if modoCalificando:
            self.btn_calificar.setEnabled(False)
            self.btn_detener.setEnabled(True)
            self.spinBox_tareasACalificar.setEnabled(False)
            self.btn_actualizarInfoCourseworks.setEnabled(False)
        else:
            self.btn_calificar.setEnabled(True)
            self.spinBox_tareasACalificar.setEnabled(True)
            self.btn_detener.setEnabled(False)
            self.btn_actualizarInfoCourseworks.setEnabled(True)


    def calificarTarea_or_alistarParaCalificar(self):
        '''
        Este metodo se llamara cuando el usuario de clic sobre determinado
        boton.
        Este metodo se comportara diferente en funcion del valor almacenado
        en la variable de bandera: 'self.LISTA_CALIFICAR'

        Si self.LISTA_CALIFICAR es igual a True:
            * Significara que la clase esta lista para calificar el numero de entregas
            que  el usuario indico en spinbox, por lo cual este metodo al ser llamado:
                - Primero le preguntara al usuario si en realidad desea calificar
                esa cantidad de entregas.
                - Si el usuario responde positivamente lo anterior entonces este
                metodo iniciara con el proceso de calificacion

        Si self.LISTA_CALIFICAR es igual a False:
            * Significara que la clase acaba de calificar entregas de tareas, por lo tanto
            contiene  aun las calificaciones obtenidas de dichas entregas en la tabla,por
            lo cual este metodo al ser llamado:
                - Primero le preguntara al usuario si esta seguro de calificar mas tareas
                advirtiendole que se borraran de la tabla lo datos que se muestran de las
                tareas ya fueron calificadas.
                - Si el usuario responde positivamente entonces este metodo procedera a
                limpiar la tabla y a actualizar el valor de la variable bandera:
                self.LISTA_CALIFICAR para que la proxima vez que sea llamado este metodo
                ya se puedan calificar el numero de entregas indicadas por el usuario
        '''

        # ¿ la clase esta lista para calificar mas tareas de programacion?
        if self.LISTA_CALIFICAR:
            # obteniendo el numero de entregas que desea calificar el usuario
            noTareasDeseanCalificar=self.spinBox_tareasACalificar.value()

            # ¿el usuario por lo menos desea calificar 1 entrega?
            if noTareasDeseanCalificar>0:

                # preguntando al usuario si en realidad esta seguro de calificar el numero de entregas
                # que selecciono
                respuestaPositiva=self.msg_preguntarAcercaAccionCalificar(noTareasDeseanCalificar)
                if respuestaPositiva:
                    # El texto del boton cambia ya que  el usuario acaba de iniciar el proceso
                    # de calificacion de las entregas de la tarea, y cuando se termine de calificar
                    # todas las entregas que el usuario indico, se  debera dar clic izquierdo sobre
                    # este boton para poder volver a calificar mas tareas.
                    self.btn_calificar.setText('Calificar\nmas tareas')
                    self.ponerModoCalificando(True)
                    self.LISTA_CALIFICAR=False
                    self.administradorProgramasClassRoom.hiloCalificadorTarea.activarHiloParaCalificar()
                    self.tareasLogradasCalificar=0
                    # la siguiente funcion ejecuta el hilo que se encarga de obtener  la calificacion
                    # de las entregas de la tarea.
                    self.administradorProgramasClassRoom.calificarEstudiantes(
                        courseWork_id=self.coursework_id,
                        courseWork_name=self.coursework_name,
                        noMaxEstudiantesCalificar=noTareasDeseanCalificar
                    )
            else:
                self.msg_minimoTareasCalificar()

        # la clase no esta lista para calificar mas tareas
        else:
            # se le pregunta al usuario si en realidad desea calificar mas tareas, y se le advierte
            # que al confirmar lo anterior se borraran los datos de las tareas ya calificadas
            respuestaPositiva=self.msg_calificarMasTareas()

            if respuestaPositiva:
                self.LISTA_CALIFICAR=True

                # preparando los datos que se muestran para calificar
                # nuevamente entregas de taeas.
                self.tableWidget_alumnosCalif.setRowCount(0)
                self.btn_calificar.setText('Calificar')
                self.bel_noTareasCalificadas.setText('0')
                self.bel_noTareasAcalificar.setText('0')
                self.spinBox_tareasACalificar.setValue(0)
                self.spinBox_tareasACalificar.setMaximum(self.numeroTareasCalificar)
                self.spinBox_tareasACalificar.setEnabled(True)





    def mostrarDatosAlumnoCalificado_enTablaAlumnosCalificados(self, tuplaDatosAlumnoCalificado):
        '''
        Este metodo se llamara cada vez que el programa termine de calificar una entrega
        de cada alumno, es decir este metodo sera llamado cada vez que  el programa haya
        calificado una tarea.
        El objetivo de este metodo es mostrar en la tabla de alumnos calificados el
        nombre, correo electronico y calificación que obtuvo el alumno cuya entrega se
        acabo de calificar.

        Parámetros:
            tuplaDatosAlumnoCalificado (tuple): Es una tupla con 4 elementos
                - el primer elemento (bool): Representa si el alumno NO presento un error al
                entregar la tarea, si su valor es True significa que el alumno NO presento
                ningun error al entregar su tarea, si su valor es False significa que el alumno
                presento un error al entregar su tarea.
                - el segundo elemento (str): Representa el nombre del alumno cuya entrega
                de tarea fue calificada
                - el tercer elemento (str): Representa el correo electronico del alumno
                cuya entrega de tarea fue calificada
                - el cuarto elemento (str): Representa la calificacion que obtuvo el
                alumno cuya entrega fue calificada.
        '''


        noRenglones = self.tableWidget_alumnosCalif.rowCount()
        self.tableWidget_alumnosCalif.insertRow(noRenglones)

        elAlumnoRealizoBienLaEntrega=tuplaDatosAlumnoCalificado[0]

        # adjuntando el nombre,correo y calificacion del alumno cuya entrega
        # de tarea fue califcada.
        for noDato,dato in enumerate(tuplaDatosAlumnoCalificado[1:]):
            celda=QtWidgets.QTableWidgetItem(str(dato))
            celda.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget_alumnosCalif.setItem(noRenglones,noDato,celda )

        if elAlumnoRealizoBienLaEntrega:
            colorRenglon=recursos.App_Principal.COLOR_EXCELENTE
        else:
            colorRenglon=recursos.App_Principal.COLOR_MALO

        self.colorearRenglon(noRenglon=noRenglones,
                            color=colorRenglon)

        # actualizando los valores de las tareas calificadas.
        self.tareasLogradasCalificar+=1
        self.numeroTareasCalificadasTotales+=1
        self.numeroTareasCalificar-=1

        # mostrando los nuevos cambios en las label respectivas de la GUI
        self.bel_noTareasCalificadas.setText( str(self.tareasLogradasCalificar)  )
        self.bel_noTareasPorCalificar.setText( str(self.numeroTareasCalificar) )
        self.bel_noTareasCalificadasTotales.setText( str(self.numeroTareasCalificadasTotales) )


    def tareasDeseanCalificar_actualizar(self,numero):
        '''
        Este metodo se llamara cada vez que el usuario cambie el valor de numero
        de tareas que desea calificar atravez del spin box.
        Lo que hara este metodo es mostrar en la label respectiva de la GUI el
        numero de tareas que el usuario esta decidiendo calificar.

        Parámetros:
            - numero (int) : Representa el numero de entregas que el usuario quiere
            calificar.
        '''

        if numero!=None:
            self.bel_noTareasAcalificar.setText(str(numero))



    def refrescarDatosCourseWork(self):
        '''
        El objetivo de este metodo es actualizar la informacion que tiene esta clase
        de las entregas de la tarea que los alumnos han realizado.

        Este metodo consultara a la API de google classroom para saber:
            - Cuantas entregas de dicha tarea ya han sido calificadas
            - Cuantas entregas de dicha tarea han sido entregadas pero NO calificadas
            - Cuantas entregas de dicha tarea faltan por entregar

        Despues de consultar la información mencionada anteriormente, este metodo
        actualizara los valores que tenia y los mostrara las label correspondiente
        ee la GUI
        '''


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



    def colorearRenglon(self,noRenglon,color):
        '''
        Coloreara en la tabla de entregas de tareas calificadas: el renglon cuyo valor
        es igual al parametro 'noRenglon'  de color cuyo valor de igual parametro 'color'

        Parámetros:
            - noRenglon (int): Dato de tipo entero que representa el numero renglon de la
            tabla topics seleccionables que se desea colorear
            - color (str) : Representa el color al cual se desea colorear el renglon, cabe
            aclarar que se espera que el color se defina en su valor hexadecimal,
            ejemplo: "#0DDEFF"
        '''

        for c in range(3):
            self.tableWidget_alumnosCalif.item(noRenglon,c).setBackground(QtGui.QColor(color))


    def configurarTabla(self):
        '''
        Se encargara de darle un formato a la tabla de entregas de tareas calificadas
         - Se encargara de definir el numero de columnas de la tabla
         - Se encargara de definirla interaccion que se tendra con dicha tabla.
         - Se encargara de definir el diseño de la tabla(color de tabla, color de renglones,etc)
        '''

        self.tableWidget_alumnosCalif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_alumnosCalif.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_alumnosCalif.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget_alumnosCalif.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.tableWidget_alumnosCalif.verticalHeader().setDefaultSectionSize(40)

        # la tabla tiene 3 columnas
        # ("NOMBRE","CORREO_EECTRONICO",CALIFICACION_DE_TAREA")
        header = self.tableWidget_alumnosCalif.horizontalHeader()
        for columna in range(0,3):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)


    def closeEvent(self, event):
        '''
        Cuando el usuario le de clic izquierdo sobre el boton de cerrar de esta clase, el metodo
        que se llamara es este, el cual le preguntara al usuario si esta seguro de cerrar el
        programa, en caso de que su respuesta sea afirmativa se cerrara el programa, sin emmbargo
        como es posible que el usuario al abrir esta ventana haya realizado la calificacion o
        la actualizacion de los datos de las entregas de la tarea seleccionada, entonces antes
        de cerrarse esta clase, mandara una señal con los datos que se tienen de las entregas
        de la tarea seleccionada, con el objetivo de que el receptor de esta señal pueda actualizar
        su informacion.
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
            event.ignore()

####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################

    def msf_preguntarSalidaVentana(self):
        '''
        Mostrara un cuadro de dialogo con el objetivo de: preguntarle al usuario
        si en realidad desea cerrar la aplicacion

        Returns:
            True : En caso de que el profesor presione el boton de 'Si'
            False: En caso de que el profesor presione el boton de 'No'
        '''

        mensaje = "¿Seguro que quieres salir?"

        resultado= self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado

    def msg_preguntarAcercaAccionCalificar(self,noTareasCalificar):
        '''
        Mostrara un cuadro de dialogo con el objetivo de: preguntarle al usuario
        si en realidad desea calificar dicho determinado numero de entregas que
        realizaron los alumnos del usuario de la tarea que el usuario selecciono

        Returns:
            True : En caso de que el profesor presione el boton de 'Si'
            False: En caso de que el profesor presione el boton de 'No'
        '''


        mensaje = "¿En verdad quieres calificar {} tareas?".format(noTareasCalificar)

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado


    def msg_minimoTareasCalificar(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que
        para calificar debe existir por lo menos una entrega que falte ser calificada.
        '''

        mensaje = "No se pueden calificar cero tareas"

        self.ventanaEmergenteDe_error(mensaje)

    def msg_refrescoExitosamente(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que se
        han actualizado y descargado con exito los datos de  las entregas de la tarea
        que se selecciono por el usuario
        '''

        mensaje = "Se ha refrescado exitosamente los datos de courseworks "
        mensaje+="si no vez nuevos courseworks por calificar es porque no "
        mensaje+="hay nuevas entregas hechas por tus alumnos"

        self.ventanaEmergenteDe_informacion(mensaje)

    def msg_preguntar_refrescarDatosCourseWork(self):
        '''
        Mostrara un cuadro de dialogo al usuario para preguntarle si
        en realidad desea refrescar.

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si
            desea  refrescar
            - False (bool): Si el usuario dijo que NO desea refrescar
        '''

        mensaje = "Solo es recomendable refrescar si deseas ver si ya no hay mas tareas por calificar "
        mensaje+="¿en realidad deseas refrescar?"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado

    def msg_detenerCalificador(self):
        '''
        Mostrara un cuadro de dialogo al usuario para preguntarle si
        en realidad desea detener el proceso de calificacion

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si
            - False (bool): Si el usuario dijo que NO
        '''


        mensaje = "¿En verdad deseas detener el proceso de calificacion? "

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return  resultado


    def msg_calificarMasTareas(self):
        '''
        Mostrara un cuadro de dialogo al usuario para preguntarle si desea calificar
        mas tareas de las que ya fueron calificadas

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si
            - False (bool): Si el usuario dijo que NO
        '''



        mensaje = "Recuerda que si deseas calificar mas tareas aparte de las que ya calificaste "
        mensaje+="se limpiaran los datos ocacionados por la calificacion previa ¿en realidad deseas "
        mensaje+="calificar nuevamente"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado

    def msg_errorRed(self,tituloError,error):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que se
        produjo un error al querer calificar automaticamente las tareas del alumno,
        '''


        mensaje = "Al calificar las tareas se ha presentado un error de conexion "
        mensaje+= "el cual es el siguiente: <<{}:    {}>>".format(tituloError,error)

        self.ventanaEmergenteDe_error(mensaje)

    def msg_calificadorTerminoCalificar(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle  al usuario que se
        termino de calificar exitosamente el numero de tareas que determino
        '''

        mensaje = "Se ha terminado de calificar con exito, recuerda que si "
        mensaje+="deseas calificar mas tareas da clic izquierdo sobre el boton "
        mensaje+="con la leyenda <<Calificar mas tareas>> "

        self.ventanaEmergenteDe_informacion(mensaje)

if __name__ == '__main__':
    app = QApplication([])
    application = CalificadorTareas()
    application.show()
    app.exit(app.exec())