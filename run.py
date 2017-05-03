# -*- coding: utf-8 -*-
from ui import *

if __name__ == "__main__":
    app = MyApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())