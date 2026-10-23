import sqlite3
import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import*
from aggregate import AggregateData
from dataBase import dataBase

class TabWidget(QWidget):        
    def __init__(self,parent):  
        super().__init__(parent)
        # Main　layout
        self.layout = QVBoxLayout()
        # Get current month from today's date
        today = datetime.date.today()
        self.current_month = today.month
        # Call dataBase class
        self.data = dataBase()
        self.aggregateNum = AggregateData()
        # Tab layout
        self.tabs = QTabWidget()
        # Tab1 layout
        self.createSummaryTab()
        self.summaryTab = QWidget()
        self.summaryTab.layout=QVBoxLayout(self)
        self.summaryTab.setFixedHeight(200)
        print(self.summaryTab.size())
        self.summaryTab.layout.addLayout(self.summaryTabLayout)
        self.summaryTab.setLayout(self.summaryTab.layout)
        # Tab2 layout
        self.createInputTab()
        self.inputTab = QWidget()
        self.inputTab.layout=QVBoxLayout(self)
        self.inputTab.layout.addLayout(self.inputTabLayout)
        self.inputTab.setLayout(self.inputTab.layout)

        self.tabs.addTab(self.summaryTab,'サマリー')
        self.tabs.addTab(self.inputTab,'入力')
        self.tabs.currentChanged.connect(self.summaryTabClicked)
        self.layout.addWidget(self.tabs)
        # Set tab to layout
        self.setLayout(self.layout)
    
    def summaryTabClicked(self):
        currentTab = self.tabs.currentIndex()
        if currentTab == 0:
            self.createLabel(self.current_month)
            self.prevButton.clearFocus()

    def createSummaryTab(self):
        # SummaryBox main layout
        self.summaryTabLayout = QGridLayout()
        # Layout for month
        monthLayout = QHBoxLayout()
        self.prevButton = QPushButton('prev')
        self.prevButton.setFixedWidth(40)
        self.prevButton.clicked.connect(self.prevButtonClick)
        self.monthLabel = QLabel(str(self.current_month) + '月')
        self.monthLabel.setFixedWidth(30)
        nextButton = QPushButton('next')
        nextButton.setFixedWidth(40)
        nextButton.clicked.connect(self.nextButtonClick)
        monthLayout.addWidget(self.prevButton, alignment=Qt.AlignmentFlag.AlignRight)
        monthLayout.addWidget(self.monthLabel, alignment=Qt.AlignmentFlag.AlignRight)
        monthLayout.addWidget(nextButton, alignment=Qt.AlignmentFlag.AlignRight)
        dataLayout = QGridLayout()
        incomeLabel = QLabel('収入:')
        self.incomeText = QLabel()
        expenseLabel = QLabel('支出:')
        self.expenseText = QLabel()
        balanceLabel = QLabel('収支:')
        self.balanceText = QLabel()
        budgetLabel = QLabel('予算:')
        self.budgetText = QLabel('0')
        dataLayout.addWidget(incomeLabel, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        dataLayout.addWidget(self.incomeText, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)
        dataLayout.addWidget(balanceLabel, 0, 2, alignment=Qt.AlignmentFlag.AlignRight)
        dataLayout.addWidget(self.balanceText, 0, 3, alignment=Qt.AlignmentFlag.AlignRight)
        dataLayout.addWidget(expenseLabel, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        dataLayout.addWidget(self.expenseText, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        dataLayout.addWidget(budgetLabel, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)
        dataLayout.addWidget(self.budgetText, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        self.createLabel(self.current_month)
        # Add each layout to main layout
        self.summaryTabLayout.addLayout(monthLayout, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.summaryTabLayout.addLayout(dataLayout, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

    def createLabel(self, month):
        # Get aggregated data
        incomeData = self.aggregateNum.incomeSum(month)
        expenseData = self.aggregateNum.expenseSum(month)
        balanceData = self.aggregateNum.Difference(incomeData, expenseData)
        self.incomeText.setText(str(incomeData))
        self.expenseText.setText(str(expenseData))
        if balanceData == 0:
            self.balanceText.setText('+-' + str(0))
        elif balanceData > 0:
            self.balanceText.setText('+' + str(balanceData))
        else:
            self.balanceText.setText(str(balanceData))
    
    def prevButtonClick(self):
        self.current_month = self.current_month-1
        self.monthLabel.setText(str(self.current_month) + '月')
        # Get aggregated data
        self.createLabel(self.current_month)

    def nextButtonClick(self):
        self.current_month = self.current_month+1
        self.monthLabel.setText(str(self.current_month) + '月')
        # Get aggregated data
        self.createLabel(self.current_month)

    def createInputTab(self):
        # Main layout
        self.inputTabLayout = QVBoxLayout()
        expenceLayout = self.createInputWidget('支出')
        inputLayout = self.createInputWidget('収入')
        # Set tab
        tabs = QTabWidget()
        # Add layout to expense tab
        expense_tab = QWidget()
        expense_tab.setLayout(expenceLayout)
        # Add layout to income tab
        income_tab = QWidget()
        income_tab.setLayout(inputLayout)
        #Add tab to UI
        tabs.addTab(expense_tab,'支出')
        tabs.addTab(income_tab,'収入')
        self.inputTabLayout.addWidget(tabs)

    def createInputWidget(self, balance):
        calendar = self.createCalendarWidget()
        item, itemText = self.createItemWidget()
        money, moneyText = self.createMoneyWidget()
        # Set value for the combobox from category database
        cursor = self.data.fetchQueryValue('SELECT name FROM category WHERE type = ?', (balance,))
        categoryValues = cursor.fetchall()
        category, categoryText = self.createCategoryWidget(categoryValues)
        # Set value for the combobox from bank database
        cursor = self.data.fetchQuery('SELECT name FROM bank')
        bankValues = cursor.fetchall()
        bank, bankText = self.createBankWidget(bankValues)
        inputButton = self.createInputButton()
        inputButton.clicked.connect(lambda: self.inputButtonClicked(calendar, itemText, moneyText, categoryText, bankText, balance))
        # Set widget to expence tab layout
        inputLayout = QVBoxLayout()
        inputLayout.addWidget(calendar)
        inputLayout.addLayout(item)
        inputLayout.addLayout(money)
        inputLayout.addLayout(category)
        inputLayout.addLayout(bank)
        inputLayout.addWidget(inputButton)

        return inputLayout

    def createCalendarWidget(self):
        # Set calendar view setting 
        calendar = QCalendarWidget()
        calendar.setFirstDayOfWeek(Qt.DayOfWeek(1))
        calendar.setGridVisible(True)

        return calendar

    def createItemWidget(self):
        # Create item widget
        itemBox = QHBoxLayout()
        itemLabel = QLabel('項目:')
        itemInput = QLineEdit()
        itemInput.setPlaceholderText('項目を入力')
        itemInput.setFixedWidth(250)
        # Set widget to layout
        itemBox.addWidget(itemLabel)
        itemBox.addWidget(itemInput, alignment=Qt.AlignmentFlag.AlignLeft)

        return itemBox,itemInput

    def createMoneyWidget(self):
        # Create money widget
        moneyBox = QHBoxLayout()
        moneyLabel = QLabel('金額:')
        moneyInput = QLineEdit()
        validator = QIntValidator(self)
        moneyInput.setValidator(validator)
        moneyInput.setFixedWidth(250)
        # Set widget to layout
        moneyBox.addWidget(moneyLabel)
        moneyBox.addWidget(moneyInput, alignment=Qt.AlignmentFlag.AlignLeft)

        return moneyBox,moneyInput

    def createCategoryWidget(self, values):
        # Create category widget
        categoryBox = QHBoxLayout()
        categoryLabel = QLabel('カテゴリー :')
        categoryCombo = QComboBox()
        for value in values:
            categoryCombo.addItem(str(value[0]))
        categoryCombo.setFixedWidth(120)
        categoryButton = QPushButton("+")
        categoryButton.setFixedWidth(50)
        # Set widget to layout
        categoryBox.addWidget(categoryLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        categoryBox.addWidget(categoryCombo, alignment=Qt.AlignmentFlag.AlignLeft)
        categoryBox.addWidget(categoryButton, alignment=Qt.AlignmentFlag.AlignLeft)

        return categoryBox, categoryCombo

    def createBankWidget(self, values):
        # Set expense bank layout
        bankBox = QHBoxLayout()
        bankLabel = QLabel('出入先:')
        bankCombo = QComboBox()
        for value in values:
            bankCombo.addItem(str(value[0]))
        bankCombo.setFixedWidth(120)
        bankButton = QPushButton('+')
        bankButton.setFixedWidth(50)
        # Set widget to layout
        bankBox.addWidget(bankLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        bankBox.addWidget(bankCombo, alignment=Qt.AlignmentFlag.AlignLeft)
        bankBox.addWidget(bankButton, alignment=Qt.AlignmentFlag.AlignLeft)

        return bankBox, bankCombo

    def createInputButton(self):
        record_button = QPushButton('記録')

        return record_button

    def inputButtonClicked(self, Calendar, itemText, moneyText, categoryText, bankText, balance):
        # Get data from calendar
        calendar = Calendar.selectedDate().toString('yyyy-MM-dd')
         # Get item name from textbox
        item = itemText.text()
        # Get amount of money from textbox
        if(moneyText.text()):
            money = int(moneyText.text())
        else:
            money = 0.00
        # Get category name from textbox and find the ID for the name throgh category database 
        category_name = categoryText.currentText()
        cursor = self.data.exeQuery('SELECT id FROM category WHERE name = ?', (category_name,))
        category_id = cursor.fetchone()
        # Get bank name from textbox and find the ID for the name throgh bank database 
        bank_name = bankText.currentText()
        cursor = self.data.exeQuery('SELECT id FROM bank WHERE name = ?', (bank_name,))
        bank_id = cursor.fetchone()
        # Set expense as a value for balance
        balance_name = balance
        # Insert data into database
        self.data.exeQuery('INSERT INTO report(date,description,amount,category_id,bank_id,balance) VALUES(?,?,?,?,?,?)', (calendar, item, money, str(category_id[0]), str(bank_id[0]), balance_name))
        # Clear out data from text box
        itemText.clear()
        moneyText.clear()



       