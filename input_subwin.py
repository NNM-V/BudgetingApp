from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QDialog
)


class InputSubWindow(QDialog):
    def __init__(self, balance=None, parent=None):
        super().__init__(parent)
        self.balance = balance
        self.setGeometry(300, 300, 200, 100)
        subwin = self.create_subwin_tab()
        self.setLayout(subwin)

    def create_subwin_tab(self):
        subwin_layout = QVBoxLayout()
        # Set label
        item_label = QLabel('Add Category:')
        # Set textbox
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText('type category')
        # Connect add_item_input to function
        self.item_input.textChanged.connect(self.text_changed)
        self.add_button = QPushButton("追加")
        self.add_button.setEnabled(False)
        # Set process for when add_item_button is clicked
        self.add_button.clicked.connect(self.add_button_clicked)
        # Add widget to layout
        subwin_layout.addWidget(item_label)
        subwin_layout.addWidget(self.item_input)
        subwin_layout.addWidget(self.add_button)

        return subwin_layout

    def text_changed(self, s):
        # Enable add_item_button when text is input
        if s:
            self.add_button.setEnabled(True)

    def add_button_clicked(self, balance):
        # Get input from QLineEdit
        self._res = self.item_input.text()
        # Accept dialog to close
        self.accept()

    @property
    def set_result(self):
        # Return text
        return self._res
