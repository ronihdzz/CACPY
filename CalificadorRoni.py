from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen
import sys, time, os
import recursos
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QApplication, QSpinBox, QActionGroup,
                             QLabel, QWidget, QPushButton, QVBoxLayout, QScrollArea, QMessageBox, QStackedWidget)


###############################################################
#  IMPORTACION DEL LOGICA...
##############################################################
from CUERPO.LOGICA.MAIN.Main import Main
from CUERPO.LOGICA.API.CalificadorConfiguracion import CalificadorConfiguracion
from CUERPO.LOGICA.API.ClassRoomControl import ClassRoomControl
from CUERPO.LOGICA.API.BaseDatosLocal import BaseDatos_ClassRoomProgramas
from CUERPO.LOGICA.MAIN.CargadorCredencial import CargadorCrendencial

if __name__ == '__main__':
    ###############################################################
    # Corrigiendo las rutas de nuestra carpeta de recursos
    ###############################################################
    direccionTotal=sys.argv[0]
    direccionPartes=os.path.normpath(direccionTotal)
    direccionPartes=direccionPartes.split(os.sep)
    ruta_direccionTotal = os.sep.join( direccionPartes[:-1] )
    if len(direccionPartes)>1:
        ruta_direccionTotal+=os.sep
    recursos.App_Principal.actualizarUbicaciones(ruta_direccionTotal)
    recursos.App_Principal.serciorarExistenciaCarpetaRecursos()


    exiteArchivoCredenciales=os.path.isfile(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)

    # Se obtiene un objeto que podra hacer consultas al classroom del profesor
    # que abrio la aplicacion
    elClassRoomControl=ClassRoomControl()


    if not exiteArchivoCredenciales:
        app = QApplication(sys.argv)
        splash_pix = QPixmap(recursos.App_Principal.IMAGEN_SPLASH_SCREEN)
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()

        # Simulate something that takes time
        time.sleep(1)
        form = CargadorCrendencial(
            classRoomControl=elClassRoomControl
        )
        form.show()
        splash.finish(form)
        app.exec_()


    else:

        ejecutarPrograma=True

        # En caso de no existir el token que permite el acceso del classroom
        # y del drive del profesor, el token se crea.
        try:
            elClassRoomControl.obtenerValor_service_classroom_and_drive()
            ejecutarPrograma=True
        except Exception as e:
            try:
                print(f"Es posible curar el error: <<{e}>> eliminando el token viejo")
                elClassRoomControl.eliminarArchivoToken()
                elClassRoomControl.obtenerValor_service_classroom_and_drive()
                ejecutarPrograma=True
            except Exception as e:
                print("Error:<<",e,">>, por favor consultalo con el programador")
                ejecutarPrograma=False

        if ejecutarPrograma:
            configuracionCalificador=CalificadorConfiguracion()
            configuracionCalificador.cargarDatosProfesor(recursos.App_Principal.ARCHIVO_DATOS_PROFESOR)
            configuracionCalificador.cargarDatosUltimaSesion(recursos.App_Principal.ARCHIVO_TRABAJO_PROFESOR)

            # Se obtiene un objeto que permitira el manejo de la base de datos local
            # que almacenara los datos de classroom del profesor.
            baseDatosLocalClassRoomProgramas = BaseDatos_ClassRoomProgramas(
                NOMBRE_BASE_DATOS=recursos.App_Principal.NOMBRE_COMPLETO_BASE_DATOS
            )

            # Si no existe la base de datos local, entonces se crea
            baseDatosLocalClassRoomProgramas.crearBaseDatos()


            # Si no hay datos registrados del profesor entonces se pediran
            if configuracionCalificador.getNombreProfesor()==None:
                correo,nombre= elClassRoomControl.get_datosProfesor(
                    nombreCompletoFoto_guardar=recursos.App_Principal.FOTO_PERFIL_PROFESOR)

                configuracionCalificador.cargarDatosProfesorSinArchivo(
                    nombre=nombre,
                    correo=correo
                )

            app = QApplication(sys.argv)
            splash_pix = QPixmap(recursos.App_Principal.IMAGEN_SPLASH_SCREEN)
            splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
            splash.setMask(splash_pix.mask())
            splash.show()
            app.processEvents()

            # Simulate something that takes time
            time.sleep(1)
            form = Main(
                classRoomControl=elClassRoomControl,
                baseDatosLocalClassRoom=baseDatosLocalClassRoomProgramas,
                configuracionCalificador=configuracionCalificador
            )
            form.show()
            splash.finish(form)
            app.exec_()
