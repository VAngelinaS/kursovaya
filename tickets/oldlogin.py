from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_login_menu(object):
    def setupUi(self, login_menu):
        login_menu.setObjectName("login_menu")
        login_menu.resize(982, 549)
        login_menu.setStyleSheet("background-color:#0f1021;")
        self.label = QtWidgets.QLabel(login_menu)
        self.label.setGeometry(QtCore.QRect(0, 0, 981, 81))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:#ffcee4;background-color:#d01257;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(login_menu)
        self.lineEdit.setGeometry(QtCore.QRect(350, 210, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("color:#ffcee4;border:2px solid #d01257;border-radius:10px;")
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setMaxLength(32767)
        self.lineEdit.setFrame(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(login_menu)
        self.lineEdit_2.setGeometry(QtCore.QRect(350, 260, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("color:#ffcee4;border:2px solid #d01257;border-radius:10px;")
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setMaxLength(32767)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(login_menu)
        self.pushButton.setGeometry(QtCore.QRect(380, 310, 221, 31))
        self.pushButton.setStyleSheet("QPushButton{\n"
"background-color:#d01257;border: none;border-radius:10px\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #850c38;\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(login_menu)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 350, 151, 21))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"background-color:#d01257;border: none;border-radius:10px\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #850c38;\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(login_menu)
        self.label_2.setGeometry(QtCore.QRect(340, 190, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:#ffcee4;background-color:none;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(login_menu)
        self.label_3.setGeometry(QtCore.QRect(340, 240, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:#ffcee4;background-color:none;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(login_menu)
        QtCore.QMetaObject.connectSlotsByName(login_menu)

    def retranslateUi(self, login_menu):
        _translate = QtCore.QCoreApplication.translate
        login_menu.setWindowTitle(_translate("login_menu", "App"))
        self.label.setText(_translate("login_menu", "Вход"))
        self.pushButton.setText(_translate("login_menu", "Войти"))
        self.pushButton_2.setText(_translate("login_menu", "Зарегистрироваться"))
        self.label_2.setText(_translate("login_menu", "Логин"))
        self.label_3.setText(_translate("login_menu", "Пароль"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_menu = QtWidgets.QDialog()
    ui = Ui_login_menu()
    ui.setupUi(login_menu)
    login_menu.show()
    sys.exit(app.exec_())
