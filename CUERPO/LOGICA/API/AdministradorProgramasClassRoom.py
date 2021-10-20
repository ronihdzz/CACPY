from __future__ import print_function

import datetime     # for general datetime object handling
import recursos

from nbgrader.apps import NbGraderAPI
from traitlets.config import Config



##########################################################################################################################################
#  IMPORTANCION LOGICA
###########################################################################################################################################

from CUERPO.LOGICA.API.HiloCalificadorTarea import HiloCalificadorTarea




class AdministradorProgramasClassRoom:
    def __init__(self,classroom_control,baseDatosLocalClassRoom,configuracionCalificador):
        self.classroom_control=classroom_control
        self.configuracionCalificador=configuracionCalificador
        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.nbGrader_control=None


        self.hiloCalificadorTarea=HiloCalificadorTarea(
            configuracionCalificador=self.configuracionCalificador,
            nbGrader_control=self.nbGrader_control,
            classroom_control=self.classroom_control
        )


    def get_LinkAccesoClaseClassroom(self):
        idCurso = self.configuracionCalificador.getIdApi_cursoClassroom()
        datosClaseClassroom = self.classroom_control.service_classroom.courses().get(
            id=idCurso
        ).execute()

        if datosClaseClassroom != None:
            linkAcceso = datosClaseClassroom.get("alternateLink")
            return linkAcceso

    def getErrorEn_idDelColabQueSeDiceSerQueEsUnIdDeUnArchivoValidoDeTarea(self, idDelColab):
        '''
        El siguiente


        Returns:
            None: Si no existio ningun error
            str : Si existion un error
        '''

        if idDelColab != "":
            try:
                # obteniendo el archivo de google drive al que le corresponde
                # el ID que ingreso el usuario
                response = self.classroom_control.service_drive.files().get(
                    fileId=idDelColab,
                    fields='name,mimeType'
                ).execute()

                mimeType = response.get('mimeType')
                nombreArchivo = response.get('name')
                if type(nombreArchivo) != str:
                    nombreArchivo = ""

                # ¿el ID ingresado  NO es el ID de un colab?
                if mimeType != 'application/vnd.google.colaboratory' and mimeType != 'application/json' and nombreArchivo.endswith(
                        ".ipynb") != True:
                    mensajeDeError = f"El ID que ingresaste corresponde a un archivo cuyo nombre es: <<{nombreArchivo}>> y cuyo tipo es:" \
                                     f"<<{mimeType}>>, sin embargo, DICHO ARCHIVO NO CORRESPONDE A UN ARCHIVO VALIDO, ya que no paso las pruebas " \
                                     f"que validan que es un archivo de un google colab o un jupyter notebook pues su tipo no coincide con: " \
                                     f"<<application/vnd.google.colaboratory>> y ni tampoco con: <<application/json>> y ni siquiera el archivo " \
                                     f"tiene la terminacion: <<.ipynb>>"
                    return mensajeDeError

                # significa que el archivo que correspone al ID cumplio por lo menos con alguna restriccion que se valida en el
                # anterior condicional
                else:
                    return None

            except Exception as e:
                return str(e)

        else:
            mensajeDeError = "no se ingreso ningun ID en el colab de la tarea"

            return mensajeDeError



    def get_datosCurso(self):
        return (self.configuracionCalificador.curso_idApi, self.configuracionCalificador.curso_nombre)

    def get_datosTopic(self):
        return (self.configuracionCalificador.topic_idApi, self.configuracionCalificador.topic_nombre)


    def seleccionarBaseLocal_coursework(self,idCourseWork):
        self.baseDatosLocalClassRoom.cambiarEstadoEleccion(
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi,
            idCourseWorkElegido=idCourseWork
        )


    def get_dictTareasDejadas(self):
        listaTareas=self.classroom_control.get_listaTareasTopic(
            self.configuracionCalificador.curso_idApi,
            self.configuracionCalificador.topic_idApi
        )
        #datos = [
        #    tarea.get('id'), curso_id, topic_id, tarea.get('title'),
        #    tarea.get('description'), fechaCreacion
        #]

        print(listaTareas)
        return listaTareas

    def crearTarea(self,titulo,descripccion,colab_id):

        idTarea= self.classroom_control.create_asignacionPrograma(
                    course_id=self.configuracionCalificador.curso_idApi,
                    topic_programas_id=self.configuracionCalificador.topic_idApi,
                    colab_id=colab_id,
                    titulo=titulo,
                    description=descripccion
        )
        # formato de cadena ISO8601:  YYYY-MM-DD HH:MM:SS.SSS para compatibilidad con sqlite3
        fechaCreacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # tuplaDatos=(id,title,description,fechaCreacion)
        self.agregarCourseWorks_baseDatosLocal(
            tuplaDatos=(  (idTarea,titulo,descripccion,fechaCreacion),   )
        )

        # registrar como ya agregada
        #self.seleccionarBaseLocal_coursework(idCourseWork=idTarea)

        return idTarea,fechaCreacion


    def get_courseWorksLibres_baseDatosLocal(self):

        tuplaDatosCourseWorks=self.baseDatosLocalClassRoom.get_courseWorksLibres(
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi
        )
        return tuplaDatosCourseWorks

    def get_courseWorksAgregados_baseDatosLocal(self):

        tuplaDatosCourseWorks=self.baseDatosLocalClassRoom.get_courseWorksAgregados(
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi
        )
        return tuplaDatosCourseWorks


    def agregarCourseWorks_baseDatosLocal(self,tuplaDatos):
        self.baseDatosLocalClassRoom.agregar_soloNuevosCourseWorks(
            tuplaDatos=tuplaDatos,
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi
        )

    def eliminarCourseWork_baseDatosLocal(self,courseWork_id):
        self.baseDatosLocalClassRoom.eliminarCourseWork(
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi,
            coursework_id=courseWork_id
        )


    def get_informacionTareasEntregadas(self,courseWork_id):

        #dictEntregas[user_id] = [url, asignacion_id]

        datosEntraga=self.classroom_control.list_submissions(
            course_id=self.configuracionCalificador.curso_idApi,
            coursework_id=courseWork_id
        )

        print(datosEntraga)


    def getDatosCourseWork(self, courseWork_id):

        dictDatosEntrega= self.classroom_control.get_datosEntregas(
            course_id=self.configuracionCalificador.curso_idApi,
            coursework_id=courseWork_id
        )

        #    dictDatosEntrega={
        #        'calificados':0, #RETURNED
        #        'porCalificar':0, # TURNED_IN
        #        'porEntregar':0,
        #    }


        return dictDatosEntrega




    def calificarEstudiantes(self,courseWork_id,courseWork_name,noMaxEstudiantesCalificar=5):
        self.hiloCalificadorTarea.setDatosTareaCalificar(
            nuevoCourseWork_id=courseWork_id,
            nuevoCourseWork_name=courseWork_name
        )
        self.hiloCalificadorTarea.nbGrader_control=self.nbGrader_control


        self.hiloCalificadorTarea.setNoMaxEstudiantesCalificar(nuevoValor=noMaxEstudiantesCalificar)

        self.hiloCalificadorTarea.start()

    def actualizar_nbGraderControl(self):
        '''
        Cuando el valor de la clase es cambio, debera ser llamado este metodo
        ya que este metodo renueva la nueva ruta en donde se encuentra ubicada el
        nbGrader control.


        :param nombreNuevaClase:
        :return:
        '''

        nombreNuevaClase=self.configuracionCalificador.claseNbGrader_nombre

        # create a custom config object to specify options for nbgrader
        config = Config()
        config.CourseDirectory.course_id = nombreNuevaClase
        config.CourseDirectory.root =recursos.App_Principal.RUTA_NB_GRADER+nombreNuevaClase+'/'
        self.nbGrader_control = NbGraderAPI(config=config)

        print("Tareas:",self.nbGrader_control.get_source_assignments())

    def existeEsaTarea_cursoNbGrader(self,nombreTarea):


        if self.nbGrader_control!=None:
            tareasExistentes=self.nbGrader_control.get_source_assignments()
            print(tareasExistentes)
            if nombreTarea in tareasExistentes:
                return True
            else:
                return False



