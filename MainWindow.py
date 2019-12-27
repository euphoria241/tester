import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from Interface import Interface

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.interface = Interface()
        self.setCentralWidget(self.interface)
        self.setWindowTitle('Тесты Python')
        self.setFixedSize(600,500)
        # self.setGeometry(300, 300, 500, 450)
        self.show() 

if __name__ == '__main__':
    if os.name == "nt":  # if windows
        from PyQt5 import __file__
        pyqt_plugins = os.path.join(os.path.dirname(__file__), "Qt", "plugins")
        QApplication.addLibraryPath(pyqt_plugins)
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = pyqt_plugins
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())