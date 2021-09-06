


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import  QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtCore,QtGui
import recursos
from CUERPO.LOGICA.API import FuncionesDrive



###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.ALUMNO.AlumnoMain_d import Ui_Form




class AlumnoMain(QtWidgets.QWidget,Ui_Form,recursos.HuellaAplicacion):
    NO_COLUMNAS=2

    def __init__(self,baseDatosLocalClassRoom,classRoomControl,configuracionCalificador):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)

        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.classRoomControl=classRoomControl
        self.configuracionCalificador=configuracionCalificador

        self.btn_refrescarListaAlumnos.clicked.connect(self.cargarEstudiantes)
        self.tableWidget_alumnos.installEventFilter(self)

        self.configurarTabla()

        self.tableWidget_alumnos.itemDoubleClicked.connect(self.verDetallesEstudiante)
        self.btn_regresar.clicked.connect(lambda : self.listWidget.setCurrentIndex(0) )
        self.listaIdsEstudiantes=[]


        self.mostrarDatosCurso()


        self.textBrowser_datosEstudiante.setOpenExternalLinks(True)
        self.textBrowser_datosEstudiante.setOpenLinks(True)
        self.textBrowser_datosEstudiante.setReadOnly(True)




    def generarHtmlEstudianteMostrar(self,nombre,correo,linkCarpetaRetroalimentacion):
        htmlEstudiante = f'''
        <p>
            <span style=" font-size:16px;font-family: TamilSangamMN;"> 
            Estudiante: {nombre}
            </span>
            <br>
            <br>
            
            <span style=" font-size:12px;font-family: TamilSangamMN;"> 
            Correo: {correo}
            </span>
            <br>
            <br>

            <span style=" font-size:12px;font-family: TamilSangamMN;"> 
             Retroalimentaciones:
            </span>

            <span style=" font-size:12px;font-family: TamilSangamMN;">
                <a href="{linkCarpetaRetroalimentacion}"  style="color:black;"> 
                    <strong>carpeta de todas las retrolimentaciones<\strong> 
                </a>
            </span>
        <p>  
        '''

        return htmlEstudiante



    def actuarCambioCurso(self):
        self.borrarListaAlumnos()
        self.mostrarDatosCurso()


    def getLinkCarpetaRetroAlumno(self,user_id):

        # DATOS DE LA CARPETA EN DONDE SE ADJUNTARAN LAS RETROALIMENTACIONES
        folder_id = self.configuracionCalificador.getIdApiCarpetaRetro()
        idClase, nombreClase = self.configuracionCalificador.get_id_nombre_cursoClassroom()

        nombreCarpetaCurso = "{}_{}".format(nombreClase, idClase)  # sera el id del curso
        drive_service = self.classRoomControl.service_drive

        ############################################################################################################################################
        #   POSIBLE ERROR POR CONEXION DE RED 1:
        #   ¿EXISTE EN DRIVE LA CARPETA DE LA CLASE DE CLASSROOM EN DONDE SE SUBIRAN LAS RETROALIMENTACIONES?
        ############################################################################################################################################

        print("*" * 100)
        print("PASO 1: ¿EXISTE EN DRIVE LA CARPETA DE LA CLASE DE CLASSROOM EN DONDE SE SUBIRAN LAS RETROALIMENTACIONES?")

        # obteniendo el id o creando la carpeta donde se guardara las retroalimentaciones
        # de la clase de classroom
        respuesta = FuncionesDrive.getId_carpeta(nombre=nombreCarpetaCurso,
                                                 idCarpetaAlmacena=folder_id,
                                                 intermediarioAPI_drive=drive_service)

        if respuesta['exito'] is False:
            errorPresentado = respuesta['resultado']
            print(errorPresentado)
            #self.HILO_ACTIVO = False
            #self.senal_errorRed.emit((self.LISTA_ERRORES_RED[0], errorPresentado))


        else:
            id_carpetaRetroClase = respuesta['resultado']['id']

            ############################################################################################################################################
            #   POSIBLE ERROR POR CONEXION DE RED 4
            #   Buscando o creando la carpeta que contiene todas retroalimentaciones de todas las tareas de  un alumno en especifico
            ############################################################################################################################################

            print("*" * 100)
            print("PASO 4: Buscando o creando la carpeta que contiene todas retroalimentaciones de todas las "
                  "tareas de  un alumno en especifico")

            # Buscando si ya existe una carpeta con el id del estudiante la cual es donde
            # se almacenan todas las retroalimentaciones de sus tareas entragadas
            respuesta = FuncionesDrive.getId_carpeta(
                nombre=user_id,
                idCarpetaAlmacena=id_carpetaRetroClase,
                intermediarioAPI_drive=drive_service
            )

            if respuesta['exito'] is False:
                errorPresentado = respuesta['resultado']
                print(errorPresentado)
            else:
                link_carpetaEstudiante=respuesta['resultado']['webViewLink']
                return link_carpetaEstudiante

        return None


    def borrarListaAlumnos(self):

        print("BORRANDO TODOS LOS DATOS DE LA TABLA")
        self.tableWidget_alumnos.setRowCount(0)
        self.listaIdsEstudiantes = []



    def cargarEstudiantes(self,cargarAutomaticamente=False):

        seDeseaCargarListaAlumnos=True
        if cargarAutomaticamente is False:
            seDeseaCargarListaAlumnos=self.msg_preguntarAcercaRefrescarListaEstudiantes()

        if seDeseaCargarListaAlumnos:

            claseClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()
            alumnos=self.classRoomControl.get_listaAlumnos(claseClassroom_id)
            listaEstudiantes=[]
            self.listaIdsEstudiantes=[]

            for id,nombre,correo in alumnos:
                print(id,'-',nombre,'-',correo)
                listaEstudiantes.append( (nombre,correo) )
                self.listaIdsEstudiantes.append(id)
                # [idEstudiante] = nombreCompleto


            self.bel_numeroAlumnos.setText(str(len(self.listaIdsEstudiantes)))

            self.cargarDatosEnTabla(listaEstudiantes)


    def verDetallesEstudiante(self,index):
        index = index.row()

        # Cargando los datos del coursework
        nombre = self.tableWidget_alumnos.item(index, 0).text()
        correo=self.tableWidget_alumnos.item(index, 1).text()
        idEstudiante = self.listaIdsEstudiantes[index]

        linkCarpetaRetroalimentacion=self.getLinkCarpetaRetroAlumno(
            user_id=idEstudiante
        )

        htmlEstudiante=self.generarHtmlEstudianteMostrar(
            nombre=nombre,
            correo=correo,
            linkCarpetaRetroalimentacion=linkCarpetaRetroalimentacion,
        )

        self.textBrowser_datosEstudiante.setHtml(htmlEstudiante)


        claseClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()
        datosDict=self.classRoomControl.list_todasEntregasEstudiante(
            course_id=claseClassroom_id,
            user_id=idEstudiante
        )

        self.listWidget.setCurrentIndex(1)

        print(datosDict)

        self.cargarDatosAlumnoDeseaVer(idAlumno=idEstudiante,datosAlumnoDict=datosDict)


    def mostrarDatosCurso(self):
        nombreCurso=self.configuracionCalificador.getNombre_cursoClassroom()
        self.bel_numeroAlumnos.setText("0")

        if nombreCurso!=None:
            self.bel_nombreCurso.setText(nombreCurso)




    def cargarDatosAlumnoDeseaVer(self,idAlumno,datosAlumnoDict):

            self.tableWidget_tareasAlumno.setRowCount(0)

            # cargando los datos de correo electronico

            #self.bel_nombreAlumno_selec.setText(idAlumno)
            #self.bel_correoAlumnoSelec.setText(idAlumno)


            # cada topic tiene n elementos { 'llave_1':[()], 'llave_2':[()] ...  }


            #self.tableWidget_alumnos.clear()
            numeroRenglones=0

            for llave in datosAlumnoDict.keys():
                nombreTopic=llave



                for nombreCourseWork,calificacion in datosAlumnoDict[nombreTopic]:
                    self.tableWidget_tareasAlumno.insertRow(numeroRenglones)

                    print(nombreCourseWork,nombreTopic,calificacion)

                    # nombre coursework...
                    a = QtWidgets.QTableWidgetItem(nombreCourseWork)
                    a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                    self.tableWidget_tareasAlumno.setItem(numeroRenglones,0, a)

                    # nombre topic...
                    b = QtWidgets.QTableWidgetItem(nombreTopic)
                    b.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                    self.tableWidget_tareasAlumno.setItem(numeroRenglones,1,b)

                    # calificacion...
                    c = QtWidgets.QTableWidgetItem(str(calificacion))
                    c.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                    self.tableWidget_tareasAlumno.setItem(numeroRenglones,2, c)

                    numeroRenglones += 1





    def eventFilter(self, source, event):
        """
        Cada vez que alguien haga click derecho sobre algun item de la
        'listWid_soniMio' significara que probablemente quiera borrar
        esa canción asi que debe  mostrar la opcion de borrar, y en caso
        de ser seleccionada dicha opcion se mandara a borrar a dicha cancion
        """

        if event.type() == QtCore.QEvent.ContextMenu and source is self.tableWidget_alumnos:

            try:
                item = source.itemAt(event.pos())
                print("objeto=", item)
                print("indice a eliminar:", item.row())
                indiceEliminar = item.row()

                menu = QtWidgets.QMenu()
                menu.addAction("eliminar")  # menu.addAction("eliminar",metodoA_llamar)
                print("Clic derecho")

                # indice=self.listWid_soniMio.currentIndex().row()
                # cancionEliminar=self.listWid_soniMio.item(indice).text()
                # print(f"Indice {indice} indice{event.pos()}  cancionEliminar{cancionEliminar}")

                if menu.exec_(event.globalPos()):
                    self.eliminarEstudiante(indiceEliminar)

                    # if self.indice_topic_sele!=indiceEliminar:
                    #    print("DEBEMOS ELIMINAR")
                    #    self.eliminarRenglonTopic(indiceEliminar)
                    # else:
                    #    print("NO DEBEMOS ELIMINAR")
                    # self.eliminarCancion()
            except Exception as e:
                print(e)

            return True
        return super().eventFilter(source, event)



