import sys, subprocess, os, urllib, zipfile, mysql.connector, time, json, PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from urllib import request
from io import BytesIO
from urllib.request import urlopen

# --- 1. Thêm phần số lần nộp 						--> Done
# --- 2. Sửa phần hiển thị môn học					--> Done
# --- 3. Giới hạn thời gian chạy
# --- 4. Fix resize 								--> Done
# --- 5. Kiểm tra máy client đã có compiler chưa
# --- 6. Ẩn file input, output



url = "https://raw.githubusercontent.com/nt-vu/finetest22/main/data.json"
response = urlopen(url)
main_data = json.loads(response.read())


class LoginPage(QDialog):
	def __init__(self):

		# current_version
		__version = 1.1
		super(LoginPage, self).__init__()

		
		# check version
		url = 'https://bsite.net/tuanvu02/version.txt'
		file = urllib.request.urlopen(url)
		version = float(file.read())
		if (version > __version):
			print("Update!")
			reply = QMessageBox.question(self,'Update', 'Hiện đã có phiên bản mới\nTải về để tiếp tục!',
			QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

			if reply == QMessageBox.Yes:
				app = QApplication(sys.argv)
				app.exit()
				os.startfile("update.exe")
			else:
				app = QApplication(sys.argv)
				app.exit()
		else:
			print("Continue!")


			# Load loginpage 
			loadUi("loginpage.ui", self)
			self.setWindowTitle("Login")
			widget.setFixedHeight(262)
			widget.setFixedWidth(580)
			widget.setWindowTitle('Đăng nhập')
			self.loginButton.clicked.connect(self.select_subject)

			


	def select_subject(self):
		global name, msv, lop, sjSelection, main_data, sj_id_list
		name = self.namefield.text()
		msv = self.idfield.text()
		lop = self.classfield.text()

		sj_id_list = []
		sj_list = []
		# check if user_id exist
		if(msv in main_data.keys()):
			sj_id_list = list(main_data[msv]["subject"].keys())
			for i in sj_id_list:
				sj_list.append(main_data[msv]["subject"][i]["name"])

			sjSelection = QDialog(self)
			sjSelection.setWindowTitle("Bạn chọn làm bài nào trong danh sách dưới đây")
			sjSelection.setFixedHeight(80 * int(len(sj_list)))
			sjSelection.setFixedWidth(500)
			connect_box = QVBoxLayout(sjSelection)
			connect_box.setAlignment(Qt.AlignCenter)  
			self.errorLogin.setText("")
			for i in sj_list:
				sj = QPushButton(i)
				sj.setFixedSize(350, 39)
				sj.clicked.connect(self.goToMainPage)
				connect_box.addWidget(sj, alignment=Qt.AlignCenter)
			sjSelection.exec()
		else:
			self.errorLogin.setText("* Vui lòng kiểm tra lại thông tin đăng nhập")
			print("Wrong!")
	def goToMainPage(self):
		global name, msv, lop, sjSelection, main_data, sj_id_list
		subject = self.sender().text()
		for i in sj_id_list:
			check = main_data[msv]["subject"][i]["name"]
			if(check == subject):
				main_sj_id = i
				break
		main = mainPage(name, msv, lop, subject, main_sj_id)
		widget.addWidget(main)
		widget.setCurrentIndex(widget.currentIndex()+1)
		widget.setFixedHeight(596)
		widget.setFixedWidth(801)
		sjSelection.reject()
		
		


class mainPage(QDialog):
	def __init__(self, name, msv, lop, subject, main_sj_id):
		global _msv, _main_sj_id
		_msv = msv
		_main_sj_id = main_sj_id
		widget.setWindowTitle('Finetest')
		
		global mark, totalMark
		super(mainPage, self).__init__()
		loadUi("mainpage.ui", self)
		self.progressBar.setVisible(False)
		self.nameDisplay.setText(f'Họ và tên : {name}')
		self.idDisplay.setText(f'Mã sinh viên : {msv}')
		self.classDisplay.setText(f'Lớp : {lop}')
		self.sjDisplay.setText(f'Môn học : {subject}')

		self.setFixedHeight(596)
		self.setFixedWidth(801)
		
		mark = 0
		totalMark = 0

		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		widget.move(qr.topLeft())
		
		mark = main_data[msv]["subject"][main_sj_id]["mark"]
		total_sj = main_data[msv]["subject"][main_sj_id]["title_total"]

		totalMark += total_sj * 100
		self.markDisplay.setText(f'Điểm tổng : {mark} / {totalMark}')
		self.viewButton.clicked.connect(self.open)
		self.exitButton.clicked.connect(self.exit)
		self.submitButton.clicked.connect(self.submit)



		self.tableWidget = self.titleList

		#Row count
		self.tableWidget.setRowCount(total_sj + 1) 

		#Column count
		self.tableWidget.setColumnCount(6)
		self.tableWidget.verticalHeader().setVisible(False)

		
		exercise_info = main_data[msv]["subject"][main_sj_id]["exercise"]
		exercise_id_list = list(exercise_info)
		# print(exercise_id_list)
		
		print(total_sj)
		for i in range(total_sj):
			exercise_id = exercise_id_list[i]
			self.tableWidget.setItem(i,0, QTableWidgetItem(exercise_id))
			self.tableWidget.setItem(i,1, QTableWidgetItem(exercise_info[exercise_id]["name"]))
			self.tableWidget.setItem(i,2, QTableWidgetItem(exercise_info[exercise_id]["topic"]))
			self.tableWidget.setItem(i,3, QTableWidgetItem(str(exercise_info[exercise_id]["timeLimit"]) + " giây"))
			self.tableWidget.item(i,3).setTextAlignment(Qt.AlignCenter)
			
			submit_times = exercise_info[exercise_id]["submit_times"]
			temp_mark = exercise_info[exercise_id]["mark"]
			self.tableWidget.setItem(i,5, QTableWidgetItem(str(submit_times)))
			self.tableWidget.item(i,5).setTextAlignment(Qt.AlignCenter)
			self.tableWidget.setItem(i,4, QTableWidgetItem(str(temp_mark)))
			self.tableWidget.item(i,4).setTextAlignment(Qt.AlignCenter)
			if (temp_mark == 100.0):
				for k in range(6):
					self.tableWidget.item(i,k).setForeground(QtGui.QColor(250, 3, 0))

			

		self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
		self.tableWidget.setFocusPolicy(Qt.NoFocus)
		self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tableWidget.setShowGrid(False)


		

		#Table will fit the screen horizontally
		self.tableWidget.setHorizontalHeaderLabels(['MÃ BÀI','BÀI TẬP', 'CHỦ ĐỀ', 'GIỚI HẠN', 'ĐIỂM', 'NỘP'])
		self.tableWidget.setColumnWidth(0,60)
		self.tableWidget.setColumnWidth(1,250)
		self.tableWidget.setColumnWidth(2,200)
		self.tableWidget.setColumnWidth(3,80)
		self.tableWidget.setColumnWidth(4,60)
		self.tableWidget.setColumnWidth(5,50)
		self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView { font: bold Bahnschrift; font-size: 10pt;}")

		
		self.scroll = self.statusScroll             # Scroll Area which contains the widgets, set as the centralWidget
		self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
		self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

		

	
	def submit(self):
		try:
			global mark, totalMark, main_data, msv, _main_sj_id
			
			tempMark = 0
			crRow = self.tableWidget.currentRow()
			content = self.tableWidget.item(crRow,0).text()
			num_test = int(main_data[msv]["subject"][_main_sj_id]["exercise"][content]["testcase"])
			path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.cpp *.py)')
			if path != ('', ''):
				try:
					newFolder = f"{os.getcwd()}/User/{content}"
					os.mkdir(newFolder)
				except:
					print("Folder existed!")
				print(path[0])
				object = QLabel("---BẮT ĐẦU CHẤM BÀI---")
				self.vbox.addWidget(object)
				self.widget.setLayout(self.vbox)
				self.scroll.setWidget(self.widget)
				self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)

				#create a new folder to contain user's output
				newpath = f'./User/{content}' 
				if not os.path.exists(newpath):
				    os.makedirs(newpath)
				if path[0][-3:] == '.py':
					drRun = f'python {path[0]}'
				else:
					drRun = 'a.exe'
				self.progressBar.setVisible(True)
				prbar_val = 100/num_test
				for i in range(1,num_test+1):
					
					if i == 1 and path[0][-3:] == 'cpp':
						subprocess.run(f'g++ {path[0]}', shell=True)

					process = subprocess.Popen(f"{drRun} <./Submit/{content}/{i}.inp> ./User/{content}/output{i}.out", shell=True)
					
					try:
						start_time = time.time()
						print('Running in process', process.pid)
						process.wait(timeout=1)
						file1 = open(f"./Submit/{content}/{i}.out",'r')
						var1 = file1.read()
						file1.close()

						file1 = open(f'./User/{content}/output{i}.out', 'r')
						var2 = file1.read()
						file1.close()

						exe_time = round((time.time() - start_time), 3)
						# Compare
						if var2 == var1:
							tempMark+=20
							object = QLabel(f'[{content}] Test {i}: Hoàn toàn chính xác - thời gian chạy {exe_time}s')
							object.setStyleSheet("color: green")
							self.vbox.addWidget(object)
							self.widget.setLayout(self.vbox)
							# process1 = subprocess.run('self.widget.setLayout(self.vbox)')
							# process1.wait(timeout=0.1)
							self.scroll.setWidget(self.widget)
							self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
							QApplication.processEvents()
							
						else:
							tempVar1 = var1.split()
							tempVar2 = var2.split()

							if ''.join(tempVar2) == ''.join(tempVar1):
								tempMark+=15
								object = QLabel(f'[{content}] Test {i}: Đúng nhưng sai sót về trình bày')
								self.vbox.addWidget(object)
								self.widget.setLayout(self.vbox)
								self.scroll.setWidget(self.widget)
								self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
								#prevent freeze
								QApplication.processEvents()
								
							else:
								object = QLabel(f'[{content}] Test {i}: Kết quả sai, hãy kiểm tra lại bài làm - thời gian chạy {exe_time}s')
								object.setStyleSheet("color: red")
								self.vbox.addWidget(object)
								self.widget.setLayout(self.vbox)
								self.scroll.setWidget(self.widget)
								self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
								QApplication.processEvents()
								
					except subprocess.TimeoutExpired:
						exe_time = round((time.time() - start_time), 3)
						print('Timed out - killing', process.pid)
						os.system("TASKKILL /F /IM a.exe /T")
						process.kill()
						object = QLabel(f'[{content}] Test {i}: Chương trình chạy quá thời gian - thời gian chạy {exe_time}s')
						object.setStyleSheet("color: red")
						self.vbox.addWidget(object)
						self.widget.setLayout(self.vbox)
						self.scroll.setWidget(self.widget)
						self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
						QApplication.processEvents()
						
						
					self.progressBar.setValue(i*prbar_val)
					print("--- %s seconds ---" % (time.time() - start_time))
					print(f"Test {i} oke!")
				self.progressBar.setVisible(False)
				object = QLabel(f'=== KẾT THÚC: ĐIỂM 100% ===')
				self.vbox.addWidget(object)
				self.widget.setLayout(self.vbox)
				self.scroll.setWidget(self.widget)
				self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)

				# con.execute(f"SELECT mark FROM user_exercise WHERE user_id like '{_msv}' and exercise_id like '{content}'; ")
				# userMark = con.fetchall()
				# if(tempMark > userMark[0][0]):
				# 	self.tableWidget.setItem(crRow,4, QTableWidgetItem(f'{float(tempMark)}'))
				# 	self.tableWidget.item(crRow,4).setTextAlignment(Qt.AlignCenter)
				# 	con.execute(f"UPDATE user_exercise SET mark = {float(tempMark)} WHERE user_id like '{_msv}' and exercise_id like '{content}';")
				# 	mydb.commit()

				# 	# Update submit_times
				# 	con.execute(f"SELECT submit FROM user_exercise WHERE user_id like '{_msv}' and exercise_id like '{content}'; ")
				# 	submit_times = int(con.fetchall()[0][0])
				# 	self.tableWidget.setItem(crRow,5, QTableWidgetItem(f'{submit_times + 1}'))
				# 	self.tableWidget.item(crRow,5).setTextAlignment(Qt.AlignCenter)
				# 	con.execute(f"UPDATE user_exercise SET submit = {submit_times + 1} WHERE user_id like '{_msv}' and exercise_id like '{content}';")
				# 	mydb.commit()

				# 	if(tempMark == 100):
				# 		for i in range(6):
				# 			self.tableWidget.item(crRow,i).setForeground(QtGui.QColor(250, 3, 0))
				# 	mark+=tempMark
				# 	con.execute(f"UPDATE user_subject SET mark = {float(mark)} WHERE user_id like '{_msv}' and subject_id like 'TTUD';")
				# 	mydb.commit()
				# 	self.markDisplay.setText(f'Điểm tổng : {mark} / {totalMark}')
				# else:
				# 	object = QLabel("--GIỮ NGUYÊN ĐIỂM--")
				# 	self.vbox.addWidget(object)
				# 	self.widget.setLayout(self.vbox)
				# 	self.scroll.setWidget(self.widget)
				# 	self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
				subprocess.run(f"del /f a.exe",shell=True)
			else:
				print("No choose file!")
		except Exception as e:
			print(e)
			print("Do not select!")
	def ResizeScroll(self, min, maxi): #auto scroll
		self.scroll.verticalScrollBar().setValue(maxi)

	def open(self):
		try:
			crRow = self.tableWidget.currentRow()
			content = self.tableWidget.item(crRow,0).text()
			simp_path_Data = 'Data'
			abs_path_Data = os.path.abspath(simp_path_Data)
			file = f'{abs_path_Data}\\{_main_sj_id}\\{content}.pdf'
			subprocess.Popen([file],shell=True)
			print(content)
		except Exception as e:
			print(e)
			print("Do not select!")
	def exit(self):
		app.exit()





#main

app = QApplication(sys.argv)

widget = QStackedWidget()
welcome = LoginPage()
widget.addWidget(welcome)
widget.show()
try:
	sys.exit(app.exec_())
except:
	print("Exiting")	

