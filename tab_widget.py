from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import*
from summary_tab_widget import SummaryTabWidget
from input_tab_widget import InputTabWidget
import datetime


class TabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # Get widget
        self.summary_tab_widget = SummaryTabWidget()
        self.input_tab_widget = InputTabWidget()
        # Add widget to tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.summary_tab_widget, 'サマリー')
        self.tabs.addTab(self.input_tab_widget, '入力')
        # Set process for when summary tab is clicked
        self.tabs.currentChanged.connect(self.summary_tab_clicked)
        # Set tabs to tab_layout
        self.tab_layout = QVBoxLayout()
        self.tab_layout.addWidget(self.tabs)
        # Set tab_layout to layout
        self.setLayout(self.tab_layout)

    def summary_tab_clicked(self):
        today = datetime.date.today()
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:
            self.summary_tab_widget.year_month_label(today)
            self.summary_tab_widget.balance_label(today)

  