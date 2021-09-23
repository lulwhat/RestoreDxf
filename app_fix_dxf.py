import sys
import os.path
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout, 
	QLabel, QLineEdit, QProgressBar, QPushButton, QFileDialog, QMessageBox
		)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from fix_dxf_functionality import *

class GuiFixDxf(QDialog):
	def __init__(self, parent=None):
		super(GuiFixDxf, self).__init__(parent)

		self.dxf_path = os.path.expanduser("~/Documents")
		self.originalPalette = QApplication.palette()

		# create top horisontal layout for dxf path
		labelDxf = QLabel("Выберите dxf:")
		self.textFieldDxf = QLineEdit()
		browseDxfButton = QPushButton("Обзор")
		browseDxfButton.clicked.connect(self.chooseDxfFileDialog)

		topLayout = QHBoxLayout()
		topLayout.addWidget(labelDxf)
		topLayout.addWidget(self.textFieldDxf)
		topLayout.addWidget(browseDxfButton)

		#bottom layout with restore button
		restoreButton = QPushButton("Восстановить")
		restoreButton.clicked.connect(self.restoreButtonAction)
		self.progressBar = QProgressBar()
		self.progressBar.setValue(0)

		botLayout = QHBoxLayout()
		botLayout.addWidget(self.progressBar)
		botLayout.addWidget(restoreButton)


		# create main layout
		mainLayout = QGridLayout()        
		mainLayout.addLayout(topLayout, 0, 0, 1, 2)
		mainLayout.addLayout(botLayout, 1, 0, 1, 2)

		self.setLayout(mainLayout)
		self.setWindowTitle("Ремонт dxf")
		self.setFixedSize(640, 150)
		self.setWindowIcon(QIcon(self.resourcePath("logo_ug.png")))
		self.setWindowFlags(Qt.WindowFlags())

	# pyinstaller stuff to fold icon into exe
	def resourcePath(self, relative_path):
		try:
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.abspath(".")
		return os.path.join(base_path, relative_path)
		
	def chooseDxfFileDialog(self):
		self.progressBar.setValue(0)
		options = QFileDialog.Options()
		fileName, _ = QFileDialog.getOpenFileName(
			self,
			"Выберите dxf",
			self.dxf_path + "/*.dxf",
			"Файлы чертежей (*.dxf);;Все файлы (*)",
			options=options
		)
		if fileName:
			self.dxf_path = fileName
			# change forward slash to windows one
			self.textFieldDxf.setText(fileName.replace("/", "\\"))

	def restoreButtonAction(self):
		self.progressBar.setValue(0)
		dxfFixer = DxfFixer()
		try:
			dxfFixer.restore(self.textFieldDxf.text())
			self.progressBar.setValue(100)
			QMessageBox.about(self, "Ремонт dxf", "Восстановленный dxf файл создан")
		except WrongFileFormatError:
			msg = QMessageBox()
			msg.warning(self, "Ошибка", "Неверный формат файла")
		except DxfNotFoundError:
			msg = QMessageBox()
			msg.warning(self, "Ошибка", "Dxf файл не найден")
		except NoDxfIssuesFoundError:
			msg = QMessageBox()
			msg.warning(self, "Ошибка", "Программе не удалось найти ошибки в чертеже")
		except Exception:
			msg = QMessageBox()
			msg.warning(self, "Ошибка", "Неизвестная ошибка приложения")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setStyle("Fusion")
	gallery = GuiFixDxf()
	gallery.show()
	sys.exit(app.exec_())