##################################################################################################################################################
# OTRAS COSAS
##################################################################################################################################################

    def eliminarEstudiante(self,numeroRenglon):
        respuestaPositiva=self.msg_preguntarEleccionBorrarEstudiante(
            estudianteEliminar=self.tableWidget_alumnos.item(numeroRenglon, 0).text()
        )

        if respuestaPositiva:
            #cursoClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()
            #self.baseDatosLocalClassRoom.eliminarTopic(curso_id=cursoClassroom_id,
            #                                           topicProgramas_id=self.listaIds_topicsClaseClassroom[numeroRenglon])
            self.tableWidget_alumnos.removeRow(numeroRenglon)
            self.listaIdsEstudiantes.pop(numeroRenglon)

            #self.listaIds_topicsClaseClassroom.pop(numeroRenglon)


    def configurarTabla(self):

        self.tableWidget_alumnos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_alumnos.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_alumnos.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        #self.tableWidget_alumnos.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        header = self.tableWidget_alumnos.horizontalHeader()

        self.COLOR_TABLA = "#EEF2F3"
        self.COLOR_RESPUESTA = "#9AE5E0"
        stylesheet = f"""
        QTableView{{selection-background-color:{recursos.App_Principal.COLOR_TOPIC_SELECCIONADO};
        background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }};
        """

        #stylesheet = f"""QTableView{{ background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }}; """

        # stylesheet += "background-color:" + self.COLOR_TABLA + ";}"
        self.tableWidget_alumnos.setStyleSheet(stylesheet)

        self.tableWidget_alumnos.verticalHeader().setDefaultSectionSize(70)

        # la tabla tiene 3 columnas
        # ("NOMBRE","DATA_TIME", "PREGUNTAS")
        header = self.tableWidget_alumnos.horizontalHeader()
        for columna in range(0, self.NO_COLUMNAS):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)
            # header.setSectionResizeMode(columna, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)


        # Configuracion de la tabla de alumnos...

        self.tableWidget_tareasAlumno.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_tareasAlumno.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_tareasAlumno.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget_tareasAlumno.setStyleSheet(stylesheet)

        header = self.tableWidget_tareasAlumno.horizontalHeader()
        for columna in range(0,3):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)



    def cargarDatosEnTabla(self,tuplaDatos):
        '''
        Cargara los nombre de los topcis que vienen inmerso en el valor que tomara el
        parametro con nombre de: 'tuplaDatos'

        Parametros:
            tuplaDatos (tuple): Es una tupla de n elementos donde cada elemento de ellas
            representa el nombre de un topic de la clase de classroom seleccionada.
        '''

        if len(tuplaDatos)>0:
            FILAS = len(tuplaDatos)
            self.tableWidget_alumnos.setRowCount(FILAS)

            for f in range(FILAS):
                for c in range(self.NO_COLUMNAS):
                    dato_celda_string = str(tuplaDatos[f][c])
                    a = QtWidgets.QTableWidgetItem(dato_celda_string)
                    a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                    self.tableWidget_alumnos.setItem(f,c, a)


