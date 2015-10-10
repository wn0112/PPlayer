# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading.ui'
#
# Created: Tue Jul 14 10:44:44 2015
#	  by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import images
from push_button import *

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class loading(QtGui.QDialog):
	def __init__(self, parent=None):
		super(loading, self).__init__(parent)
		self.setObjectName(_fromUtf8("loading"))
		self.resize(321, 209)
		self.setStyleSheet(_fromUtf8("background: #234775;"))
		self.setWindowModality(QtCore.Qt.ApplicationModal)
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)	
		self.verticalLayout = QtGui.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(5, 0, 5, 10)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.frame = QtGui.QFrame(self)
		self.frame.setMaximumSize(QtCore.QSize(16777215, 30))
		self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtGui.QFrame.Raised)
		self.frame.setObjectName(_fromUtf8("frame"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
		self.horizontalLayout.setSpacing(6)
		self.horizontalLayout.setMargin(0)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.min = PushButton(self.frame)
		self.min.setMaximumSize(QtCore.QSize(30, 16777215))
		self.min.setObjectName(_fromUtf8("min"))
		self.min.loadPixmap(":/icons/mini.png")
		self.horizontalLayout.addWidget(self.min)
		self.closeBt = PushButton(self.frame)
		self.closeBt.setMaximumSize(QtCore.QSize(30, 16777215))
		self.closeBt.setObjectName(_fromUtf8("closeBt"))
		self.closeBt.loadPixmap(":/icons/close.png")
		self.horizontalLayout.addWidget(self.closeBt)
		self.verticalLayout.addWidget(self.frame)
		self.label = QtGui.QLabel(self)
		self.label.setMinimumSize(QtCore.QSize(0, 150))
		self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Arial"))
		font.setPointSize(25)
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setStyleSheet(_fromUtf8("color: white;"))
		self.label.setObjectName(_fromUtf8("label"))
		self.verticalLayout.addWidget(self.label)
		spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem1)
		self.label_2 = QtGui.QLabel(self)
		self.label_2.setMaximumSize(QtCore.QSize(16777215, 25))
		self.label_3 = QtGui.QLabel(self)
		self.label_3.setMaximumSize(QtCore.QSize(16777215, 25))
		font = QtGui.QFont("verdana", 7)
		self.label_2.setFont(font)
		self.label_2.setStyleSheet(_fromUtf8("color: white;"))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_2.setAlignment(QtCore.Qt.AlignHCenter)
		self.label_3.setFont(font)
		self.label_3.setStyleSheet(_fromUtf8("color: white;"))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_3.setAlignment(QtCore.Qt.AlignHCenter)
		self.verticalLayout.addWidget(self.label_3)
		self.verticalLayout.addWidget(self.label_2)
		self.label_3.setText("--/--")
		self.movie = QtGui.QMovie(QtCore.QString('./icons/logo.gif'), QtCore.QByteArray())
		self.movie.setCacheMode(QtGui.QMovie.CacheAll)
		self.movie.setSpeed(100)
		self.label_2.setMovie(self.movie)

		self.movie.start()
		self.connect(self.min, QtCore.SIGNAL("clicked()"), self.showMinimized)
		self.connect(self.closeBt, QtCore.SIGNAL("clicked()"), self.closed)
		self.connect(self.parent(), QtCore.SIGNAL("loadCompleted()"), self.closeWhenCompleted)
		self.connect(self.parent(), QtCore.SIGNAL("progress(QString)"), self.showProgress)
		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)	
		
	def retranslateUi(self):
		self.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.min.setText(_translate("Dialog", "PushButton", None))
		self.min.setToolTip("Minimize")
		self.closeBt.setText(_translate("Dialog", "PushButton", None))
		self.closeBt.setToolTip("Close")
		# self.label.setText(_translate("Dialog", "Pinus Player", None))
		self.label.setPixmap(QtGui.QPixmap(":/icons/pinus.png"))

	def showProgress(self, s):
		self.label_3.setText(s)
		
	def closed(self):
		self.emit(QtCore.SIGNAL("loadingclosed()"))
		self.close()
		
	def closeWhenCompleted(self):
		self.parent().show()
		self.parent().trayIcon.show()
		self.close()
	