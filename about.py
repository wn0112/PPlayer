from PyQt4.QtGui import *
from PyQt4.QtCore import *
from push_button import *
import images


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

		
class about(QDialog):
	def __init__(self, parent=None):
		super(about, self).__init__(parent)
		self.setStyleSheet("font: 11px verdana;")
		self.setObjectName(_fromUtf8("about"))
		self.setWindowModality(Qt.ApplicationModal)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Dialog)	
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setMargin(0)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)		
		self.titleFrame = QFrame(self)
		self.titleFrame.setMaximumSize(QSize(16777215, 30))
		self.titleFrame.setFrameShape(QFrame.NoFrame)
		self.titleFrame.setFrameShadow(QFrame.Raised)
		self.titleFrame.setObjectName(_fromUtf8("titleFrame"))
		self.verticalLayout.addWidget(self.titleFrame, 0, Qt.AlignTop)
		self.horizontalLayout = QHBoxLayout(self.titleFrame)
		self.horizontalLayout.setSpacing(0)
		self.horizontalLayout.setMargin(0)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.horizontalLayout.setContentsMargins(5, 5, 5, 0)
		self.iconLabel = QLabel(self.titleFrame)
		self.iconLabel.setObjectName(_fromUtf8("iconLabel"))
		self.iconLabel.setScaledContents(True)
		self.iconLabel.setMaximumSize(20, 20)
		self.horizontalLayout.addWidget(self.iconLabel)
		self.titleLabel = QLabel(self.titleFrame)
		self.titleLabel.setMinimumSize(QSize(0, 20))
		self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
		self.titleLabel.setContentsMargins(5, 0, 0, 0)
		self.horizontalLayout.addWidget(self.titleLabel)
		self.titleLabel.setStyleSheet(_fromUtf8("color: white; font-family:verdana; font-weight:bold;font-size:12px;"))
		spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.closeBt = PushButton(self.titleFrame)
		self.closeBt.setObjectName(_fromUtf8("closeBt"))
		self.closeBt.loadPixmap(":/icons/close.png")
		self.horizontalLayout.addWidget(self.closeBt)
		self.setFont(QFont(_fromUtf8('Tahoma')))
		self.contentFrame = QFrame(self)
		self.verticalLayout.addWidget(self.contentFrame)
		QMetaObject.connectSlotsByName(self)		
		self.connect(self.closeBt, SIGNAL("clicked()"), self.close)	
		self.setupUI()

	def setupUI(self):
		self.setTitleIcon(":/icons/appicon.png")
		self.setTitle("About")
		self.resize(280, 184)
		self.icon = QLabel(self)
		self.icon.setGeometry(QRect(20, 40, 70, 70))
		self.icon.setMinimumSize(QSize(70, 70))
		self.icon.setMaximumSize(QSize(70, 70))
		self.icon.setText(_fromUtf8(""))
		self.icon.setPixmap(QPixmap(_fromUtf8(":/icons/headset.png")))
		self.icon.setScaledContents(True)
		self.icon.setObjectName(_fromUtf8("icon"))
		self.OK_Bt = QPushButton(self)
		self.OK_Bt.setGeometry(QRect(180, 145, 75, 23))
		self.OK_Bt.setObjectName(_fromUtf8("OK_Bt"))
		self.OK_Bt.setStyleSheet("QPushButton{border:1px solid lightgray;background:transparent}}"
			"QPushButton:hover{border-color:#A9A9A9;background:transparent}"
			"QPushButton:hover:pressed{border:1px solid lightgray;background:rgb(230,230,230)")
		self.label_version = QLabel(self)
		self.label_version.setGeometry(QRect(110, 40, 131, 20))
		font = QFont()
		font.setBold(True)
		self.label_version.setFont(font)
		self.label_version.setObjectName(_fromUtf8("label_version"))
		self.label_version.setStyleSheet("font-family:verdana; font-weight:bold;font-size:12px;")
		self.label_year = QLabel(self)
		self.label_year.setGeometry(QRect(110, 70, 150, 16))
		self.label_year.setObjectName(_fromUtf8("label_year"))
		self.label_author = QLabel(self)
		self.label_author.setGeometry(QRect(110, 96, 130, 20))
		self.label_author.setObjectName(_fromUtf8("label_author"))
		self.label_email = QLabel(self)
		self.label_email.setGeometry(QRect(110, 110, 160, 20))
		self.label_email.setObjectName(_fromUtf8("label_email"))
		self.OK_Bt.setText(_translate("about", "OK", None))
		self.label_version.setText(_translate("about", "Pinus Player v1.2", None))
		self.label_year.setText(_translate("about", "PyQt4 application, 2015", None))
		self.label_author.setText(_translate("about", "Author: Andy Wen", None))
		self.label_email.setText(_translate("about", "Email: wn0112@gmail.com", None))
		self.connect(self.OK_Bt, SIGNAL("clicked()"), self.close)		
		self.connect(self.OK_Bt, SIGNAL("clicked()"), self.close)
		
	def setTitleIcon(self, str):
		self.iconLabel.setPixmap(QPixmap(str))
		
	def setTitle(self, str):
		self.titleLabel.setText(str)

	def isInTitle(self, xPos, yPos):
		return yPos <= 30 and not (yPos <= 22 and (xPos >= self.closeBt.pos().x() and xPos <= self.closeBt.pos().x() + 47))	

	def paintEvent(self, event):	
		linear = QLinearGradient(QPoint(self.rect().topLeft()), QPoint(self.rect().bottomLeft()))
		linear.start()
		linear.setColorAt(0, QColor(35, 71, 117, 255))
		linear.finalStop()
		
		self.painter = QPainter()
		self.painter.begin(self)
		self.painter.setBrush(linear)
		self.painter.drawRect(QRect(0, 0, self.width(), 30))
		self.painter.end()	

		linear2 = QLinearGradient(QPoint(self.rect().topLeft()), QPoint(self.rect().bottomLeft()))
		linear2.start()
		linear2.setColorAt(0, Qt.white)
		linear2.finalStop()
		
		self.painter2 = QPainter()
		self.painter2.begin(self)
		self.painter2.setBrush(linear2)
		self.painter2.drawRect(QRect(0, 30, self.width(), self.height() - 30));
		self.painter2.end()
		
		self.painter3 = QPainter()
		self.painter3.begin(self)
		self.painter3.setPen(Qt.gray)
		self.painter3.drawPolyline(QPointF(0, 0), QPointF(0, self.height() - 1), QPointF(self.width() - 1, self.height() - 1), QPointF(self.width() - 1, 0))
		self.painter3.drawPolyline(QPointF(0, 0), QPointF(self.width() - 1, 0))
		self.painter3.end()		
		
