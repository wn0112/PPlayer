# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from push_button import *
import images, time, locale

try:
	_fromUtf8 = QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QApplication.translate(context, text, disambig)

class lyric_ui(QDialog):
	def __init__(self, parent=None):	
		self.lyric = QString('Lyric Show.')
		self.intervel = 0
		self.maskRect = QRectF(0, 0, 0, 0)
		self.maskWidth = 0
		self.widthBlock = 0
		self.t = QTimer()
		self.screen = QApplication.desktop().availableGeometry()		
		super(lyric_ui, self).__init__(parent)		
		self.setObjectName(_fromUtf8("Dialog"))
		self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint | Qt.Tool)
		self.setMinimumHeight(65)
		self.setAttribute(Qt.WA_TranslucentBackground)	
		self.handle = lyric_handle(self)
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setMargin(0)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.font = QFont(_fromUtf8('微软雅黑, verdana'), 50)
		self.font.setPixelSize(50)				
		QMetaObject.connectSlotsByName(self)
	
		
		self.connect(self.handle, SIGNAL("lyricmoved(QPoint)"), self.newPos)
		self.connect(self.t, SIGNAL("timeout()"), self.changeMask)
				
	def changeMask(self):
		self.maskWidth += self.widthBlock
		self.update()
	
	def setText(self, s, intervel=0):
		self.lyric = s
		self.intervel = intervel
		self.maskWidth = 0
		self.update()
		
	def hideLyric(self):
		self.hide()
		self.emit(SIGNAL('lyrichide()'))
					
	def leaveEvent(self, event):
		self.handle.leaveEvent(event)
	
	def show(self):
		super(lyric_ui, self).show()
	
	def hide(self):
		super(lyric_ui, self).hide()
		self.handle.hide()
		
	def enterEvent(self, event):
		self.handle.handler.setFocus()
		self.handle.show()
	
	def newPos(self, p):
		self.move(self.pos().x() + p.x(), self.pos().y() + p.y())

	def startMask(self):	
		self.t.start(100)
			
	def stopMask(self):
		self.t.stop()
		self.update()
		
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setFont(self.font)
		
		linear = QLinearGradient(QPoint(self.rect().topLeft()), QPoint(self.rect().bottomLeft()))
		linear.setStart(0, 10)
		linear.setFinalStop(0, 50)
		linear.setColorAt(0.1, QColor(14, 179, 255));
		linear.setColorAt(0.5, QColor(154, 232, 255));
		linear.setColorAt(0.9, QColor(14, 179, 255));
		
		linear2 = QLinearGradient(QPoint(self.rect().topLeft()), QPoint(self.rect().bottomLeft()))
		linear2.setStart(0, 10)
		linear2.setFinalStop(0, 50)
		linear2.setColorAt(0.1, QColor(222, 54, 4));
		linear2.setColorAt(0.5, QColor(255, 172, 116));
		linear2.setColorAt(0.9, QColor(222, 54, 4));
		
		painter.setPen(QColor(0, 0, 0, 200));
		painter.drawText(QRect(1, 1, self.screen.width(), 60), Qt.AlignHCenter | Qt.AlignVCenter, self.lyric)
		
		painter.setPen(QColor('transparent'));
		self.textRect = painter.drawText(QRect(0, 0, self.screen.width(), 60), Qt.AlignHCenter | Qt.AlignVCenter, self.lyric)

		painter.setPen(QPen(linear, 0))
		painter.drawText(self.textRect, Qt.AlignLeft | Qt.AlignVCenter, self.lyric)
		if self.intervel != 0:
			self.widthBlock = self.textRect.width()/(self.intervel/150.0)
		else:
			self.widthBlock = 0
		self.maskRect = QRectF(self.textRect.x(), self.textRect.y(), self.textRect.width(), self.textRect.height())
		self.maskRect.setWidth(self.maskWidth)
		painter.setPen(QPen(linear2, 0));
		painter.drawText(self.maskRect, Qt.AlignLeft | Qt.AlignVCenter, self.lyric)
		
