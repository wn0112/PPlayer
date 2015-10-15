# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import *
from Ui_MP3_Player import *
from searchWidget import *
from lyric_ui import *
from about import *
from logo import *
from mutagen.mp3 import MP3		# mutagen v1.30: https://bitbucket.org/lazka/mutagen/downloads
from mutagen.asf import ASF		# mutagen v1.30
from progressslider import *
import sip, sys, random, ConfigParser, images, re, chardet, locale, codecs

defaultcode = 'utf-8'

c = QString(locale.getdefaultlocale()[0]).toLower()
if c.contains('zh_cn'):
	defaultcode = 'gbk'
elif c.contains('zh_tw'):
	defaultcode = 'big5'
else:
	defaultcode = 'gb2312'


try:
	_fromUtf8 = QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s
		
try:
	_toUtf8 = QString.toUtf8
except AttributeError:
	def _toUtf8(s):
		return s

try:
	_encoding = QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QApplication.translate(context, text, disambig)
		
class MainWindow(QMainWindow, QWidget):

	def __init__(self, parent=None):
		self.border = 4
		self.path = QString()
		self.playList = []
		self.allList = []
		self.favList = []
		self.playList = self.allList
		self.current = 0
		self.offset = 0
		self.history = []
		self.playingTab = 0
		self.fileType = ['mp3', 'wma']
		self.file = QFileInfo()
		self.lyricExists = False
	
		
		QMainWindow.__init__(self, parent)
		sip.setdestroyonexit(False)
		self.setObjectName(_fromUtf8("mainwindow"))
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)		
		self.lyric_ui = lyric_ui()
		self.lyric_ui_scroll = lyric_ui_scroll()
		self.searchWidget = float_ui(self)
		self.logo = loading(self)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.mediaObj = phonon.Phonon.MediaObject(self)
		self.audioSink = phonon.Phonon.AudioOutput(phonon.Phonon.MusicCategory, self)
		self.audioPath = phonon.Phonon.createPath(self.mediaObj, self.audioSink)
		self.ui.volumeSlider.setAudioOutput(self.audioSink)
		self.mediaObj.setTickInterval(10)
		self.audioSink.setVolume(0.8)
		self.setAcceptDrops(True)
		self.qss = QtCore.QFile(':/qss/qss.qss')
		self.qss.open(QIODevice.ReadOnly)
		self.qssStyle = QString().fromUtf8(self.qss.readAll())
		self.qss.close()
		self.setStyleSheet(self.qssStyle)

		# -- right click menu --
		self.contextMenu = QMenu(self)
		iconOpen = QIcon(QPixmap(_fromUtf8(":/icons/folder.png")))
		iconGlobal = QIcon(QPixmap(_fromUtf8(":/icons/global.png")))
		iconSave = QIcon(QPixmap(_fromUtf8(":/icons/save.png")).copy(40, 0, 20, 20))
		iconSettings = QIcon(QPixmap(_fromUtf8(":/icons/settings.png")).copy(0, 0, 20, 20))
		iconAbout = QIcon(QPixmap(_fromUtf8(":/icons/about.png")))
			
		self.open = QAction('&Open', self)
		self.open.setShortcut(_translate("MainWindow", "Ctrl+O", None))
		self.openURL = QAction('Open &URL...', self, triggered=self.openFileFromURL)
		self.save = QAction('&Save as playlist...', self, triggered=self.addToPlayList)
		self.save.setShortcut(_translate("MainWindow", "Ctrl+S", None))
		self.settings = QAction('Settings...', self, triggered=self.settings)
		self.about = QAction('&About', self, triggered=self.showAbout)		
		self.save.setIcon(iconSave)			
		self.open.setIcon(iconOpen)			
		self.openURL.setIcon(iconGlobal)			
		self.settings.setIcon(iconSettings)			
		self.about.setIcon(iconAbout)			
		
		self.contextMenu.addAction(self.open)
		self.contextMenu.addAction(self.openURL)
		self.contextMenu.addAction(self.save)
		self.contextMenu.addSeparator()
		self.contextMenu.addAction(self.settings)
		self.contextMenu.addSeparator()
		self.contextMenu.addAction(self.about)
				
		self.connect(self.open, SIGNAL("triggered()"), self.addMusic)
		
		# -- menu end --

		# -- system tray icon --													
		iconQuit = QIcon(QPixmap(_fromUtf8(":/icons/quit.png")))									

		self.restoreAction = QtGui.QAction("P&inus Player", self, triggered=self.showNormal)
		self.settingsAction = QtGui.QAction(iconSettings, "&Settings...", self, triggered=self.showNormal)
		self.quitAction = QtGui.QAction(iconQuit, "&Quit", self, triggered=self.close)
		self.shuffleAction = QtGui.QAction("&Shuffle", self, triggered=self.randomOn)		
		self.repeat1Action = QtGui.QAction("Single &Cycle", self, triggered=self.singleRepeatOn)
		self.repeatAction = QtGui.QAction("&Repeat All", self, triggered=self.repeatOn)
		self.shuffleAction.setCheckable(True)
		self.repeat1Action.setCheckable(True)
		self.repeatAction.setCheckable(True)
			
		self.trayIconMenu = QtGui.QMenu(self)
		# self.trayIconMenu.setObjectName(_fromUtf8("traymenu"))
		self.playMenu = QtGui.QWidget()
		self.playMenuAction = QtGui.QWidgetAction(self.playMenu)
		self.playMenuAction.setDefaultWidget(self.playMenu)
		self.playmbt = PushButton()
		self.playmbt.setText("Play")
		self.previousmbt = PushButton()
		self.nextmbt = PushButton()
		self.playmbt.loadPixmap(QPixmap(_fromUtf8(":/icons/play.png")))
		self.previousmbt.loadPixmap(QPixmap(_fromUtf8(":/icons/previous.png")))
		self.nextmbt.loadPixmap(QPixmap(_fromUtf8(":/icons/next.png")))
		self.playmbt.clicked.connect(self.menuPlayPressed)
		self.previousmbt.clicked.connect(self.previousSong)
		self.nextmbt.clicked.connect(self.nextSong)
		self.playmbt.setToolTip("Play")
		self.previousmbt.setToolTip("Previous")
		self.nextmbt.setToolTip("Next")
		font = QtGui.QFont('Verdana, thoma', 8)
		self.name = menuNameLabel(self.playMenu)
		self.name.setObjectName(_fromUtf8("musicname"))
		self.name.setAlignment(QtCore.Qt.AlignCenter)
		self.color = QtGui.QPalette()
		self.color.setColor(QtGui.QPalette.Foreground, QtGui.QColor(255, 255, 255, 255))
		self.name.setPalette(self.color)
		self.layout = QtGui.QHBoxLayout()
		self.layout.addWidget(self.previousmbt)
		self.layout.addWidget(self.playmbt)
		self.layout.addWidget(self.nextmbt)
		self.layout.setSpacing(15)
		self.layout.setContentsMargins(20, 0, 20, 0)
		self.layout2 = QtGui.QVBoxLayout(self.playMenu)
		self.layout2.addWidget(self.name)
		self.layout2.addLayout(self.layout)

		self.layout2.setSpacing(10)
		self.layout2.setContentsMargins(0, 5, 0, 5)	
	
		self.trayIconMenu.addAction(self.playMenuAction)
		self.trayIconMenu.addSeparator()
		self.playMode = QtGui.QMenu(self.trayIconMenu)
		# self.playMode.setObjectName(_fromUtf8("traymenu"))
		self.playMode.setTitle("Play &Mode")
		self.playMode.addAction(self.shuffleAction)
		self.playMode.addAction(self.repeat1Action)
		self.playMode.addAction(self.repeatAction)
		self.trayIconMenu.addAction(self.playMode.menuAction())
		self.trayIconMenu.addSeparator()
		self.trayIconMenu.addAction(self.settingsAction)
		self.trayIconMenu.addSeparator()
		self.trayIconMenu.addAction(self.quitAction)
		
		self.trayIcon = QtGui.QSystemTrayIcon()
		self.trayIcon.setContextMenu(self.trayIconMenu)
		self.trayIcon.setIcon(QIcon(":/icons/headset.png"))
		self.trayIcon.setToolTip("Pinus Player")
		self.trayIcon.activated.connect(self.trayIconActivated)
				
		## -- system tray icon end --
		self.connect(self.ui.tableView_2, SIGNAL("clicked(const QModelIndex&)"), self.clickStarFav)
		self.connect(self.ui.tableView, SIGNAL("clicked(const QModelIndex&)"), self.clickStarAll)
		self.connect(self.ui.seekSlider, SIGNAL("sliderMoved(int)"), self.sliderMoved)
		self.connect(self.lyric_ui, SIGNAL("lyrichide()"), self.singleLyrichide)
		self.connect(self.lyric_ui_scroll, SIGNAL("lyrichide()"), self.multipleLyrichide)
		self.connect(self, SIGNAL("err(QString)"), self.showErr)
		self.connect(self.ui.tabWidget, SIGNAL("currentChanged(int)"), self.tabChanged)
		self.connect(self.audioSink, SIGNAL("volumeChanged(qreal)"), self.volumeChanged)
		self.connect(self.ui.tableView, SIGNAL("doubleClicked(const QModelIndex&)"), self.doubleClicked)
		self.connect(self.ui.tableView_2, SIGNAL("doubleClicked(const QModelIndex&)"), self.doubleClickedFavoriteTable)
		self.connect(self.ui.tableView, SIGNAL("entered(const QModelIndex&)"), self.allMusicEntered)
		self.connect(self.ui.tableView_2, SIGNAL("entered(const QModelIndex&)"), self.favoriteEntered)
		self.connect(self.ui.miniBt, SIGNAL("clicked()"), self.showMinimized)		
		self.connect(self.ui.closeBt, SIGNAL("clicked()"), self.hideMainWindow)		
		self.connect(self.ui.add, SIGNAL("clicked()"), self.addMusic)		
		self.connect(self, SIGNAL("addMusic(QStringList)"), self.addMusic)		
		self.connect(self.ui.delete, SIGNAL("clicked()"), self.delete)		
		self.connect(self.ui.delete_2, SIGNAL("clicked()"), self.removeFavorite)		
		self.connect(self.ui.save, SIGNAL("clicked()"), self.addToPlayList)		
		self.connect(self.ui.save_2, SIGNAL("clicked()"), self.addToPlayList)		
		self.connect(self.ui.stop, SIGNAL("clicked()"), self.stopPressed)		
		self.connect(self.ui.stop, SIGNAL("released()"), self.stopReleased)		
		self.connect(self.ui.play, SIGNAL("clicked()"), self.playPressed)	
		self.connect(self.ui.play, SIGNAL("released()"), self.playReleased)	
		self.connect(self.ui.next, SIGNAL("clicked()"), self.nextPressed)	
		self.connect(self.ui.next, SIGNAL("released()"), self.nextReleased)	
		self.connect(self.ui.previous, SIGNAL("clicked()"), self.previousPressed)	
		self.connect(self.ui.previous, SIGNAL("released()"), self.previousReleased)	
		self.connect(self.ui.repeat, SIGNAL("clicked()"), self.repeatOn)	
		self.connect(self.ui.repeat1, SIGNAL("clicked()"), self.singleRepeatOn)	
		self.connect(self.ui.shuffle, SIGNAL("clicked()"), self.randomOn)	
		self.connect(self.ui.search, SIGNAL("clicked()"), self.searchClicked)	
		self.connect(self.ui.volume, SIGNAL("clicked()"), self.muteClicked)	
		self.connect(self.mediaObj, SIGNAL("finished()"), self.nextSong)
		self.connect(self.mediaObj, SIGNAL("tick(qint64)"), self.setCurrentTime)
		self.connect(self.mediaObj, SIGNAL("metaDataChanged()"), self.fileChanged)	
		self.connect(self.mediaObj, SIGNAL("stateChanged(Phonon::State,Phonon::State)"), self.stateChanged)	
		self.connect(self.ui.tableView, SIGNAL("delete()"), self.delete)
		self.connect(self.ui.tableView, SIGNAL("addToPlayList()"), self.addToPlayList)
		self.connect(self.ui.tableView_2, SIGNAL("addToPlayList()"), self.addToPlayList)
		self.connect(self.ui.tableView_2, SIGNAL("removeFavorite()"), self.removeFavorite)
		self.connect(self.ui.tableView, SIGNAL("addToFavorite()"), self.addToFavorite)
		self.connect(self.ui.tableView, SIGNAL("openFolder()"), self.openFolder_all)
		self.connect(self.ui.tableView_2, SIGNAL("openFolder()"), self.openFolder_fav)
		self.connect(self, SIGNAL("autoSave(QString)"), self.exportIni)	
		self.connect(self.searchWidget.lineEdit, SIGNAL("textChanged(QString)"), self.textChanged)
		self.connect(self.logo, SIGNAL("loadingclosed()"), self.close)
		self.connect(self, SIGNAL("loadCompleted()"), self.loadCompleted)
		self.connect(self.ui.singleLine, SIGNAL('triggered()'), self.showSingleLineLyric)
		self.connect(self.ui.multipleLines, SIGNAL('triggered()'), self.showMultipleLinesLyric)

		self.logo.show()
		self.initialUI()
		self.initialTable()
		config = QFileInfo('./playerconfig.ini')
		if config.isReadable():
			self.importIni(config.filePath())		
		else:
			self.emit(SIGNAL("loadCompleted()"))

	def openFolder_all(self):
		selectModel = self.ui.tableView.selectionModel()
		selectedRows = selectModel.selectedRows()
		if len(self.allList) == self.model.rowCount():
			afile = self.allList[selectedRows[0].row()]
		else:
			afile = self.allList[int(self.matchID[selectedRows[0].row()])]
		
		f = QFileInfo(afile.getFilePath())
		try:
			QProcess.startDetached("explorer.exe /select, " + f.filePath().replace("/", "\\").toUtf8().data().decode('utf-8'))
		except:
			QProcess.startDetached("explorer.exe " + f.absolutePath().replace("/", "\\").toUtf8().data().decode('utf-8'))
	
	def openFolder_fav(self):
		selectModel = self.ui.tableView_2.selectionModel()
		selectedRows = selectModel.selectedRows()
		afile = self.favList[selectedRows[0].row()]
		f = QFileInfo(afile.getFilePath())
		try:
			QProcess.startDetached("explorer.exe /select, " + f.filePath().replace("/", "\\").toUtf8().data().decode('utf-8'))
		except:
			QProcess.startDetached("explorer.exe " + f.absolutePath().replace("/", "\\").toUtf8().data().decode('utf-8'))
		
	def hideMainWindow(self):
		self.emit(SIGNAL("autoSave(QString)"), _fromUtf8('./playerconfig.ini'))
		self.showMinimized()
		self.hide()
		
	def clickStarAll(self, index):
		i = index.row()
		if index.column() == 4:
			if self.model.item(index.row(), index.column()).text() == '1':
				if self.model.rowCount() != len(self.allList):
					indexOfFav = self.favList.index(self.allList[int(self.matchID[index.row()])])		
					self.model.setItem(i, 4, QStandardItem(QIcon(":/icons/unfavorite.png"), "0"))					
				else:
					indexOfFav = self.favList.index(self.allList[index.row()])
				self.removeFavorite(indexOfFav)
			else:
				self.addToFavorite()
			# self.ui.tableView.setCurrentIndex(self.model.index(i, 0))			
			self.ui.tableView.clearSelection()			
						
	def clickStarFav(self, index):
		if index.column() == 4:
			self.removeFavorite(index.row())
		
	def showSingleLineLyric(self):
		if self.ui.singleLine.isChecked():
			screen = QApplication.desktop().availableGeometry()	
			self.lyric_ui.resize(screen.width(), 50)
			self.lyric_ui.move(0, screen.height() - 100)
			self.lyric_ui.handle.move((screen.width()/2) + 100, screen.height() - 120)
			self.lyric_ui.show()

		else:
			self.lyric_ui.hide()
		
	def showMultipleLinesLyric(self):
		if self.ui.multipleLines.isChecked():
			self.lyric_ui_scroll.show()
			self.lyric_ui_scroll.handle.move(self.lyric_ui_scroll.pos().x()+ self.lyric_ui_scroll.width()/2 - 30, self.lyric_ui_scroll.pos().y()+self.lyric_ui_scroll.height()/2 + 100)
		else:
			self.lyric_ui_scroll.hide()
			
	def settings(self):
		pass
			
	def pressed(self, index):
		self.emit(SIGNAL('listdoubleclicked(int)'), index.row())
			
	def sliderMoved(self, time):
		self.mediaObj.seek(time)
					
	def singleLyrichide(self):
		self.ui.singleLine.setChecked(False)
		
	def multipleLyrichide(self):
		self.ui.multipleLines.setChecked(False)
			
	def showErr(self, str):
		msg = invalidFileMsg(self)
		msg.setLabelText(_toUtf8(str).data())
		self.show()
		self.showNormal()
		msg.show()
					
	def trayIconActivated(self, reason):
		if self.mediaObj.state() == 2:
			self.playmbt.loadPixmap(QPixmap(":/icons/stop.png"))
			self.playmbt.update()
			self.playmbt.setText("Stop")
			self.playmbt.setToolTip("Stop")
		else:
			self.playmbt.loadPixmap(QPixmap(":/icons/play.png"))
			self.playmbt.update()		
			self.playmbt.setText("Play")
			self.playmbt.setToolTip("Play")

		self.shuffleAction.setChecked(self.ui.shuffle.isChecked())
		self.repeat1Action.setChecked(self.ui.repeat1.isChecked())
		self.repeatAction.setChecked(self.ui.repeat.isChecked())
		self.previousmbt.setDisabled(self.mediaObj.state() != 2)
		self.nextmbt.setDisabled(self.mediaObj.state() != 2)
		if reason == QtGui.QSystemTrayIcon.Trigger and self.isHidden() and self.movie.state() == 0:
			self.showNormal()
			self.show()
			self.activateWindow()
	
	def tabChanged(self):
		self.emit(SIGNAL('mouseleavetable()'))
		if self.ui.search.isChecked():
			self.searchClicked()
			self.ui.search.status = 0
			self.ui.search.update()
	
	def openFileFromURL(self):
		enterURL = openURL(self)	
		enterURL.show()
		
	def contextMenuEvent(self, event):
		if event.pos().y() < self.ui.frame_4.pos().y():
			self.contextMenu.exec_(event.globalPos())
		
	def showAbout(self):
		ab = about(self)	
		ab.show()
		
	def searchClicked(self):
		if not self.ui.search.isChecked():
			self.ui.search.setChecked(True)	
			self.searchWidget.resize(self.width()-12, 35)			
			self.searchWidget.move(self.pos().x()+6, self.pos().y()+self.rect().height()-self.ui.operationFrame.height()-36)
			self.searchWidget.show()
		elif self.ui.search.isChecked() and self.searchWidget.lineEdit.text():
			self.restoreTableAll()
			self.ui.search.setChecked(False)
			self.searchWidget.lineEdit.rst()
			self.searchWidget.hide()		
		else:
			self.ui.search.setChecked(False)
			self.searchWidget.lineEdit.rst()
			self.searchWidget.hide()
			self.setPos()
		
	def textChanged(self, Qstr):
		r1 = QRegExp('.*'+Qstr.toLower()+'.*')
		length = len(self.allList)
		if Qstr and self.searchWidget.lineEdit.palette().color(QtGui.QPalette.Text).red() != 150:
			self.model.removeRows(0, self.model.rowCount())
			self.matchID = []			
			for i in xrange(length):
				if r1.exactMatch(self.allList[i].getTitle().toLower()):
					self.matchID.append(str(i))
					lst = [QStandardItem(""), \
							QStandardItem(self.allList[i].getTitle()), \
							QStandardItem(self.allList[i].getTime()), \
							QStandardItem(self.allList[i].getBitrate()), \
							QStandardItem(QIcon(":/icons/unfavorite.png"), "0")]
					self.model.appendRow(lst)
					curIndex = self.model.rowCount()-1
					self.model.item(curIndex, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)					
					if self.allList[i] in self.favList:
						self.model.setItem(curIndex, 4, QStandardItem(QIcon(":/icons/favorite.png"), "1"))
					
		elif self.model.rowCount() != len(self.allList):
			self.restoreTableAll()
			
	def moveEvent(self, event):
		self.emit(SIGNAL("parentMoved(QPoint)"), event.pos() - event.oldPos())
		self.emit(SIGNAL('mouseleavetable()'))

	def resizeEvent(self, event):
		self.emit(SIGNAL("parentResized(QSize)"), event.size() - event.oldSize())
		self.emit(SIGNAL('mouseleavetable()'))

	def volumeChanged(self, q):
		if q > 0.66:
			self.audioSink.setMuted(False)
			self.ui.volume.setChecked(False)
			self.volumePixmap = self.volumeIcon.copy(0, 60, 80, 20)
		elif 0.66 >= q > 0.33:
			self.audioSink.setMuted(False)
			self.ui.volume.setChecked(False)
			self.volumePixmap = self.volumeIcon.copy(0, 40, 80, 20)		
		elif 0 < q <= 0.33:
			self.audioSink.setMuted(False)
			self.ui.volume.setChecked(False)
			self.volumePixmap = self.volumeIcon.copy(0, 20, 80, 20)
		elif q == 0:
			self.muteClicked()
		self.ui.volume.loadPixmap(self.volumePixmap)
		self.ui.volume.update()

	def muteClicked(self):
		if not self.ui.volume.isChecked():
			self.ui.volume.setChecked(True)
			self.audioSink.setMuted(True)
			self.volumePixmap = self.volumeIcon.copy(0, 0, 80, 20)
		else:
			self.ui.volume.setChecked(False)
			self.audioSink.setMuted(False)
			self.volumeChanged(self.audioSink.volume())

		self.ui.volume.loadPixmap(self.volumePixmap)
		self.ui.volume.update()
			
	def allMusicEntered(self, index):
		title = self.model.item(index.row(), 1).text()
		if len(self.allList) == self.model.rowCount():
			afile = self.allList[index.row()]
		else:
			afile = self.allList[int(self.matchID[index.row()])]
	
		if self.allList[index.row()].getType() == 0:
			QToolTip.showText(QCursor.pos(),  title + "\n" + afile.getFilePath().replace("/", "\\"))
		elif self.allList[index.row()].getType() == 1:
			QToolTip.showText(QCursor.pos(), title + "\n" + afile.getFilePath())
		
	def favoriteEntered(self, index):
		if self.favList[index.row()].getType() == 0:
			QToolTip.showText(QCursor.pos(), self.model_2.item(index.row(), 1).text() + "\n" +self.favList[index.row()].getFilePath().replace("/", "\\"))
		elif self.favList[index.row()].getType() == 1:
			QToolTip.showText(QCursor.pos(), self.model_2.item(index.row(), 1).text() + "\n" +self.favList[index.row()].getFilePath())
			
	def delete(self):
		a = []
		selectModel = self.ui.tableView.selectionModel()
		selectedRows = selectModel.selectedRows()
		if self.model.rowCount() != len(self.allList):
			a = [ int(self.matchID[i.row()]) for i in selectedRows ]
		else:
			a = [ i.row() for i in selectedRows ]

		a.sort()
		a.reverse()
		
		if self.mediaObj.currentSource().type() != 4:
			curIndex = self.getCurrentIndex()
		else:
			curIndex = -1
			
		for i in a:
			if self.model.rowCount() != len(self.allList):
				mindex = self.matchID.index(str(i))
				self.model.removeRows(mindex, 1)
				self.matchID.remove(str(i))
				
				# update matchID list
				for j in xrange(mindex, len(self.matchID)):
					self.matchID[j] = str(int(self.matchID[j])-1)
			else:
				self.model.removeRows(i, 1)
				
			if self.allList[i] in self.favList:
				self.model_2.removeRows(self.favList.index(self.allList[i]), 1)
				self.favList.remove(self.allList[i]) 
				
			del self.allList[i]
			
				
		# if deleted a current playing song	
		if not self.playingTab and curIndex in a:
			self.stopPressed()
			self.stopReleased()
			self.ui.musicName.setText("")
			self.ui.playTime.setText("")
			if len(self.allList):
				if curIndex < len(self.allList):
					self.mediaObj.setCurrentSource(self.allList[curIndex].getMediaSource())
				else:
					lenOfAll = len(self.allList)
					while(curIndex >= lenOfAll):
						curIndex -= 1
					self.mediaObj.setCurrentSource(self.allList[curIndex].getMediaSource())
			else:
				self.mediaObj.clear()
				self.current = -1				
		elif self.playingTab and curIndex in a:	
			self.stopPressed()
			self.stopReleased()
			self.ui.musicName.setText("")
			self.ui.playTime.setText("")
			if len(self.favList):
				if curIndex < len(self.favList):
					self.mediaObj.setCurrentSource(self.favList[curIndex].getMediaSource())
				else:
					while(curIndex >= len(self.favList)):
						curIndex -= 1
					self.mediaObj.setCurrentSource(self.favList[curIndex].getMediaSource())
			else:
				self.mediaObj.clear()
				self.current = -1
				
		if not len(self.allList) and not len(self.favList):
			self.playingTab = 0
			self.playList = self.allList
			
		self.emit(SIGNAL("autoSave(QString)"), _fromUtf8('./playerconfig.ini'))
		
	def addToPlayList(self):
		file = QFileDialog.getSaveFileName(self, 'Save Playlist', './', 'M3U File (*.m3u);;')
		if file:
			lst = []
			playlist = codecs.open(_toUtf8(file).data(), 'wb+', 'utf-8')
			playlist.write(u"#EXTM3U\n")
			
			if self.ui.tabWidget.currentIndex():
				selectModel = self.ui.tableView_2.selectionModel()
				lst = self.favList
			elif self.model.rowCount() != len(self.allList):		
				selectModel = self.ui.tableView.selectionModel()
				lst = [ self.allList[int(i)] for i in self.matchID ]
			else:
				selectModel = self.ui.tableView.selectionModel()
				lst = self.allList
			selectedRows = selectModel.selectedRows()
			if len(selectedRows):
				a = []
				a = [ i.row() for i in selectedRows ]
				a.sort()
				for song in a:
					if lst[song].getType() == 0:
						self.file.setFile(lst[song].getFilePath())
						playlist.write(u"#EXTINF:0,"+self.file.fileName().toUtf8().data().decode("utf-8")+u"\n")
						playlist.write(self.file.filePath().replace(u"/", u"\\").toUtf8().data().decode('utf-8')+u'\n\n')
					elif lst[song].getType() == 1:
						playlist.write(u"#EXTINF:0,"+lst[song].getFilePath().replace(QRegExp(".*/"), u"").toUtf8().data().decode('utf-8')+u"\n")
						playlist.write(lst[song].getFilePath().toUtf8().data().decode('utf-8')+u'\n\n')
			else:
				for song in lst:
					if song.getType() == 0:
						self.file.setFile(song.getFilePath())			
						playlist.write(u"#EXTINF:0,"+self.file.fileName().toUtf8().data().decode("utf-8")+u"\n")
						playlist.write(self.file.filePath().replace(u"/", u"\\").toUtf8().data().decode('utf-8')+u'\n\n')
					elif song.getType() == 1:
						playlist.write(u"#EXTINF:0,"+song.getFilePath().replace(QRegExp(".*/"), u"").toUtf8().data().decode('utf-8')+u"\n")
						playlist.write(song.getFilePath().toUtf8().data().decode('utf-8')+u'\n\n')
			playlist.close()
	
	def addToFavorite(self):
		selectModel = self.ui.tableView.selectionModel()
		selectedRows = selectModel.selectedRows()
		self.ui.tableView.clearSelection()	
		icon = QIcon(':/icons/favorite.png')
		if self.model.rowCount() != len(self.allList):
			for i in selectedRows:
				index = i.row()
				row = self.allList[int(self.matchID[index])]
				if row in self.favList:
					continue
				lst = [QStandardItem(""), \
						QStandardItem(self.model.item(index, 1)), \
						QStandardItem(self.model.item(index, 2)), \
						QStandardItem(self.model.item(index, 3)), \
						QStandardItem(icon, "1")]
				self.model_2.appendRow(lst)	
				curIndex = self.model_2.rowCount() - 1
				self.model_2.item(curIndex, 1).setForeground((QBrush(QColor(0, 0, 0))))
				self.model_2.item(curIndex, 2).setForeground((QBrush(QColor(0, 0, 0))))
				self.favList.append(row)
				# self.model.setItem(index, 4, QStandardItem(icon,'1'))
				
			if len(selectedRows) > 1:
				self.model.removeRows(0, self.model.rowCount())
				length = len(self.matchID)
				for i in xrange(length):
					lst = [QStandardItem(""), \
							QStandardItem(self.allList[int(self.matchID[i])].getTitle()), \
							QStandardItem(self.allList[int(self.matchID[i])].getTime()), \
							QStandardItem(self.allList[int(self.matchID[i])].getBitrate()), \
							QStandardItem(QIcon(":/icons/unfavorite.png"), "0")]
					self.model.appendRow(lst)
					self.model.item(self.model.rowCount()-1, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
					if self.allList[int(self.matchID[i])] in self.favList:
						self.model.setItem(i, 4, QStandardItem(icon, "1"))
			else:
				self.model.setItem(index, 4, QStandardItem(icon, "1"))
		else:		
			for i in selectedRows:
				index = i.row()
				if self.allList[index] in self.favList:
					continue
				# self.model.setItem(index, 4, QStandardItem(QIcon(":/icons/favorite.png"), "1"))
				lst = [QStandardItem(""), \
						QStandardItem(self.model.item(index, 1)), \
						QStandardItem(self.model.item(index, 2)), \
						QStandardItem(self.model.item(index, 3)), \
						QStandardItem(icon, "1")]
				self.model_2.appendRow(lst)	
				curIndex = self.model_2.rowCount() - 1
				self.model_2.item(curIndex, 1).setForeground((QBrush(QColor(0, 0, 0))))
				self.model_2.item(curIndex, 2).setForeground((QBrush(QColor(0, 0, 0))))
				self.favList.append(self.allList[index])
					
			# 
			if len(selectedRows) > 1:
				self.restoreTableAll()
			else:
				self.model.setItem(index, 4, QStandardItem(icon, "1"))
				
		if self.mediaObj.currentSource().type() == 4 and self.playingTab:
			self.mediaObj.setCurrentSource(self.playList[0].getMediaSource())
				
		

	def restoreTableAll(self):
		unfavIcon = QIcon(":/icons/unfavorite.png")
		favIcon = QIcon(":/icons/favorite.png")
		self.model.removeRows(0, self.model.rowCount())
		length = len(self.allList)
		for i in xrange(length):
			lst = [QStandardItem(""), \
					QStandardItem(self.allList[i].getTitle()), \
					QStandardItem(self.allList[i].getTime()), \
					QStandardItem(self.allList[i].getBitrate()), \
					QStandardItem(unfavIcon, "0")]
			self.model.appendRow(lst)
			self.model.item(self.model.rowCount()-1, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
			if self.allList[i] in self.favList:
				self.model.setItem(i, 4, QStandardItem(favIcon, "1"))
		self.setPos()
		
	def removeFavorite(self, row=None):	
		a = []
		if row != None:
			a.append(row)
		else:			
			selectModel = self.ui.tableView_2.selectionModel()
			selectedRows = selectModel.selectedRows()			
			a = [ i.row() for i in selectedRows ]
			a.sort()
			a.reverse()		

		self.ui.tableView.clearSelection()			
		if self.mediaObj.currentSource().type() != 4:
			curIndex = self.getCurrentIndex()
		else:
			curIndex = -1
			
		for i in a:
			if not self.ui.search.isChecked():
				self.model.setItem(self.allList.index(self.favList[i]), 4, QStandardItem(QIcon(":/icons/unfavorite.png"), "0"))
			self.model_2.removeRows(i, 1)
			del self.favList[i]
			
		if self.playingTab and curIndex in a:	
			self.stopPressed()
			self.stopReleased()
			self.ui.musicName.setText("")
			self.ui.playTime.setText("")
			if len(self.favList):
				if curIndex < len(self.favList):
					self.mediaObj.setCurrentSource(self.favList[curIndex].getMediaSource())
				else:
					while(curIndex >= len(self.favList)):
						curIndex -= 1
					self.mediaObj.setCurrentSource(self.favList[curIndex].getMediaSource())
			else:
				self.mediaObj.clear()
				self.current = -1	
			
		#self.emit(SIGNAL("autoSave(QString)"), _fromUtf8('./playerconfig.ini'))
			
	def menuPlayPressed(self):
		if self.playmbt.text() == "Play":
			self.playPressed()
		else:
			self.menuStopPressed()
					
	def playPressed(self, invoke=None):
		if not self.ui.play.isChecked():
			if invoke == None:
				self.ui.previous.rbPressed()
			self.ui.play.setChecked(True)		
			self.ui.stop.lbPressed()
		
		if not len(self.playList) or self.mediaObj.currentSource().type() == 4:
			self.ui.play.setChecked(False)
			return
			
		if self.mediaObj.state() != phonon.Phonon.PlayingState:
			self.mediaObj.play()

	def playReleased(self):
		if not len(self.playList) or self.mediaObj.currentSource().type() == 4:
			self.ui.play.rst()		
			self.ui.previous.rbReleased()
			self.ui.stop.lbReleased()
			
	def setPos(self):
		self.lyric_ui.stopMask()
		if self.mediaObj.currentSource().type() == 4:
			return
			
		if self.model.rowCount() != len(self.allList):
			return

		curIndex = self.getCurrentIndex()
		if not self.playingTab:
			self.ui.tableView.clearSelection()	
			self.model.setItem(curIndex, 0, QStandardItem(QIcon(QPixmap(":/icons/pos.png")), ""))
			self.model.item(curIndex, 1).setForeground((QBrush(QColor(0, 0, 255))))
			self.model.item(curIndex, 2).setForeground((QBrush(QColor(0, 0, 255))))
			if self.isVisible():
				self.ui.tableView.scrollTo(self.model.index(curIndex, 0))
							
		elif self.playingTab:
			self.ui.tableView_2.clearSelection()	
			self.model_2.setItem(curIndex, 0, QStandardItem(QIcon(QPixmap(":/icons/pos.png")), ""))
			self.model_2.item(curIndex, 1).setForeground((QBrush(QColor(0, 0, 255))))
			self.model_2.item(curIndex, 2).setForeground((QBrush(QColor(0, 0, 255))))
			if self.isVisible():
				self.ui.tableView_2.scrollTo(self.model_2.index(curIndex, 0))
			
	def removePos(self):
		if self.playingTab and self.mediaObj.currentSource().type() == 4:
			return
		else:
			curIndex = self.getCurrentIndex()
		
		if self.model.rowCount() != len(self.allList):
			return
		
		if self.playingTab:
			self.ui.tableView.clearSelection()	
			self.model_2.setItem(curIndex, 0, QStandardItem(""))
			self.model_2.item(curIndex, 1).setForeground((QBrush(QColor(0, 0, 0))))
			self.model_2.item(curIndex, 2).setForeground((QBrush(QColor(0, 0, 0))))

		else:
			self.ui.tableView_2.clearSelection()	
			self.model.setItem(curIndex, 0, QStandardItem(""))
			self.model.item(curIndex, 1).setForeground((QBrush(QColor(0, 0, 0))))
			self.model.item(curIndex, 2).setForeground((QBrush(QColor(0, 0, 0))))
						
	def doubleClicked(self, index):
		self.ui.tableView.clearSelection()
		if self.model.rowCount() != len(self.allList):
			i = index.row()
			if self.playingTab:
				self.removePos()
			self.playList = self.allList
			self.playingTab = 0
			self.mediaObj.setCurrentSource(self.playList[int(self.matchID[i])].getMediaSource())
			self.searchClicked()
			self.ui.search.status = 0
			self.ui.search.update()
		else:	
			self.removePos()
			self.playList = self.allList
			self.playingTab = 0
			self.mediaObj.setCurrentSource(self.playList[index.row()].getMediaSource())
			
		self.resetSlider()
		self.playPressed()	
		self.emit(SIGNAL('listdoubleclicked(int)'), index.row())
			
	def doubleClickedFavoriteTable(self, index):
		self.ui.tableView.clearSelection()	
		self.removePos()
		self.playList = self.favList
		self.ui.tableView_2.clearSelection()
		self.playingTab = 1
		self.mediaObj.setCurrentSource(self.playList[index.row()].getMediaSource())
		self.resetSlider()
		self.playPressed()
		self.emit(SIGNAL('listdoubleclicked(int)'), index.row())
	
	def nextSong(self):
		if self.playList:
			self.resetSlider()
			curIndex = self.getCurrentIndex()
			if self.ui.repeat1.isChecked():
				self.mediaObj.stop()			
				self.mediaObj.play()			
			elif curIndex != len(self.playList)-1 or self.ui.repeat.isChecked():
				self.removePos()
				if self.ui.shuffle.isChecked():
					num = curIndex
					while(num == curIndex and len(self.playList) != 1):
						num = random.randint(0, len(self.playList)-1)
					self.mediaObj.setCurrentSource(self.playList[num].getMediaSource())
				else:
					self.mediaObj.setCurrentSource(self.playList[curIndex+1-len(self.playList)].getMediaSource())
				self.playPressed()
			else:
				self.mediaObj.stop()
				self.ui.play.setChecked(False)
				self.ui.previous.rst()
				self.ui.play.rst()
				self.ui.stop.rst()	
				
	def nextPressed(self):	
		self.nextSong()
		if self.ui.play.isChecked():
			self.ui.stop.bothPressed()
		else:
			self.ui.stop.rbPressed()
			self.ui.previous.rst()
			self.ui.play.rst()			
			
	def nextReleased(self):
		if self.ui.play.isChecked():
			self.ui.stop.lbPressed()
		else:
			self.ui.stop.rbReleased()	

	def previousPressed(self):
		self.previousSong()
		if not self.ui.play.isChecked():
			self.ui.play.lbPressed()
					
	def previousSong(self, invoke=None):
		if self.playList:
			self.resetSlider()		
			curIndex = self.getCurrentIndex()
			if self.ui.repeat1.isChecked():
				self.mediaObj.stop()			
				self.mediaObj.play()
			elif curIndex != 0 or self.ui.repeat.isChecked():
				self.removePos()
				if self.ui.shuffle.isChecked():
					num = curIndex
					while(num == curIndex and len(self.playList) != 1):
						num = random.randint(0, len(self.playList)-1)
					self.mediaObj.setCurrentSource(self.playList[num].getMediaSource())
				else:
					self.mediaObj.setCurrentSource(self.playList[curIndex-1].getMediaSource())
				self.playPressed(1)
			else:
				self.mediaObj.stop()
				self.ui.play.setChecked(False)
				if invoke != None:
					self.ui.previous.rst()
				self.ui.play.rst()
				self.ui.stop.rst()
	
	def previousReleased(self):
		if not self.ui.play.isChecked():
			self.ui.play.lbReleased()
			self.ui.previous.rst()
		else:
			self.ui.previous.rbPressed()

	def menuStopPressed(self):
		self.stopPressed()
		self.stopReleased()
			
	def stopPressed(self):
		self.stopLyric()
		self.ui.previous.rbReleased()
		self.ui.play.rbPressed()
		self.ui.next.lbPressed()
		self.ui.play.setChecked(False)
		self.mediaObj.stop()
		
	def stopReleased(self):
		self.ui.play.rst()
		self.ui.next.rst()	
		self.ui.stop.rst()	
	
	def resetSlider(self):
		self.ui.currentTime.setText('00:00')
		self.ui.seekSlider.setValue(0)
				
	def singleRepeatOn(self):
		if not self.ui.repeat1.isChecked():
			self.ui.repeat1.setChecked(True)
			self.ui.repeat1.status = 2
			self.ui.repeat1.update()
			if not self.ui.shuffle.isChecked() and not self.ui.repeat.isChecked():
				self.ui.shuffle.rbPressed()
				self.ui.repeat.lbPressed()
			elif not self.ui.shuffle.isChecked() and self.ui.repeat.isChecked():
				self.ui.shuffle.rbPressed()
			elif self.ui.shuffle.isChecked() and not self.ui.repeat.isChecked():
				self.ui.repeat.lbPressed()
		else:
			self.ui.repeat1.setChecked(False)
			self.ui.repeat1.status = 0
			self.ui.repeat1.update()	
			if not self.ui.shuffle.isChecked() and not self.ui.repeat.isChecked():
				self.ui.shuffle.rst()
				self.ui.repeat.rst()
				self.ui.repeat1.rst()
			elif not self.ui.shuffle.isChecked() and self.ui.repeat.isChecked():
				self.ui.shuffle.rst()
				self.ui.repeat1.rbPressed()
			elif self.ui.shuffle.isChecked() and not self.ui.repeat.isChecked():
				self.ui.repeat.rst()
				self.ui.repeat1.lbPressed()
			else:
				self.ui.repeat1.bothPressed()
		
	def repeatOn(self):	
		if not self.ui.repeat.isChecked():
			self.ui.repeat.setChecked(True)
			self.ui.repeat.status = 2
			self.ui.repeat.update()
			if not self.ui.shuffle.isChecked() and not self.ui.repeat1.isChecked():
				self.ui.repeat1.rbPressed()
			elif self.ui.shuffle.isChecked() and not self.ui.repeat1.isChecked():
				self.ui.repeat1.bothPressed()				
		else:
			self.ui.repeat.setChecked(False)
			self.ui.repeat.status = 0
			self.ui.repeat.update()
			if not self.ui.shuffle.isChecked() and not self.ui.repeat1.isChecked():
				self.ui.repeat1.rst()
				self.ui.repeat.rst()
			elif self.ui.shuffle.isChecked() and not self.ui.repeat1.isChecked():
				self.ui.repeat1.lbPressed()
				self.ui.repeat.rst()
			else:
				self.ui.repeat.lbPressed()
			
	def randomOn(self):
		if not self.ui.shuffle.isChecked():
			self.ui.shuffle.setChecked(True)
			self.ui.shuffle.status = 2
			self.ui.shuffle.update()
			if not self.ui.repeat1.isChecked() and not self.ui.repeat.isChecked():
				self.ui.repeat1.lbPressed()
			elif not self.ui.repeat1.isChecked() and self.ui.repeat.isChecked():
				self.ui.repeat1.bothPressed()
		else:
			self.ui.shuffle.setChecked(False)
			self.ui.shuffle.status = 0
			self.ui.shuffle.update()
			if not self.ui.repeat1.isChecked() and not self.ui.repeat.isChecked():
				self.ui.shuffle.rst()
				self.ui.repeat1.rst()
			elif not self.ui.repeat1.isChecked() and self.ui.repeat.isChecked():
				self.ui.shuffle.rst()
				self.ui.repeat1.rbPressed()
			else:
				self.ui.shuffle.rbPressed()
	
	def addMusic(self, file=None, fav=None):
		if self.ui.search.isChecked():
			self.searchClicked()
			self.ui.search.status = 0
			self.ui.search.update()
		if file == None:
			self.audioFiles = QFileDialog.getOpenFileNames(self, 'Open Audio File', self.path,'Audio File (*.mp3; *.wma;);;Playlist file (*.m3u;)')
		else:
			self.audioFiles = file
		
		if len(self.audioFiles):
			self.ui.tabWidget.setCurrentIndex(0)
			self.ui.previous.setDisabled(True)		
			self.ui.play.setDisabled(True)
			self.ui.stop.setDisabled(True)
			self.ui.next.setDisabled(True)
			self.ui.search.setDisabled(True)
			self.ui.statusLabel.setToolTip("Loading")
			self.ui.statusLabel.setMovie(self.movie)
			self.movie.start()
			
			self.th1 = myThread(self, self.audioFiles, fav)
			self.connect(self.th1, SIGNAL("appendrow(PyQt_PyObject)"), self.appendRow)
			self.connect(self.th1, SIGNAL("appendfav(int)"), self.appendFav)
			# print QTime().currentTime()
			self.th1.start()

	def loadCompleted(self):
		if self.mediaObj.currentSource().type() == 4 and self.model.rowCount():
			self.mediaObj.setCurrentSource(self.playList[self.current].getMediaSource())
				
		self.ui.previous.setDisabled(False)
		self.ui.play.setDisabled(False)
		self.ui.stop.setDisabled(False)
		self.ui.next.setDisabled(False)
		self.ui.search.setDisabled(False)
		self.ui.statusLabel.setPixmap(self.readyIcon)
		self.ui.statusLabel.setToolTip("Ready")
		self.movie.stop()
		# self.th1.quit()
		self.emit(SIGNAL("autoSave(QString)"), _fromUtf8('./playerconfig.ini'))
		
	def addMusicFromURL(self, url):
		newfile = AudioFile(url)
		self.allList.append(newfile)
		lst = [QStandardItem(''), \
				QStandardItem(newfile.getFilePath().replace(QRegExp('.*/'), '')), \
				QStandardItem(''), QStandardItem('')]
		self.model.appendRow(lst)

	def readM3U(self, file):
		global defaultcode
		df = open(file.toUtf8().data().decode('utf-8'), 'rb')
		code = chardet.detect(df.read())['encoding']
		df.close()
	
		file = QFile(file)
		file.open(QFile.ReadOnly)
		r1 = QRegExp("^#.*")
		r2 = QRegExp("^(\r)?\n.*")
		r3 = QRegExp("^[a-zA-Z]:.*")
		r4 = QRegExp("^[a-zA-Z]+://.*")
		lst = []
		while(not file.atEnd()):
			line = _fromUtf8(file.readLine().data().decode(code))
			if (not r1.exactMatch(line) and not r2.exactMatch(line)):
				if r3.exactMatch(line):
					lst.append(line.trimmed())
				elif r4.exactMatch(line):
					lst.append(line.trimmed())
		file.close()
		return lst

	def readLyric(self, name):
		global defaultcode
		df = open(name.toUtf8().data().decode('utf-8'), 'r+')
		code = chardet.detect(df.read())['encoding']
		df.close()

		lrc = QFile(name)
		lrc.open(QFile.ReadOnly)
		r1 = re.compile("\[(\d{2}:\d{2}(.\d+)?)\]")
		r2 = re.compile("\[\d+:+.+\](.*)")
		r3 = re.compile("\[offset:(-?\d+)\]")
		item = []
		lrc_lst = []
		offset = 0
		while(not lrc.atEnd()):
			line = lrc.readLine()
			offsetline = r3.findall(line)
			if offsetline:
				offset = offsetline[0]
				continue
			times = r1.findall(line)
			lrc_words = r2.findall(line)
			if lrc_words:
				lrc_words = lrc_words[0]
			else:
				lrc_words = []
				
			if len(lrc_words) and lrc_words[0].rstrip():
				for i in times:
					item.append(QString(i[0]))
					try:
						if QString(code).toLower().contains('utf-8'):
							item.append(QString().fromUtf8(lrc_words.data().decode(code)).trimmed())
						elif QString(code).toLower().contains('ascii'):
							item.append(QString(lrc_words).trimmed())
						else:
							item.append(QString().fromUtf8(lrc_words.data().decode(defaultcode)).trimmed())
					except:
						item.append(QString().fromUtf8(lrc_words).trimmed())
						
					lrc_lst.append(item)
					item = []
		lrc.close()
		lrc_lst.sort()
		return lrc_lst, offset
	
	def findLyric(self):
		finded = QFileInfo()
		curIndex = self.getCurrentIndex()
		playingFile = QFileInfo(self.mediaObj.currentSource().fileName())
		folder = QDir(playingFile.absolutePath())
		folder.setNameFilters(QStringList(['*.lrc']))
		for file in folder.entryInfoList():
			lyc_name = file.baseName().toLower()
			playing_name = playingFile.baseName().toLower()
			title = self.allList[curIndex].getTitleOnly()
			if lyc_name.contains(playing_name) or lyc_name.contains(title.toLower()):
				finded = file
		return finded
							
	def initialUI(self):
		self.ui.shuffle.setToolTip("Shuffle")
		self.ui.repeat.setToolTip("Repeat All")
		self.ui.repeat1.setToolTip("Single Cycle")
		self.ui.play.setToolTip("Play")
		self.ui.next.setToolTip("Next")
		self.ui.previous.setToolTip("Previous")
		self.ui.stop.setToolTip("Stop")
		self.ui.add.setToolTip("Add files")
		self.ui.delete.setToolTip("Delete")
		self.ui.delete_2.setToolTip("Remove")
		self.ui.search.setToolTip("Search")
		self.ui.save.setToolTip("Save as playlist")
		self.ui.save_2.setToolTip("Save as playlist")
		self.ui.volume.setToolTip("Volume")
		self.ui.showOnDesk.setToolTip("Show On Desktop")
				
		self.ui.appName.setStyleSheet(_fromUtf8("font-family: Verdana; font-size: 15px; font-weight: bold; color: white"))		
		self.ui.playTime.setStyleSheet(_fromUtf8("font-family: Verdana; color: white"))
		self.ui.currentTime.setStyleSheet(_fromUtf8("font-family: Verdana; color: white"))
		
		self.ui.label_1.setPixmap(QtGui.QPixmap(":/icons/appicon.png"))
		self.ui.add.loadPixmap(":/icons/add.png")
		self.ui.delete.loadPixmap(":/icons/delete.png")
		self.ui.save.loadPixmap(":/icons/save.png")
		self.ui.search.loadPixmap(":/icons/search.png")
		self.ui.save_2.loadPixmap(":/icons/save.png")
		self.ui.delete_2.loadPixmap(":/icons/delete.png")
		self.ui.miniBt.loadPixmap(":/icons/mini.png")
		self.ui.closeBt.loadPixmap(":/icons/close.png")	
		self.ui.showOnDesk.loadPixmap(":/icons/lyricsetting.png")	
		self.pixmap = QtGui.QPixmap(":/icons/button24.png")
		self.s1r = QtGui.QPixmap(":/icons/rs_16h.png")
		self.volumeIcon = QtGui.QPixmap(_fromUtf8(":/icons/volume.png"))
		self.volumePixmap = self.volumeIcon.copy(0, 60, 80, 20)		
		self.readyIcon = QtGui.QPixmap(":/icons/ready.png")
		self.ui.statusLabel.setPixmap(self.readyIcon)	
		self.movie = QtGui.QMovie(QString(':/icons/loading.gif'), QByteArray())
		self.movie.setCacheMode(QMovie.CacheAll)
		self.movie.setSpeed(100)
		
		self.ui.volume.loadPixmap(self.volumePixmap)
		self.ui.previous.loadPixmap(self.pixmap.copy(0, 0, 34, 144))
		self.ui.play.loadPixmap(self.pixmap.copy(34, 0, 30, 144))
		self.ui.stop.loadPixmap(self.pixmap.copy(64, 0, 30, 144))		
		self.ui.next.loadPixmap(self.pixmap.copy(94, 0, 34, 144))
		self.ui.shuffle.loadPixmap(self.s1r.copy(0, 0, 30, 96))
		self.ui.repeat1.loadPixmap(self.s1r.copy(30, 0, 25, 96))
		self.ui.repeat.loadPixmap(self.s1r.copy(55, 0, 30, 96))
			
	def initialTable(self):
		# -- All Music table --
		self.model = QStandardItemModel()
		self.model.setColumnCount(5)
		self.model.setHorizontalHeaderItem(0, QStandardItem(""))
		self.model.setHorizontalHeaderItem(1, QStandardItem("Name"))
		self.model.setHorizontalHeaderItem(2, QStandardItem("Time"))
		self.model.setHorizontalHeaderItem(3, QStandardItem("Bitrate"))
		self.model.setHorizontalHeaderItem(4, QStandardItem("Favorite"))
		self.ui.tableView.setModel(self.model)
		self.ui.tableView.setColumnWidth(0, 7)
		self.ui.tableView.setColumnWidth(2, 40)
		self.ui.tableView.setColumnWidth(3, 0)
		self.ui.tableView.setColumnWidth(4, 15)
		self.ui.tableView.setShowGrid(False)
		self.ui.tableView.setWordWrap(False)
		self.ui.tableView.setMouseTracking(True)
		self.ui.tableView.horizontalHeader().setResizeMode(0, QHeaderView.Fixed)
		self.ui.tableView.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
		self.ui.tableView.horizontalHeader().setResizeMode(2, QHeaderView.Fixed)
		self.ui.tableView.horizontalHeader().setResizeMode(3, QHeaderView.Fixed)
		self.ui.tableView.horizontalHeader().setResizeMode(4, QHeaderView.Fixed)
		self.ui.tableView.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
		self.ui.tableView.verticalHeader().setClickable(True)
		self.ui.tableView.verticalHeader().setAlternatingRowColors(True)
		self.ui.tableView.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
		self.ui.tableView.horizontalHeader().setClickable(False)
		self.ui.tableView.horizontalHeader().hide()
		self.ui.tableView.verticalHeader().setDefaultSectionSize(15)
		self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.ui.tableView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.tableView.setTabKeyNavigation(False)
		self.ui.tableView.setFocusPolicy(Qt.NoFocus)
		self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.model.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
		self.ui.tableView.resizeRowsToContents()   
		self.ui.tableView.setAlternatingRowColors(True)


		# -- My Favorite table --
		self.model_2 = QStandardItemModel()
		self.model_2.setColumnCount(5)
		self.model_2.setHorizontalHeaderItem(0, QStandardItem(""))
		self.model_2.setHorizontalHeaderItem(1, QStandardItem("Name"))
		self.model_2.setHorizontalHeaderItem(2, QStandardItem("Time"))
		self.model_2.setHorizontalHeaderItem(3, QStandardItem("Bitrate"))
		self.model_2.setHorizontalHeaderItem(4, QStandardItem("Favorite"))
		self.ui.tableView_2.setModel(self.model_2)
		self.ui.tableView_2.setColumnWidth(0, 7)
		self.ui.tableView_2.setColumnWidth(2, 40)
		self.ui.tableView_2.setColumnWidth(3, 0)
		self.ui.tableView_2.setColumnWidth(4, 15)
		self.ui.tableView_2.setShowGrid(False)
		self.ui.tableView_2.setWordWrap(False)
		self.ui.tableView_2.setMouseTracking(True)
		self.ui.tableView_2.horizontalHeader().setResizeMode(0, QHeaderView.Fixed)
		self.ui.tableView_2.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
		self.ui.tableView_2.horizontalHeader().setResizeMode(2, QHeaderView.Fixed)
		self.ui.tableView_2.horizontalHeader().setResizeMode(3, QHeaderView.Fixed)
		self.ui.tableView_2.horizontalHeader().setResizeMode(4, QHeaderView.Fixed)
		self.ui.tableView_2.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
		self.ui.tableView_2.verticalHeader().setClickable(True)
		self.ui.tableView_2.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
		self.ui.tableView_2.horizontalHeader().setClickable(False)
		self.ui.tableView_2.horizontalHeader().hide()
		self.ui.tableView_2.verticalHeader().setDefaultSectionSize(15)
		self.ui.tableView_2.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.ui.tableView_2.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.tableView_2.setTabKeyNavigation(False)
		self.ui.tableView_2.setFocusPolicy(Qt.NoFocus)
		self.ui.tableView_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.model_2.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
		self.ui.tableView_2.resizeRowsToContents()   
		self.ui.tableView_2.setAlternatingRowColors(True)
							
	def fileChanged(self):		
		index = self.getCurrentIndex()
		self.current = index
		if self.playingTab:
			time = self.model_2.item(index, 2).text()
			name = self.model_2.item(index, 1).text()
			bitrate =  self.model_2.item(index, 3).text()
		else:
			if self.model.rowCount() != len(self.allList):			
				time = self.allList[index].getTime()
				name = self.allList[index].getTitle()			
				bitrate = self.allList[index].getBitrate()
			else:
				time = self.model.item(index, 2).text()	
				name = self.model.item(index, 1).text()			
				bitrate = self.model.item(index, 3).text()			
		self.ui.playTime.setText(time)
		totalTime = QTime().fromString(time, 'mm:ss')
		self.ui.seekSlider.setRange(0, QTime().msecsTo(totalTime))
		
		self.setPos()
		self.ui.musicName.setText(name+' - '+bitrate)	
		self.name.setText(name)
		self.name.setToolTip(name)	
		
	def stateChanged(self, new, old):
		if new == phonon.Phonon.PlayingState:
			self.ui.play.status = 2
			self.ui.play.update()
			self.previousmbt.setDisabled(False)
			self.nextmbt.setDisabled(False)
			self.playmbt.loadPixmap(QPixmap(":/icons/stop.png"))
			self.playmbt.update()
			self.playmbt.setText("Stop")
			self.playmbt.setToolTip("Stop")
			
			self.clearLyric()
			self.stopLyric()
				
			if self.mediaObj.currentSource().type() == 0:
				lrc = self.findLyric()
				self.lyricExists = lrc.exists()
				if self.lyricExists:					
					self.lrc_lst, self.offset = self.readLyric(lrc.filePath())
					curIndex = self.getCurrentIndex()
					self.lyric_ui.setText(self.playList[curIndex].getTitle())
					lyc = QString()
					for item in self.lrc_lst:
						lyc.append(item[1]+'\n')
					self.ui.textEdit.setText(QString(''), QString(''), QString(''), lyc)
					self.lyric_ui_scroll.setText(QString(''), QString(''), QString(''), lyc)
			
					
		elif new == phonon.Phonon.StoppedState:
			self.previousmbt.setDisabled(True)
			self.nextmbt.setDisabled(True)
			self.playmbt.loadPixmap(QPixmap(":/icons/play.png"))
			self.playmbt.update()
			self.playmbt.setText("Play")
			self.playmbt.setToolTip("Play")
			self.ui.currentTime.setText("00:00")
			self.resetSlider()
		
		elif new == phonon.Phonon.ErrorState:
			if not self.model.rowCount():
				return
			if not self.model_2.rowCount() and self.playingTab:
				return
			
			index = self.getCurrentIndex()	
			msg = invalidFileMsg(self)
			if self.allList[index].getType() == 0:
				msg.setLabelText(self.allList[index].getFilePath().replace('/', '\\'))
			else:
				msg.setLabelText(self.allList[index].getFilePath())
				
			if not self.playingTab:
				self.model.item(index, 0).setForeground((QBrush(QColor(255, 0, 0))))
				self.model.item(index, 1).setForeground((QBrush(QColor(255, 0, 0))))
				self.model.item(index, 2).setForeground((QBrush(QColor(255, 0, 0))))
				if self.allList[index] in self.favList:
					indexFav = self.favList.index(self.allList[index])
					self.model_2.item(indexFav, 0).setForeground((QBrush(QColor(255, 0, 0))))
					self.model_2.item(indexFav, 1).setForeground((QBrush(QColor(255, 0, 0))))
					self.model_2.item(indexFav, 2).setForeground((QBrush(QColor(255, 0, 0))))
			else:
				self.model_2.item(index, 0).setForeground((QBrush(QColor(255, 0, 0))))
				self.model_2.item(index, 1).setForeground((QBrush(QColor(255, 0, 0))))
				self.model_2.item(index, 2).setForeground((QBrush(QColor(255, 0, 0))))				
				indexAll = self.allList.index(self.favList[index])
				self.model.item(indexAll, 0).setForeground((QBrush(QColor(255, 0, 0))))
				self.model.item(indexAll, 1).setForeground((QBrush(QColor(255, 0, 0))))
				self.model.item(indexAll, 2).setForeground((QBrush(QColor(255, 0, 0))))
			self.showNormal()
			self.show()
			msg.show()
					
	def setCurrentTime(self, time):  
		self.ui.seekSlider.setValue(time)
		t = QTime().addMSecs(time).addMSecs(int(self.offset))
		self.ui.currentTime.setText(t.toString("mm:ss"))
		lycF = QString()
		lycL = QString()
		lycM = QString()
		if self.lyricExists:
			lenOfLrc = len(self.lrc_lst)
			for i in xrange(lenOfLrc):
				if self.lrc_lst[i][0].contains(t.toString("mm:ss")):					
					t1 = t
					if i < lenOfLrc - 1:
						t1 = QTime().fromString(self.lrc_lst[i+1][0].replace(QRegExp('[\[\]]'), ''), 'mm:ss.z')
						intervel = t.msecsTo(t1)
					else:
						t1 = QTime().fromString('00:10.99')
						intervel = 3000
						self.stopLyric()
					self.lyric_ui.stopMask()
					self.lyric_ui.setText(self.lrc_lst[i][1], intervel)				
					self.lyric_ui.startMask()
					if i > 0:
						lycM = self.lrc_lst[i-1][1]
					j = 0
					while(j < i-1):
						lycF.append(self.lrc_lst[j][1]+'\n')
						j += 1
					j = i
					while(j < lenOfLrc - 1):
						lycL.append(self.lrc_lst[j+1][1]+'\n')
						j += 1
					self.ui.textEdit.setText(lycF, lycM, self.lrc_lst[i][1], lycL, intervel)
					self.lyric_ui_scroll.setText(lycF, lycM, self.lrc_lst[i][1], lycL, intervel)
					break

	def clearLyric(self):
		self.lyric_ui.setText(_fromUtf8('Lyric Show.'))
		self.ui.textEdit.setText(QString(''), QString(''), QString('Lyric Show.'), QString(''))
		self.lyric_ui_scroll.setText(QString(''),  QString(''), QString('Lyric Show.'), QString(''))

	def stopLyric(self):
		self.lyric_ui.stopMask()
		self.ui.textEdit.stopScroll()
		self.lyric_ui_scroll.stopScroll()
		
	def exportIni(self, file):
		cfg = open(_toUtf8(file).data(), 'w+')
		cf = ConfigParser.ConfigParser()
		cf.add_section('Player')
		cf.add_section('Window')
		cf.add_section('Latest_list')
		cf.set('Player', 'path', _toUtf8(self.path).data())
		cf.set('Player', 'volume', self.audioSink.volume())
		cf.set('Player', 'muted', self.ui.volume.isChecked())
		cf.set('Player', 'shuffle', self.ui.shuffle.isChecked())
		cf.set('Player', 'repeat1', self.ui.repeat1.isChecked())
		cf.set('Player', 'repeat', self.ui.repeat.isChecked())
		if self.mediaObj.currentSource().type() != 4:
			cf.set('Player', 'pos', '['+str(self.playingTab)+','+str(self.getCurrentIndex())+']')
		favlst = []
		favlst = [self.allList.index(i) for i in self.favList]
	
		cf.set('Player', 'favorites', favlst)	
		cf.set('Window', 'x', self.pos().x())
		cf.set('Window', 'y', self.pos().y())
		cf.set('Window', 'width', self.rect().width())
		cf.set('Window', 'height', self.rect().height())

		if len(self.allList) != 0:
			list = []
			for song in self.allList:
				list.append(_toUtf8(song.getFilePath()).data())
			cf.set('Latest_list', 'list', list)
			
		cf.write(cfg)
		cfg.close()

	def importIni(self, file):
		try:
			self.playingTab = 0
			cf = ConfigParser.ConfigParser()
			cf.read(_toUtf8(file).data())
			self.path = _fromUtf8(cf.get('Player', 'path'))
			self.audioSink.setVolume(cf.getfloat('Player', 'volume'))
			if cf.getboolean('Player', 'muted'):
				self.muteClicked()	
			self.ui.shuffle.setChecked(not cf.getboolean('Player', 'shuffle'))					
			self.ui.repeat1.setChecked(not cf.getboolean('Player', 'repeat1'))
			self.ui.repeat.setChecked(not cf.getboolean('Player', 'repeat'))
			self.singleRepeatOn()
			self.repeatOn()
			self.randomOn()
			self.resize(cf.getint('Window', 'width'), cf.getint('Window', 'height'))
			self.move(cf.getint('Window', 'x'), cf.getint('Window', 'y'))
			self.favlst = eval(cf.get('Player', 'favorites'))
			if cf.has_option('Player', 'pos'):	
				self.playingTab = int(eval(cf.get('Player', 'pos'))[0])
				self.current = int(eval(cf.get('Player', 'pos'))[1])
				if self.playingTab:
					self.playList = self.favList
				else:
					self.playList = self.allList
			qlist = QStringList()
			if cf.has_option('Latest_list', 'list'):
				list = eval(cf.get('Latest_list', 'list'))
				qlist = [ QString.fromUtf8(song) for song in list ]
				self.addMusic(qlist, self.favlst)
				self.ui.tabWidget.setCurrentIndex(self.playingTab)
			else:
				self.emit(SIGNAL("loadCompleted()"))
				
		except:
			reminder = QWidget()
			reminder.setWindowIcon(QIcon(':/appicon.png'))
			QMessageBox.warning(reminder,'Warning', 'Bad config file.', QMessageBox.Ok)
			self.emit(SIGNAL("loadCompleted()"))
		
	def isInTitle(self, xPos, yPos):
		return yPos <= 25 and not (yPos <= 22 and (self.ui.closeBt.pos().x() + self.ui.closeBt.width() > xPos > self.ui.miniBt.pos().x()))
			
	def isTop(self, yPos):
		return 0 <= yPos <= self.border			
	
	def isBottom(self, yPos):
		return self.height() >= yPos >= self.height() - self.border	

	def isLeft(self, xPos):
		return  0 <= xPos <= self.border	
		
	def isRight(self, xPos):
		return self.width() >= xPos >= self.width() - self.border	
		
	def isTopLeft(self, xPos, yPos):
		return (0 <= xPos <= self.border) and (0 <= yPos <= self.border)	
	
	def isTopRight(self, xPos, yPos):
		return (xPos <= self.width() and xPos >= self.width() - self.border) and (yPos >= 0 and yPos <= self.border)
	
	def isBottomLeft(self, xPos, yPos):
		return (yPos <= self.height() and yPos >= self.height() - self.border) and (xPos >= 0 and xPos <= self.border)
	
	def isBottomRight(self, xPos, yPos):
		return (yPos <= self.height() and yPos >= self.height() - self.border) and (xPos <= self.width() and xPos >= self.width() - self.border)
		
	def closeEvent(self, event):
		if self.movie.state() == 0:
			self.emit(SIGNAL("autoSave(QString)"), _fromUtf8('./playerconfig.ini'))
		event.accept()	
				
	def dragEnterEvent(self, event):
		if len(event.mimeData().urls()):
			self.dragFilesList = []
			self.dragFilesList = [ file.toLocalFile() for file in event.mimeData().urls() ]
			event.accept()
			
	def dropEvent(self, event):
		self.emit(SIGNAL("addMusic(QStringList)"), self.dragFilesList)		

	def appendRow(self, obj):
		self.allList.append(obj)
		row = [QStandardItem(""), \
				QStandardItem(self.allList[-1].getTitle()), \
				QStandardItem(self.allList[-1].getTime()), \
				QStandardItem(self.allList[-1].getBitrate()), \
				QStandardItem(QIcon(":/icons/unfavorite.png"),"0")]
		self.model.appendRow(row)
		curIndex = self.model.rowCount()-1
		self.model.item(curIndex, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
				
	def appendFav(self, i):
		self.favList.append(self.allList[i])
		row = [QStandardItem(""), \
				QStandardItem(self.model.item(i, 1)), \
				QStandardItem(self.model.item(i, 2)), \
				QStandardItem(self.model.item(i, 3)), \
				QStandardItem(QIcon(":/icons/favorite.png"),"1")]
		self.model_2.appendRow(row)	
		curIndex = self.model_2.rowCount() - 1
		self.model_2.item(curIndex, 1).setForeground((QBrush(QColor(0, 0, 0))))
		self.model_2.item(curIndex, 2).setForeground((QBrush(QColor(0, 0, 0))))
		self.model_2.item(curIndex, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
		self.model.setItem(i, 4, QStandardItem(QIcon(":/icons/favorite.png"),"1"))

	def keyPressEvent(self, event):
		if event.modifiers() == Qt.ControlModifier:
			if event.key() == Qt.Key_A:
				if self.ui.tabWidget.currentIndex():
					selectModel = self.ui.tableView_2.selectionModel()	
					rowCount = self.model_2.rowCount()
					columnCount = self.model_2.columnCount()
					selectModel.select(QItemSelection(self.model_2.index(0, 0),self.model_2.index(rowCount-1, columnCount-1)),  QItemSelectionModel.Select)
				else:
					selectModel = self.ui.tableView.selectionModel()
					rowCount = self.model.rowCount()
					columnCount = self.model.columnCount()
					selectModel.select(QItemSelection(self.model.index(0, 0),self.model.index(rowCount-1, columnCount-1)),  QItemSelectionModel.Select)
			elif event.key() == Qt.Key_S:
				self.addToPlayList()				
			elif event.key() == Qt.Key_O:
				self.addMusic()

	def getCurrentIndex(self):
		src = self.mediaObj.currentSource()
		if src.type() == 4:
			return -1
		for i in xrange(len(self.playList)):
			if self.playList[i].src == src:
				return i
		return -1
								
class AudioFile(object):
	def __init__(self, fileName):
		self.file = QFileInfo(fileName)
		self.title = QString()
		self.artist = QString()
		self.time = QString()
		self.bitrate = QString()
		self.isFavorite = False
		self.src = None
		self.audioInfo(self.file)
		
	def isFavorited(self):
		return self.isFavorite
		
	def setFavorite(self, bool):
		self.isFavorite = bool
	
	def suffix(self):
		return self.file.suffix().toLower()

	def getTitle(self):
		if self.artist:
			return self.title + ' - ' + self.artist
		else:
			return self.title

	def getTitleOnly(self):
		return self.title
		
	def getArtist(self):
		return self.artist
		
	def getTime(self):
		return self.time
		
	def getBitrate(self):
		return self.bitrate
		
	def getFileName(self):
		return self.file.fileName()
	
	def getFilePath(self):
		return self.file.filePath()
		
	def getBaseName(self):
		return self.file.baseName()

	def getType(self):	
		return self.getMediaSource().type()
		
	def getMediaSource(self):
		if self.src:
			return  self.src
		else:
			self.src = Phonon.MediaSource(self.file.filePath())
			return self.src
		
	def getStringCode(self, s):
		global defaultcode
		try:
			code = chardet.detect(s)['encoding']			
			if QString(s).toLower().contains('\\u'):
				s = s.decode('raw_unicode_escape')
			elif not code:
				s = s.decode(defaultcode)
			elif QString(code).toLower().contains('ascii'):
				s = s.decode(code)
			else:
				s = s.decode(defaultcode)
			return s
		except:
			s = s.decode('raw_unicode_escape')
			return s
	
	def audioInfo(self, file):
		title = self.getBaseName()
		artist = QString()
		time = QString()
		bitrate = QString()
		
		if self.getType() == 1:
			self.title = file.fileName()		
			return
			
		suffix = self.suffix()
		if suffix == 'mp3':
			audio = MP3(unicode(file.filePath().toUtf8().data(), 'utf-8'))						
			if audio.has_key('TIT2'):
				s = audio.tags.get('TIT2').text[0].encode('raw_unicode_escape')
				title = QString().fromUtf8(self.getStringCode(s))
			if audio.has_key('TPE1'):
				s = audio.tags.get('TPE1').text[0].encode('raw_unicode_escape')								
				artist = QString().fromUtf8(self.getStringCode(s))
			if audio.info.length:
				time = QTime().addSecs(audio.info.length).toString("mm:ss")
			if audio.info.bitrate:
				bitrate = QString(str(audio.info.bitrate/1000)+'kbps')
		elif suffix == 'wma':
			audio = ASF(unicode(file.filePath().toUtf8().data(), 'utf-8'))
			if audio.has_key('Title'):
				s = audio.tags.get('Title')[0].value.encode('raw_unicode_escape')
				title = QString().fromUtf8(self.getStringCode(s))
			if audio.has_key('Author'):
				s = audio.tags.get('Author')[0].value.encode('raw_unicode_escape')
				artist = QString().fromUtf8(self.getStringCode(s))		
			if audio.info.length:
				time = QTime().addSecs(audio.info.length).toString("mm:ss")
			if audio.info.bitrate:
				bitrate = QString(str(audio.info.bitrate/1000)+'kbps')
		self.title, self.artist, self.time, self.bitrate = title, artist, time, bitrate
						
class MyApplication(QApplication):
	
	def __init__(self, args):
		super(MyApplication, self).__init__(args)
	
	def GET_X_LPARAM(self, param):
		return param & 0xffff

	def GET_Y_LPARAM(self, param):
		return param >> 16
	
	def winEventFilter(self, msg):
		if msg.message == 0x84:
			form = self.activeWindow()
			if form:
				xPos = self.GET_X_LPARAM(msg.lParam) - form.frameGeometry().x()
				yPos = self.GET_Y_LPARAM(msg.lParam) - form.frameGeometry().y()
				self.desktop = QDesktopWidget()
				self.desktopSize = QDesktopWidget.availableGeometry(self.desktop).size()				
				if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isTopLeft') and form.isTopLeft(xPos, yPos):
					return True, 0xD
				if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isTopRight') and form.isTopRight(xPos, yPos):
					return True, 0xE			
				if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isBottomLeft') and form.isBottomLeft(xPos, yPos):
					return True, 0x10				
				if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isBottomRight') and form.isBottomRight(xPos, yPos):
					return True, 0x11				
				if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isLeft') and form.isLeft(xPos):
					return True, 0xA								
				if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isRight') and form.isRight(xPos):
					return True, 0xB				
				if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isTop') and form.isTop(yPos):
					return True, 0xC
				if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isBottom') and form.isBottom(yPos):
					return True, 0xF
				if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isInTitle') and form.isInTitle(xPos, yPos):
					return True, 0x2	
		
		elif msg.message == 0xA3:
			pass
		return False, 0		
		
class myThread(QtCore.QThread):
	def __init__(self, ui, fileList, favList=None):
		QtCore.QThread.__init__(self)
		self.ui = ui
		self.audioFiles = fileList
		self.favlst = favList
					
	def run(self):
		try:			
			self.file = QFileInfo()
			self.file.setFile(self.audioFiles[0])
			self.ui.path = self.file.absolutePath()	
			lenOfAudio = QString(str(len(self.audioFiles)))
			if self.file.suffix().toLower() in self.ui.fileType:
				for i in xrange(len(self.audioFiles)):
					newfile = AudioFile(self.audioFiles[i])				
					self.emit(SIGNAL("appendrow(PyQt_PyObject)"), newfile)		
					self.ui.emit(SIGNAL("progress(QString)"), QString(str(i+1))+ "/" +lenOfAudio)

			elif self.file.suffix().toLower() == "m3u":
				for m in self.audioFiles:
					lst = self.ui.readM3U(m)
					lenOfLst = QString(str(len(lst)))
					for i in xrange(len(lst)):
						newfile = AudioFile(lst[i])
						self.emit(SIGNAL("appendrow(PyQt_PyObject)"), newfile)	
						self.ui.emit(SIGNAL("progress(QString)"), QString(str(i+1))+ "/" +lenOfLst)						
			if self.favlst:
				for i in self.favlst:
					self.emit(SIGNAL("appendfav(int)"), i)
						
			self.ui.emit(SIGNAL("loadCompleted()"))
			
		except Exception,e:
			self.ui.emit(QtCore.SIGNAL("err(QString)"), _fromUtf8(e.message.capitalize()))
			self.ui.emit(QtCore.SIGNAL("loadCompleted()"))
		
if __name__ == "__main__":
    app = MyApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())
