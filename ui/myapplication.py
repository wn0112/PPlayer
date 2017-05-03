# -*- coding: utf-8 -*-
from PyQt4.QtGui import *

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