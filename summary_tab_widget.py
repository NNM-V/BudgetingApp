import datetime
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton, 
    QVBoxLayout, QDialog
)
from PySide6.QtCore import Qt
from dateutil.relativedelta import relativedelta
from aggregate import AggregateData
from piechart import PieChart
from summary_subwin import SummarySubWindow


class SummaryTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_date = datetime.date.today()
        self.pie_chart = PieChart()
        self.aggregate_num = AggregateData()
        summary_tab = self.create_summary_tab()
        self.setLayout(summary_tab)

    @property
    def set_date(self):
        print(f'now:{self.current_date}')
        return self.current_date

    def create_summary_tab(self):
        # Set Data to piechart
        self.set_chart()
        # Add each widget to main layout
        summary_tab_layout = QVBoxLayout()
        summary_tab_layout.addLayout(self.create_year_month_widget())
        summary_tab_layout.addWidget(self.create_monthly_balance_widget())
        summary_tab_layout.addWidget(self.pie_chart)
        summary_tab_layout.addLayout(self.create_setting_widget())
        summary_tab_layout.setSpacing(10)

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
        self.year_month_label()

        return year_month_box

    def create_monthly_balance_widget(self):
        # Set summary data widget
        income_label = QLabel('収入:')
        income_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.income_text = QLabel()
        self.income_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.income_text.setFixedWidth(80)
        expense_label = QLabel('支出:')
        expense_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expense_text = QLabel()
        self.expense_text.setFixedWidth(80)
        self.expense_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        balance_label = QLabel('収支:')
        balance_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.balance_text = QLabel()
        self.balance_text.setFixedWidth(80)
        self.balance_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        budget_label = QLabel('予算:')
        budget_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.budget_text = QLabel(f'{100000000.0}')
        self.budget_text.setFixedWidth(80)
        self.budget_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Set widget to layout
        monthly_balance_layout = QGridLayout()
        monthly_balance_layout.addWidget(income_label, 0, 0)
        monthly_balance_layout.addWidget(self.income_text, 0, 1)
        monthly_balance_layout.addWidget(balance_label, 0, 2)
        monthly_balance_layout.addWidget(self.balance_text, 0, 3)
        monthly_balance_layout.addWidget(expense_label, 1, 0)
        monthly_balance_layout.addWidget(self.expense_text)
        monthly_balance_layout.addWidget(budget_label, 1, 2)
        monthly_balance_layout.addWidget(self.budget_text, 1, 3)
        monthly_balance_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter
        )
        monthly_balance_layout.setSpacing(30)
        # Set balance data
        self.balance_label()
        # Set layout to groupbox
        monthly_balance_groupbox = QGroupBox('Monthly Balance')
        monthly_balance_groupbox.setLayout(monthly_balance_layout)

        return monthly_balance_groupbox

    def year_month_label(self):
        # Convert datetime data to String
        year_month_str = self.current_date.strftime('%Y.%m')
        # Set string as current month
        self.year_month_text.setText(f'{year_month_str}')

    def balance_label(self):
        # Get aggregated data
        income_data = self.aggregate_num.monthly_sum(self.current_date, '収入')
        expense_data = self.aggregate_num.monthly_sum(self.current_date, '支出')
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
        first = self.current_date.replace(day=1)
        # Get the day before the first day
        self.current_date = first - datetime.timedelta(days=1)
        # Set string to label function
        self.year_month_label()
        self.balance_label()
        # Update data for pie chart
        self.set_chart()

    def next_button_clicked(self):
        # Replace current day to first day of the month
        first = self.current_date.replace(day=1)
        # Get 32 days after the first day
        # self.current_date = (
        # first + datetime.timedelta(days=32)).replace(day=1)
        self.current_date = first + relativedelta(months=1)
        # Set string to label function
        self.year_month_label()
        self.balance_label()
        # Update data for pie chart
        self.set_chart()

    def set_chart(self):
        # Get balance sum for each category
        category_dict = self.aggregate_num.monthly_category_sum(
            self.current_date, '支出'
        )
        # Append dictionary data to pie graph
        self.pie_chart.append_data(category_dict)

    def create_setting_widget(self):
        # Set month label widget
        setting_button = QPushButton('Setting')
        setting_button.setFixedWidth(70)
        setting_button.clicked.connect(self.setting_button_clicked)
        setting_layout = QHBoxLayout()
        setting_layout.addWidget(setting_button)
        setting_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        return setting_layout
    '''
    def subwin_result(self):
        subwin = SummarySubWindow()
        # Return input data if QDialog is accepted to close
        if subwin.exec() == QDialog.DialogCode.Accepted():
            res = subwin.result_text
            return res
        else:
            return None
    '''
    def setting_button_clicked(self):
        year_month_str = self.current_date.strftime('%Y-%m')
        subwin = SummarySubWindow(year_month_str)
        # Return input data if QDialog is accepted to close
        if subwin.exec() == QDialog.DialogCode.Accepted():
            res = subwin.result_text
            return res
        else:
            return None