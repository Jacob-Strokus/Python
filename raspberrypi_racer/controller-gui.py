from PySide2.QtWidgets import*
from PySide2.QtGui import*
from PySide2.QtWebEngineWidgets import*
from PySide2.QtCore import*
import sys
import keyboard
import time

class Window(QWidget):

    url = None
    view = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Racer 3")
        self.setGeometry (300,300,1080,720)
        self.setMinimumHeight(100)
        self.setMinimumWidth(100)
        self.createGridLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

    def createGridLayout(self):
        self.groupBox = QGroupBox("Racer 3")
        self.groupBox.setFont(QFont("Sanserif",13))
        gridLayout = QGridLayout()
        button = QPushButton("Exit", self)
        button.clicked.connect(self.exitButton)
        gridLayout.addWidget(button, 4, 0)
        self.view = QWebEngineView()
        self.view.load(QUrl(""))
        self.view.show
        gridLayout.addWidget(self.view, 0, 0)
        label = QLabel("Type address and press enter: ")
        gridLayout.addWidget(label, 1, 0)
        lineEdit = QLineEdit(self)
        lineEdit.returnPressed.connect(lambda: self.textBoxPressed(lineEdit.text()))
        gridLayout.addWidget(lineEdit, 2,0)
        button = QPushButton("Start", self)
        button.clicked.connect(self.startButton)
        gridLayout.addWidget(button, 3, 0)

        self.groupBox.setLayout(gridLayout)

    def exitButton(self):
        app.quit()

    def textBoxPressed(self, text):
        self.url = text
        self.view.load(QUrl(self.url))

    def startButton(self):
        while (True):
            if keyboard.is_pressed("a"):
                print("a")
            if keyboard.is_pressed("w"):
                print("w")
            if keyboard.is_pressed("d"):
                print("d")
            if keyboard.is_pressed("s"):
                print("s")
            if keyboard.is_pressed("x"):
                break
            time.sleep(0.1)




#url = input("Enter the web address:")
#print()

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()
sys.exit(0)
