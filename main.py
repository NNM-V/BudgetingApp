import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from tab_widget import TabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window title
        self.setWindowTitle('家計簿')
        # Window size
        self.setGeometry(200, 200, 500, 600)
        # Set tab
        self.main_tabs = TabWidget(self)
        self.setCentralWidget(self.main_tabs)
        self.show()


if __name__ == '__main__':
    # Start app
    app = QApplication(sys.argv)
    # Create instance
    window = MainWindow()
    # Show mainwindow
    window.show()
    # Close app
    sys.exit(app.exec())
