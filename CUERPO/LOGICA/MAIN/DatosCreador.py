
'''
DatosCreador.py :   Contiene una sola  clase, la clase 'Dialog_datosCreador', la cual a grosso
                    modo se encarga de que el usuario vea y tenga acceso a los principales
                    contactos de información del programador de la aplicacion.
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5 import QtWidgets, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from  CUERPO.DISENO.MAIN.DatosCreador_d import Ui_Dialog
from recursos import HuellaAplicacion,App_datosCreador


class Dialog_datosCreador(QtWidgets.QDialog, Ui_Dialog,HuellaAplicacion):
    '''
    La finalidad de esta clase es proporcionar los contactos del programador
    asi como los accesos directos a sus redes sociales.
    Es importante mencionar que esta clase obtiene los datos del programador
    de la clase: 'App_datosCreador'
    '''


    def __init__(self):
        Ui_Dialog.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        HuellaAplicacion.__init__(self)

        # nombre de la aplicacion del programa
        nombre=App_datosCreador.NOMBRE_PROGRAMADOR

        # likedin del programador
        likedin=App_datosCreador.LIKEDIN_NOMBRE
        likedin_link=App_datosCreador.LIKEDIN_LINK

        # github del programador
        github=App_datosCreador.GITHUB_NOMBRE
        github_link=App_datosCreador.GITHUB_LINK

        # repositorio de este proyecto en especifico
        repositorio=App_datosCreador.REPOSITORIO_PROYECTO_NOMBRE
        repositorio_link=App_datosCreador.REPOSITORIO_PROYECTO_LINK

        # foto del programador
        fotoProgramador=App_datosCreador.FOTO_PROGRAMADOR

        # lista de gmails de contacto del progrmador
        gmails=App_datosCreador.GMAILS

        # asunto del mensaje que se le adjuntara al programador cuando el usuario decida mandarle mensaje
        subject=App_datosCreador.GMAIL_SUBJECT

        # sugerencia de como iniciar el mensaje que se de le desea adjuntar al programador
        body=App_datosCreador.GMAIL_CUERPO
        
        # como los datos del programador se muestran en formato de html, entonces a continuacion
        # se procede a hacer el codigo respectivo en html de cada seccion de contacto del programador
        gmail_html=f'<span style=" font-size:13px;font-family:TamilSangamMN;"><a href="mailto:{",".join(gmails)}?subject={subject}&body={body}" style="color:black;text-decoration:none;">{gmails[0]}</a></span>'
        likedin_html=f'<span style=" font-size:13px;font-family:TamilSangamMN;"><a href="{likedin_link}" style="color:black;text-decoration:none;">{likedin}</a></span>'
        github_html=f'<span style=" font-size:13px;font-family:TamilSangamMN;"><a href="{github_link}" style="color:black;text-decoration:none;">{github}</a></span>'

        # adjuntando el texto a cada repectivo apartado de la ventana
        self.textBrowser_repositorio.setHtml(f"""
            <span style=" font-size:13px;font-family: TamilSangamMN;">Repositorio de todo el proyecto</span></p>
            <span style=" font-size:13px;font-family: TamilSangamMN;"><a href="{repositorio_link}"  style="color:black;"> <b>{repositorio}<\b> </a></span>
        """)

        self.textBrowser_nombreProgra.setHtml(f"""
        <p align="center"><span style="font-size:13px; font-family:TamilSangamMN; style='text-align:center">Desarrollador</span>
        <br>
        <span style="font-size:16px;font-family: TamilSangamMN;text-align:center;"><b>{nombre}</b></span>
        </p>""")


        self.bel_fotoProgramador.setStyleSheet(f"""
                    border-image: url({fotoProgramador});
                    border-radius:87%;""")

        self.bel_likedin.setText(likedin_html)
        self.bel_github.setText(github_html)
        self.bel_gmail.setText(gmail_html)

        # permitiendo que se puedan abrirs link a partir de dar click izqueirdo sobre los links que contengan
        # los objetos siguientes

        self.bel_likedin.setOpenExternalLinks(True)
        self.bel_github.setOpenExternalLinks(True)
        self.bel_gmail.setOpenExternalLinks(True)
        self.textBrowser_repositorio.setOpenLinks(True)
        self.textBrowser_repositorio.setOpenExternalLinks(True)

        # hace que el texto pueda ser seleccionado
        #self.bel_gmail.setTextInteractionFlags(Qt.TextSelectableByMouse)



    def cargarImagen_programador(self,imagen):
        '''
        Este metodo fue diseñado para cargar una imagen del programador que se encuentre en una ruta
        en particular.

        Parámetros:
            imagen (str) : Nombre completo de la imagen que se quiere adjuntar como
            foto de programador, cabe mencionar que por nombre completo me refiero
            que el nombre debe incluir tambien la ruta del archivo completa.
        '''

        # Cargando la imagen
        ancho=self.bel_fotoProgramador.width()
        alto=self.bel_fotoProgramador.height()

        pixmapImagen = QPixmap(imagen).scaled(ancho * 0.95, alto * 0.95, Qt.IgnoreAspectRatio,
                                              Qt.SmoothTransformation)
        self.bel_fotoProgramador.setAlignment(Qt.AlignCenter)
        self.bel_fotoProgramador.setPixmap(pixmapImagen)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Dialog_datosCreador()
    application.show()
    app.exec()
    #sys.exit(app.exec())
