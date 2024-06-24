db_config = {
	'user': 'root',
	'password': '',
	'host': 'localhost',
	'database': 'kino',

}

import sys
import os
import mysql.connector
import ctypes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from login import Ui_login_menu
from afisha import Ui_Dialog
from places import PlacesUi_Dialog
from cabinet import Ui_Cabinet
from admin import Ui_Admin

def get_user(login, password=None):
	conn = mysql.connector.connect(**db_config)
	cursor = conn.cursor(dictionary=True, buffered=True)
	if password!=None:
		query = "SELECT * FROM users WHERE login = %s AND password = %s"
		cursor.execute(query, (login, password,))
	else:
		query = "SELECT * FROM users WHERE login = %s"
		cursor.execute(query, (login,))
	user=cursor.fetchone()
	cursor.close();conn.close()

	if password!=None:
		return user
	else:
		if user!=None:return True
		else: return False

def open_login_menu():
	class Login_menu(QtWidgets.QMainWindow):
		def __init__(self):
			super(Login_menu, self).__init__()
			self.ui = Ui_login_menu()
			self.ui.setupUi(self)
			self.ui.pushButton.clicked.connect(self.login_button)
			self.ui.pushButton_2.clicked.connect(self.register_button)

		def menu_step(self, login, password):
			f=open('data','w+')
			f.write(f'{login}?&password={password}')
			f.close()
			app.quit()
			self.close()
			os.execl(sys.executable, sys.executable, *sys.argv)
		def login_button(self):
			login, password = self.ui.lineEdit.text(), self.ui.lineEdit_2.text()
			user=get_user(login,password)
			if user==None:ctypes.windll.user32.MessageBoxW(0, u"Не верный логин или пароль", u"Ошибка", 0)
			else:
				self.menu_step(login, password)

		def register_button(self):
			login, password, fio, dr = self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text(), self.ui.dateEdit.text()
			print(dr)
			if login != '' and password != '' and fio != '' and dr != '0000-00-00':
				user=get_user(login)
				if user==True:ctypes.windll.user32.MessageBoxW(0, u"Этот логин уже занят", u"Ошибка", 0)
				else:
					conn = mysql.connector.connect(**db_config)
					cursor = conn.cursor(dictionary=True, buffered=True)
					query = "INSERT INTO users (login, password, fio, dr) VALUES (%s, %s, %s, %s)"
					cursor.execute(query, (login, password,fio,dr,))
					conn.commit()
					cursor.close();conn.close()
					self.menu_step(login, password)
			else:ctypes.windll.user32.MessageBoxW(0, u"Заполните все поля", u"Ошибка", 0)
	
	app = QtWidgets.QApplication([])
	application = Login_menu()
	application.show()
	 
	app.exec()