class openURL(about):
	def __init__(self, parent=None):
		super(openURL, self).__init__(parent)

	def setupUI(self):
		self.setTitleIcon(":/icons/appicon.png")
		self.setTitle("Open URL")
		self.resize(400, 140)
		self.contentVerticalLayout = QtGui.QVBoxLayout(self.contentFrame)
		self.contentVerticalLayout.setObjectName(_fromUtf8("contentVerticalLayout"))
		self.contentVerticalLayout.setContentsMargins(10, 0, 10, 10)
		self.contentVerticalLayout.setSpacing(10)
		self.label = QtGui.QLabel(self.contentFrame)
		self.label.setObjectName(_fromUtf8("label"))
		
		self.label.setWordWrap(True)
		self.contentVerticalLayout.addWidget(self.label)
		self.lineEdit = QtGui.QComboBox(self.contentFrame)
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		self.lineEdit.setFocus()
		self.lineEdit.setEditable(True)
		self.lineEdit.addItems(self.parent().history)
		self.lineEdit.clearEditText()
		self.lineEdit.setFixedSize(380, 23)
		self.contentVerticalLayout.addWidget(self.lineEdit)
		self.btFrame = QtGui.QFrame(self.contentFrame)
		self.btFrame.setFrameShape(QtGui.QFrame.StyledPanel)
		self.btFrame.setFrameShadow(QtGui.QFrame.Raised)
		self.btFrame.setObjectName(_fromUtf8("btFrame"))
		
		self.btHorizontalLayout = QtGui.QHBoxLayout(self.btFrame)
		self.btHorizontalLayout.setObjectName(_fromUtf8("btHorizontalLayout"))
		self.btHorizontalLayout.setContentsMargins(0, 0, 0, 0)
		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.btHorizontalLayout.addItem(spacerItem)
		self.ok = QtGui.QPushButton(self.btFrame)
		self.ok.setObjectName(_fromUtf8("ok"))
		self.ok.setStyleSheet("QPushButton{border:1px solid lightgray;background:transparent}}"
			"QPushButton:hover{border-color:#A9A9A9;background:transparent}"
			"QPushButton:hover:pressed{border:1px solid lightgray;background:rgb(230,230,230)")
		self.ok.setFixedSize(75, 23)
		self.btHorizontalLayout.addWidget(self.ok)
		self.cancel = QtGui.QPushButton(self.btFrame)
		self.cancel.setObjectName(_fromUtf8("cancel"))
		self.cancel.setStyleSheet("QPushButton{border:1px solid lightgray;background:transparent}}"
			"QPushButton:hover{border-color:#A9A9A9;background:transparent}"
			"QPushButton:hover:pressed{border:1px solid lightgray;background:rgb(230,230,230)")		
		self.cancel.setFixedSize(75, 23)
		self.btHorizontalLayout.addWidget(self.cancel)
		self.browse = QtGui.QPushButton(self.btFrame)
		self.browse.setObjectName(_fromUtf8("browse"))
		self.browse.setStyleSheet("QPushButton{border:1px solid lightgray;background:transparent}}"
			"QPushButton:hover{border-color:#A9A9A9;background:transparent}"
			"QPushButton:hover:pressed{border:1px solid lightgray;background:rgb(230,230,230)")
		self.browse.setFixedSize(75, 23)
		self.btHorizontalLayout.addWidget(self.browse)
		self.contentVerticalLayout.addWidget(self.btFrame)
		self.retranslateUi()
		
		self.connect(self.cancel, SIGNAL("clicked()"), self.close)		
		self.connect(self.browse, SIGNAL("clicked()"), self.clickBrowse)		
		self.connect(self.ok, SIGNAL("clicked()"), self.clickOK)		

	def retranslateUi(self):
		self.label.setText(_translate("Dialog", "Enter the URL or path to a media file on the Internet, your computer, or your network that you want to play.", None))
		self.ok.setText(_translate("Dialog", "OK", None))
		self.cancel.setText(_translate("Dialog", "Cancel", None))
		self.browse.setText(_translate("Dialog", "Browse...", None))

	def clickBrowse(self):
		self.close()
		self.parent().addMusic()
		
	def clickOK(self):
		if not len(self.lineEdit.currentText()):
			msg = promptMsg(self)
			msg.show()
		else:
			lst = []
			url = self.lineEdit.currentText()
			file = QUrl(url)
			r1 = QRegExp('^http(s)?://.*')
			if file.isValid():				
				self.parent().addMusicFromURL(file)
				if not url in self.parent().history:
					self.parent().history.append(url)
				self.close()
			else:
				msg = promptMsg(self)
				msg.show()
				
