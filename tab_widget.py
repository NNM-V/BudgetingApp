import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import*
from aggregate import AggregateData
from database import DataBase
from category_window import InputSubWindow
from my_proxystyle import MyProxyStyle


class TabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # Main　layout
        self.layout = QVBoxLayout()
        # Get current month from today's date
        today = datetime.date.today()
        self.current_month = today.month
        # Call database class
        self.data = DataBase()
        self.aggregate_num = AggregateData()
        # Tab layout
        self.tabs = QTabWidget()
        # Summary tab layout
        summary_tab = QWidget()
        summary_tab_layout = self.create_summary_tab()
        summary_tab.setLayout(summary_tab_layout)
        summary_tab.setFixedHeight(200)
        # Input tab layout
        input_tab = QWidget()
        input_tab_layout = self.create_input_tab()
        input_tab.setLayout(input_tab_layout)
        self.tabs.addTab(summary_tab, 'サマリー')
        self.tabs.addTab(input_tab, '入力')
        # Set process for when summary tab is clicked
        self.tabs.currentChanged.connect(self.summary_tab_clicked)
        # Set widget to layout
        self.layout.addWidget(self.tabs)
        # Set tab to layout
        self.setLayout(self.layout)

    def summary_tab_clicked(self):
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:
            self.create_label(self.current_month)
            self.prev_button.clearFocus()

    def create_summary_tab(self):
        # SummaryBox main layout
        summary_tab_layout = QGridLayout()
        # Set month label widget
        month_layout = QHBoxLayout()
        self.prev_button = QPushButton('prev')
        self.prev_button.setFixedWidth(40)
        self.prev_button.clicked.connect(self.prev_button_clicked)
        self.month_label = QLabel(str(self.current_month) + '月')
        self.month_label.setFixedWidth(30)
        next_button = QPushButton('next')
        next_button.setFixedWidth(40)
        # Set process for when next button is clicked
        next_button.clicked.connect(self.next_button_clicked)
        # Set widget to month layout
        month_layout.addWidget(
            self.prev_button, alignment=Qt.AlignmentFlag.AlignRight
        )
        month_layout.addWidget(
            self.month_label, alignment=Qt.AlignmentFlag.AlignRight
        )
        month_layout.addWidget(
            next_button, alignment=Qt.AlignmentFlag.AlignRight
        )
        # Set summary data widget
        data_layout = QGridLayout()
        income_label = QLabel('収入:')
        self.income_text = QLabel()
        expense_label = QLabel('支出:')
        self.expense_text = QLabel()
        balance_label = QLabel('収支:')
        self.balance_text = QLabel()
        budget_label = QLabel('予算:')
        self.budget_text = QLabel('0')
        # Set widget to data layout
        data_layout.addWidget(
            income_label, 0, 0, alignment=Qt.AlignmentFlag.AlignRight
        )
        data_layout.addWidget(
            self.income_text, 0, 1, alignment=Qt.AlignmentFlag.AlignRight
        )
        data_layout.addWidget(
            balance_label, 0, 2, alignment=Qt.AlignmentFlag.AlignRight
        )
        data_layout.addWidget(
            self.balance_text, 0, 3, alignment=Qt.AlignmentFlag.AlignRight
        )
        data_layout.addWidget(
            expense_label, 1, 0, alignment=Qt.AlignmentFlag.AlignRight
        )
        data_layout.addWidget(
            self.expense_text, 1, 1, alignment=Qt.AlignmentFlag.AlignRight
        )
        data_layout.addWidget(
            budget_label, 1, 2, alignment=Qt.AlignmentFlag.AlignRight
        )
        data_layout.addWidget(
            self.budget_text, 1, 3, alignment=Qt.AlignmentFlag.AlignRight
        )
        self.create_label(self.current_month)
        # Add each layout to main layout
        summary_tab_layout.addLayout(
            month_layout, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        summary_tab_layout.addLayout(
            data_layout, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        return summary_tab_layout

    def create_label(self, month):
        # Set current month
        self.month_label.setText(str(self.current_month) + '月')
        # Get aggregated data
        income_data = self.aggregate_num.income_sum(month)
        expense_data = self.aggregate_num.expense_sum(month)
        balance_data = self.aggregate_num.difference(income_data, expense_data)
        # Set aggregated data to UI
        self.income_text.setText(str(income_data))
        self.expense_text.setText(str(expense_data))
        if balance_data == 0:
            self.balance_text.setText('+-' + str(0))
        elif balance_data > 0:
            self.balance_text.setText('+' + str(balance_data))
        else:
            self.balance_text.setText(str(balance_data))

    def prev_button_clicked(self):
        # Get previous month from current month
        self.current_month = self.current_month-1
        # Get aggregated data
        self.create_label(self.current_month)

    def next_button_clicked(self):
        # Get next month from current month
        self.current_month = self.current_month+1
        # Get aggregated data
        self.create_label(self.current_month)

    def create_input_tab(self):
        # Main layout
        input_tab_layout = QVBoxLayout()
        expence_layout = self.create_input_widget('支出')
        input_layout = self.create_input_widget('収入')
        # Set tab
        tabs = QTabWidget()
        # Add layout to expense tab
        expense_tab = QWidget()
        expense_tab.setLayout(expence_layout)
        # Add layout to income tab
        income_tab = QWidget()
        income_tab.setLayout(input_layout)
        # Add tab to UI
        tabs.addTab(expense_tab, '支出')
        tabs.addTab(income_tab, '収入')
        input_tab_layout.addWidget(tabs)

        return input_tab_layout

    def create_input_widget(self, balance_text):
        # Get calendar widget
        date = self.create_calendar_widget()
        # Get item input widget and variable for text
        item_input, item_text = self.create_item_widget()
        # Get money input widget and variable for text
        money_input, money_text = self.create_money_widget()
        # Set value for the combobox from category database
        cursor = self.data.fetchQueryValue(
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
        cursor = self.data.fetchQuery('SELECT name FROM bank')
        bank_values = cursor.fetchall()
        # Get bank input widget and variable for text
        bank_input, bank_text = self.create_bank_widget(bank_values)
        # Set variable for bank text from balance
        if balance_text == '支出':
            self.bank_out_text = bank_text
        elif balance_text == '収入':
            self.bank_in_text = bank_text
        input_button = self.create_input_button()
        input_button.clicked.connect(
            lambda: self.input_button_clicked(
                date, item_text, money_text,
                category_text, bank_text, balance_text
            )
        )
        # Set widget to expence tab layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(date)
        input_layout.addLayout(item_input)
        input_layout.addLayout(money_input)
        input_layout.addLayout(category_input)
        input_layout.addLayout(bank_input)
        input_layout.addWidget(input_button)

        return input_layout

    def create_calendar_widget(self):
        # Set calendar view setting
        calendar = QCalendarWidget()
        calendar.setFirstDayOfWeek(Qt.DayOfWeek(1))
        calendar.setGridVisible(True)

        return calendar

    def create_item_widget(self):
        # Create item widget
        item_box = QHBoxLayout()
        item_label = QLabel('項目:')
        item_input = QLineEdit()
        item_input.setPlaceholderText('項目を入力')
        item_input.setFixedWidth(250)
        # Set widget to layout
        item_box.addWidget(item_label)
        item_box.addWidget(item_input, alignment=Qt.AlignmentFlag.AlignLeft)

        return item_box, item_input

    def create_money_widget(self):
        # Create money widget
        money_box = QHBoxLayout()
        money_label = QLabel('金額:')
        money_input = QLineEdit()
        # Set validation to check if input is a number
        validator = QIntValidator(self)
        money_input.setValidator(validator)
        money_input.setFixedWidth(250)
        # Set widget to layout
        money_box.addWidget(money_label)
        money_box.addWidget(money_input, alignment=Qt.AlignmentFlag.AlignLeft)

        return money_box, money_input

    def create_category_widget(self, values, balance):
        # Create category widget
        category_box = QHBoxLayout()
        category_label = QLabel('カテゴリー :')
        category_combo = self.set_combo_box(values)
        category_button = QPushButton("+")
        category_button.setFixedWidth(50)
        # Set process for when category_button is clicked
        category_button.clicked.connect(
            lambda: self.category_button_clicked(balance)
        )
        # Set widget to layout
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
        bank_box = QHBoxLayout()
        bank_label = QLabel('出入先:')
        bank_combo = QComboBox()
        bank_combo = self.set_combo_box(values)
        bank_button = QPushButton('+')
        bank_button.setFixedWidth(50)
        # Set process for when bank_button is clicked
        bank_button.clicked.connect(lambda: self.bank_button_clicked())
        # Set widget to layout
        bank_box.addWidget(bank_label, alignment=Qt.AlignmentFlag.AlignLeft)
        bank_box.addWidget(bank_combo, alignment=Qt.AlignmentFlag.AlignLeft)
        bank_box.addWidget(bank_button, alignment=Qt.AlignmentFlag.AlignLeft)

        return bank_box, bank_combo

    def set_combo_box(self, values):
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
            money = int(money_text.text())
        else:
            money = 0.00
        # Get category name from textbox and find the ID throgh database
        category = category_text.currentText()
        cursor = self.data.fetchQueryValue(
            'SELECT id FROM category WHERE name = ?', (category,)
        )
        category_id = cursor.fetchone()
        # Get bank name from textbox and find the ID throgh database
        bank = bank_text.currentText()
        cursor = self.data.fetchQueryValue(
            'SELECT id FROM bank WHERE name = ?', (bank,)
        )
        bank_id = cursor.fetchone()
        # Set expense as a value for balance
        balance = balance_text
        # Insert data into database
        self.data.exe_query(
            'INSERT INTO report(date, description, amount, category_id, bank_id, balance) VALUES(?,?,?,?,?,?)', (
                date, item, money, str(category_id[0]),
                str(bank_id[0]), balance
            )
        )
        # Clear out data from text box
        item_text.clear()
        money_text.clear()

    def category_button_clicked(self, balance):
        subwin = InputSubWindow(balance)
        if subwin.exec() == QDialog.DialogCode.Accepted:
            name = subwin.result_text
            self.data.exe_query(
                'INSERT INTO category(name, type) VALUES(?,?)', (name, balance)
            )
            last_row_id = self.data.last_row('SELECT id FROM category')
            cursor = self.data.fetchQueryValue(
                'SELECT name FROM category WHERE id = ?', (last_row_id,)
            )
            category_name = cursor.fetchone()
            if balance == '支出':
                self.combo_out_text.addItem(str(category_name[0]))
            elif balance == '収入':
                self.combo_in_text.addItem(str(category_name[0]))

    def bank_button_clicked(self):
        subwin = CategoryWindow()
        if subwin.exec() == QDialog.DialogCode.Accepted:
            name = subwin.result_text
            self.data.exe_query('INSERT INTO bank(name) VALUES(?)', (name,))
            last_row_id = self.data.last_row('SELECT id FROM category')
            cursor = self.data.fetchQueryValue(
                'SELECT name FROM bank WHERE id = ?', (last_row_id,)
            )
            bank_name = cursor.fetchone()
            self.bank_out_text.addItem(str(bank_name[0]))
            self.bank_in_text.addItem(str(bank_name[0]))
