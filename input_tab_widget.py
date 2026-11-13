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
        self.setLayout(self.set_input_tab())

    def set_input_tab(self):
        # input main layout
        tab_layout = QVBoxLayout()
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
        tab_layout.addWidget(tabs)

        return tab_layout

    def create_input_tab(self, balance):
        input_tab_layout = QVBoxLayout()
        # Get calendar widget
        date = self.create_calendar_widget()
        # Get item input widget and variable for text
        item_layout, item_input = self.create_item_widget()
        # Get money input widget and variable for text
        money_layout, money_input = self.create_money_widget()
        # Set value for the combobox from category database
        category_names = self.data.fetch_query(
            'SELECT name FROM category WHERE type = ?', (balance,)
        ).fetchall()
        # Get category input widget and variable for text
        category_layout, category_combo = self.create_category_widget(
            category_names, balance
        )
        # Set variable for category text from balance
        if balance == '支出':
            self.expence_category_combo = category_combo
        elif balance == '収入':
            self.income_categoty_combo = category_combo
        # Set value for the combobox from bank database
        bank_names = self.data.fetch_query('SELECT name FROM bank').fetchall()
        # Get bank input widget and variable for text
        bank_layout, bank_combo = self.create_bank_widget(bank_names)
        # Set variable for bank text from balance
        if balance == '支出':
            self.expence_bank_combo = bank_combo
        elif balance == '収入':
            self.income_bank_combo = bank_combo
        # Get input button widget
        input_button = self.create_input_button()
        input_button.clicked.connect(
            lambda: self.input_button_clicked(
                date, item_input, money_input,
                category_combo, bank_combo, balance
            )
        )
        # Add each widget to main layout
        input_tab_layout.addWidget(date)
        input_tab_layout.addLayout(item_layout)
        input_tab_layout.addLayout(money_layout)
        input_tab_layout.addLayout(category_layout)
        input_tab_layout.addLayout(bank_layout)
        input_tab_layout.addWidget(input_button)

        return input_tab_layout

    def create_calendar_widget(self):
        # Set calendar view setting
        calendar = QCalendarWidget()
        calendar.setFirstDayOfWeek(Qt.DayOfWeek(1))
        calendar.setGridVisible(True)

        return calendar

    def create_item_widget(self):
        item_layout = QHBoxLayout()
        # Create item widget
        item_label = QLabel('項目:')
        item_input = QLineEdit()
        item_input.setPlaceholderText('項目を入力')
        item_input.setFixedWidth(250)
        # Set widget to layout
        item_layout.addWidget(item_label)
        item_layout.addWidget(item_input, alignment=Qt.AlignmentFlag.AlignLeft)

        return item_layout, item_input

    def create_money_widget(self):
        money_layout = QHBoxLayout()
        # Create money widget
        money_label = QLabel('金額:')
        money_input = QLineEdit()
        # Set validation to check if input is a number
        validator = QDoubleValidator()
        money_input.setValidator(validator)
        money_input.setFixedWidth(250)
        # Set widget to layout
        money_layout.addWidget(money_label)
        money_layout.addWidget(
            money_input, alignment=Qt.AlignmentFlag.AlignLeft
        )

        return money_layout, money_input

    def create_category_widget(self, values, balance):
        category_layout = QHBoxLayout()
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
        category_layout.addWidget(
            category_label, alignment=Qt.AlignmentFlag.AlignLeft
        )
        category_layout.addWidget(
            category_combo, alignment=Qt.AlignmentFlag.AlignLeft
        )
        category_layout.addWidget(
            category_button, alignment=Qt.AlignmentFlag.AlignLeft
        )

        return category_layout, category_combo

    def create_bank_widget(self, values):
        bank_layout = QHBoxLayout()
        # Set expense bank layout
        bank_label = QLabel('出入先:')
        bank_combo = QComboBox()
        bank_combo = self.set_combobox(values)
        bank_button = QPushButton('+')
        bank_button.setFixedWidth(50)
        # Set process for when bank_button is clicked
        bank_button.clicked.connect(self.bank_button_clicked)
        # Set widget to layout
        bank_layout.addWidget(bank_label, alignment=Qt.AlignmentFlag.AlignLeft)
        bank_layout.addWidget(bank_combo, alignment=Qt.AlignmentFlag.AlignLeft)
        bank_layout.addWidget(
            bank_button, alignment=Qt.AlignmentFlag.AlignLeft
        )

        return bank_layout, bank_combo

    def set_combobox(self, values):
        # Create combobox
        combo = QComboBox()
        # Set item in combo_box from values
        for value in values:
            combo.addItem(str(value[0]))
        combo.setFixedWidth(120)
        # Set max number of item to show at once
        combo.setMaxVisibleItems(6)
        # Set scrollbar
        combo.view().setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        # setMaxVisibleItems is ignored on Mac style
        # Set SH_ComboBox_Popup false
        style = MyProxyStyle()
        combo.setStyle(style)

        return combo

    def create_input_button(self):
        # Create record button
        record_button = QPushButton('記録')

        return record_button

    def input_button_clicked(
            self, calendar, item_input, money_input,
            category_input, bank_input, balance
    ):
        # Get data from calendar
        date = calendar.selectedDate().toString('yyyy-MM-dd')
        # Get item name from textbox
        item = item_input.text()
        # Get amount of money from textbox
        if money_input.text():
            money = float(money_input.text())
        else:
            money = 0.00
        # Get category name from textbox and find the ID throgh database
        category = category_input.currentText()
        category_id = self.data.fetch_query(
            'SELECT id FROM category WHERE name = ? AND type = ?', (
                category, balance
            )
        ).fetchone()
        # Get bank name from textbox and find the ID throgh database
        bank = bank_input.currentText()
        bank_id = self.data.fetch_query(
            'SELECT id FROM bank WHERE name = ?', (bank,)
        ).fetchone()
        # Insert data into database
        self.data.exe_query(
            'INSERT INTO report (date, category_id, description, \
            amount, bank_id, balance) VALUES(?,?,?,?,?,?)', (
                date, str(category_id[0]), item,
                money, str(bank_id[0]), balance
            )
        )
        # Clear out data from text box
        item_input.clear()
        money_input.clear()

    def subwin_result(self, balance=None):
        subwin = InputSubWindow(balance)
        # Return input data if QDialog is accepted to close
        if subwin.exec() == QDialog.DialogCode.Accepted:
            res = subwin.set_result
            return res
        else:
            return None

    def category_button_clicked(self, balance):
        category = self.subwin_result(balance)
        # Set input to combo box if input exists
        if category is not None:
            self.data.exe_query(
                'INSERT INTO category(name, type) VALUES(?,?)', (
                    category, balance
                )
            )
            if balance == '支出':
                self.expence_category_combo.addItem(category)
            elif balance == '収入':
                self.income_categoty_combo.addItem(category)
        else:
            return

    def bank_button_clicked(self):
        bank = self.subwin_result()
        # Set input to combo box if input exists
        if bank is not None:
            self.data.exe_query(
                'INSERT INTO bank(name) VALUES(?)', (bank,)
            )
            self.expence_bank_combo.addItem(bank)
            self.income_bank_combo.addItem(bank)
        else:
            return
