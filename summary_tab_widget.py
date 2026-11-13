import datetime
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton,
    QVBoxLayout, QDialog
)
from PySide6.QtCore import Qt
from aggregate import AggregateData
from database import DataBase
from dateutil.relativedelta import relativedelta
from piechart import PieChart
from summary_subwin import SummarySubWindow


class SummaryTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.aggregate_num = AggregateData()
        self.current_date = datetime.date.today()
        self.data = DataBase()
        self.pie_chart = PieChart()
        self.setLayout(self.create_summary_tab())

    @property
    def set_date(self):
        print(f'now:{self.current_date}')
        return self.current_date

    def create_summary_tab(self):
        summary_tab_layout = QVBoxLayout()
        # Set Data to piechart
        self.set_chart()
        # Add each widget to main layout
        summary_tab_layout.addLayout(self.create_year_month_widget())
        summary_tab_layout.addWidget(self.create_monthly_balance_widget())
        summary_tab_layout.addWidget(self.pie_chart)
        summary_tab_layout.addLayout(self.create_setting_widget())
        summary_tab_layout.setSpacing(10)

        return summary_tab_layout

    def create_year_month_widget(self):
        year_month_box = QHBoxLayout()
        # Set month label widget
        prev_button = QPushButton('prev')
        prev_button.setFixedWidth(40)
        prev_button.clicked.connect(self.prev_button_clicked)
        self.year_month_label = QLabel()
        self.year_month_label.setFixedWidth(60)
        self.year_month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        next_button = QPushButton('next')
        next_button.setFixedWidth(40)
        # Set process for when next button is clicked
        next_button.clicked.connect(self.next_button_clicked)
        # Set widget to month layout
        year_month_box.addWidget(prev_button)
        year_month_box.addWidget(self.year_month_label)
        year_month_box.addWidget(next_button)
        self.set_year_month_label()

        return year_month_box

    def create_monthly_balance_widget(self):
        monthly_balance_layout = QGridLayout()
        # Set summary data widget
        income_label = QLabel('収入:')
        income_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.income = QLabel()
        self.income.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.income.setFixedWidth(80)
        expense_label = QLabel('支出:')
        expense_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expense = QLabel()
        self.expense.setFixedWidth(80)
        self.expense.setAlignment(Qt.AlignmentFlag.AlignRight)
        balance_label = QLabel('収支:')
        balance_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.balance = QLabel()
        self.balance.setFixedWidth(80)
        self.balance.setAlignment(Qt.AlignmentFlag.AlignRight)
        budget_label = QLabel('予算:')
        budget_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.budget = QLabel()
        self.budget.setFixedWidth(80)
        self.budget.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Set widget to layout
        monthly_balance_layout.addWidget(income_label, 0, 0)
        monthly_balance_layout.addWidget(self.income, 0, 1)
        monthly_balance_layout.addWidget(balance_label, 0, 2)
        monthly_balance_layout.addWidget(self.balance, 0, 3)
        monthly_balance_layout.addWidget(expense_label, 1, 0)
        monthly_balance_layout.addWidget(self.expense)
        monthly_balance_layout.addWidget(budget_label, 1, 2)
        monthly_balance_layout.addWidget(self.budget, 1, 3)
        monthly_balance_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter
        )
        monthly_balance_layout.setSpacing(30)
        # Set balance data
        self.set_balance_label()
        # Set layout to groupbox
        monthly_balance_groupbox = QGroupBox('Monthly Balance')
        monthly_balance_groupbox.setLayout(monthly_balance_layout)

        return monthly_balance_groupbox

    def set_year_month_label(self):
        # Convert datetime data to String
        year_month = self.current_date.strftime('%Y.%m')
        # Set string as current month
        self.year_month_label.setText(f'{year_month}')

    def set_balance_label(self):
        # Get aggregated data
        income_sum = self.aggregate_num.monthly_sum(self.current_date, '収入')
        expense_sum = self.aggregate_num.monthly_sum(self.current_date, '支出')
        balance_sum = self.aggregate_num.difference(income_sum, expense_sum)
        # Set aggregated data to UI
        self.income.setText(f'{income_sum}')
        self.expense.setText(f'{expense_sum}')
        if balance_sum == 0:
            self.balance.setText(f'+- {0}')
        elif balance_sum > 0:
            self.balance.setText(f'+ {balance_sum}')
        else:
            self.balance.setText(f'{balance_sum}')
        self.set_budget_label()

    def set_budget_label(self):
        budget_sum = self.aggregate_num.monthly_budget_sum(
            self.current_date.year, self.current_date.month
        )
        # Set default number to lineedit if budget table is empty
        year_month = self.current_date.strftime('%Y-%m')
        budget_count = self.data.fetch_query(
                'SELECT COUNT(*) FROM budget WHERE year_month=?', (year_month,)
            ).fetchone()[0]
        if budget_count == 0:
            self.budget.setText(f'{0}')
        else:
            # Set data to lineedit if budget table exists
            self.budget.setText(f'{budget_sum}')

    def prev_button_clicked(self):
        # Replace current day to first day of the month
        first = self.current_date.replace(day=1)
        # Get the day before the first day
        self.current_date = first - datetime.timedelta(days=1)
        # Update data
        self.set_year_month_label()
        self.set_balance_label()
        self.set_chart()

    def next_button_clicked(self):
        # Replace current day to first day of the month
        first = self.current_date.replace(day=1)
        # Get 32 days after the first day
        self.current_date = first + relativedelta(months=1)
        # Update data
        self.set_year_month_label()
        self.set_balance_label()
        self.set_chart()

    def set_chart(self):
        # Get balance sum for each category
        category_sum = self.aggregate_num.monthly_category_sum(
            self.current_date, '支出'
        )
        # Convert dataframe to dictionary
        category_dict = category_sum.to_dict()
        # Set default data if month has no data
        empty_dict = {}
        if category_dict == empty_dict:
            category_dict = {'No data': 0}
        # Append dictionary data to pie graph
        self.pie_chart.append_data(category_dict)

    def create_setting_widget(self):
        setting_layout = QHBoxLayout()
        # Set month label widget
        setting_button = QPushButton('Setting')
        setting_button.setFixedWidth(70)
        setting_button.clicked.connect(self.setting_button_clicked)
        setting_layout.addWidget(setting_button)
        setting_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        return setting_layout

    def subwin_result(self):
        subwin = SummarySubWindow(self.current_date)
        # Return input data if QDialog is accepted to close
        if subwin.exec() == QDialog.DialogCode.Accepted:
            res = subwin.result_text
            return res
        else:
            return None

    def setting_button_clicked(self):
        budget_sum = self.subwin_result()
        if budget_sum is not None:
            self.set_budget_label()
        else:
            return
