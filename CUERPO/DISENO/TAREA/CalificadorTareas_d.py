# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CalificadorTareas_d.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(591, 576)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(0, 50))
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setMinimumSize(QtCore.QSize(100, 30))
        self.label_4.setMaximumSize(QtCore.QSize(70, 30))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.bel_nombreCourseWork = QtWidgets.QLabel(Dialog)
        self.bel_nombreCourseWork.setMinimumSize(QtCore.QSize(200, 30))
        self.bel_nombreCourseWork.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bel_nombreCourseWork.setStyleSheet("border: 2px solid   black;\n"
"border-radius:5px\n"
"")
        self.bel_nombreCourseWork.setText("")
        self.bel_nombreCourseWork.setObjectName("bel_nombreCourseWork")
        self.horizontalLayout_7.addWidget(self.bel_nombreCourseWork)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setMinimumSize(QtCore.QSize(100, 30))
        self.label_5.setMaximumSize(QtCore.QSize(70, 30))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_8.addWidget(self.label_5)
        self.bel_fechaCreacion = QtWidgets.QLabel(Dialog)
        self.bel_fechaCreacion.setMinimumSize(QtCore.QSize(200, 30))
        self.bel_fechaCreacion.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bel_fechaCreacion.setStyleSheet("border: 2px solid   black;\n"
"border-radius:5px\n"
"")
        self.bel_fechaCreacion.setText("")
        self.bel_fechaCreacion.setObjectName("bel_fechaCreacion")
        self.horizontalLayout_8.addWidget(self.bel_fechaCreacion)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bel_noTareasCalificadasTotales = QtWidgets.QLabel(Dialog)
        self.bel_noTareasCalificadasTotales.setMinimumSize(QtCore.QSize(30, 30))
        self.bel_noTareasCalificadasTotales.setMaximumSize(QtCore.QSize(40, 40))
        self.bel_noTareasCalificadasTotales.setStyleSheet("border: 2px solid   black;\n"
"border-radius:5px\n"
"")
        self.bel_noTareasCalificadasTotales.setText("")
        self.bel_noTareasCalificadasTotales.setObjectName("bel_noTareasCalificadasTotales")
        self.horizontalLayout.addWidget(self.bel_noTareasCalificadasTotales)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(70, 30))
        self.label_3.setMaximumSize(QtCore.QSize(70, 30))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.horizontalLayout_10.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setMinimumSize(QtCore.QSize(70, 30))
        self.label_14.setMaximumSize(QtCore.QSize(70, 30))
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_4.addWidget(self.label_14)
        self.bel_noTareasPorCalificar = QtWidgets.QLabel(Dialog)
        self.bel_noTareasPorCalificar.setMinimumSize(QtCore.QSize(30, 30))
        self.bel_noTareasPorCalificar.setMaximumSize(QtCore.QSize(40, 40))
        self.bel_noTareasPorCalificar.setStyleSheet("border: 2px solid   black;\n"
"border-radius:5px\n"
"")
        self.bel_noTareasPorCalificar.setText("")
        self.bel_noTareasPorCalificar.setObjectName("bel_noTareasPorCalificar")
        self.horizontalLayout_4.addWidget(self.bel_noTareasPorCalificar)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setMinimumSize(QtCore.QSize(70, 30))
        self.label_18.setMaximumSize(QtCore.QSize(70, 30))
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_6.addWidget(self.label_18)
        self.bel_noTareasPorEntregar = QtWidgets.QLabel(Dialog)
        self.bel_noTareasPorEntregar.setMinimumSize(QtCore.QSize(30, 30))
        self.bel_noTareasPorEntregar.setMaximumSize(QtCore.QSize(40, 40))
        self.bel_noTareasPorEntregar.setStyleSheet("border: 2px solid   black;\n"
"border-radius:5px\n"
"")
        self.bel_noTareasPorEntregar.setText("")
        self.bel_noTareasPorEntregar.setObjectName("bel_noTareasPorEntregar")
        self.horizontalLayout_6.addWidget(self.bel_noTareasPorEntregar)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(298, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem)
        self.spinBox_tareasACalificar = QtWidgets.QSpinBox(Dialog)
        self.spinBox_tareasACalificar.setMinimumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBox_tareasACalificar.setFont(font)
        self.spinBox_tareasACalificar.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_tareasACalificar.setObjectName("spinBox_tareasACalificar")
        self.horizontalLayout_13.addWidget(self.spinBox_tareasACalificar)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.bel_noTareasCalificadas = QtWidgets.QLabel(Dialog)
        self.bel_noTareasCalificadas.setMinimumSize(QtCore.QSize(30, 30))
        self.bel_noTareasCalificadas.setMaximumSize(QtCore.QSize(40, 40))
        self.bel_noTareasCalificadas.setStyleSheet("border: 2px solid   black;\n"
"border-radius:5px\n"
"")
        self.bel_noTareasCalificadas.setText("")
        self.bel_noTareasCalificadas.setObjectName("bel_noTareasCalificadas")
        self.horizontalLayout_12.addWidget(self.bel_noTareasCalificadas)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setMinimumSize(QtCore.QSize(70, 30))
        self.label_6.setMaximumSize(QtCore.QSize(70, 30))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_12.addWidget(self.label_6)
        self.bel_noTareasAcalificar = QtWidgets.QLabel(Dialog)
        self.bel_noTareasAcalificar.setMinimumSize(QtCore.QSize(30, 30))
        self.bel_noTareasAcalificar.setMaximumSize(QtCore.QSize(40, 40))
        self.bel_noTareasAcalificar.setStyleSheet("border: 2px solid   black;\n"
"border-radius:5px\n"
"")
        self.bel_noTareasAcalificar.setText("")
        self.bel_noTareasAcalificar.setObjectName("bel_noTareasAcalificar")
        self.horizontalLayout_12.addWidget(self.bel_noTareasAcalificar)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(15)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setMinimumSize(QtCore.QSize(50, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.proBar_progresoCalif = QtWidgets.QProgressBar(Dialog)
        self.proBar_progresoCalif.setMinimumSize(QtCore.QSize(40, 0))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.proBar_progresoCalif.setFont(font)
        self.proBar_progresoCalif.setProperty("value", 50)
        self.proBar_progresoCalif.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.proBar_progresoCalif.setTextVisible(True)
        self.proBar_progresoCalif.setOrientation(QtCore.Qt.Vertical)
        self.proBar_progresoCalif.setInvertedAppearance(False)
        self.proBar_progresoCalif.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.proBar_progresoCalif.setObjectName("proBar_progresoCalif")
        self.verticalLayout.addWidget(self.proBar_progresoCalif, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_9.addLayout(self.verticalLayout)
        self.tableWidget_alumnosCalif = QtWidgets.QTableWidget(Dialog)
        self.tableWidget_alumnosCalif.setMinimumSize(QtCore.QSize(300, 150))
        self.tableWidget_alumnosCalif.setObjectName("tableWidget_alumnosCalif")
        self.tableWidget_alumnosCalif.setColumnCount(3)
        self.tableWidget_alumnosCalif.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_alumnosCalif.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_alumnosCalif.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_alumnosCalif.setHorizontalHeaderItem(2, item)
        self.horizontalLayout_9.addWidget(self.tableWidget_alumnosCalif)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(20)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem2)
        self.btn_calificar = QtWidgets.QPushButton(Dialog)
        self.btn_calificar.setMinimumSize(QtCore.QSize(100, 60))
        self.btn_calificar.setObjectName("btn_calificar")
        self.horizontalLayout_11.addWidget(self.btn_calificar)
        self.btn_detener = QtWidgets.QPushButton(Dialog)
        self.btn_detener.setMinimumSize(QtCore.QSize(100, 60))
        self.btn_detener.setObjectName("btn_detener")
        self.horizontalLayout_11.addWidget(self.btn_detener)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "CALIFICADOR"))
        self.label_4.setText(_translate("Dialog", "Nombre tarea:"))
        self.label_5.setText(_translate("Dialog", "Fecha emision:"))
        self.label_3.setText(_translate("Dialog", "Calificadas:"))
        self.label_14.setText(_translate("Dialog", "Por calificar:"))
        self.label_18.setText(_translate("Dialog", "Por entregar:"))
        self.label_2.setText(_translate("Dialog", "¿Cuantos alumnos  deseas calificar?"))
        self.label_6.setText(_translate("Dialog", "Calificadas de"))
        self.label_7.setText(_translate("Dialog", "50%"))
        self.proBar_progresoCalif.setFormat(_translate("Dialog", "%p%"))
        item = self.tableWidget_alumnosCalif.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Nombre"))
        item = self.tableWidget_alumnosCalif.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Correo"))
        item = self.tableWidget_alumnosCalif.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Calificacion"))
        self.btn_calificar.setText(_translate("Dialog", "Calificar"))
        self.btn_detener.setText(_translate("Dialog", "Detener"))