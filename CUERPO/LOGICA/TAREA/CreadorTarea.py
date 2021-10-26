
'''
CreadorTarea.py :
                    Contiene una sola  clase, la clase 'CreadorTareas', la cual a grosso
                    modo sirve para asignar a los estudiantes tareas de programación en google
                    classroom.
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# librerias estandar
###########################################################################################################################################
import sys
###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import webbrowser
###########################################################################################################################################
# fuente local
###########################################################################################################################################
from CUERPO.DISENO.TAREA.CreadorTarea_d import Ui_Dialog
import recursos


class CreadorTareas(QtWidgets.QDialog, Ui_Dialog,recursos.HuellaAplicacion):
    '''
    Esta clase sirve para crear un borrador de la tarea que desea asignar a los estudiantes
    en google classroom.Es importante recordar que para que las tareas puedan ser calificadas
    por el programa deberan ser asignadas por el programa, esa es una retricción que pone
    la API de google classroom, por tal motivo existe esta clase.
    Cabe mencionar que la razon por lo que  esta clase crea la tarea se crea como borrador es por
    que si se publicara todos los estudiantes les llegaria la notificacion de la tarea, y si el  el
    usuario  cometido un error, en la tarea que asigno, ya no podra cancelar las notificaciones
    que le llegan a los estudiantes cuando un profesor crea una tarea, por tal motivo se crean las
    tareas como borradores, para que el usuario vea la tarea en classroom antes de hacerla publica
    con todos sus estuiantes.

    Esta clase presenta un formulario que pide los datos necesario  para crear el borrador de tarea
    en google classroom, tambien esta clase se encarga de validar que los datos ingresados
    sean correctos antes de crear el borrador y finalmente una vez creado el borrador de la tarea en
    classroom, esta clase proseguira a abrir en el navegador web del usuario la clase de classroom en donde
    se encuentra el borrador de la tarea de programación  para que el usuario  pueda revisar si la tarea
    creada es correcta y asignarsela a sus alumnos cuando lo desee.
    '''


    # las siguientes constantes almacenan los nombres de las imagenes que cambiaran en función
    # del comportamiento de cada boton...
    IMAGEN_MAL = '''QPushButton{border-image:url(:/main/IMAGENES/tache_off.png);}
                  QPushButton:hover{ border-image:url(:/main/IMAGENES/tache_on.png);}
                  QPushButton:pressed{border-image:url(:/main/IMAGENES/tache_off.png);}'''
    IMAGEN_BIEN = '''QPushButton{border-image:url(:/main/IMAGENES/paloma_off.png);}
                  QPushButton:hover{ border-image:url(:/main/IMAGENES/paloma_on.png);}
                  QPushButton:pressed{border-image:url(:/main/IMAGENES/paloma_off.png);}'''



    def __init__(self,administradorProgramasClassRoom):
        '''
        - administradorProgramasClassroom (objeto de la clase: AdministradorProgramasClassRoom): dicho
        objeto permite calificar tareas de los estudiantes  del classroom seleccionado por el usuario, este
        objeto tambien permite obtener informacion de una manera mas sencilla acerca de las tareas del classroom
        y topic seleccionadas por el usuario
        '''


        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)


        self.restringirLasEntradas()

        self.administradorProgramasClassRoom=administradorProgramasClassRoom
        self.SE_CREO_BORRADOR_TAREA_EXITOSAMENTE=False

        # vinculandos los botones de informativos con el respetivo metodo que mostrara
        # la informacion de lo que se debe poner en cada apartado al que corresponde
        # cada boton
        self.btn_infoGeneralCreacionTarea.clicked.connect(lambda : self.msg_informar(0) )
        self.btn_info_nombreTarea.clicked.connect( lambda : self.msg_informar(1) )
        self.btn_info_idColabDeTarea.clicked.connect(lambda : self.msg_informar(2))
        self.btn_info_indicacionesTarea.clicked.connect( lambda : self.msg_informar(3) )

        self.btn_crearBorrador.clicked.connect(self.crearBorradorDeTareaEnClassroom)


    def restringirLasEntradas(self):
        '''
        Este metodo pondra las respectivas validaciones de cada seccion del
        formulario
        '''

        # validacion del nombre de la tarea...
        # maximo solo 30 caracteres, sin espacios en blanco y caracteres
        # especiales validos unicamente el guion bajo y guion medio
        validator = QRegExpValidator(QRegExp("[0-9a-zA-Z_-]{1,30}"))
        self.lineEdit_nombreTarea.setValidator(validator)

    def crearBorradorDeTareaEnClassroom(self):
        '''
        Primero comprobara si todos los datos ingresados por el usuario son correctos, en caso de ser correctos
        proseguira en preguntarle al usuario si en realidad esta seguro de crear el borrador de la tarea con dichos
        datos, si el usuario confirma positivamente entonces proseguira a crear el borrador de la tarea en classroom
        con los datos proporcionados por el usuario.

        Si a la hora de comprobara si todos los datos ingresados por el usuario son correctos, detecto algun error
        entonces se lo mostrara al usuario.
        '''

        mensajeTodosErroresDetectados = self.buscarErrorEn_TodosLosDatosIngresadosPorUsuario()

        # ¿se detecto por lo menos un error?
        if mensajeTodosErroresDetectados != None:
            encabezadoMensaje = "Para crear el borrador de la tarea en google classroom, todos los datos ingresados " \
                                "deben ser correctos, sin embargo al procesar los datos ingresados se presentaron los " \
                                "siguientes errores:"
            finMensaje = "Por favor corrige todos los errores. "
            mensajeTodosErroresDetectados = encabezadoMensaje + mensajeTodosErroresDetectados + finMensaje
            # mostrando los errores detectados
            self.ventanaEmergenteDe_error(mensajeTodosErroresDetectados)

        # el usuario no cometio ningun error con los datos que ingreso
        else:
            usuarioDecididoDeHacerBorradorDeTarea = self.msg_confirmacionDatosBorradorDeTarea()

            if usuarioDecididoDeHacerBorradorDeTarea:
                # obteniedo el titulo de la tarea que escribio el usuario
                nombreTarea = self.lineEdit_nombreTarea.text()

                idColabTarea = self.plainText_idColab.toPlainText()

                # obteniedo las descripcciones de la tarea que se escribio el usuario
                descripccionTarea = self.textEdit_indicaciones.toPlainText()

                self.administradorProgramasClassRoom.crearTarea(
                    titulo=nombreTarea,
                    descripccion=descripccionTarea,
                    colab_id=idColabTarea,
                )
                linkAccesoClaseClassroom = self.administradorProgramasClassRoom.get_LinkAccesoClaseClassroom()
                self.msg_exitoAlCrearBorradorDeTarea()

                # abriendo la clase de classroom que contiene la tarea que se creo como borrador
                webbrowser.open(linkAccesoClaseClassroom)
                self.SE_CREO_BORRADOR_TAREA_EXITOSAMENTE = True
                self.close()

    def buscarErrorEn_TodosLosDatosIngresadosPorUsuario(self):
        '''
        El siguiente metodo se encarga de revisar si los datos ingresados por el usuario para poder
        crear el borrador de la tarea son correctos, la validacion que hace por cada campo es la
        siguiente:
            * En el nombre de la tarea: Revisa que el nombre de la tarea que ingreso el usuario
            exista en las tareas de la clase de NbGrader seleccionada en el apartado de configuraciones
            * En el ID del colab: Revisa que el ID que ingreso el usuario corresponda al de un ID de
            un archivo jupyter o colab, pues esos son los formatos de los archivos que el usuario
            debera asignar las tareas de programación a sus alumnos
            * En las indicaciones: Revisa que por lo menos haya puesto alguna indicacion.

        Si se detecta que todos los datos que ingreso el usuario son correctos,retornara un None
        Si detecta almenos un error, retornara un mensaje que explica cual error fue el detectado

        En la seccion que haya detectado un error le asignara un imagen de tache al boton de informacion
        de dicha seccion y en la seccion que no haya detectado un error le asignara un imagen de paloma
        al boton de informacion respectivo de dicha seccion

        Returns:
            None -.  Si se detecta que todos los datos que ingreso el usuario son correctos
            str  -.  Si detecta almenos un error, retornara un mensaje que explica cual error
                    u errores fueron detectados
        '''

        dictErrores={
            'nombreTarea': None,
            'idColab':None,
            'descripccionTarea':None
        }

        # obteniedo el titulo de la tarea que escribio el usuario
        nombreTarea = self.lineEdit_nombreTarea.text()

        idColabTarea=self.plainText_idColab.toPlainText()

        # obteniedo las descripcciones de la tarea que se escribio el usuario
        descripccionTarea = self.textEdit_indicaciones.toPlainText()



        # VALIDANDO LA DESCRIPCCION DE LA TAREA
        # ¿puso algo en la descripccion de la tarea el usuario?
        if descripccionTarea=="":
            mensajeError="(ERROR EN LA DESCRIPCCION DE LA TAREA INGRESADA) <<No se puso ninguna descripccion," \
                         "y el apartado de descripccion de la tarea no debe quedar vacio>>"
            dictErrores['descripccionTarea']=mensajeError
            self.btn_info_indicacionesTarea.setStyleSheet(self.IMAGEN_MAL)
        else:
            self.btn_info_indicacionesTarea.setStyleSheet(self.IMAGEN_BIEN)


        # VALIDANDO EL NOMBRE DE LA TAREA QUE SE ADJUNTO
        nombreTareaEsCorrecto = self.administradorProgramasClassRoom.existeEsaTarea_cursoNbGrader(nombreTarea=nombreTarea)
        if nombreTareaEsCorrecto is False:
            mensajeError="(ERROR EN EL NOMBRE DE LA TAREA INGRESADO) <<No se encontro con el nombre de la tarea" \
                         "que ingresaste, ninguna tarea existente en la clase de NbGrader que seleccionaste en el " \
                         "apartado de: 'Mis configuraciones' y recuerda que el nombre de la tarea que ingreses debe " \
                         "ser el mismo nombre que el nombre de una tarea una tarea existente en la clase de NbGrader " \
                         "que seleccionaste en el apartado de: 'Mi configuraciones' "

            dictErrores['nombreTarea']=mensajeError
            self.btn_info_nombreTarea.setStyleSheet(self.IMAGEN_MAL)
        else:
            self.btn_info_nombreTarea.setStyleSheet(self.IMAGEN_BIEN)


        # VALIDANDO EL ID DEL COLAB QUE SE ADJUNTO
        erroresPresentadosEnID_colabTarea=self.administradorProgramasClassRoom.getErrorEn_idDelColabQueSeDiceSerQueEsUnIdDeUnArchivoValidoDeTarea(
            idDelColab=idColabTarea
        )

        if erroresPresentadosEnID_colabTarea!=None:
            mensajeError = "(ERROR EN EL ID QUE SE INGRESO DEL GOOGLE COLAB DE LA TAREA )<< Al procesar el ID que ingresaste en el apartado de ID " \
                           "del colab, se detecto el siguiente error: "+erroresPresentadosEnID_colabTarea+">>"
            dictErrores['idColab'] = mensajeError
            self.btn_info_idColabDeTarea.setStyleSheet(self.IMAGEN_MAL)
        else:
            self.btn_info_idColabDeTarea.setStyleSheet(self.IMAGEN_BIEN)


        # Agrupando todos los mensaje de error en una sola variable de tipo 'str'
        mensajeTodosErroresDetectados=""
        for errorDetectado in dictErrores.values():
            if errorDetectado!=None:
                mensajeTodosErroresDetectados+=errorDetectado+"\n"

        if mensajeTodosErroresDetectados=="":
            mensajeTodosErroresDetectados=None

        return mensajeTodosErroresDetectados

#############################################################################################################################################
#      A C C I O N E S     F I N A L E S :
#############################################################################################################################################

    def borrarTodo(self):
        '''
        Se encargara de limpiar el contenido de los apartados del formulario para que el usuario
        pueda usar este formario com un formulario nuevo.
        '''
        self.lineEdit_nombreTarea.setText("")
        self.plainText_idColab.setPlainText("")
        self.textEdit_indicaciones.setPlainText("")

        self.btn_info_indicacionesTarea.setStyleSheet(self.IMAGEN_MAL)
        self.btn_info_idColabDeTarea.setStyleSheet(self.IMAGEN_MAL)
        self.btn_info_nombreTarea.setStyleSheet(self.IMAGEN_MAL)


    def closeEvent(self, event):
        '''
        Este metodo cerrara la ventana, sin embargo tendra un comportamiento diferente en funcion del
        valor que tenga la variable bandera: 'self.SE_CREO_BORRADOR_TAREA_EXITOSAMENTE', es decir:

        Si 'self.SE_CREO_BORRADOR_TAREA_EXITOSAMENTE' tiene un valor igual a True:
            - Significara que el usuario creo un borrador de la tarea con exito, y que por lo tanto
            ya no es necesario que la ventana del formulario siga abierta asi que el metodo
            simplemente cerrar dicha ventana

        Si 'self.SE_CREO_BORRADOR_TAREA_EXITOSAMENTE' tiene un valor igual a False:
            - Significa que el usuario quiere salir del formulario(esta ventana), por tal motivo
            este metodo le preguntara al usuario si esta seguro de querer salir, ya que si
            sale se perderan todos los datos de los ingresados
        '''

        if self.SE_CREO_BORRADOR_TAREA_EXITOSAMENTE:
            self.borrarTodo()
            self.SE_CREO_BORRADOR_TAREA_EXITOSAMENTE=False
            event.accept()

        else:
            resultado = self.msg_cerrarVentana()
            if resultado:
                self.borrarTodo()
                event.accept()
            else:
                event.ignore()  # No saldremos del evento


##################################################################################################################################################
# MENSAJES
##################################################################################################################################################

    def msg_confirmacionDatosBorradorDeTarea(self):
        '''
        Mostrara un cuadro de dialogo al usuario para preguntarle si
        en realidad los datos que adjunto en el formulario son los
        correctos para la creacion del borrador de tarea en classroom

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si
            - False (bool): Si el usuario dijo que NO
        '''

        mensaje = "Los datos que ingresaste para la creacion del borrador de tarea son correctos " \
                  "ahora solo confirma lo siguiente: ¿estas seguro de que los datos que ingresaste " \
                  "son los que querias ingresar? Si responde afirmativamente se proseguira a crear " \
                  "con dichos datos el borrador de tarea en classroom "

        resultado = self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado


    def msg_cerrarVentana(self):
        '''
        Mostrara un cuadro de dialogo con el objetivo de: preguntarle al usuario
        si en realidad desea cerrar la aplicacion

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si
            - False (bool): Si el usuario dijo que NO
        '''

        mensaje = "¿Esta seguro que deseas salir de este formulario,recuerda que si " \
                  "sales de este formulario los datos que adjuntaste se perderan ?"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado



    def msg_informar(self,idDuda):
        '''
        Cada seccion del formulario contiene un boton que puede contener una imagen
        de tache o una imagen de paloma, si dicho boton es presionado se le mostrara
        un cuadro de dialogo al usuario en donde vendra la explicacion de cual es el
        dato que te debe adjuntar en dicho apartado del formulario, y lo que hara
        este metodo es mostrar dicho mensaje respectivo.

        Parámetros:
            idDuda(int) : Representa el numero de boton que fue presionado y sirve
                          para que el metodo sepa que mensaje de expicacion mostrar
        '''

        TUPLA_RESOLUCION_DUDAS = (

            "Cada seccion del formulario contiene una breve explicacion de cual es el dato  que "
            "debe ser ingresado asi como las  restricciones de dicho dato, para poder ver esa informacion "
            "debes dar click en el  boton que tiene forma de tache o  paloma, este boton se encuentra a lado "
            "derecho de cada  seccion del formulario.Es importante mencionar que cuando hayas ingresado todos "
            "los datos de cada seccion del formulario deberas dar clic sobre el boton: <<Generar borrador de tarea "
            "en classroom>> cuando hagas esto CACPY creara en classroom un borrador de tarea con los datos que "
            "ingresaste en el formulario, despues CACPY abrira en tu navegador la clase de classroom que contiene "
            "dicho borrador de tarea, con la finalidad de que puedas revisar que los datos de la tarea son correctos "
            "y despues puedas quitar el estatus de borrador y asignar dicha tarea para que todos tus alumnos puedan verla "
            "y resolverla",

            "Recuerda que el nombre de la tarea: solo puede ser una palabra,solo puede estar conformado de letras "
            "minusculas,letras mayusculas,numeros,guiones bajos,guiones medios y no debe tener espacios en blanco.El nombre de la tarea "
            "que ingreses  debe ser el mismo nombre que el de una tarea existente en la clase de NbGrader que seleccionaste "
            "en el apartado de: 'Mi configuraciones' ",
            

            "Aqui debes inscrutar el id que le asigna google drive al  google colab o jupyter  de la tarea que le "
            "asignaras a tus estudiantes",
            
            "Por lo menos debes escribir una instruccion breve acerca de lo que lo que trata la tarea que deseas adjuntar."
        )

        mensaje = TUPLA_RESOLUCION_DUDAS[idDuda]

        self.ventanaEmergenteDe_informacion(mensaje)



    def msg_exitoAlCrearBorradorDeTarea(self):
        '''
        Ventana emergente informativa que se le mostrara al usuario cuando la tarea  haya sido
        asignada correctamente en classroom,sin embargo este mensaje tambien le recuerda al usuario
        que la tarea que  ya se encuentra en classroom esta en forma de borrador, y que si desea
        que la vean sus estudiantes debe entrar a classroom y ponerla en forma de no borrador.
        '''

        _,nombreClase_classroom=self.administradorProgramasClassRoom.get_datosCurso()
        _,nombreTopic_classroom=self.administradorProgramasClassRoom.get_datosTopic()

        mensaje= f"Felicidades, tu tarea ha sido registrada correctamente en tu clase de classroom:<<" \
                 f"{nombreClase_classroom}>> en el topic: <<{nombreTopic_classroom}>>" \
                 ", sin embargo es importante que recuerdes que dicha tarea se encuentra " \
                 "en estatus de borrador, esto significa que tus estudiantes aun no pueden ver que les " \
                 "asignaste la tarea, si deseas que esta tarea la puedan ver tus alumnos con el objetivo " \
                 "de que la puedan resolver, entonces deberas entrar al  classroom y topic en donde " \
                 "ya se encuentra esta tarea y quitarle el estatus de borrador y asignarla.Otro punto importante que mencionar " \
                 "es que  esta tarea no se visualizara en el tabla de tareas calificables, tu la deberas agregar si deseas calificar " \
                 "las entregas que hagan tus alumnos de dicha tarea, sin embargo es " \
                 "importante mencionar que solo la podras agregar si no se encuentra como borrador, ya que si se encuentra como borrador " \
                 "el programa no la detectara  y por ende no podras agregarla a la tabla de tareas calificables.A continuacion se cerrara esta ventana " \
                 "por que ya creaste el borrador de la tarea, despues de que se cierre la ventana se abrira en tu navegador web tu clase de classroom " \
                 "que almacena la tarea que creaste como borrador, todo es con la finalidad de que puedas verificar que la tarea que creaste como borrador " \
                 "es correcta o tambien para que puedas editarla " \
                 "y finalmente puedas decidir si ya asignarla o eliminarla por que algo salio mal."

        self.ventanaEmergenteDe_informacion(mensaje)



if __name__ == "__main__":
    # Cambiando de direcciones sus carpetas u archivos...
    app = QtWidgets.QApplication([])
    application = CreadorTareas()
    application.show()
    sys.exit(app.exec())




