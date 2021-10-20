
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
    y que pertenecen a la tarea seleccionada por el usuario
    '''


    senal_calificadorTareas_cerro=pyqtSignal( dict ) # se emitira esta señal cuando se cierre
                                                     # la clase, el diccionario que se emitira
                                                     # contentra las siguientes llaves:
                                                     # 'porCalificar','calificados' y 'porEnntregar'


    def __init__(self,administradorProgramasClassRoom):
        '''
        - administradorProgramasClassroom (objeto de la clase: AdministradorProgramasClassRoom): dicho
        objeto permite calificar tareas de los estudiantes  del classroom seleccionado por el usuario, este
        objeto tambien permite obtener informacion de una manera mas sencilla acerca de las tareas que se
        encuentran en la clase de classroom  y topic seleccionadas por el usuario
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


    def prepararParaMostrar(self,cousework_id,coursework_name,coursework_fechaCreacion,dictDatosEntrega):
        '''
        Hace las configuraciones necesarias en la clase  para que el usuario  pueda calificar las entregas realizadas 
        por sus estudiantes de la tarea que selecciono.Tambien carga los datos de las entregas realizadas por los 
        estudiantes en las respectivos apartados de la GUI

        Parámetros:
            coursework_id (str) : Representa el ID de la tarea que el usuario selecciono para calificar las
            entregas que ha realizado sus alumnos de dicha tarea
            coursework_name (str) : Nombre de la tarea que el usuario selecciono para  calificar las entregas
            que han realizado los alumnos de dicha tarea
            coursework_fechaCreacion (str): Fecha en la cual fue creada la tarea que el usuario selecciono para
            calificar las entregas  que han realizado los alumnos de dicha tarea
            dictDatosEntrega (dict) : Diccionario que contiene informacion acerca de las entregas que han realizado
            los alumnos de la tarea que selecciono el usuario.Dicho diccionario contiene las siguientes llaves:
                * 'porCalificar' : El value de esta llave sera el numero de alumnos que ya entrego la tarea, pero
                aun no han sido calificados
                * 'calificadas' : El value de esta llave sera el numero de alumnos que ya fueron calificados en
                la tarea que entregaron
                * 'porEntregar': El value de esta llave representa el numero de alumnos que aun no realizan la
                entrega de la tarea que el usuario selecciono
        '''


        self.coursework_id=cousework_id
        self.coursework_name=coursework_name

        self.bel_nombreCourseWork.setText(self.coursework_name)
        self.bel_fechaCreacion.setText(coursework_fechaCreacion)

        self.numeroTareasCalificar=dictDatosEntrega['porCalificar']
        self.numeroTareasCalificadasTotales=dictDatosEntrega['calificados']
        self.numeroTareasPorEntregar=dictDatosEntrega['porEntregar']

        self.actualizarLosDatosSeMuestran_deLasEntregas()
        self.ponerModoCalificando(modoCalificando=False)



    def refrescarDatosCourseWork(self,resfrecarAutomaticamente=False):
        '''
        Este metodo solo podra ser llamado cuando la clase este lista para calificar
        entregas de tareas, es decir cuando la variable bandera: ' self.LISTA_CALIFICAR'
        tenga un valor igual a True.

        El objetivo de este metodo es actualizar la informacion que tiene esta clase
        de las entregas de la tarea que los alumnos han realizado.

        Este metodo consultara a la API de google classroom para saber:
            - Cuantas entregas de dicha tarea ya han sido calificadas
            - Cuantas entregas de dicha tarea han sido entregadas pero NO calificadas
            - Cuantas entregas de dicha tarea faltan por entregar

        Despues de consultar la información mencionada anteriormente, este metodo
        actualizara los valores que tenia y los mostrara las label correspondientes
        de la GUI

        Parámetros:
            - refrescarAutomaticamente (bool): Si su valor es True, este metodo no le
            mostrara un cuadro emergente al usuaario para preguntarle si en realidad
            desea refrescar.Si su valor es False este metodo SI le  mostrara un cuadro
            emergente al usuario para preguntarle si en realidad desea refrescar.
        '''

        seVaArefrescar=True
        if resfrecarAutomaticamente is False:
            seVaArefrescar=self.msg_preguntar_refrescarDatosCourseWork()


        if seVaArefrescar:
            dictDatosEntrega=self.administradorProgramasClassRoom.getDatosCourseWork(
                courseWork_id=self.coursework_id
            )

            self.numeroTareasCalificar=dictDatosEntrega['porCalificar']
            self.numeroTareasCalificadasTotales=dictDatosEntrega['calificados']
            self.numeroTareasPorEntregar=dictDatosEntrega['porEntregar']

            self.actualizarLosDatosSeMuestran_deLasEntregas()
            if resfrecarAutomaticamente is False:
                self.msg_refrescoExitosamente()


    def actualizarLosDatosSeMuestran_deLasEntregas(self):
        '''
        Este metodo esta pensado para llamarse cuando puede que haya registrado
        un cambio en los siguientes datos:
            - Numero de alumnos que ya entrego la tarea, pero aun no han sido
            calificados
            - Numero de alumnos que ya fueron calificados en  la tarea que
            entregaron
            - Numero de alumnos que aun no realizan la entrega de la tarea que el
            usuario selecciono
        
        Lo que hara este metodo es actualizar los valores que se muestran en la GUI
        que representan a los valores mencionados anteriormente
        '''

        self.spinBox_tareasACalificar.setMaximum(self.numeroTareasCalificar)

        # se actualizan los siguiente valores ya que  pudo cambiar el valor de: 'self.numeroTareasCalificar'
        self.spinBox_tareasACalificar.setValue(0)
        self.bel_noTareasAcalificar.setText('0') 

        self.bel_noTareasPorCalificar.setText( str(self.numeroTareasCalificar) )
        self.bel_noTareasCalificadasTotales.setText( str(self.numeroTareasCalificadasTotales) )
        self.bel_noTareasPorEntregar.setText( str(self.numeroTareasPorEntregar) )



    def calificarTarea_or_alistarParaCalificar(self):
        '''
        Este metodo se llamara cuando el usuario de clic sobre determinado
        boton.
        Este metodo se comportara diferente en funcion del valor almacenado
        en la variable de bandera: 'self.LISTA_CALIFICAR'

        Si self.LISTA_CALIFICAR es igual a True:
            * Significara que la clase esta lista para calificar el numero de entregas
            que  el usuario indico en el spinbox, por lo cual este metodo al ser llamado:
                - Primero le preguntara al usuario si en realidad desea calificar
                la cantidad de tareas registrada en el spinBox
                - Si el usuario responde positivamente lo anterior entonces este
                metodo iniciara con el proceso de calificacion

        Si self.LISTA_CALIFICAR es igual a False:
            * Significara que la clase acaba de calificar entregas de tareas, por lo tanto
            contiene  aun las calificaciones obtenidas de dichas entregas en la tabla,por
            lo cual este metodo al ser llamado:
                - Primero le preguntara al usuario si esta seguro de calificar mas tareas
                advirtiendole que se borraran de la tabla lo datos que se muestran de las
                tareas que acabaron de ser calificadas.
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
                    self.ponerModoCalificando(True)
                    self.administradorProgramasClassRoom.hiloCalificadorTarea.activarHiloParaCalificar()
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
                self.refrescarDatosCourseWork(resfrecarAutomaticamente=True)

                # preparando a la clase para calificar las entregas de los estudiantes
                # que el usuario indique
                self.ponerModoCalificando(modoCalificando=False)


    def ponerModoCalificando(self,modoCalificando):
        '''
        Esta metodo tiene dos modos diferentes de actuar, en funcion de
        si se desea poner en la clase en el modo: "ESTOY CALIFICANDO,
        NO MOLESTAR" o en el modo: "YA ESTOY LISTA PARA CALIFICAR NUEVAMENTE"

        El valor que tome el parametro 'modoCalificando' es el que le dira a 
        este metodo en que modo poner a la clase:
            - Si su valor es True, el metodo pondra a la clase en el modo: 
            "ESTOY CALIFICANDO,NO MOLESTAR"
            - Si su valor es False, el metodo pondra a la clase en el modo:
            "YA ESTOY LISTA PARA CALIFICAR NUEVAMENTE"


        * En el modo "ESTOY CALIFICANDO,NO MOLESTAR" el metodo hara lo siguiente:
            * Desabilitara:
                -  El boton de calificar
                -  El spinBox  en donde se indican cuantas entregas se
                desean calificar
                -  El boton de actualizar entrega de tareas
            * Habilitara: unicamente el boton de detener proceso de
            calificacion de tareas

            * Cambiara el texto del boton para hacerle  entender al usuario
            que despues de que se haya finalizado el proceso de calificacion
            de entregas debera oprimirse este boton si se desea volver a calificar
            tareas

            * Cambiara el valor de la variable bandera 'self.LISTA_CALIFICAR' a valor
            igual a False


        * En el modo: "YA ESTOY LISTA PARA CALIFICAR NUEVAMENTE", el metodo hara 
        lo siguiente:
            * Habilitara:
                -  El boton de calificar
                -  El spinBox  en donde se indican cuantas entregas se
                desean calificar
                -  El boton de actualizar entregas de tareas
            * Desabilitara: unicamente el boton de detener proceso de
            calificacion de tareas

            * Cambiara el texto del boton para hacerle  entender al usuario
            que ya puede volver a calificar las tareas que indique en el
            spingBox si da clic izquierdo sobre ese boton

            * Cambiara el valor de la variable bandera 'self.LISTA_CALIFICAR' a valor
            igual a True

            * Se limpiara la tabla en donde se muestran las calificaciones de las entregas
            de los alumnos

            * Se limpiaran las label que muestran las entregas que se van calificando en 
            tiempo real.
        
        Parámetros:
            modoCalficando (bool):
            - Si su valor es True, el metodo pondra a la clase en el modo: 
            "ESTOY CALIFICANDO,NO MOLESTAR"
            - Si su valor es False, el metodo pondra a la clase en el modo:
            "YA ESTOY LISTA PARA CALIFICAR NUEVAMENTE"

        '''

        if modoCalificando:

            # El texto del boton cambia ya que  el usuario acaba de iniciar el proceso
            # de calificacion de las entregas de la tarea, y cuando se termine de calificar
            # todas las entregas que el usuario indico, se  debera dar clic izquierdo sobre
            # este boton para poder volver a calificar mas tareas.
            self.btn_calificar.setText('Calificar\nmas tareas')

            self.btn_detener.setEnabled(True)

            self.btn_calificar.setEnabled(False)
            self.spinBox_tareasACalificar.setEnabled(False)
            self.btn_actualizarInfoCourseworks.setEnabled(False)
            self.tareasLogradasCalificar=0
            self.LISTA_CALIFICAR=False
        else:

            # El boton cambiara de texto por que ahora cuando se presione
            # servira para calificar el numero de entregas especificado
            # en el spinBox
            self.btn_calificar.setText('Calificar')

            self.btn_detener.setEnabled(False)

            self.btn_calificar.setEnabled(True)
            self.spinBox_tareasACalificar.setEnabled(True)
            self.btn_actualizarInfoCourseworks.setEnabled(True)

            # Cuando se pone en modo NO CALIFICANDO
            # se borraran los datos de la tabla que muestras las califcaciones
            # que se obtienen al calificar las entregas de los estudiantes de
            # la tarea
            self.tableWidget_alumnosCalif.setRowCount(0)


            # Como se volvera a calificar tareas, se actualizan los
            # valores de las siguientes etiquetes y del spinBox
            self.bel_noTareasCalificadas.setText('0')
            self.bel_noTareasAcalificar.setText('0')
            self.spinBox_tareasACalificar.setValue(0)

            # Se actualiza el valor maximo del spinBox
            self.spinBox_tareasACalificar.setMaximum(self.numeroTareasCalificar)

            self.LISTA_CALIFICAR=True



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
# METODOS QUE SE PUEDEN LLAMAR CUANDO YA SE ESTA CALIFICANDO ENTREGAS
####################################################################################################################################

    def mostrarErrorRed(self,tuplaDatos):
        '''
        Este metodo se encargara de mostrar el error que se presento
        a la hora de calificar las entregas realizadas por los estudiantes
        de la tarea de programación que selecciono el usuario

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
        las entregas realizadas por los estudiantes de la tarea de programación
        que selecciono el usuario
        '''

        # preguntando si en realidad se desea detener el proceso de calificacion
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
            * Habilitara el boton  que permitira al usuario volver a calificar
             mas entregas de la tarea de programacion.

        Parámetros:
            terminoNaturalmente (bool): Si el valor de dicho parametro es igual a
            False, significa que  se presento un error al calificar las entregas de
            la tarea o significa que el usuario interrumpio el proceso de calificacion
            de tareas.Si el valor de dicho parametro es igual a True: significa que se
            calificaron exitosamente el numero de entregas que el usuario indico que se
            calificaran.
        '''

        # Por medio del spinBox el usuario puede elegir la cantidad de tareas
        # que desea calificar por tal motivo cuando se deja de calificar tareas
        # se actualiza al valor maximo del 'spinBox' ya que al califcar tareas,
        # reducio el numero de tareas que restan por calificar.
        self.spinBox_tareasACalificar.setMaximum(self.numeroTareasCalificar)

        # Habilitando el boton que permitira al usuario volver a calificar
        # mas entregas de la tarea de programacion que selecciono
        self.btn_calificar.setEnabled(True)

        # Si no ocurrio a calificar ningun errro al calificar las entregas de la tarea
        # o si no se detuvo la calificacion de las tareas.
        if terminoNaturalmente:
            self.msg_calificadorTerminoCalificar()





####################################################################################################################################
# TABLA DE TAREAS CALIFICADAS
####################################################################################################################################

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