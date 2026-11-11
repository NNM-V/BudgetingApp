from PySide6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit,
    QCalendarWidget, QComboBox, QPushButton,
    QDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from input_subwin import InputSubWindow
from my_proxystyle import MyProxyStyle
from database import DataBase


class InputTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Call database class
        self.data = DataBase()
        # Set layout to tab_widget class
        input_tab = self.set_input_tab()
        self.setLayout(input_tab)

    def set_input_tab(self):
        # input main layout
        input_tab_layout = QVBoxLayout()
        expence_layout = self.create_input_tab('支出')
        input_layout = self.create_input_tab('収入')
        # Set tab
        tabs = QTabWidget()
        # Add layout to expense tab
        expense_tab = QWidget()
        expense_tab.setLayout(expence_layout)
        # Add layout to income tab
        income_tab = QWidget()
        income_tab.setLayout(input_layout)
        # Create tab
        tabs.addTab(expense_tab, '支出')
        tabs.addTab(income_tab, '収入')
        input_tab_layout.addWidget(tabs)

        return input_tab_layout

    def create_input_tab(self, balance_text):
        # Get calendar widget
        date = self.create_calendar_widget()
        # Get item input widget and variable for text
        item_input, item_text = self.create_item_widget()
        # Get money input widget and variable for text
        money_input, money_text = self.create_money_widget()
        # Set value for the combobox from category database
        cursor = self.data.fetch_query(
            'SELECT name FROM category WHERE type = ?', (balance_text,)
        )
        category_values = cursor.fetchall()
        # Get category input widget and variable for text
        category_input, category_text = self.create_category_widget(
            category_values, balance_text
        )
        # Set variable for category text from balance
        if balance_text == '支出':
            self.combo_out_text = category_text
        elif balance_text == '収入':
            self.combo_in_text = category_text
        # Set value for the combobox from bank database
        cursor = self.data.fetch_query('SELECT name FROM bank')
        bank_values = cursor.fetchall()
        # Get bank input widget and variable for text
        bank_input, bank_text = self.create_bank_widget(bank_values)
        # Set variable for bank text from balance
        if balance_text == '支出':
            self.bank_out_text = bank_text
        elif balance_text == '収入':
            self.bank_in_text = bank_text
        # Get input button widget
        input_button = self.create_input_button()
        input_button.clicked.connect(
            lambda: self.input_button_clicked(
                date, item_text, money_text,
                category_text, bank_text, balance_text
            )
        )
        # Add each widget to main layout
        input_tab_layout = QVBoxLayout()
        input_tab_layout.addWidget(date)
        input_tab_layout.addLayout(item_input)
        input_tab_layout.addLayout(money_input)
        input_tab_layout.addLayout(category_input)
        input_tab_layout.addLayout(bank_input)
        input_tab_layout.addWidget(input_button)

        return input_tab_layout

    def create_calendar_widget(self):
        # Set calendar view setting
        calendar = QCalendarWidget()
        calendar.setFirstDayOfWeek(Qt.DayOfWeek(1))
        calendar.setGridVisible(True)

        return calendar

    def create_item_widget(self):
        # Create item widget
        item_label = QLabel('項目:')
        item_input = QLineEdit()
        item_input.setPlaceholderText('項目を入力')
        item_input.setFixedWidth(250)
        # Set widget to layout
        item_box = QHBoxLayout()
        item_box.addWidget(item_label)
        item_box.addWidget(item_input, alignment=Qt.AlignmentFlag.AlignLeft)

        return item_box, item_input

    def create_money_widget(self):
        # Create money widget
        money_label = QLabel('金額:')
        money_input = QLineEdit()
        # Set validation to check if input is a number
        validator = QDoubleValidator()
        money_input.setValidator(validator)
        money_input.setFixedWidth(250)
        # Set widget to layout
        money_box = QHBoxLayout()
        money_box.addWidget(money_label)
        money_box.addWidget(money_input, alignment=Qt.AlignmentFlag.AlignLeft)

        return money_box, money_input

    def create_category_widget(self, values, balance):
        # Create category widget
        category_label = QLabel('カテゴリー :')
        category_combo = self.set_combobox(values)
        category_button = QPushButton("+")
        category_button.setFixedWidth(50)
        # Set process for when category_button is clicked
        category_button.clicked.connect(
            lambda: self.category_button_clicked(balance)
        )
        # Set widget to layout
        category_box = QHBoxLayout()
        category_box.addWidget(
            category_label, alignment=Qt.AlignmentFlag.AlignLeft
        )
        category_box.addWidget(
            category_combo, alignment=Qt.AlignmentFlag.AlignLeft
        )
        category_box.addWidget(
            category_button, alignment=Qt.AlignmentFlag.AlignLeft
        )

        return category_box, category_combo

    def create_bank_widget(self, values):
        # Set expense bank layout
        bank_label = QLabel('出入先:')
        bank_combo = QComboBox()
        bank_combo = self.set_combobox(values)
        bank_button = QPushButton('+')
        bank_button.setFixedWidth(50)
        # Set process for when bank_button is clicked
        bank_button.clicked.connect(self.bank_button_clicked)
        # Set widget to layout
        bank_box = QHBoxLayout()
        bank_box.addWidget(bank_label, alignment=Qt.AlignmentFlag.AlignLeft)
        bank_box.addWidget(bank_combo, alignment=Qt.AlignmentFlag.AlignLeft)
        bank_box.addWidget(bank_button, alignment=Qt.AlignmentFlag.AlignLeft)

        return bank_box, bank_combo

    def set_combobox(self, values):
        # Create combobox
        combo_box = QComboBox()
        # Set item in combo_box from values
        for value in values:
            combo_box.addItem(str(value[0]))
        combo_box.setFixedWidth(120)
        # Set max number of item to show at once
        combo_box.setMaxVisibleItems(6)
        # Set scrollbar
        combo_box.view().setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        # setMaxVisibleItems is ignored on Mac style
        # Set SH_ComboBox_Popup false
        style = MyProxyStyle()
        combo_box.setStyle(style)

        return combo_box

    def create_input_button(self):
        # Create record button
        record_button = QPushButton('記録')

        return record_button

    def input_button_clicked(
            self, calendar, item_text, money_text,
            category_text, bank_text, balance_text
    ):
        # Get data from calendar
        date = calendar.selectedDate().toString('yyyy-MM-dd')
        # Get item name from textbox
        item = item_text.text()
        # Get amount of money from textbox
        if money_text.text():
            money = float(money_text.text())
        else:
            money = 0.00
        # Get category name from textbox and find the ID throgh database
        category = category_text.currentText()
        cursor = self.data.fetch_query(
            'SELECT id FROM category WHERE name = ? AND type = ?', (
                category, balance_text
            )
        )
        category_id = cursor.fetchone()
        # Get bank name from textbox and find the ID throgh database
        bank = bank_text.currentText()
        cursor = self.data.fetch_query(
            'SELECT id FROM bank WHERE name = ?', (bank,)
        )
        bank_id = cursor.fetchone()
        # Set expense as a value for balance
        balance = balance_text
        # Insert data into database
        self.data.exe_query(
            'INSERT INTO report (date, description, amount, category_id, bank_id, balance) VALUES(?,?,?,?,?,?)', (
                date, item, money, str(category_id[0]),
                str(bank_id[0]), balance
            )
        )
        # Clear out data from text box
        item_text.clear()
        money_text.clear()

    def subwin_result(self, balance=None):
        subwin = InputSubWindow(balance)
        # Return input data if QDialog is accepted to close
        if subwin.exec() == QDialog.DialogCode.Accepted:
            res = subwin.result_text
            return res
        else:
            return None

    def category_button_clicked(self, balance):
        category_name = self.subwin_result(balance)
        # Set input to combo box if input exists
        if category_name is not None:
            self.data.exe_query(
                'INSERT INTO category(name, type) VALUES(?,?)', (
                    category_name, balance
                )
            )
            if balance == '支出':
                self.combo_out_text.addItem(category_name)
            elif balance == '収入':
                self.combo_in_text.addItem(category_name)
        else:
            return

    def bank_button_clicked(self):
        bank_name = self.subwin_result()
        # Set input to combo box if input exists
        if bank_name is not None:
            self.data.exe_query(
                'INSERT INTO bank(name) VALUES(?)', (bank_name,)
            )
            self.bank_out_text.addItem(bank_name)
            self.bank_in_text.addItem(bank_name)
        else:
            return
