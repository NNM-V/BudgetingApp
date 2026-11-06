import datetime
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtGraphs import *
from dateutil.relativedelta import relativedelta
from aggregate import AggregateData
from database import DataBase


class SummaryTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.today = datetime.date.today()
        self.aggregate_num = AggregateData()
        summary_tab = self.create_summary_tab()
        self.setLayout(summary_tab)
        self.setFixedHeight(200)

    def create_summary_tab(self):
        # Call widget
        year_month = self.create_year_month_widget()
        monthly_balance = self.create_monthly_balance_widget()
        # Add each widget to main layout
        summary_tab_layout = QGridLayout()
        summary_tab_layout.addLayout(
            year_month, 0, 0, 1, 1,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        summary_tab_layout.addWidget(
            monthly_balance, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        return summary_tab_layout

    def create_year_month_widget(self):
        # Set month label widget
        prev_button = QPushButton('prev')
        prev_button.setFixedWidth(40)
        prev_button.clicked.connect(self.prev_button_clicked)
        self.year_month_text = QLabel()
        self.year_month_text.setFixedWidth(60)
        self.year_month_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        next_button = QPushButton('next')
        next_button.setFixedWidth(40)
        # Set process for when next button is clicked
        next_button.clicked.connect(self.next_button_clicked)
        # Set widget to month layout
        year_month_box = QHBoxLayout()
        year_month_box.addWidget(prev_button)
        year_month_box.addWidget(self.year_month_text)
        year_month_box.addWidget(next_button)
        self.year_month_label(self.today)

        return year_month_box

    def create_monthly_balance_widget(self):
        # Set summary data widget
        income_label = QLabel('収入:')
        self.income_text = QLabel()
        self.income_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.income_text.setFixedWidth(80)
        expense_label = QLabel('支出:')
        self.expense_text = QLabel()
        self.expense_text.setFixedWidth(80)
        self.expense_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        balance_label = QLabel('収支:')
        self.balance_text = QLabel()
        self.balance_text.setFixedWidth(80)
        self.balance_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        budget_label = QLabel('予算:')
        self.budget_text = QLabel(f'{100000000.0}')
        self.budget_text.setFixedWidth(80)
        self.budget_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Set widget to data layout
        monthly_balance_layout = QGridLayout()
        monthly_balance_layout.addWidget(income_label, 0, 0)
        monthly_balance_layout.addWidget(self.income_text, 0, 1)
        monthly_balance_layout.addWidget(balance_label, 0, 2)
        monthly_balance_layout.addWidget(self.balance_text, 0, 3)
        monthly_balance_layout.addWidget(expense_label, 1, 0)
        monthly_balance_layout.addWidget(self.expense_text)
        monthly_balance_layout.addWidget(budget_label, 1, 2)
        monthly_balance_layout.addWidget(self.budget_text, 1, 3)
        monthly_balance_layout.setSpacing(30)
        self.balance_label(self.today)
        monthly_balance_groupbox = QGroupBox('Monthly Balance')
        monthly_balance_groupbox.setLayout(monthly_balance_layout)
        self.create_graph_widget(self.today)

        return monthly_balance_groupbox

    def year_month_label(self, year_month):
        year_month_str = year_month.strftime('%Y.%m')
        # Set current month
        self.year_month_text.setText(f'{year_month_str}')

    def balance_label(self, year_month):
        # Get aggregated data
        income_data = self.aggregate_num.monthly_sum(year_month, '収入')
        expense_data = self.aggregate_num.monthly_sum(year_month, '支出')
        balance_data = self.aggregate_num.difference(income_data, expense_data)
        # Set aggregated data to UI
        self.income_text.setText(f'{income_data}')
        self.expense_text.setText(f'{expense_data}')
        if balance_data == 0:
            self.balance_text.setText(f'+- {0}')
        elif balance_data > 0:
            self.balance_text.setText(f'+ {balance_data}')
        else:
            self.balance_text.setText(f'{balance_data}')

    def prev_button_clicked(self):
        # Replace current day to first day of the month
        first = self.today.replace(day=1)
        # Get the day before the first day
        self.today = first - datetime.timedelta(days=1)
        # Set string to label function
        self.year_month_label(self.today)
        self.balance_label(self.today)
        self.create_graph_widget(self.today)

    def next_button_clicked(self):
        # Replace current day to first day of the month
        first = self.today.replace(day=1)
        # Get 32 days after the first day
        #self.today = (first + datetime.timedelta(days=32)).replace(day=1)
        self.today = first + relativedelta(months=1)
        # Set string to label function
        self.year_month_label(self.today)
        self.balance_label(self.today)

    def create_graph_widget(self, year_month):
        category_dict = self.aggregate_num.monthly_category(year_month, '支出')
        print(category_dict)
        '''
        self.series = QPieSeries()
        for category, amount in category_dict.items():
            self.series.append(category, amount)
        '''