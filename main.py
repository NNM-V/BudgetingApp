import sys
import sqlite3
from tab_widget import TabWidget
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from dataBase import dataBase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window title
        self.setWindowTitle('空っぽな窓') 
        # Window size
        self.setGeometry(200, 200, 500, 600) 
        # Set tab
        self.tabs = TabWidget(self)
        self.setCentralWidget(self.tabs)
        self.show()

        data = dataBase()
        data.close()

if __name__ == '__main__':
    # Start app
    app = QApplication(sys.argv)  
    # Create instance
    window = MainWindow() 
    # Show mainwindow 
    window.show()  
    # Close app
    sys.exit(app.exec()) 