####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################


    def msg_preguntarEleccionBorrarEstudiante(self,estudianteEliminar):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Critical)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Seguro de querer ELIMINAR al estudiante <<{}>> ?".format(estudianteEliminar)

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



    def msg_preguntarAcercaRefrescarListaEstudiantes(self):
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Question)
            ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            mensaje = "Solo es recomendable refrescar la lista de estudiantes " \
                      "si eliminaste a un estudiante por accidente o si no vez " \
                      "la lista de nombres de tus estudiantes"

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



###############################################################################################################################################################################
# METODOS POR IMPLEMENTAR
################################################################################################################################################################################


    def cargarAlumnos(self,curso_id):
        '''
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

                self.listWidget_topicsTareasProgramas.addItems(  tuple( self.dictTopics.values() )  )
        '''
        pass

    def refrescarAlumnos(self):
        '''
        Agregara todos los alumnos no agregados a la base de datos....
        Posteriormente comenzara a agregar con la tecnica de join a los alumnos-curso que no existan...
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


                tuplaDatosTopics=self.baseDatosLocalClassRoom.get_topicsLibres(course_id_api=self.curso_id)
                self.dictTopics={}

                if tuplaDatosTopics!=() and len(tuplaDatosTopics)!=0:
                    for topic_api_id,topic_nombre in tuplaDatosTopics:
                        self.dictTopics[topic_api_id]=topic_nombre

                    self.listWidget_topicsTareasProgramas.addItems(  tuple( self.dictTopics.values() )  )

                self.msg_exitoDescargarTopics()
        '''
        pass







if __name__ == '__main__':
    app = QApplication([])
    application = AlumnoMain()
    application.show()
    app.exit(app.exec())