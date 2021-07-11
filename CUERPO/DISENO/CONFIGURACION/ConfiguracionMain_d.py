# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConfiguracionMain_d.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(618, 498)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setMinimumSize(QtCore.QSize(400, 150))
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setMinimumSize(QtCore.QSize(0, 18))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, -1, 20, -1)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btn_editarClase = QtWidgets.QPushButton(self.widget)
        self.btn_editarClase.setMinimumSize(QtCore.QSize(35, 35))
        self.btn_editarClase.setMaximumSize(QtCore.QSize(35, 35))
        self.btn_editarClase.setBaseSize(QtCore.QSize(20, 20))
        self.btn_editarClase.setStyleSheet("QPushButton {\n"
"border-image: url(:/main/IMAGENES/edit_off.png);\n"
" }\n"
"QPushButton:hover {\n"
"border-image: url(:/main/IMAGENES/edit_on.png);\n"
"}\n"
"QPushButton:pressed {\n"
"border-image: url(:/main/IMAGENES/edit_off.png);\n"
"}\n"
"")
        self.btn_editarClase.setText("")
        self.btn_editarClase.setObjectName("btn_editarClase")
        self.verticalLayout_6.addWidget(self.btn_editarClase)
        self.label_15 = QtWidgets.QLabel(self.widget)
        self.label_15.setMinimumSize(QtCore.QSize(35, 35))
        self.label_15.setMaximumSize(QtCore.QSize(35, 35))
        self.label_15.setBaseSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setWordWrap(True)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_6.addWidget(self.label_15)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setMinimumSize(QtCore.QSize(40, 50))
        self.label_4.setMaximumSize(QtCore.QSize(70, 50))
        self.label_4.setBaseSize(QtCore.QSize(40, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.bel_nombreClase = QtWidgets.QLabel(self.widget)
        self.bel_nombreClase.setMinimumSize(QtCore.QSize(200, 50))
        self.bel_nombreClase.setMaximumSize(QtCore.QSize(16777215, 50))
        self.bel_nombreClase.setBaseSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.bel_nombreClase.setFont(font)
        self.bel_nombreClase.setStyleSheet("border: 1px solid black;\n"
"border-radius:5px;")
        self.bel_nombreClase.setObjectName("bel_nombreClase")
        self.horizontalLayout_2.addWidget(self.bel_nombreClase)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setMinimumSize(QtCore.QSize(0, 18))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(-1, -1, 20, -1)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.btn_eliminarApartado = QtWidgets.QPushButton(Form)
        self.btn_eliminarApartado.setMinimumSize(QtCore.QSize(50, 50))
        self.btn_eliminarApartado.setMaximumSize(QtCore.QSize(35, 35))
        self.btn_eliminarApartado.setBaseSize(QtCore.QSize(30, 30))
        self.btn_eliminarApartado.setStyleSheet("\n"
"QPushButton {\n"
"border-image: url(:/main/IMAGENES/eliminar_off.png);\n"
" }\n"
"\n"
"QPushButton:hover {\n"
"border-image: url(:/main/IMAGENES/eliminar_on.png);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"border-image: url(:/main/IMAGENES/eliminar_off.png);\n"
"}\n"
"")
        self.btn_eliminarApartado.setText("")
        self.btn_eliminarApartado.setObjectName("btn_eliminarApartado")
        self.verticalLayout_7.addWidget(self.btn_eliminarApartado)
        self.bel_agregar_or_guardar_apar_2 = QtWidgets.QLabel(Form)
        self.bel_agregar_or_guardar_apar_2.setMinimumSize(QtCore.QSize(50, 35))
        self.bel_agregar_or_guardar_apar_2.setMaximumSize(QtCore.QSize(35, 35))
        self.bel_agregar_or_guardar_apar_2.setBaseSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.bel_agregar_or_guardar_apar_2.setFont(font)
        self.bel_agregar_or_guardar_apar_2.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_agregar_or_guardar_apar_2.setWordWrap(True)
        self.bel_agregar_or_guardar_apar_2.setObjectName("bel_agregar_or_guardar_apar_2")
        self.verticalLayout_7.addWidget(self.bel_agregar_or_guardar_apar_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(-1, -1, 20, -1)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.btn_editApartado = QtWidgets.QPushButton(Form)
        self.btn_editApartado.setMinimumSize(QtCore.QSize(35, 35))
        self.btn_editApartado.setMaximumSize(QtCore.QSize(35, 35))
        self.btn_editApartado.setBaseSize(QtCore.QSize(20, 20))
        self.btn_editApartado.setStyleSheet("QPushButton {\n"
"border-image: url(:/main/IMAGENES/edit_off.png);\n"
" }\n"
"QPushButton:hover {\n"
"border-image: url(:/main/IMAGENES/edit_on.png);\n"
"}\n"
"QPushButton:pressed {\n"
"border-image: url(:/main/IMAGENES/edit_off.png);\n"
"}\n"
"")
        self.btn_editApartado.setText("")
        self.btn_editApartado.setObjectName("btn_editApartado")
        self.verticalLayout_5.addWidget(self.btn_editApartado)
        self.bel_edit_or_cancelEdit_aparSelec = QtWidgets.QLabel(Form)
        self.bel_edit_or_cancelEdit_aparSelec.setMinimumSize(QtCore.QSize(35, 35))
        self.bel_edit_or_cancelEdit_aparSelec.setMaximumSize(QtCore.QSize(35, 35))
        self.bel_edit_or_cancelEdit_aparSelec.setBaseSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.bel_edit_or_cancelEdit_aparSelec.setFont(font)
        self.bel_edit_or_cancelEdit_aparSelec.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_edit_or_cancelEdit_aparSelec.setWordWrap(True)
        self.bel_edit_or_cancelEdit_aparSelec.setObjectName("bel_edit_or_cancelEdit_aparSelec")
        self.verticalLayout_5.addWidget(self.bel_edit_or_cancelEdit_aparSelec)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, -1, 20, -1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_agregarApartado = QtWidgets.QPushButton(Form)
        self.btn_agregarApartado.setMinimumSize(QtCore.QSize(35, 35))
        self.btn_agregarApartado.setMaximumSize(QtCore.QSize(35, 35))
        self.btn_agregarApartado.setBaseSize(QtCore.QSize(30, 30))
        self.btn_agregarApartado.setStyleSheet("\n"
"QPushButton {\n"
"border-image: url(:/main/IMAGENES/plus_off.png);\n"
" }\n"
"\n"
"QPushButton:hover {\n"
"border-image: url(:/main/IMAGENES/plus_on.png);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"border-image: url(:/main/IMAGENES/plus_off.png);\n"
"}\n"
"")
        self.btn_agregarApartado.setText("")
        self.btn_agregarApartado.setObjectName("btn_agregarApartado")
        self.verticalLayout_2.addWidget(self.btn_agregarApartado)
        self.bel_agregar_or_guardar_apar = QtWidgets.QLabel(Form)
        self.bel_agregar_or_guardar_apar.setMinimumSize(QtCore.QSize(35, 35))
        self.bel_agregar_or_guardar_apar.setMaximumSize(QtCore.QSize(35, 35))
        self.bel_agregar_or_guardar_apar.setBaseSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.bel_agregar_or_guardar_apar.setFont(font)
        self.bel_agregar_or_guardar_apar.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_agregar_or_guardar_apar.setWordWrap(True)
        self.bel_agregar_or_guardar_apar.setObjectName("bel_agregar_or_guardar_apar")
        self.verticalLayout_2.addWidget(self.bel_agregar_or_guardar_apar)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 150))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_15.setText(_translate("Form", "Editar"))
        self.label_4.setText(_translate("Form", "Clase:"))
        self.bel_nombreClase.setText(_translate("Form", "Python pre-intermedio"))
        self.label_6.setText(_translate("Form", "Apartados tareas"))
        self.bel_agregar_or_guardar_apar_2.setText(_translate("Form", "Eliminar\n"
""))
        self.bel_edit_or_cancelEdit_aparSelec.setText(_translate("Form", "Editar"))
        self.bel_agregar_or_guardar_apar.setText(_translate("Form", "Agregar\n"
"apartado"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Topic programas"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Topic retroalimentacion"))
import img_rc