class lyric_handle(QDialog):
	def __init__(self, parent=None):			
		super(lyric_handle, self).__init__(parent)	
		self.timer = QTimer()		
		self.setObjectName(_fromUtf8("Dialog"))
		self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint | Qt.Tool)
		self.setStyleSheet('QDialog { background: #2c7ec8; border: 0px solid black;}')
		self.horiLayout = QHBoxLayout(self)
		self.horiLayout.setSpacing(5)
		self.horiLayout.setMargin(0)
		self.horiLayout.setObjectName(_fromUtf8("horiLayout"))
		self.handler = QLabel(self)
		self.handler.setToolTip('Move Lyric')
		self.handler.setPixmap(QPixmap(':/icons/handler.png'))
		self.handler.setMouseTracking(True)
		self.lockBt = PushButton2(self)
		self.lockBt.setToolTip('Unlocked')
		self.lockBt.loadPixmap(QPixmap(':/icons/unlock.png'))
		self.hideBt = PushButton2(self)
		self.hideBt.setToolTip('Hide Lyric')
		self.hideBt.loadPixmap(QPixmap(':/icons/close.png').copy(48, 0, 16, 16))
		self.lockBt.setCheckable(True)
		
		self.horiLayout.addWidget(self.handler)
		self.horiLayout.addWidget(self.lockBt)
		self.horiLayout.addWidget(self.hideBt)
	
		self.connect(self.lockBt, SIGNAL("clicked()"), self.lockLyric)
		self.connect(self.hideBt, SIGNAL("clicked()"), self.hideLyric)
		self.connect(self.timer, SIGNAL("timeout()"), self.hide)
	
		
	def lockLyric(self):
		if self.lockBt.isChecked():
			self.lockBt.loadPixmap(QPixmap(':/icons/lock.png'))			
			self.lockBt.setToolTip('Locked')
			self.lockBt.update()
		else:
			self.lockBt.loadPixmap(QPixmap(':/icons/unlock.png'))
			self.lockBt.setToolTip('Unlocked')
			self.lockBt.update()
	
	def hideLyric(self):
		self.parent().emit(SIGNAL('lyrichide()'))
		self.parent().hide()
		self.hide()
				
	def isInTitle(self, xPos, yPos):
		if self.lockBt.isChecked():
			return False
		else:
			return yPos <= self.height() and 0 <= xPos <= self.handler.width()
			
	def moveEvent(self, event):
		self.emit(SIGNAL("lyricmoved(QPoint)"), event.pos() - event.oldPos())
	
	def enterEvent(self, event):
		self.setFocus()
		self.timer.stop()
		
	def leaveEvent(self, event):
		self.timer.stop()
		self.timer.start(3000)
		
		
