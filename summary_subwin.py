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
    def __init__(self, current_date, parent=None):
        super().__init__(parent)
        self.aggregate = AggregateData()
        self.current_date = current_date
        self.year_month = self.current_date.strftime('%Y-%m')
        self.database = DataBase()
        # Set size of dialog
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
        self.layout.addWidget(self.create_add_button())

    def create_subwin_tab(self):
        subwin_layout = QVBoxLayout()
        # Set label
        item_label = QLabel('Set budget for this month:')
        # Get category names from category table and set to list
        category_name = self.database.fetch_query(
            'SELECT name FROM category WHERE type = "支出"'
        )
        category_list = [name for name, in category_name.fetchall()]
        # Set widget dynamically based on data in the category table
        validator = QDoubleValidator()
        form_layout = QFormLayout()
        self.category_dict = {}
        for category in category_list:
            # Get category name and set to label
            category_label = QLabel(f'{category}:')
            # Set default number to lineedit if budget table is empty
            budget_count = self.database.fetch_query(
                'SELECT COUNT (*) FROM budget WHERE year_month = ?', (
                    self.year_month,
                )
            ).fetchone()[0]
            if budget_count == 0:
                self.item_input = QLineEdit(f'{0}')
            else:
                # Set data to lineedit if budget table exists
                budget_amount = self.database.fetch_query(
                    'SELECT budget.amount FROM budget JOIN category \
                    ON budget.category_id = category.id \
                    WHERE budget.year_month = ? AND category.name = ?', (
                        self.year_month, category
                    )
                ).fetchone()
                if budget_amount is not None:
                    budget_amount = ''.join((map(str, budget_amount)))
                    self.item_input = QLineEdit(f'{budget_amount}')
                else:
                    self.item_input = QLineEdit(f'{0}')
            # Set validator
            self.item_input.setValidator(validator)
            # Add label and lineedit to form layout
            form_layout.addRow(category_label, self.item_input)
            # Add lineedit to list
            self.category_dict[category] = self.item_input
        # Add layout to main layout
        subwin_layout.addWidget(item_label)
        subwin_layout.addLayout(form_layout)

        return subwin_layout

    def create_add_button(self):
        # Create set button
        self.add_button = QPushButton('Set Budget')
        # Connect button to function
        self.add_button.clicked.connect(self.add_button_clicked)

        return self.add_button

    def add_button_clicked(self):
        # Get text data from lineedit box and set it to list
        budget_dict = {
            category: self.item_input.text() for category,
            self.item_input in self.category_dict.items()
        }
        # Set data to budget table
        for category, amount in budget_dict.items():
            category_id = self.database.fetch_query(
                'SELECT id FROM category WHERE name = ?', (category,)
            ).fetchone()
            if category_id is not None:
                category_id = ''.join((map(str, category_id)))
            else:
                print('category_id is none')
            self.database.exe_query(
                'INSERT INTO budget (year_month, category_id, amount) \
                VALUES(?, ?, ?) ON CONFLICT(year_month, category_id) \
                DO UPDATE SET amount = EXCLUDED.amount', (
                    self.year_month, category_id, amount
                )
            )
        # Add budget of each category and get monthly sum
        self._sum = self.aggregate.monthly_budget_sum(
            self.current_date.year, self.current_date.month
        )
        # Accept dialog to close
        self.accept()

    @property
    def result_text(self):
        # Return text
        return self._sum
