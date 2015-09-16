from PyQt4 import QtGui, QtCore

class PushButton(QtGui.QPushButton):
	def __init__(self,parent = None):
		super(PushButton,self).__init__(parent)
		
		self.status = 0 

	def loadPixmap(self, pic_name):	
		self.pixmap = QtGui.QPixmap(pic_name)
		self.btn_width = self.pixmap.width()/4
		self.btn_height = self.pixmap.height()
		self.setFixedSize(self.btn_width, self.btn_height)
	
	def enterEvent(self,event):	
		if not self.isChecked() and self.isEnabled():
			self.status = 1 
			self.update()
	
	def setDisabled(self, bool):
		super(PushButton,self).setDisabled(bool)
		if not self.isEnabled():
			self.status = 2
			self.update()
		else:
			self.status = 0
			self.update()
		

	def mousePressEvent(self,event):	
		if event.button() == QtCore.Qt.LeftButton:		
			self.status = 2 
			self.update()	


	def mouseReleaseEvent(self,event):	
		if event.button() == QtCore.Qt.LeftButton: 
			self.clicked.emit(True)
		if not self.isChecked():
			self.status = 3
		if self.menu():
			self.menu().exec_(event.globalPos())
		self.update()
		
	def leaveEvent(self,event):	
		if not self.isChecked() and self.isEnabled():
			self.status = 0 
			self.update()
	

	def paintEvent(self,event):	
		self.painter = QtGui.QPainter()
		self.painter.begin(self)
		self.painter.drawPixmap(self.rect(), self.pixmap.copy(self.btn_width * self.status, 0, self.btn_width, self.btn_height))
		self.painter.end()	
		
class PushButton2(QtGui.QPushButton):
	def __init__(self,parent = None):
		super(PushButton2,self).__init__(parent)
		
		# self.status = 0 

	def loadPixmap(self, pic_name):	
		self.pixmap = QtGui.QPixmap(pic_name)
		self.btn_width = self.pixmap.width()
		self.btn_height = self.pixmap.height()
		self.setFixedSize(self.btn_width, self.btn_height)
		

	def paintEvent(self,event):	
		self.painter = QtGui.QPainter()
		self.painter.begin(self)
		self.painter.drawPixmap(self.rect(), self.pixmap.copy(0, 0, self.btn_width, self.btn_height))
		self.painter.end()	