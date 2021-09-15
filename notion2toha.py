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
        self.btnSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnSave.setObjectName("btnSave")
        self.verticalLayout_2.addWidget(self.btnSave)
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
        self.btnSave.clicked.connect(self.btnSave_clicked)
          
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Alt 속성 생성기"))
        self.tedtOri.setPlainText(_translate("MainWindow", "변경하실 파일을 선택해주세요."))
        self.btnFind.setText(_translate("MainWindow", "불러오기"))
        self.btnSave.setText(_translate("MainWindow", "저장하기"))
        self.btnFind.setFocus()

    def btnFind_clicked(self):
        # 찾기

        zipPath = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "불러오기", "./", "zip(*.zip)")

        self.tedtOri.setPlainText(func.getMemo(zipPath[0]))

        # self.tedtMod.setPlainText(func.getPost(self.tedtOri.toPlainText()))

    def btnSave_clicked(self):
        # 저장하기
        
        # 저장경로 기존에 설정되어 있으면 그대로 아니면 다른경로로
        if(settings.PROJECT_PATH == ''):
            isProjectPath = True
        else:   
            isProjectPath = False

        QtWidgets.QMessageBox.about(MainWindow, '알림', str(isProjectPath))
        
        func.savePost(isProjectPath, savePath, self.tedtMod.toPlainText())
        
        # QtWidgets.QMessageBox.about(MainWindow, '알림', "저장 완료!")
        # 내용 비우기


if __name__ == "__main__":
    settings.init()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
