from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from input_tab_widget import InputTabWidget
from summary_tab_widget import SummaryTabWidget


class TabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # Get widget
        self.summary_tab_widget = SummaryTabWidget()
        self.input_tab_widget = InputTabWidget()
        # Add widget to tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.summary_tab_widget, 'Summary')
        self.tabs.addTab(self.input_tab_widget, 'Input')
        # Set process for when summary tab is clicked
        self.tabs.currentChanged.connect(self.summary_tab_clicked)
        # Set tabs to tab_layout
        self.tab_layout = QVBoxLayout()
        self.tab_layout.addWidget(self.tabs)
        # Set tab_layout to layout
        self.setLayout(self.tab_layout)

    def summary_tab_clicked(self):
        current_tab = self.tabs.currentIndex()
        # Update data when summary tab is clicked
        if current_tab == 0:
            self.summary_tab_widget.set_year_month_label()
            self.summary_tab_widget.set_balance_label()
            self.summary_tab_widget.set_chart()
