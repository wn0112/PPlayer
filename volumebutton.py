from PyQt4 import QtGui, QtCore

class VolumeButton(QtGui.QPushButton):
	def __init__(self,parent = None):
		super(VolumeButton,self).__init__(parent)
		self.status = 0 

	def loadPixmap(self, pic_name):	
		self.pixmap = QtGui.QPixmap(pic_name)
		self.btn_width = self.pixmap.width()/4
		self.btn_height = self.pixmap.height()
		self.setFixedSize(self.btn_width, self.btn_height)

	def enterEvent(self,event):	
		self.status = 1 
		self.update()
	
	def mousePressEvent(self,event):	
		if(event.button() == QtCore.Qt.LeftButton):		
			self.mouse_press = True
			self.status = 2 
			self.update()			
			
	def mouseReleaseEvent(self,event):	
		if(self.mouse_press):		
			self.mouse_press = False
			self.status = 0 
			self.update()
			self.clicked.emit(True)
			self.released.emit()		

	def leaveEvent(self,event):	
		self.status = 0
		self.update()

	def paintEvent(self,event):	
		self.painter = QtGui.QPainter()
		self.painter.begin(self)
		self.painter.drawPixmap(self.rect(), self.pixmap.copy(self.btn_width * self.status, 0, self.btn_width, self.btn_height))
		self.painter.end()	