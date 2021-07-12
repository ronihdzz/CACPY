# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PerfilMain_d.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(424, 530)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.bel_imagenPerfilProfesor = QtWidgets.QLabel(Form)
        self.bel_imagenPerfilProfesor.setMinimumSize(QtCore.QSize(180, 175))
        self.bel_imagenPerfilProfesor.setMaximumSize(QtCore.QSize(200, 200))
        self.bel_imagenPerfilProfesor.setStyleSheet("")
        self.bel_imagenPerfilProfesor.setText("")
        self.bel_imagenPerfilProfesor.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.bel_imagenPerfilProfesor.setObjectName("bel_imagenPerfilProfesor")
        self.horizontalLayout.addWidget(self.bel_imagenPerfilProfesor)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setMinimumSize(QtCore.QSize(60, 50))
        self.label_4.setMaximumSize(QtCore.QSize(50, 50))
        self.label_4.setBaseSize(QtCore.QSize(50, 50))
        self.label_4.setStyleSheet("border-image: url(:/main/IMAGENES/profesor.png);\n"
"margin-left:10px;")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.bel_profesor_nombre = QtWidgets.QLabel(Form)
        self.bel_profesor_nombre.setMinimumSize(QtCore.QSize(200, 20))
        self.bel_profesor_nombre.setMaximumSize(QtCore.QSize(200, 30))
        self.bel_profesor_nombre.setStyleSheet("font-family: TamilSangamMN;\n"
"font-size: 13px;")
        self.bel_profesor_nombre.setOpenExternalLinks(True)
        self.bel_profesor_nombre.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.bel_profesor_nombre.setObjectName("bel_profesor_nombre")
        self.horizontalLayout_3.addWidget(self.bel_profesor_nombre)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(60, 50))
        self.label_3.setMaximumSize(QtCore.QSize(50, 50))
        self.label_3.setBaseSize(QtCore.QSize(50, 50))
        self.label_3.setStyleSheet("border-image: url(:/main/IMAGENES/gmail.png);\n"
"margin-left:10px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.bel_profesor_correo = QtWidgets.QLabel(Form)
        self.bel_profesor_correo.setMinimumSize(QtCore.QSize(200, 20))
        self.bel_profesor_correo.setMaximumSize(QtCore.QSize(16777215, 30))
        self.bel_profesor_correo.setStyleSheet("font-family: TamilSangamMN;\n"
"font-size: 13px;")
        self.bel_profesor_correo.setOpenExternalLinks(True)
        self.bel_profesor_correo.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.bel_profesor_correo.setObjectName("bel_profesor_correo")
        self.horizontalLayout_2.addWidget(self.bel_profesor_correo)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem9)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem10)
        self.btn_cerrarSesion = QtWidgets.QCommandLinkButton(Form)
        self.btn_cerrarSesion.setMinimumSize(QtCore.QSize(120, 40))
        self.btn_cerrarSesion.setMaximumSize(QtCore.QSize(140, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.btn_cerrarSesion.setFont(font)
        self.btn_cerrarSesion.setIconSize(QtCore.QSize(0, 20))
        self.btn_cerrarSesion.setDescription("")
        self.btn_cerrarSesion.setObjectName("btn_cerrarSesion")
        self.horizontalLayout_4.addWidget(self.btn_cerrarSesion)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem11)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem12)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.bel_profesor_nombre.setText(_translate("Form", "David Roni Hernández Beltrán"))
        self.bel_profesor_correo.setText(_translate("Form", "ronroni.99@gmail.com"))
        self.btn_cerrarSesion.setText(_translate("Form", "Cerrar sesión"))
import img_rc