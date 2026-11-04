from PyQt6.QtWidgets import *
from database import DataBase


class InputSubWindow(QDialog):
    def __init__(self, balance=None, parent=None):
        super().__init__(parent)
        self.balance = balance
        self.setGeometry(300, 300, 200, 100)
        self.data = DataBase()
        subwin = self.create_subwin_tab()
        self.setLayout(subwin)

    def create_subwin_tab(self):
        subwin_layout = QVBoxLayout()
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
        self.add_item_button.clicked.connect(self.add_button_clicked)
        # Set widget to layout
        subwin_layout.addWidget(add_item_label)
        subwin_layout.addWidget(self.add_item_input)
        subwin_layout.addWidget(self.add_item_button)

        return subwin_layout

    def text_changed(self, s):
        # Enable add_item_button when text is input
        if s:
            self.add_item_button.setEnabled(True)

    def add_button_clicked(self):
        input_text = self.add_item_input.text()
        print(input_text)
        self.data.exe_query(
            'INSERT INTO category(name, type) VALUES(?,?)', (
                input_text, self.balance
            )
        )
        cursor_last_row = self.data.fetchQuery(
            'SELECT id FROM category'
         )
        last_row_id = cursor_last_row.lastrowid
        cursor = self.data.fetchQuery(
            'SELECT name FROM category WHERE id = ?', (last_row_id,)
        )
        self._res = cursor.fetchone()
        print(self._res)
        self.accept()
        
    @property
    def result_text(self):

        return self._res

