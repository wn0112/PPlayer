from PyQt4.QtGui import *
from PyQt4.QtCore import *
import images, locale

try:
	_fromUtf8 = QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s
class myTableView(QTableView):
	def __init__(self, parent=None):
		QTableView.__init__(self, parent)
		self.contextMenu = QMenu(self)
		# self.contextMenu.setFont(QFont("", 8))
		iconDelete = QIcon()
		iconSave = QIcon()
		iconFavorite = QIcon()								
		iconDelete.addPixmap(QPixmap(_fromUtf8(":/icons/delete.png")).copy(40, 0, 20, 20), QIcon.Normal, QIcon.Off)
		iconSave.addPixmap(QPixmap(_fromUtf8(":/icons/save.png")).copy(40, 0, 20, 20), QIcon.Normal, QIcon.Off)
		iconFavorite.addPixmap(QPixmap(_fromUtf8("./icons/favorites_add.png")).copy(0, 0, 24, 24), QIcon.Normal, QIcon.Off)
			
		self.action = QAction('&Save to playlist...', self)
		self.actionDelete = QAction('&Delete', self)
		self.actionFavorite = QAction('&Add to favorite', self)		
		self.actionDelete.setIcon(iconDelete)			
		self.action.setIcon(iconSave)			
		self.actionFavorite.setIcon(iconFavorite)			
					
		self.contextMenu.addAction(self.actionFavorite)
		self.contextMenu.addSeparator()
		self.contextMenu.addAction(self.action)
		self.contextMenu.addSeparator()
		self.contextMenu.addAction(self.actionDelete)
				
		self.connect(self.action, SIGNAL("triggered()"), self.addToPlayList)
		self.connect(self.actionDelete, SIGNAL("triggered()"), self.delete)
		self.connect(self.actionFavorite, SIGNAL("triggered()"), self.addToFavorite)
		

	def contextMenuEvent(self, event):
		self.contextMenu.exec_(event.globalPos())

	def delete(self):
		self.emit(SIGNAL("delete()"))
	
	def addToPlayList(self):
		self.emit(SIGNAL("addToPlayList()"))
	
	def addToFavorite(self):
		self.emit(SIGNAL("addToFavorite()"))		

class myFavoriteTable(QTableView):
	def __init__(self, parent=None):
		QTableView.__init__(self, parent)
		self.contextMenu = QMenu(self)
		# self.contextMenu.setFont(QFont("", 8))
		iconDelete = QIcon()
		iconSave = QIcon()
		iconFavorite = QIcon()								
		iconDelete.addPixmap(QPixmap(_fromUtf8(":/icons/delete.png")).copy(40, 0, 20, 20), QIcon.Normal, QIcon.Off)
		iconSave.addPixmap(QPixmap(_fromUtf8(":/icons/save.png")).copy(40, 0, 20, 20), QIcon.Normal, QIcon.Off)
		iconFavorite.addPixmap(QPixmap(_fromUtf8("./icons/favorites_remove.png")).copy(0, 0, 24, 24), QIcon.Normal, QIcon.Off)
			
		self.action = QAction('&Save to playlist...', self)
		# self.actionDelete = QAction('&Delete', self)
		self.actionFavorite = QAction('&Remove', self)		
		# self.actionDelete.setIcon(iconDelete)			
		self.action.setIcon(iconSave)			
		self.actionFavorite.setIcon(iconFavorite)			
					
		self.contextMenu.addAction(self.actionFavorite)
		# self.contextMenu.addSeparator()
		self.contextMenu.addAction(self.action)
		# self.contextMenu.addSeparator()
		# self.contextMenu.addAction(self.actionDelete)
				
		self.connect(self.action, SIGNAL("triggered()"), self.addToPlayList)
		# self.connect(self.actionDelete, SIGNAL("triggered()"), self.delete)
		self.connect(self.actionFavorite, SIGNAL("triggered()"), self.removeFavorite)
		

	def contextMenuEvent(self, event):
		self.contextMenu.exec_(event.globalPos())

	# def delete(self):
		# self.emit(SIGNAL("delete()"))
	
	def addToPlayList(self):
		self.emit(SIGNAL("addToPlayList()"))
	
	def removeFavorite(self):
		self.emit(SIGNAL("removeFavorite()"))		
		

class lyricTable(QLabel):
	def __init__(self, parent=None):
		super(QLabel, self).__init__(parent)
		self.setStyleSheet('background: #C1E0E5;')
		c = QString(locale.getdefaultlocale()[0]).toLower()
		if c.contains('zh_cn'):
			fontname = '微软雅黑'
		else:
			fontname = 'verdana'
		self.font = QFont(_fromUtf8(fontname), 8)
		self.y = self.height()/2
		self.cheight = 0
		self.t = QTimer()
		self.intervel = 0
		self.pastColor = '#ff0000'
		self.curColor = QColor(self.pastColor)
		hsl = self.curColor.getHsl()
		self.c = (hsl[1]+(hsl[2]/2))/13
		self.readyColor = '#A6A6A6'		
		self.baseHsl = QColor(self.readyColor).getHsl()
		self.lyric = QString(_fromUtf8(''))
		self.lyricM = QString(_fromUtf8(''))
		self.lyricFront = QString(_fromUtf8(''))
		self.lyricLast = QString(_fromUtf8(''))
		self.connect(self.t, SIGNAL("timeout()"), self.changeTxtPosition)
		
	def stopScroll(self):
		self.t.stop()
		self.intervel = 0
	
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
		self.curColor.setHsl(hsl[0], s , l)	
		self.update()	
		
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setFont(self.font)
		
		linear2 = QLinearGradient(QPoint(self.rect().topLeft()), QPoint(self.rect().bottomLeft()))
		linear2.setStart(0, 0)
		linear2.setFinalStop(0, self.height())
		linear2.setColorAt(0, QColor('transparent'));
		linear2.setColorAt(18.0/self.height(), QColor('transparent'));
		linear2.setColorAt(45.0/self.height(), QColor(self.readyColor));
		linear2.setColorAt(1.0 - 45.0/self.height(), QColor(self.readyColor));
		linear2.setColorAt(1.0 - 18.0/self.height(), QColor('transparent'));
		linear2.setColorAt(1.0, QColor('transparent'));		

		
		painter.setPen(QColor('transparent'));
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
		
		painter.setPen(QColor(self.readyColor));
		painter.drawText(QRect(0, self.y + self.cheight, self.width(), textRectM.height() - self.cheight), Qt.AlignHCenter | Qt.AlignBottom, self.lyric)
		
		painter.setPen(QColor(self.pastColor));
		painter.drawText(QRect(0, self.y, self.width(), self.cheight), Qt.AlignHCenter | Qt.AlignTop, self.lyric)
		

		
		painter.setPen(QPen(linear2, 0));	
		painter.drawText(QRect(0, self.y + textRectM.height(), self.width(), self.height()), Qt.AlignHCenter | Qt.AlignTop, self.lyricLast)	
		if textRectM.height() and self.intervel != 0:
			self.t.stop()
			self.t.start(self.intervel/(textRectM.height() + 2))
		
	def resizeEvent(self, event):
		super(QLabel, self).resizeEvent(event)
		self.y = event.size().height()/2 - self.cheight
		self.update()
