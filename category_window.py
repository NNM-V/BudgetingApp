from PyQt6.QtWidgets import *
from dataBase import dataBase

class categoryWindow(QDialog):
    def __init__(self,balance = None ,parent = None):
        super().__init__(parent)
        self.balance = balance
        self.setGeometry(300, 300, 200, 100)
        self.data = dataBase()
        layout = QVBoxLayout()
        addLabel = QLabel('カテゴリーを追加:')
        self.addInput = QLineEdit()
        self.addInput.setPlaceholderText('追加する項目を入力')
        self.addInput.textChanged.connect(self.textChanged)
        self.addButton = QPushButton("追加")
        self.addButton.setEnabled(False)
        self.addButton.clicked.connect(lambda: self.addButtonClicked(balance))
        layout.addWidget(addLabel)
        layout.addWidget(self.addInput)
        layout.addWidget(self.addButton)
        self.setLayout(layout)

    def textChanged(self, s):
        if s:
            self.addButton.setEnabled(True)

    def addButtonClicked(self, balance):
        self._categoryName = self.addInput.text()
        self.accept()

    @property
    def resultText(self):
        return self._categoryName