def open_afisha_menu():
	class AfishaMenu(QtWidgets.QMainWindow):
		def __init__(self):
			super(AfishaMenu, self).__init__()
			self.ui = Ui_Dialog()
			self.ui.setupUi(self)
			self.current_x_position = 20
			self.current_y_position = 20
			self.films_per_row = 4
			self.film_count = 0
			self.spacing = 15


			self.ui.pushButton.clicked.connect(self.cabinet)

			conn = mysql.connector.connect(**db_config)
			cursor = conn.cursor(dictionary=True, buffered=True)
			query = "SELECT * FROM films"
			cursor.execute(query)
			films=cursor.fetchall()
			cursor.close();conn.close()
			for film in films:
				self.add_film(film['id'], film['name'], film['dt'])

		def deleteAccount(self, user):
			conn = mysql.connector.connect(**db_config)
			cursor = conn.cursor(dictionary=True, buffered=True)
			query = "DELETE FROM users WHERE id = %s"
			cursor.execute(query, (user['id'],))
			query = "DELETE FROM places WHERE owner = %s"
			cursor.execute(query, (user['id'],))
			conn.commit()
			cursor.close();conn.close()
			ctypes.windll.user32.MessageBoxW(0, u"Аккаунт успешно удален", u"", 0)
			os.execl(sys.executable, sys.executable, *sys.argv)

		def changeLogin(self, user):
			newlogin=self.ui.lineEdit.text()
			if newlogin!='':
				if get_user(newlogin):
					ctypes.windll.user32.MessageBoxW(0, u"Этот логин уже занят", u"Ошибка", 0)
				else:
					conn = mysql.connector.connect(**db_config)
					cursor = conn.cursor(dictionary=True, buffered=True)
					query = "UPDATE users SET login = %s WHERE id = %s"
					cursor.execute(query, (newlogin, user['id'],))
					conn.commit()
					cursor.close();conn.close()
					ctypes.windll.user32.MessageBoxW(0, u"Логин успешно изменен", u"", 0)
					os.execl(sys.executable, sys.executable, *sys.argv)
			else:ctypes.windll.user32.MessageBoxW(0, u"Введите новый логин", u"Ошибка", 0)

		def changePassword(self, user):
			newpassword=self.ui.lineEdit_2.text()
			if newpassword!='':
				conn = mysql.connector.connect(**db_config)
				cursor = conn.cursor(dictionary=True, buffered=True)
				query = "UPDATE users SET password = %s WHERE id = %s"
				cursor.execute(query, (newpassword, user['id'],))
				conn.commit()
				cursor.close();conn.close()
				ctypes.windll.user32.MessageBoxW(0, u"Пароль успешно изменен", u"", 0)
				os.execl(sys.executable, sys.executable, *sys.argv)
			else:ctypes.windll.user32.MessageBoxW(0, u"Введите новый пароль", u"Ошибка", 0)

		def logout(self):
			os.remove('data')
			os.execl(sys.executable, sys.executable, *sys.argv)

		def cabinet(self):
			global login, password
			self.window=QtWidgets.QMainWindow()
			self.ui=Ui_Cabinet()
			self.ui.setupUi(self.window)
			self.window.show()

			user=get_user(login,password)
			fio=user['fio']
			dr=user['dr']

			self.ui.label_2.setText(f'ФИО: {fio}\nДата рождения: {dr}')
			self.ui.lineEdit.setText(f'{login}')

			self.ui.pushButton.clicked.connect(lambda: self.deleteAccount(user))
			self.ui.pushButton_2.clicked.connect(lambda: self.changeLogin(user))
			self.ui.pushButton_3.clicked.connect(lambda: self.changePassword(user))
			self.ui.pushButton_4.clicked.connect(lambda: self.logout())


			

		def buy_place(self,id,n):
			global login, password
			myid=get_user(login,password)['id']
			conn = mysql.connector.connect(**db_config)
			cursor = conn.cursor(dictionary=True, buffered=True)
			query="SELECT * FROM places where film_id=%s AND place_n = %s"
			cursor.execute(query, (id, n))
			place=cursor.fetchone()
			cursor.close();conn.close()
			if place!=None:
				try:
					if place['owner']==myid:
						ctypes.windll.user32.MessageBoxW(0, u"Это ваше место", u"", 0)
					else:ctypes.windll.user32.MessageBoxW(0, u"Место занято", u"", 0)
				except:ctypes.windll.user32.MessageBoxW(0, u"Место занято", u"", 0)
			else:
				conn = mysql.connector.connect(**db_config)
				cursor = conn.cursor(dictionary=True, buffered=True)
				query="INSERT INTO places (film_id, place_n, status, owner) VALUES (%s, %s, %s, %s)"
				cursor.execute(query, (id, n, 2, myid,))
				conn.commit();
				cursor.close();conn.close()
				ctypes.windll.user32.MessageBoxW(0, u"Вы забронировали место", u"", 0)
				self.window.close()


		def button_clicked(self,id):
			global login, password
			myid=get_user(login,password)['id']
			conn = mysql.connector.connect(**db_config)
			cursor = conn.cursor(dictionary=True, buffered=True)
			query = "SELECT * FROM films where id = %s"
			cursor.execute(query, (id,))
			film=cursor.fetchone()
			query="SELECT * FROM places where film_id=%s"
			cursor.execute(query, (film['id'],))
			places=cursor.fetchall()
			cursor.close();conn.close()
			self.pcurrent_x_position = 1
			self.pcurrent_y_position = 1
			self.pfilms_per_row = 16
			self.pfilm_count = 0
			self.pspacing = 15
			self.window=QtWidgets.QMainWindow()
			self.ui=PlacesUi_Dialog()
			self.ui.setupUi(self.window)
			self.window.show()

			self.ui.label.setText(film['name'])
			self.ui.label_2.setText(film['description'])
			
			for place in places:
				place_n=place['place_n']
				if int(place['status'])==1:
					clr='#b0d1b9'
				if int(place['status'])==2:
					clr='#8f8b53'
				if int(place['status'])==3:
					clr='#8f6166'
				if place['owner']==myid:
					custom='border:3px solid #2352b8;'
				else:
					custom=''
				exec(f"self.ui.b{place_n}.setStyleSheet('border:none;{custom}background-color:{clr};border-bottom-left-radius: 15px;border-bottom-right-radius: 15px;border-top-left-radius: 5px;border-top-right-radius: 5px;')")
			self.ui.b1.clicked.connect(lambda: self.buy_place(id,1))
			self.ui.b2.clicked.connect(lambda: self.buy_place(id,2))
			self.ui.b3.clicked.connect(lambda: self.buy_place(id,3))
			self.ui.b4.clicked.connect(lambda: self.buy_place(id,4))
			self.ui.b5.clicked.connect(lambda: self.buy_place(id,5))
			self.ui.b6.clicked.connect(lambda: self.buy_place(id,6))
			self.ui.b7.clicked.connect(lambda: self.buy_place(id,7))
			self.ui.b8.clicked.connect(lambda: self.buy_place(id,8))
			self.ui.b9.clicked.connect(lambda: self.buy_place(id,9))
			self.ui.b10.clicked.connect(lambda: self.buy_place(id,10))
			self.ui.b11.clicked.connect(lambda: self.buy_place(id,11))
			self.ui.b12.clicked.connect(lambda: self.buy_place(id,12))
			self.ui.b13.clicked.connect(lambda: self.buy_place(id,13))
			self.ui.b14.clicked.connect(lambda: self.buy_place(id,14))
			self.ui.b15.clicked.connect(lambda: self.buy_place(id,15))
			self.ui.b16.clicked.connect(lambda: self.buy_place(id,16))
			self.ui.b17.clicked.connect(lambda: self.buy_place(id,17))
			self.ui.b18.clicked.connect(lambda: self.buy_place(id,18))
			self.ui.b19.clicked.connect(lambda: self.buy_place(id,19))
			self.ui.b20.clicked.connect(lambda: self.buy_place(id,20))
			self.ui.b21.clicked.connect(lambda: self.buy_place(id,21))
			self.ui.b22.clicked.connect(lambda: self.buy_place(id,22))
			self.ui.b23.clicked.connect(lambda: self.buy_place(id,23))
			self.ui.b24.clicked.connect(lambda: self.buy_place(id,24))
			self.ui.b25.clicked.connect(lambda: self.buy_place(id,25))
			self.ui.b26.clicked.connect(lambda: self.buy_place(id,26))
			self.ui.b27.clicked.connect(lambda: self.buy_place(id,27))
			self.ui.b28.clicked.connect(lambda: self.buy_place(id,28))

		
		def add_film(self, film_id, film_name, film_data):
			label = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents_2)
			label.setGeometry(QtCore.QRect(self.current_x_position, self.current_y_position, 241, 101))
			font = QtGui.QFont()
			font.setFamily("Montserrat")
			font.setPointSize(12)
			font.setBold(True)
			font.setWeight(75)
			label.setFont(font)
			label.setStyleSheet("background-color:#1a2849;border-radius:10px;color:#ffcee4")
			label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
			label.setObjectName(f"label_{film_id}")
			label.setText(f"{film_name}\n{film_data}")
			push_button = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents_2)
			push_button.setGeometry(QtCore.QRect(self.current_x_position, self.current_y_position + 80, 241, 41))
			font = QtGui.QFont()
			font.setFamily("Montserrat")
			font.setPointSize(10)
			font.setBold(True)
			font.setWeight(75)
			push_button.setFont(font)
			push_button.setStyleSheet("border:none;border-radius:10px;background-color:#d01257;")
			push_button.setObjectName(f"pushButton_{film_id}")
			push_button.setText("Купить билет")
			push_button.clicked.connect(lambda _, id=film_id: self.button_clicked(id))
			self.film_count += 1
			if self.film_count % self.films_per_row == 0:
				self.current_x_position = 20
				self.current_y_position += 141+ self.spacing
			else:
				self.current_x_position += 276+ self.spacing

	app = QtWidgets.QApplication([])
	application = AfishaMenu()
	application.show()

	sys.exit(app.exec())

