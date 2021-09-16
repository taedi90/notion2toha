#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import settings
import func
import subprocess
import os


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
        MainWindow.setWindowTitle(_translate("MainWindow", "Notion Memo to Hugo-toha Post"))
        self.tedtOri.setPlainText(_translate("MainWindow", "변경하실 파일을 선택해주세요."))
        self.btnFind.setText(_translate("MainWindow", "불러오기"))
        self.btnSave.setText(_translate("MainWindow", "저장하기"))
        self.btnFind.setFocus()
        self.btnSave.setDisabled(True)

    # 불러오기
    def btnFind_clicked(self):
        # 압축파일 경로 받아오기
        zipPath = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "불러오기", "./", "zip(*.zip)")

        # 수정 전 md데이터 출력(압축 해제, temp 폴더 생성, 파일명 변경)
        self.tedtOri.setPlainText(func.getMemo(zipPath[0]))

        # 수정 후 md데이터 출력
        self.tedtMod.setPlainText(func.getPost(self.tedtOri.toPlainText()))
        
        # 저장하기 버튼 활성화
        self.btnSave.setEnabled(True)

    # 저장하기
    def btnSave_clicked(self):
        # 블로그 프로젝트 설정되어 있으면 그대로 아니면 다른경로로
        if settings.PROJECT_PATH != '' and os.path.isdir(path):
            isProjectPath = True
            path = settings.PROJECT_PATH
        else:   
            isProjectPath = False
            path = QtWidgets.QFileDialog.getExistingDirectory(MainWindow, "저장 폴더 선택")

        option = QtWidgets.QMessageBox.question(MainWindow, "알림", 
                "동일한 폴더가 존재하면 내용은 모두 삭제됩니다.\n"
                + "계속하시겠습니까?")
        if option == QtWidgets.QMessageBox.Yes:
            path = func.savePost(isProjectPath, path, self.tedtMod.toPlainText())

            # 내용 비우기
            self.tedtMod.clear()
            self.tedtOri.clear()
            func.eraseTemp()
            
            self.btnSave.setEnabled(True)
            option = QtWidgets.QMessageBox.question(MainWindow, "알림", 
                    "저장경로: '{0}'\n저장경로로 이동할까요?".format(path))
            if option == QtWidgets.QMessageBox.Yes:
                if sys.platform == 'darwin':
                    subprocess.check_call(['open', '--', path])
                elif sys.platform == 'linux2':
                    subprocess.check_call(['xdg-open', '--', path])
                elif sys.platform == 'win32':
                    os.startfile(path)

class MyWindow(QtWidgets.QMainWindow):            
    def closeEvent(self, event):
        func.eraseTemp()
        event.accept()

if __name__ == "__main__":
    import sys
    settings.init()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
