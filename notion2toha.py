from PyQt5 import QtCore, QtGui, QtWidgets
import re
import os
import sys

import settings
import func


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        # MainWindow.setWindowIcon(QtGui.QIcon(':/icon.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(1677215, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 1, 1, 1)
        self.tedtOri = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.tedtOri.setPlainText("")
        self.tedtOri.setObjectName("tedtOri")
        self.gridLayout.addWidget(self.tedtOri, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnFind = QtWidgets.QPushButton(self.centralwidget)
        self.btnFind.setObjectName("btnFind")
        self.verticalLayout_2.addWidget(self.btnFind)
        self.btnRun = QtWidgets.QPushButton(self.centralwidget)
        self.btnRun.setObjectName("btnRun")
        self.verticalLayout_2.addWidget(self.btnRun)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.tedtMod = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.tedtMod.setObjectName("tedtMod")
        self.gridLayout.addWidget(self.tedtMod, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ------------------------------------------------
        # UI 이벤트 설정
        # ------------------------------------------------
        self.btnFind.clicked.connect(self.btnFind_clicked)   
        self.btnRun.clicked.connect(self.btnRun_clicked)
          
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Alt 속성 생성기"))
        self.tedtOri.setPlainText(_translate("MainWindow", "변경하실 파일을 선택해주세요."))
        self.btnFind.setText(_translate("MainWindow", "찾기.."))
        self.btnRun.setText(_translate("MainWindow", "변경하기"))
        self.btnFind.setFocus()

    def btnFind_clicked(self):
        # 찾기

        fname = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "불러오기", "./", "Markdown(*.md)")

        self.tedtOri.setPlainText(func.readMd(fname[0]))

        self.tedtMod.setPlainText(func.modifyMd(self.tedtOri.toPlainText()))

    def btnRun_clicked(self):
        # 변경하기

        imgDir = func.findImgFolder()
        if imgDir != None:
            option = QtWidgets.QMessageBox.question(MainWindow, "폴더 변경", imgDir + "폴더명을 'Image'로 변경할까요?")
            if option == QtWidgets.QMessageBox.Yes:
                func.renameFolder(imgDir)
        
        func.saveMd(self.tedtMod.toPlainText())

        QtWidgets.QMessageBox.about(MainWindow, '알림', "변경 완료!")



if __name__ == "__main__":
    settings.init()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
