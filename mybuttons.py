from PyQt4 import QtGui, QtCore

class Button(QtGui.QPushButton):
	def __init__(self,parent = None):
		super(Button,self).__init__(parent)
		self.status = 0 
		
	def loadPixmap(self, pic_name):	
		self.pixmap = QtGui.QPixmap(pic_name)
		self.btn_width = self.pixmap.width()
		self.btn_height = self.pixmap.height()/6
		self.setFixedSize(self.btn_width, self.btn_height)

	def mousePressEvent(self,event):	
		if event.button() == QtCore.Qt.LeftButton:		
			self.status = 2
			self.update()	
			self.clicked.emit(True)				

	def mouseReleaseEvent(self,event):	
		if event.button() == QtCore.Qt.LeftButton:		
			self.status = 0 
			self.update()
			self.released.emit()		

	def rst(self):
		self.status = 0
		self.update()
		
	def rbReleased(self):
		self.status = 0
		self.update()
		
	def rbPressed(self):
		self.status = 4
		self.update()
		
	def lbPressed(self):
		self.status = 3
		self.update()
		
	def lbReleased(self):
		self.status = 0
		self.update()
		
	def bothPressed(self):
		self.status = 5
		self.update()
		
	def bothReleased(self):
		self.status = 0
		self.update()
		
	def paintEvent(self,event):	
		self.painter = QtGui.QPainter()
		self.painter.begin(self)
		self.painter.drawPixmap(self.rect(), self.pixmap.copy(0, self.btn_height * self.status, self.btn_width, self.btn_height))
		self.painter.end()	
		
class PlayButton(Button):
	def __init__(self,parent = None):
		super(PlayButton,self).__init__(parent)
		self.setCheckable(True)

	def mouseReleaseEvent(self, event):
		self.released.emit()
			
class SRButton(PlayButton):
	def __init__(self,parent = None):
		super(SRButton,self).__init__(parent)
		self.syn = 0
	
	def mousePressEvent(self,event):	
		if event.button() == QtCore.Qt.LeftButton:
			self.status = 2 
			self.update()
			if not self.isChecked():
				self.syn = 1
				self.clicked.emit(True)		

	def mouseReleaseEvent(self, event):
		if self.isChecked() and self.syn != 1:
			self.clicked.emit(True)
			self.released.emit()
		else:
			self.syn = 0