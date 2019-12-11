import sys
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
        self.setGeometry(300, 300, 500, 450)
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())