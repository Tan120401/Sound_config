# Form implementation generated from reading ui file '.\sound_config.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(731, 547)
        self.centralwidget = QtWidgets.QWidget(parent=mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(190, 20, 91, 41))
        self.startBtn.setObjectName("startBtn")
        self.selectallBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selectallBtn.setGeometry(QtCore.QRect(40, 20, 91, 41))
        self.selectallBtn.setObjectName("selectallBtn")
        self.tableResult = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableResult.setGeometry(QtCore.QRect(40, 120, 641, 361))
        self.tableResult.setObjectName("tableResult")
        self.tableResult.setColumnCount(0)
        self.tableResult.setRowCount(0)
        self.openlogBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.openlogBtn.setGeometry(QtCore.QRect(350, 20, 91, 41))
        self.openlogBtn.setObjectName("openlogBtn")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 731, 33))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Sound Config Test"))
        self.startBtn.setText(_translate("mainWindow", "Start"))
        self.selectallBtn.setText(_translate("mainWindow", "Select All"))
        self.openlogBtn.setText(_translate("mainWindow", "Open Log"))
