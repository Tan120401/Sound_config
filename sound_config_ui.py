# Form implementation generated from reading ui file '.\sound_config_ui.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(883, 570)
        self.centralwidget = QtWidgets.QWidget(parent=mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(440, 40, 90, 45))
        self.startBtn.setObjectName("startBtn")
        self.selectallBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.selectallBtn.setGeometry(QtCore.QRect(330, 40, 90, 45))
        self.selectallBtn.setObjectName("selectallBtn")
        self.tableResult = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableResult.setGeometry(QtCore.QRect(40, 120, 821, 401))
        self.tableResult.setObjectName("tableResult")
        self.tableResult.setColumnCount(0)
        self.tableResult.setRowCount(0)
        self.refreshBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.refreshBtn.setGeometry(QtCore.QRect(660, 40, 90, 45))
        self.refreshBtn.setObjectName("refreshBtn")
        self.searchBar = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.searchBar.setGeometry(QtCore.QRect(40, 40, 161, 45))
        self.searchBar.setText("")
        self.searchBar.setObjectName("searchBar")
        self.searchBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.searchBtn.setGeometry(QtCore.QRect(220, 40, 90, 45))
        self.searchBtn.setObjectName("searchBtn")
        self.stopBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.stopBtn.setGeometry(QtCore.QRect(550, 40, 90, 45))
        self.stopBtn.setObjectName("stopBtn")
        self.openlogBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.openlogBtn.setGeometry(QtCore.QRect(770, 40, 90, 45))
        self.openlogBtn.setObjectName("openlogBtn")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 883, 33))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Sound Config Auto"))
        self.startBtn.setText(_translate("mainWindow", "Start"))
        self.selectallBtn.setText(_translate("mainWindow", "Select All"))
        self.refreshBtn.setText(_translate("mainWindow", "Refresh"))
        self.searchBar.setPlaceholderText(_translate("mainWindow", "Type here to search..."))
        self.searchBtn.setText(_translate("mainWindow", "Search"))
        self.stopBtn.setText(_translate("mainWindow", "Stop"))
        self.openlogBtn.setText(_translate("mainWindow", "Open Result"))