def open_admin_menu():
	class AdminMenu(QtWidgets.QMainWindow):
		def __init__(self):
			super(AdminMenu, self).__init__()
			self.ui = Ui_Admin()
			self.ui.setupUi(self)
	
			self.plc=self.update_places()	
			self.ui.pushButton.clicked.connect(self.accept_place)
			self.ui.pushButton_2.clicked.connect(self.deny_place)
			self.ui.pushButton_3.clicked.connect(self.update_places)
			self.ui.pushButton_4.clicked.connect(self.cabinet)
		
		def deleteAccount(self, user):
			conn = mysql.connector.connect(**db_config)
			cursor = conn.cursor(dictionary=True, buffered=True)
			query = "DELETE FROM users WHERE id = %s"
			cursor.execute(query, (user['id'],))
			query = "DELETE FROM places WHERE owner = %s"
			cursor.execute(query, (user['id'],))
			conn.commit()
			cursor.close();conn.close()
			ctypes.windll.user32.MessageBoxW(0, u"Аккаунт успешно удален", u"", 0)
			os.execl(sys.executable, sys.executable, *sys.argv)

		def changeLogin(self, user):
			newlogin=self.ui.lineEdit.text()
			if newlogin!='':
				if get_user(newlogin):
					ctypes.windll.user32.MessageBoxW(0, u"Этот логин уже занят", u"Ошибка", 0)
				else:
					conn = mysql.connector.connect(**db_config)
					cursor = conn.cursor(dictionary=True, buffered=True)
					query = "UPDATE users SET login = %s WHERE id = %s"
					cursor.execute(query, (newlogin, user['id'],))
					conn.commit()
					cursor.close();conn.close()
					ctypes.windll.user32.MessageBoxW(0, u"Логин успешно изменен", u"", 0)
					os.execl(sys.executable, sys.executable, *sys.argv)
			else:ctypes.windll.user32.MessageBoxW(0, u"Введите новый логин", u"Ошибка", 0)

		def changePassword(self, user):
			newpassword=self.ui.lineEdit_2.text()
			if newpassword!='':
				conn = mysql.connector.connect(**db_config)
				cursor = conn.cursor(dictionary=True, buffered=True)
				query = "UPDATE users SET password = %s WHERE id = %s"
				cursor.execute(query, (newpassword, user['id'],))
				conn.commit()
				cursor.close();conn.close()
				ctypes.windll.user32.MessageBoxW(0, u"Пароль успешно изменен", u"", 0)
				os.execl(sys.executable, sys.executable, *sys.argv)
			else:ctypes.windll.user32.MessageBoxW(0, u"Введите новый пароль", u"Ошибка", 0)

		def logout(self):
			os.remove('data')
			os.execl(sys.executable, sys.executable, *sys.argv)

		def cabinet(self):
			global login, password
			self.window=QtWidgets.QMainWindow()
			self.ui=Ui_Cabinet()
			self.ui.setupUi(self.window)
			self.window.show()

			user=get_user(login,password)
			fio=user['fio']
			dr=user['dr']

			self.ui.label_2.setText(f'ФИО: {fio}\nДата рождения: {dr}')
			self.ui.lineEdit.setText(f'{login}')

			self.ui.pushButton.clicked.connect(lambda: self.deleteAccount(user))
			self.ui.pushButton_2.clicked.connect(lambda: self.changeLogin(user))
			self.ui.pushButton_3.clicked.connect(lambda: self.changePassword(user))
			self.ui.pushButton_4.clicked.connect(lambda: self.logout())

		def accept_place(self):
			cr=self.ui.listWidget.currentRow()
			plc=self.plc[cr][cr]
			conn = mysql.connector.connect(**db_config)
			cursor = conn.cursor(dictionary=True, buffered=True)
			query = "UPDATE places SET status = 3 where id = %s"
			cursor.execute(query, (plc['id'],))
			conn.commit()
			cursor.close();conn.close()
			self.plc=self.update_places()	

		def deny_place(self):
			cr=self.ui.listWidget.currentRow()
			plc=self.plc[cr][cr]
			conn = mysql.connector.connect(**db_config)
			cursor = conn.cursor(dictionary=True, buffered=True)
			query = "DELETE FROM places WHERE id = %s"
			cursor.execute(query, (plc['id'],))
			conn.commit()
			cursor.close();conn.close()
			self.plc=self.update_places()	

		def update_places(self):
			self.ui.listWidget.clear()
			conn = mysql.connector.connect(**db_config)
			cursor = conn.cursor(dictionary=True, buffered=True)
			query = "SELECT p.*, u.login FROM places p JOIN users u ON u.id=p.owner JOIN films f ON f.id=p.film_id WHERE status=2;"
			cursor.execute(query)
			places=cursor.fetchall()
			cursor.close();conn.close()

			plc=[]
			plc_n=0
			for place in places:
				film_id=place['film_id']
				place_n=place['place_n']
				login=place['login']

				item = QtWidgets.QListWidgetItem()
				self.ui.listWidget.addItem(item)
				item = self.ui.listWidget.item(plc_n)
				item.setText(f'Айди фильма: {film_id} | Место: {place_n} | Логин покупателя: {login}')
				plc.append({plc_n:place})
				plc_n+=1

			return plc

	app = QtWidgets.QApplication([])
	application = AdminMenu()
	application.show()

	sys.exit(app.exec())


try:
	f=open('data','r')
	user_data=f.readline().split('?&password=')
	f.close()
	login=user_data[0]
	password=user_data[1]
except:
	login=''
	password=''

global_user=get_user(login,password)
if global_user==None:open_login_menu()
else:
	if global_user['role']=='user':
		open_afisha_menu()
	elif global_user['role']=='admin':
		open_admin_menu()
