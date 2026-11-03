from PyQt6.QtWidgets import *
from database import DataBase


class InputSubWindow(QDialog):
    def __init__(self, balance=None, parent=None):
        super().__init__(parent)
        self.balance = balance
        self.setGeometry(300, 300, 200, 100)
        self.data = DataBase()
        layout = QVBoxLayout()
        # Set input layout
        # Set label
        add_item_label = QLabel('カテゴリーを追加:')
        # Set textbox
        self.add_item_input = QLineEdit()
        self.add_item_input.setPlaceholderText('追加する項目を入力')
        # Connect add_item_input to function
        self.add_item_input.textChanged.connect(self.text_changed)
        self.add_item_button = QPushButton("追加")
        self.add_item_button.setEnabled(False)
        # Set process for when add_item_button is clicked
        self.add_item_button.clicked.connect(
            lambda: self.add_button_clicked(balance)
        )
        # Set widget to layout
        layout.addWidget(add_item_label)
        layout.addWidget(self.add_item_input)
        layout.addWidget(self.add_item_button)
        self.setLayout(layout)

    def text_changed(self, s):
        # Enable add_item_button when text is input
        if s:
            self.add_item_button.setEnabled(True)

    def add_button_clicked(self, balance):
        self._category_name = self.add_item_input.text()
        self.accept()

    @property
    def result_text(self):

        return self._category_name
