# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from mybuttons import *
from xml.etree import ElementTree as ET
import images, ui


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
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.mainWidget = QFrame(self)
        self.mainWidget.setObjectName(_fromUtf8("dlgmainwidget"))
        self.layout.addWidget(self.mainWidget)
        self.verticalLayout = QVBoxLayout(self.mainWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.titleFrame = QFrame(self)
        self.titleFrame.setObjectName(_fromUtf8("titleframe"))
        self.titleFrame.setMaximumSize(QSize(16777215, 30))
        self.verticalLayout.addWidget(self.titleFrame, 0, Qt.AlignTop)
        self.horizontalLayout = QHBoxLayout(self.titleFrame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.iconLabel = QLabel(self.titleFrame)
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setMaximumSize(20, 20)
        self.horizontalLayout.addWidget(self.iconLabel)
        self.titleLabel = QLabel(self.titleFrame)
        self.titleLabel.setObjectName(_fromUtf8("title"))
        self.titleLabel.setMinimumSize(QSize(0, 20))
        self.titleLabel.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout.addWidget(self.titleLabel)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeBt = PushButton(self.titleFrame)
        self.closeBt.loadPixmap(":/icons/close.png")
        self.horizontalLayout.addWidget(self.closeBt)
        self.setFont(QFont(_fromUtf8('Tahoma')))
        self.contentFrame = QFrame(self)
        self.verticalLayout.addWidget(self.contentFrame)
        QMetaObject.connectSlotsByName(self)
        self.connect(self.closeBt, SIGNAL("clicked()"), self.close)
        self.setupUI()
        effect = QGraphicsDropShadowEffect(self.mainWidget)
        effect.setOffset(2)
        effect.setBlurRadius(5)
        self.mainWidget.setGraphicsEffect(effect)

    def setupUI(self):
        self.setTitleIcon(":/icons/appicon.png")
        self.setTitle("About")
        self.resize(280, 184)
        self.icon = QLabel(self)
        self.icon.setGeometry(QRect(20, 50, 70, 70))
        self.icon.setMinimumSize(QSize(70, 70))
        self.icon.setMaximumSize(QSize(70, 70))
        self.icon.setText(_fromUtf8(""))
        self.icon.setPixmap(QPixmap(_fromUtf8(":/icons/headset.png")))
        self.icon.setScaledContents(True)
        self.OK_Bt = QPushButton(self)
        self.OK_Bt.setGeometry(QRect(180, 145, 75, 23))
        self.OK_Bt.setObjectName(_fromUtf8("pushbt"))
        self.label_version = QLabel(self)
        self.label_version.setGeometry(QRect(110, 40, 131, 20))
        font = QFont()
        font.setBold(True)
        self.label_version.setFont(font)
        self.label_version.setObjectName(_fromUtf8("label_version"))
        self.label_year = QLabel(self)
        self.label_year.setGeometry(QRect(110, 70, 150, 16))
        self.label_author = QLabel(self)
        self.label_author.setGeometry(QRect(110, 96, 130, 20))
        self.label_email = QLabel(self)
        self.label_email.setGeometry(QRect(110, 110, 160, 20))
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
        return yPos <= 40 and not (yPos <= 22 and (xPos >= self.closeBt.pos().x() and xPos <= self.closeBt.pos().x() + 47))    

        
class openURL(about):
    def setupUI(self):
        try:
            if QtCore.QFile(ui.path + '/lang/'+self.parent().currentLang.toUtf8().data()+'.xml').exists():
                self.doc = ET.parse(ui.path + '/lang/'+self.parent().currentLang.toUtf8().data()+'.xml')
                title = _fromUtf8(self.doc.findall("./Message/OpenURLTitle")[0].text)
                okBt = self.doc.findall("./Message/Button/OK")[0].text
                cancelBt = self.doc.findall("./Message/Button/Cancel")[0].text
                browseBt = self.doc.findall("./Message/Button/Browse")[0].text
                urlInfo = self.doc.findall("./Message/URLInfo")[0].text
            else:
                title = QString("Open URL")
                okBt = QString("OK")
                cancelBt = QString("Cancel")
                browseBt = QString("Browse...")
                urlInfo = QString("Enter the URL or path to a media file on the Internet, your computer, or your network that you want to play.")
        except:
            title = QString("Open URL")
            okBt = QString("OK")
            cancelBt = QString("Cancel")
            browseBt = QString("Browse...")
            urlInfo = QString("Enter the URL or path to a media file on the Internet, your computer, or your network that you want to play.")
            
        self.setTitleIcon(":/icons/appicon.png")
        self.setTitle(title)
        self.resize(400, 140)
        self.contentVerticalLayout = QtGui.QVBoxLayout(self.contentFrame)
        self.contentVerticalLayout.setContentsMargins(10, 10, 10, 10)
        self.contentVerticalLayout.setSpacing(10)
        self.label = QtGui.QLabel(self.contentFrame)   
        self.label.setWordWrap(True)
        self.contentVerticalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QComboBox(self.contentFrame)
        self.lineEdit.setFocus()
        self.lineEdit.setEditable(True)
        self.lineEdit.addItems(self.parent().history)
        self.lineEdit.clearEditText()
        self.lineEdit.setFixedSize(380, 23)
        self.contentVerticalLayout.addWidget(self.lineEdit)
        self.btFrame = QtGui.QFrame(self.contentFrame)
        self.btFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.btFrame.setFrameShadow(QtGui.QFrame.Raised)

        self.btHorizontalLayout = QtGui.QHBoxLayout(self.btFrame)
        self.btHorizontalLayout.setObjectName(_fromUtf8("btHorizontalLayout"))
        self.btHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.btHorizontalLayout.addItem(spacerItem)
        self.ok = QtGui.QPushButton(self.btFrame)
        self.ok.setObjectName(_fromUtf8("pushbt"))

        self.ok.setFixedSize(75, 23)
        self.btHorizontalLayout.addWidget(self.ok)
        self.cancel = QtGui.QPushButton(self.btFrame)
        self.cancel.setObjectName(_fromUtf8("pushbt"))
     
        self.cancel.setFixedSize(75, 23)
        self.btHorizontalLayout.addWidget(self.cancel)
        self.browse = QtGui.QPushButton(self.btFrame)
        self.browse.setObjectName(_fromUtf8("pushbt"))

        self.browse.setFixedSize(75, 23)
        self.btHorizontalLayout.addWidget(self.browse)
        self.contentVerticalLayout.addWidget(self.btFrame)
                    
        self.label.setText(_translate("Dialog",urlInfo, None))
        self.ok.setText(_translate("Dialog", okBt, None))
        self.cancel.setText(_translate("Dialog", cancelBt, None))
        self.browse.setText(_translate("Dialog", browseBt, None))
        
        self.connect(self.cancel, SIGNAL("clicked()"), self.close)
        self.connect(self.browse, SIGNAL("clicked()"), self.clickBrowse)
        self.connect(self.ok, SIGNAL("clicked()"), self.clickOK)


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
            file = QString(url)
            if not file.isEmpty():
                self.parent().addMusicFromURL(file)
                if not url in self.parent().history:
                    self.parent().history.append(url)
                self.close()
            else:
                msg = promptMsg(self)
                msg.show()
                
class promptMsg(about):

    def setupUI(self):
        try:
            if QtCore.QFile(ui.path + '/lang/'+self.parent().parent().currentLang.toUtf8().data()+'.xml').exists():
                self.doc = ET.parse(ui.path + '/lang/'+self.parent().parent().currentLang.toUtf8().data()+'.xml')  
                title = _fromUtf8(self.doc.findall("./Message/PromMsgTitle")[0].text)
                info = _fromUtf8(self.doc.findall("./Message/InvalidURL")[0].text)
                okBt = _fromUtf8(self.doc.findall("./Message/Button/OK")[0].text)
            else:
                title = QString("Error")
                info = QString("Not a valid URL.")
                okBt = QString("OK")
        except:
            title = QString("Error")
            info = QString("Not a valid URL.")
            okBt = QString("OK")
            
        self.setTitleIcon(":/icons/appicon.png")
        self.setTitle(title)
        self.contentVerticalLayout = QtGui.QVBoxLayout(self.contentFrame)
        self.contentVerticalLayout.setContentsMargins(10, 10, 10, 10)
        self.contentVerticalLayout.setSpacing(10)
        self.label = QtGui.QLabel(self.contentFrame)
        self.label.setWordWrap(True)
        self.contentVerticalLayout.addWidget(self.label)
        
        self.label.setText(info)
        self.ok = QPushButton(self)
        self.ok.setObjectName(_fromUtf8("pushbt"))
        self.ok.setText(okBt)
        self.ok.setFixedSize(75, 23)
        self.contentVerticalLayout.addWidget(self.ok, 0, Qt.AlignRight)
            
        self.connect(self.ok, SIGNAL("clicked()"), self.close)

class invalidFileMsg(about):

    def setupUI(self):
        try:
            if QtCore.QFile(ui.path + '/lang/'+self.parent().currentLang.toUtf8().data()+'.xml').exists():
                self.doc = ET.parse(ui.path + '/lang/'+self.parent().currentLang.toUtf8().data()+'.xml')  
                title = _fromUtf8(self.doc.findall("./Message/InvalidFileTitle")[0].text)
                info = _fromUtf8(self.doc.findall("./Message/InvalidFileMsg")[0].text)
                okBt = _fromUtf8(self.doc.findall("./Message/Button/OK")[0].text)
            else:
                title = QString("Unrecognized files")
                info = QString("Failed to play following files:")
                okBt = QString("OK")
        except:
            title = QString("Unrecognized files")
            info = QString("Failed to play following files:")
            okBt = QString("OK")
            
        self.setTitleIcon(":/icons/appicon.png")
        self.setTitle(title)
        self.contentVerticalLayout = QtGui.QVBoxLayout(self.contentFrame)
        self.contentVerticalLayout.setContentsMargins(10, 10, 10, 10)
        self.contentVerticalLayout.setSpacing(10)
        self.label = QtGui.QLabel(self.contentFrame)
        self.label.setText(info)
        spacerItem = QtGui.QSpacerItem(20, 100, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.contentVerticalLayout.addWidget(self.label, 0, Qt.AlignTop)
        self.filesname = QtGui.QLabel(self.contentFrame)
        self.filesname.setText("")
        self.filesname.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.contentVerticalLayout.addWidget(self.filesname)
        self.ok = QPushButton(self)
        self.ok.setObjectName(_fromUtf8("pushbt"))
        self.ok.setText(okBt)
        self.ok.setFixedSize(75, 23)
        self.contentVerticalLayout.addWidget(self.ok, 0, Qt.AlignRight)
            
        self.connect(self.ok, SIGNAL("clicked()"), self.close)
    
    def setLabelText(self, s):
        self.filesname.setText(s)

class failToApplyLangMsg(about):
   
    def setupUI(self):
        title = QString("Error")
        info = QString("Fail to apply language file.")
        okBt = QString("OK")
        self.setTitleIcon(":/icons/appicon.png")
        self.setTitle(title)
        self.contentVerticalLayout = QtGui.QVBoxLayout(self.contentFrame)
        self.contentVerticalLayout.setContentsMargins(10, 10, 10, 10)
        self.contentVerticalLayout.setSpacing(10)
        self.label = QtGui.QLabel(self.contentFrame)
        self.label.setWordWrap(True)
        self.contentVerticalLayout.addWidget(self.label)
        
        self.label.setText(info)
        self.ok = QPushButton(self)
        self.ok.setObjectName(_fromUtf8("pushbt"))
        self.ok.setText(okBt)
        self.ok.setFixedSize(75, 23)
        self.contentVerticalLayout.addWidget(self.ok, 0, Qt.AlignRight)
            
        self.connect(self.ok, SIGNAL("clicked()"), self.close)