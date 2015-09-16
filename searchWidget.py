# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'float_ui.ui'
#
# Created: Fri Jul 03 10:52:42 2015
#	  by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import images

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

class float_ui(QtGui.QDialog):
	def __init__(self, parent=None):
		super(float_ui, self).__init__(parent)
		self.setObjectName(_fromUtf8("Dialog"))
		# self.resize(470, 35)
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
		self.setWindowOpacity(0.95)
		self.verticalLayout = QtGui.QVBoxLayout(self)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setMargin(0)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.setStyleSheet("background:#E1E8EF;")
		self.frame_2 = QtGui.QFrame(self)
		self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
		self.frame_2.setFrameShadow(QtGui.QFrame.Plain)
		self.frame_2.setLineWidth(1)
		self.frame_2.setObjectName(_fromUtf8("frame_2"))
		self.frame_2.setWindowOpacity(0.5)
		self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_2)
		self.horizontalLayout_5.setSpacing(0)
		self.horizontalLayout_5.setMargin(5)
		self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
		self.label = QtGui.QLabel(self.frame_2)
		self.label.setMinimumSize(QtCore.QSize(25, 25))
		self.label.setMaximumSize(QtCore.QSize(22, 25))
		self.label.setStyleSheet(_fromUtf8("background-color: white;"
											"border:2px solid gray;"
											"border-top-left-radius:10px;"
											"border-bottom-left-radius:10px;"
											"padding:2px 2px;"
											"border-right: none; "
											"border-color:#BDCCDC;"))
		self.label.setText(_fromUtf8(""))
		self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/search24.png")))
		self.label.setObjectName(_fromUtf8("label"))
		self.horizontalLayout_5.addWidget(self.label)
		self.lineEdit = myLineEdit(self.frame_2)
		self.lineEdit.setMinimumSize(QtCore.QSize(0, 25))
		self.lineEdit.setSizeIncrement(QtCore.QSize(0, 24))
		self.lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.label.setFocus()
		self.lineEdit.setStyleSheet(_fromUtf8("QLineEdit {"
												"background-color: white;"
												"border:2px solid gray;"
												"padding:2px 4px; "
												"border-left: none;"
												"border-right: none;"
												"border-color:#BDCCDC;"
												"}"
												))
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		self.horizontalLayout_5.addWidget(self.lineEdit)
		self.label_2 = myLabel(self.frame_2)
		self.label_2.setMinimumSize(QtCore.QSize(25, 25))
		self.label_2.setMaximumSize(QtCore.QSize(25, 25))
		self.label_2.setStyleSheet(_fromUtf8("background-color: white;"
												"border:2px solid gray;"
												"border-top-right-radius:10px;"
												"border-bottom-right-radius:10px;"
												"padding:2px 2px;"
												"border-color:#BDCCDC;"
												"border-left:none;"
												"color: silver;"))
		self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_2.setFont(QtGui.QFont("verdana, thoma", 8))
		self.horizontalLayout_5.addWidget(self.label_2)
		self.verticalLayout.addWidget(self.frame_2)

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)
		
		self.connect(self.parent(), QtCore.SIGNAL("parentMoved(QPoint)"), self.newPos)
		self.connect(self.parent(), QtCore.SIGNAL("parentResized(QSize)"), self.newSize)
		self.connect(self.label_2, QtCore.SIGNAL("clear()"), self.clearText)
		self.connect(self.lineEdit, QtCore.SIGNAL("getfocus()"), self.addxicon)
		self.connect(self.lineEdit, QtCore.SIGNAL("losefocus()"), self.delxicon)
		
	def retranslateUi(self):
		self.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.lineEdit.setText(_translate("Dialog", "Type keywords to search...", None))
		self.label_2.setText(_translate("Dialog", "", None))
	
	def newPos(self, p):
		self.move(self.pos().x() + p.x(), self.pos().y() + p.y())

	def newSize(self, s):
		self.resize(self.parent().width()-12, 35)
		self.move(self.pos().x(), self.pos().y() + s.height())	
	
	def clearText(self):
		if self.lineEdit.palette().color(QtGui.QPalette.Text).red() != 150:
			self.lineEdit.clear()
	
	def addxicon(self):
		self.label_2.setText("x")	
	
	def delxicon(self):
		self.label_2.setText("")
			
class myLabel(QtGui.QLabel):
	def __init__(self, parent=None):
		super(myLabel, self).__init__(parent)	

	def mousePressEvent(self, event):
		self.emit(QtCore.SIGNAL("clear()"))
		
class myLineEdit(QtGui.QLineEdit):
	def __init__(self, parent=None):
		super(myLineEdit, self).__init__(parent)		
		self.font = QtGui.QFont("verdana, thoma", 8)
		self.font.setItalic(True)
		self.setFont(self.font)
		self.color = QtGui.QPalette()
		self.color.setColor(QtGui.QPalette.Text, QtGui.QColor(150, 150, 150, 255))
		self.setPalette(self.color)
		self.setFocusPolicy(QtCore.Qt.ClickFocus)
		
	def focusInEvent(self, event):
		if self.palette().color(QtGui.QPalette.Text).red() == 150:
			self.color.setColor(QtGui.QPalette.Text, QtGui.QColor(0, 0, 0, 255))
			self.font.setItalic(False)
			self.setPalette(self.color)
			self.setFont(self.font)
			self.clear()
			self.emit(QtCore.SIGNAL("getfocus()"))
		
	def focusOutEvent(self, event):
		if not self.text():	
			self.color.setColor(QtGui.QPalette.Text, QtGui.QColor(150, 150, 150, 255))
			self.font.setItalic(True)
			self.setPalette(self.color)
			self.setFont(self.font)
			self.setText(_translate("Dialog", "Type keywords to search...", None))
			self.parent().setFocus()
			self.emit(QtCore.SIGNAL("losefocus()"))
			
	def rst(self):
		self.color.setColor(QtGui.QPalette.Text, QtGui.QColor(150, 150, 150, 255))
		self.font.setItalic(True)
		self.setPalette(self.color)
		self.setFont(self.font)
		self.setText(_translate("Dialog", "Type keywords to search...", None))
		self.parent().setFocus()
		self.emit(QtCore.SIGNAL("losefocus()"))
