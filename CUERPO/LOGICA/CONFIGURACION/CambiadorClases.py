
'''
CambiadorClases.py :  Contiene una sola  clase, la clase 'CambiadorClases', la cual  a grosso modo se encarga
                      de hacer posible que el usuario pueda seleccionar la clase de google classroom de su
                      elección
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import pyqtSignal

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.DISENO.CONFIGURACION.CambiadorClases_d import Ui_Dialog
import recursos


class CambiadorClases(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):
    '''
    Permite al usuario seleccionar la clase de google classrom de su preferencia,
    por ello le muestra al usuario las clases de google classrom que puede seleccionar
    o en otras palabras le muestra al usuario las clases de google classroom que este
    tiene registradas en sus cuenta de google. Tambien permite al usuario actualizar
    las clases de classroom mostradas ya que puede que recien haya creado una clase de
    classroom nuevo y que por ende no aparece.
    Si el usuario selecciona una clase de classroom se emitira una señal respectiva.
    '''

    senal_eligioUnCurso=pyqtSignal(bool)  # Mandara solo  el valor de: True, y este se mandara solo
                                          # cuando el usuario haya escogido una clase de Classroom

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
        self.configuracionCalificador = configuracionCalificador


        # keys: los id que le asigna la API a cada clase de classroom
        # values: los nombres de cada clase de classroom
        self.dictCursos = {}
        self.cargarDatosClase()

        self.btn_refrescarLasClases.clicked.connect(self.refrescarClases)
        self.btn_realizarCambio.clicked.connect(self.realizarCambioClase)

    def prepararMostrar(self):
        '''
        Mostrara el nombre de la clase de classroom que esta seleccionada
        asi como tambien la ubicara dentro del combo box.
        '''

        _,cursoClassroom_nombre = self.configuracionCalificador.get_id_nombre_cursoClassroom()

        if cursoClassroom_nombre!=None:
            self.bel_nombreClaseActual.setText(cursoClassroom_nombre)
            self.comboBox_clases.setCurrentText(cursoClassroom_nombre)


    def cargarDatosClase(self):
        '''
        Cargara los nombre de las clases de classroom  que se encuentran
        almacenados en la base de datos local, es importante mencionar
        que dichos nombres los cargara en un 'ComboBox' para que el
        usuario los pueda ver y elegir uno de ellos si asi lo desea.
        '''

        # obteniendo los datos de las clases de classroom que se encuentran
        # almacenadas en la base de datos local.El formato de como retornara
        # los datos la base de datos local sera el siguiente:
        # (  (id_api_1,nombre_1), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
        tuplaDatosClases=self.baseDatosLocalClassRoom.get_tuplaClases()

        # ¿la base de datos local retorno cero  datos de clases de classroom?
        if tuplaDatosClases==() or len(tuplaDatosClases)==0:

            # como no se obtuvo el dato de ninguna clase de classroom se hara una consulta
            # a la API de google classroom ya que probablemente no se ha hecho ninguna
            # consulta y por eso no hay ningun dato de ninguna clase de classroom registrado
            # La tupla retornara los datos en el siguiente formato:
            # (  (id_api_1,nombre_1), (id_api_2,nombre_2), (id_api_3,nombre_3), ...)
            tuplaDatosClases=self.classRoomControl.get_listaDatosCursos()

            # Agrengando a la base de datos local los datos que se obtuvieron despues
            # de hacer la consulta a la API  de google classroom
            self.baseDatosLocalClassRoom.add_tuplaCursos(tuplaDatos=tuplaDatosClases)

        # keys: los id que le asigna la API a cada clase de classroom
        # values: los nombres de cada clase de classroom
        self.dictCursos={}
        self.comboBox_clases.clear()
        print(tuplaDatosClases)

        if tuplaDatosClases != () or len(tuplaDatosClases) != 0:
            self.dictCursos= dict(tuplaDatosClases)
            self.comboBox_clases.addItems( tuple( self.dictCursos.values() ) )
            print(tuplaDatosClases)


    def refrescarClases(self):
        '''
        El objetivo de este metodo es actualizar su contenido con respecto a las clases
        de classroom que se muestran para que puedan ser seleccionadas.

        Consultara a la API de google classroom para obtener todos los nombres y ids de las
        clases de classroom registradas en la cuenta de google del usuario, posteriormente
        para evitar duplicacion de datos procede a borrar todos los datos de las clases de
        classroom que se tenian registrados en la base de datos local, despues guardara los
        datos de las clases de classroom obtenidos al hacer la consulta a la API de google
        classroom y finalmente mostrara en el comboxBox los nombres de las clases de classroom
        obtenidos.
        '''

        respuestaAfirmativa=self.msg_preguntarAcercaRefrescarClases()

        if respuestaAfirmativa:
            # eliminamos todos los datos de las clases de classroom registrados
            # dentro de la base de datos local
            self.baseDatosLocalClassRoom.eliminarCursosRegistrados()

            # Consultando a la API de google classroom los datos de las clases de google classroom
            # del usuario.Los datos se obtienen con el siguiente formato:
            # (  (id_api_1,nombre_1), (id_api_2,nombre_2), (id_api_3,nombre_3), ...)
            tuplaDatosClases = self.classRoomControl.get_listaDatosCursos()

            # keys: los id que le asigna la API a cada clase de classroom
            # values: los nombres de cada clase de classroom
            self.dictCursos={}

            self.comboBox_clases.clear()

            if len(tuplaDatosClases)>0:

                # agregando los datos obtenidos  de las clases de google classroom existentes
                self.baseDatosLocalClassRoom.add_tuplaCursos(tuplaDatos=tuplaDatosClases)

                # keys: los id que le asigna la API a cada clase de classroom
                # values: los nombres de cada clase de classroom
                self.dictCursos = dict(tuplaDatosClases)

            else:
                self.msg_ningunaClaseRegistrada()

            self.comboBox_clases.addItems( tuple( self.dictCursos.values() ) )
            self.msg_exitoDescargarClasesClassroom()


    def realizarCambioClase(self):
        '''
        Este metodo se llama cuando el usuario da clic sobre el boton para confirmar
        su eleccion de la clase de classroom elegida.Lo que hara este metodo sera
        lo siguiente:
            * Cerciorarse de que el usuario haya seleccionado una clase de classroom.
            * Cersiorarse que el curso que selecciono sea diferente al que ya esta
            seleccionado.
            * Preguntarle al usuario si esta seguro de la seleccion de la clase de
            classrom hecha,si el usuario responde afirmativamente:
                * Se guardaran los datos de la nueva clase de classroom seleccionada.
                * Se emitira una señal para avisar de que el usuario ha seleccionado una
                clase de classroom.
        '''

        if len(self.dictCursos)>0:
            cursoElegido_index=self.comboBox_clases.currentIndex()
            cursoElegido_nombre=self.comboBox_clases.currentText()
            cursoElegido_api_id = tuple(self.dictCursos.keys())[cursoElegido_index]
            cursoClassroomActual_id, _ = self.configuracionCalificador.get_id_nombre_cursoClassroom()


            # ¿la clase que se selecciono es diferente a la acutal seleccionada?
            if cursoClassroomActual_id !=  cursoElegido_api_id:
                respuestaPositiva=self.msg_preguntarConfirmacionEleccionCurso(nombreCursoSeleccionado=cursoElegido_nombre)

                if respuestaPositiva:
                    cursoElegido_tuplaDatos=(cursoElegido_api_id,cursoElegido_nombre)

                    # Guardando en el objeto 'configuracionCalificador' los datos de  la clase de classroom
                    # que se selecciono
                    self.configuracionCalificador.cargarDatosClaseClassroom_seleccionada(
                        clase_idApi=cursoElegido_api_id,
                        clase_nombre=cursoElegido_nombre
                    )

                    self.senal_eligioUnCurso.emit(True)
                    self.close()

            else:
                self.msg_yaTeniasEseCursoSeleccionado()

        else:
            self.msg_noPuedesElegirCurso_siNoHay()


##########################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################

    def msg_preguntarConfirmacionEleccionCurso(self,nombreCursoSeleccionado):
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de querer seleccionar la clase de classroom cuyo nombre es el valor que almacena
        el parametro: 'nombreCursoSeleccionado'

        Parámetros:
            - nombreCursoSeleccionado (str) : Nombre de la clase de classroom que el usuario quiere
            seleccionar.

        Returns:
            - True (bool) : Si el usuario confirmo positivamente de que la clase
            de classroom que selecciono si es la que desea.
            - False (bool): Si el usuario respondio que NO es la clase de classroom
            que desea seleccionar
        '''

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
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que se
        ha refrescado exitosamente.
        '''

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


    def msg_yaTeniasEseCursoSeleccionado(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que el curso
        de classroom que selecciono ya lo tenia seleccionado
        '''

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "El curso de classroom que elegiste ya lo tienes seleccionado"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()




    def msg_noPuedesElegirCurso_siNoHay(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que no
        se se tiene ninguna clase de classroom registra, y que por ende no puede seleccionar
        ninguna clase de classroom.
        '''

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
        '''
        Mostrara un cuadro de dialogo al usuario para preguntarle si
        en realidad desea refrescar.

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si
            desea  refrescar
            - False (bool): Si el usuario dijo que NO desea refrescar
        '''

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
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de informarle
        que al hacer la consulta a google classroom no se encontro ninguna
        clase de classroom en su cuenta de google.
        '''

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
    application = CambiadorClases()
    application.show()
    app.exit(app.exec())