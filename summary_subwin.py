import datetime
from PySide6.QtWidgets import (
    QFormLayout, QVBoxLayout, QLabel, 
    QLineEdit, QPushButton, QDialog,
    QScrollArea, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from aggregate import AggregateData
from database import DataBase


class SummarySubWindow(QDialog):
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.aggregate = AggregateData()
        self.date = date
        self.year_month = self.date.strftime('%Y-%m')
        self.data = DataBase()
        self.setGeometry(300, 300, 300, 200)
        # Set widget with scroll bar
        widget = QWidget()
        vbox = self.create_subwin_tab()
        widget.setLayout(vbox)
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        # Add widget to layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(scroll)
        self.layout.addWidget(self.create_set_button())

    def create_subwin_tab(self):
        subwin_layout = QVBoxLayout()
        # Set label
        add_item_label = QLabel('Set budget for this month:')
        # Get category names from category table and set to list
        cursor = self.data.fetch_query('SELECT name FROM category WHERE type = "支出"')
        category_list = [name for name, in cursor.fetchall()]
        # Set label and lineedit widget dynamically based on data that exists in the category table
        validator = QDoubleValidator()
        form_layout = QFormLayout()
        self.category_dict = {}
        for category in category_list:
            # Get category name and set to label
            category_label = QLabel(f'{category}:')
            # Set default number to lineedit if budget table is empty
            budget_count = self.data.fetch_query('SELECT COUNT(*) FROM budget WHERE year_month=?', (self.year_month,)).fetchone()[0]
            if budget_count == 0:
                self.budget_input = QLineEdit(f'{0}')
            else:
                # Set data to lineedit if budget table exists
                budget_amount = self.data.fetch_query(
                    'SELECT budget.amount FROM budget JOIN category ON budget.category_id = category.id WHERE budget.year_month = ? AND category.name = ?', (self.year_month, category)
                ).fetchone()
                budget_amount = ''.join((map(str, budget_amount)))
                self.budget_input = QLineEdit(f'{budget_amount}')
            # Set validator
            self.budget_input.setValidator(validator)
            # Add label and lineedit to form layout
            form_layout.addRow(category_label, self.budget_input)
            # Add lineedit to list
            self.category_dict[category] = self.budget_input
        # Add layout
        subwin_layout.addLayout(form_layout)
        
        return subwin_layout

    def create_set_button(self):
        # Create set button
        self.set_budget_button = QPushButton('Set Budget')
        # Connect button to function
        self.set_budget_button.clicked.connect(self.set_button_clicked)

        return self.set_budget_button

    def set_button_clicked(self):
        # Get text data from lineedit box and set it to list
        budget_dict = {category: self.budget_input.text() for category, self.budget_input in self.category_dict.items()}
        # Set data to budget table
        for category, budget in budget_dict.items():
            category_id = self.data.fetch_query(
                'SELECT id FROM category WHERE name = ?', (category,)
            ).fetchone()
            category_id = ''.join((map(str, category_id)))
            self.data.exe_query('INSERT INTO budget (year_month, category_id, amount) VALUES(?, ?, ?) ON CONFLICT(year_month, category_id) DO UPDATE SET amount = EXCLUDED.amount', (
                    self.year_month, category_id, budget
                )
            )
        # Add budget of each category and get monthly sum
        self._res = self.aggregate.monthly_budget_sum(self.date.year, self.date.month)
        # Accept dialog to close
        self.accept()
    @property
    def result_text(self):
        # Return text
        return self._res

