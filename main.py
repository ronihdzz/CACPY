from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen
import sys, time, os
import recursos

###############################################################
#  IMPORTACION DEL LOGICA...
##############################################################
from CUERPO.LOGICA.MAIN.Main import Main

if __name__ == '__main__':

    direccionTotal=sys.argv[0]
    direccionPartes=os.path.normpath(direccionTotal)
    direccionPartes=direccionPartes.split(os.sep)
    ruta_direccionTotal = os.sep.join( direccionPartes[:-1] )
    if len(direccionPartes)>1:
        ruta_direccionTotal+=os.sep
    recursos.App_Principal.actualizarUbicaciones(ruta_direccionTotal)


    correo_profesor=None
    nombre_profesor=None
    curso_id=None
    topic_id=None
    if os.path.isfile(recursos.App_Principal.ARCHIVO_DATOS_PROFESOR):
        # Contiene los datos cada uno separado por un salto de linea
        # correo del profesor, nombre completo del profesor
        with open(recursos.App_Principal.ARCHIVO_DATOS_PROFESOR) as archivo:
            datos=archivo.read()
        correo_profesor, nombre_profesor=datos.split('\n')


    if os.path.isfile(recursos.App_Principal.ARCHIVO_TRABAJO_PROFESOR):
        # Contiene los datos cada uno separado por un salto de linea
        # curso_id, topic_id
        with open(recursos.App_Principal.ARCHIVO_TRABAJO_PROFESOR) as archivo:
            datos=archivo.read()
        curso_id,topic_id=datos.split('\n')


    app = QApplication(sys.argv)
    splash_pix = QPixmap(recursos.App_Principal.IMAGEN_SPLASH_SCREEN)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    time.sleep(1)
    form = Main(
        correo_profesor=correo_profesor,
        nombre_profesor=nombre_profesor,
        curso_id=curso_id,
        topic_id=topic_id
    )
    form.show()
    splash.finish(form)
    app.exec_()


# curso_id = '267287795258'
# tareasProgramas_topic_id = '369766123712'
# c=self.elClassRoom_control.get_listaTareasTopic(curso_id=curso_id,
#                                              topic_id=tareasProgramas_topic_id)
# print(c)
# self.baseDatosLocalClassRoomProgramas.add_courseWork(c[0])

# a=self.elClassRoom_control.get_listaDatosCursos()
# print(a)
# self.baseDatosLocalClassRoomProgramas.add_curso(a[0])

# b=self.elClassRoom_control.get_listaDatosTopicsCurso(curso_id=curso_id)
# print(b)
# self.baseDatosLocalClassRoomProgramas.add_topic(b[0])