class promptMsg(about):
	def __init__(self, parent=None):
		super(promptMsg, self).__init__(parent)
		
	def setupUI(self):
		self.setTitleIcon(":/icons/appicon.png")
		self.setTitle("Error")
		self.contentVerticalLayout = QtGui.QVBoxLayout(self.contentFrame)
		self.contentVerticalLayout.setObjectName(_fromUtf8("contentVerticalLayout"))
		self.contentVerticalLayout.setContentsMargins(10, 10, 10, 10)
		self.contentVerticalLayout.setSpacing(10)
		self.label = QtGui.QLabel(self.contentFrame)
		self.label.setObjectName(_fromUtf8("label"))		
		self.label.setWordWrap(True)
		self.contentVerticalLayout.addWidget(self.label)		
		self.label.setText("Not a valid URL.")
		self.ok = QPushButton(self)
		self.ok.setObjectName(_fromUtf8("ok"))
		self.ok.setText("OK")
		self.ok.setStyleSheet("QPushButton{border:1px solid lightgray;background:transparent}}"
			"QPushButton:hover{border-color:#A9A9A9;background:transparent}"
			"QPushButton:hover:pressed{border:1px solid lightgray;background:rgb(230,230,230)")
		self.ok.setFixedSize(75, 23)
		self.contentVerticalLayout.addWidget(self.ok, 0, Qt.AlignRight)	
			
		self.connect(self.ok, SIGNAL("clicked()"), self.close)

class invalidFileMsg(about):
	def __init__(self, parent=None):
		super(invalidFileMsg, self).__init__(parent)
		
	def setupUI(self):
		self.setTitleIcon(":/icons/appicon.png")
		self.setTitle("Unrecognized files")
		self.contentVerticalLayout = QtGui.QVBoxLayout(self.contentFrame)
		self.contentVerticalLayout.setObjectName(_fromUtf8("contentVerticalLayout"))
		self.contentVerticalLayout.setContentsMargins(10, 10, 10, 10)
		self.contentVerticalLayout.setSpacing(10)
		self.label = QtGui.QLabel(self.contentFrame)
		self.label.setObjectName(_fromUtf8("label"))		
		self.label.setText("Failed to play following files:")
		self.label.setStyleSheet("font-weight: bold;")
		spacerItem = QtGui.QSpacerItem(20, 100, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.contentVerticalLayout.addWidget(self.label, 0, Qt.AlignTop)	
		self.filesname = QtGui.QLabel(self.contentFrame)
		self.filesname.setObjectName(_fromUtf8("label"))		
		self.filesname.setText("")
		self.filesname.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.contentVerticalLayout.addWidget(self.filesname)		
		self.ok = QPushButton(self)
		self.ok.setObjectName(_fromUtf8("ok"))
		self.ok.setText("OK")
		self.ok.setStyleSheet("QPushButton{border:1px solid lightgray;background:transparent}}"
			"QPushButton:hover{border-color:#A9A9A9;background:transparent}"
			"QPushButton:hover:pressed{border:1px solid lightgray;background:rgb(230,230,230)")
		self.ok.setFixedSize(75, 23)
		self.contentVerticalLayout.addWidget(self.ok, 0, Qt.AlignRight)	
			
		self.connect(self.ok, SIGNAL("clicked()"), self.close)
	
	def setLabelText(self, s):
		self.filesname.setText(s)
