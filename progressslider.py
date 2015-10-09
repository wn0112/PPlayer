# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import images
try:
	_fromUtf8 = QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

		
class progressSlider(QSlider):
	def __init__(self, orientation, parent=None):
		super(progressSlider, self).__init__(orientation, parent)

	def mousePressEvent(self, event):
		if self.topLevelWidget().mediaObj.state() != 2:
			return
		new = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
		self.setValue(new)
		self.emit(SIGNAL('sliderMoved(int)'), new)

	def mouseMoveEvent(self, event):
		if self.topLevelWidget().mediaObj.state() != 2:
			return
		new = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
		self.setValue(new)
		self.emit(SIGNAL('sliderMoved(int)'), new)
		
	def wheelEvent(self, event):
		if self.topLevelWidget().mediaObj.state() != 2:
			return
		modifier = QApplication.keyboardModifiers()
		max = self.maximum()
		min = self.minimum()
		if event.delta() >= 120:		
			new = self.value()+ max*0.03
			if new > max:
				new = max
			self.setValue(new)
			self.emit(SIGNAL('sliderMoved(int)'), new)
		elif event.delta() <= -120:			
			new = self.value()- max*0.03
			if new < min:
				new = min
			self.setValue(new)
			self.emit(SIGNAL('sliderMoved(int)'), new)
			

class menuNameLabel(QLabel):
	def __init__(self, parent=None):
		super(menuNameLabel, self).__init__(parent)
		self.txt = QString()
		self.newX = 10		
		self.t = QTimer()
		self.font = QFont(_fromUtf8('微软雅黑, verdana'), 8)
		self.connect(self.t, SIGNAL("timeout()"), self.changeTxtPosition)
	
	def changeTxtPosition(self):
		if not self.parent().isVisible():
			self.t.stop()
			self.newX = 10
			return
		if self.textRect.width() + self.newX > 0:
			self.newX -= 5
		else:
			self.newX = self.width()			
		self.update()
	
	def setText(self, s):
		self.txt = s
		self.newX = 10
		self.update()
		
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setFont(self.font)
		painter.setPen(QColor('transparent'));
		self.textRect = painter.drawText(QRect(0, -7, self.width(), 25), Qt.AlignHCenter | Qt.AlignVCenter, self.txt)

		if self.textRect.width() > self.width():	
			painter.setPen(QColor(0, 0, 0, 255))
			painter.drawText(QRect(self.newX, -7, self.textRect.width(), 25), Qt.AlignLeft | Qt.AlignVCenter, self.txt)
			self.t.start(150)
		else:
			painter.setPen(QColor(0, 0, 0, 255));
			self.textRect = painter.drawText(QRect(0, -7, self.width(), 25), Qt.AlignHCenter | Qt.AlignVCenter, self.txt)
			self.t.stop()
			
			
class nameLabel(QLabel):
	def __init__(self, parent=None):
		super(nameLabel, self).__init__(parent)
		self.txt = QString()
		self.newX = 0		
		self.t = QTimer()
		self.font = QFont(_fromUtf8('微软雅黑, verdana'), 8)
		self.connect(self.t, SIGNAL("timeout()"), self.changeTxtPosition)
	
	def changeTxtPosition(self):
		if not self.parent().isVisible():
			self.t.stop()
			self.newX = 0
			return
		if self.textRect.width() + self.newX > 0:
			self.newX -= 5
		else:
			self.newX = self.width()			
		self.update()
	
	def setText(self, s):
		self.txt = s
		self.newX = 0
		self.update()
		
	def enterEvent(self, event):
		self.t.start(150)
		
	def leaveEvent(self, event):
		self.t.stop()
		self.newX = 0
		self.update()
		
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setFont(self.font)
		painter.setPen(QColor('transparent'));
		self.textRect = painter.drawText(QRect(0, -7, self.width(), 25), Qt.AlignHCenter | Qt.AlignVCenter, self.txt)

		if self.textRect.width() > self.width():	
			painter.setPen(QColor(255, 255, 255, 255))
			painter.drawText(QRect(self.newX, -7, self.textRect.width(), 25), Qt.AlignLeft | Qt.AlignVCenter, self.txt)			
		else:
			painter.setPen(QColor(255, 255, 255, 255));
			self.textRect = painter.drawText(QRect(0, -7, self.width(), 25), Qt.AlignLeft | Qt.AlignVCenter, self.txt)
			self.t.stop()

			
class delegateLabel(QLabel):
	def __init__(self, parent=None):
		super(delegateLabel, self).__init__(parent)
		self.txt = QString()
		self.frc = '#FFFFFF'
		self.bgc = '#2c3e50'
		self.newX = 0		
		self.t = QTimer()
		self.font = QFont(_fromUtf8('微软雅黑, verdana'), 7)
		self.connect(self.t, SIGNAL("timeout()"), self.changeTxtPosition)
	
	def changeTxtPosition(self):
		if not self.parent().isVisible():
			self.t.stop()
			self.newX = 0
			return
		if self.textRect.width() + self.newX > 0:
			self.newX -= 5
		else:
			self.newX = self.width()			
		self.update()
			
	def setText(self, s):
		self.txt = s
		self.newX = 0
		self.update()
	
	def enterEvent(self, event):
		self.t.start(150)
		
	def leaveEvent(self, event):
		self.t.stop()
		self.newX = 0
		self.update()
		
		
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setFont(self.font)
		painter.setPen(QColor(self.bgc));
		self.textRect = painter.drawText(QRect(0, -3, self.width(), 25), Qt.AlignHCenter | Qt.AlignVCenter, self.txt)

		if self.textRect.width() > self.width():	
			painter.setPen(QColor(self.frc))
			painter.drawText(QRect(self.newX, -3, self.textRect.width(), 25), Qt.AlignLeft | Qt.AlignVCenter, self.txt)			
		else:
			painter.setPen(QColor(self.frc));
			self.textRect = painter.drawText(QRect(0, -3, self.width(), 25), Qt.AlignLeft | Qt.AlignVCenter, self.txt)
			self.t.stop()
			
			
class starWidget(QDialog):
	def __init__(self, parent=None, bool=False):
		super(starWidget, self).__init__(parent)
		self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Dialog)
		self.setWindowOpacity(0.01)		
		self.setFixedSize(10, 10)
		self.setFocusPolicy(Qt.NoFocus)
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setMargin(0)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.star = star(self)
		self.star.setChecked(bool)
		self.verticalLayout.addWidget(self.star)		
		
class star(QCheckBox):
	def __init__(self, parent=None):
		super(star,self).__init__(parent)
		self.index = 0
		self.setProperty("cursor", QCursor(Qt.PointingHandCursor))
		self.setFocusPolicy(Qt.NoFocus)
		self.connect(self, SIGNAL('stateChanged(int)'), self.starClicked)
		
	def setIndex(self, index):
		self.index = index
	
	def starClicked(self, state):		
		self.emit(SIGNAL('fav(int, int)'), state, self.index)