class lyric_ui_scroll(QDialog):
	def __init__(self, parent=None):	
		super(lyric_ui_scroll, self).__init__(parent)		
		self.setObjectName(_fromUtf8("Dialog"))
		self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint | Qt.Tool)
		self.setMinimumHeight(65)
		self.setAttribute(Qt.WA_TranslucentBackground)	
		self.resize(600, 200)
		self.handle = lyric_handle(self)
		c = QString(locale.getdefaultlocale()[0]).toLower()
		if c.contains('zh_cn'):
			fontname = '微软雅黑'
		else:
			fontname = 'verdana'
		self.font = QFont(_fromUtf8(fontname), 9)
		self.y = self.height()/2
		self.t = QTimer()
		self.cheight = 0
		self.intervel = 0
		self.pastColor = '#ff0000'
		self.readyColor = '#A6A6A6'
		self.baseHsl = QColor(self.readyColor).getHsl()
		self.curColor = QColor(self.pastColor)
		hsl = self.curColor.getHsl()
		self.c = (hsl[1]/14)
		self.lyric = QString(_fromUtf8('Lyric Show.'))
		self.lyricM = QString(_fromUtf8(''))
		self.lyricFront = QString(_fromUtf8(''))
		self.lyricLast = QString(_fromUtf8(''))
		self.connect(self.t, SIGNAL("timeout()"), self.changeTxtPosition)
		self.connect(self.handle, SIGNAL("lyricmoved(QPoint)"), self.newPos)
	
	def stopScroll(self):
		self.t.stop()
		self.intervel = 0
	
	def hideLyric(self):
		self.hide()
		self.emit(SIGNAL('lyrichide()'))
					
	def leaveEvent(self, event):
		self.handle.leaveEvent(event)
	
	def show(self):
		super(lyric_ui_scroll, self).show()
	
	def hide(self):
		super(lyric_ui_scroll, self).hide()
		self.handle.hide()
		
	def enterEvent(self, event):
		self.handle.handler.setFocus()
		self.handle.show()
			
	def newPos(self, p):
		self.move(self.pos().x() + p.x(), self.pos().y() + p.y())

	def setText(self, f, m1, m, l, intervel=0):
		self.t.stop()
		self.y = self.height()/2
		self.intervel = intervel
		self.cheight = 0
		self.lyricFront = f
		self.lyricM = m1
		self.lyric = m
		self.lyricLast = l
		self.curColor = QColor(self.pastColor)
		self.update()
		
	def changeTxtPosition(self):
		self.y -= 1	
		self.cheight += 1
		hsl = self.curColor.getHsl()
		result = hsl[1] - self.c
		if result > self.baseHsl[1]:
			s = result
		else:
			s = self.baseHsl[1]
			
		result = hsl[2] + 2
		if result < self.baseHsl[2]:
			l = result
		else:
			l = self.baseHsl[2]
			
		self.curColor.setHsl(hsl[0], s, l)
		self.update()	
		
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setFont(self.font)
		
		linear2 = QLinearGradient(QPoint(self.rect().topLeft()), QPoint(self.rect().bottomLeft()))
		linear2.setStart(0, 0)
		linear2.setFinalStop(0, self.height())
		linear2.setColorAt(0, QColor('transparent'));
		linear2.setColorAt(0.15, QColor('transparent'));
		linear2.setColorAt(0.3, QColor(self.readyColor));
		linear2.setColorAt(0.7, QColor(self.readyColor));
		linear2.setColorAt(0.85, QColor('transparent'));
		linear2.setColorAt(1.0, QColor('transparent'));		

		
		painter.setPen(QColor('transparent'))
		textRectF = painter.drawText(QRect(0, 0, 400, 200), Qt.AlignHCenter | Qt.AlignTop, self.lyricFront)
		painter.setPen(QColor('transparent'));
		textRectM1 = painter.drawText(QRect(0, 0, 400, 200), Qt.AlignHCenter | Qt.AlignTop, self.lyricM)
		painter.setPen(QColor('transparent'));
		textRectM = painter.drawText(QRect(0, 0, 400, 200), Qt.AlignHCenter | Qt.AlignTop, self.lyric)
		painter.setPen(QPen(linear2, 0));	
		painter.drawText(QRect(0, self.y - textRectF.height(), self.width(), textRectF.height()), Qt.AlignHCenter | Qt.AlignBottom, self.lyricFront)		

		# painter.setPen(QColor(self.pastColor));
		# painter.drawText(QRect(0, self.y - textRectM1.height() + self.cheight, self.width(), textRectM1.height() - self.cheight), Qt.AlignHCenter | Qt.AlignBottom, self.lyricM)
		
		# painter.setPen(QColor(self.readyColor));
		# painter.drawText(QRect(0, self.y - textRectM1.height(), self.width(), self.cheight), Qt.AlignHCenter | Qt.AlignTop, self.lyricM)	
		
		painter.setPen(QColor(self.curColor));
		painter.drawText(QRect(0, self.y - textRectM1.height(), self.width(), textRectM1.height()), Qt.AlignHCenter | Qt.AlignTop, self.lyricM)
		print textRectM.height()
		
		painter.setPen(QColor(self.readyColor));
		painter.drawText(QRect(0, self.y + self.cheight, self.width(), textRectM.height() - self.cheight), Qt.AlignHCenter | Qt.AlignBottom, self.lyric)
		
		painter.setPen(QColor(self.pastColor));
		painter.drawText(QRect(0, self.y, self.width(), self.cheight), Qt.AlignHCenter | Qt.AlignTop, self.lyric)
		
		painter.setPen(QPen(linear2, 0));	
		painter.drawText(QRect(0, self.y + textRectM.height(), self.width(), self.height()), Qt.AlignHCenter | Qt.AlignTop, self.lyricLast)	
		if textRectM.height() and self.intervel != 0:
			self.t.stop()
			self.t.start(self.intervel/(textRectM.height()+2))
	
