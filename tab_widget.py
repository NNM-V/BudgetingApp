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
        # Call dataBase class
        self.data = dataBase()
        # Tab layout
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)
        # Tab1 layout
        self.createSummaryBox()
        self.tab1 = QWidget()
        self.tab1.layout=QVBoxLayout(self)
        self.tab1.layout.addLayout(self.summaryLayout)
        self.tab1.setLayout(self.tab1.layout)
        # Tab2 layout
        self.createInputBox()
        self.tab2 = QWidget()
        self.tab2.layout=QVBoxLayout(self)
        self.tab2.layout.addLayout(self.inputLayout)
        self.tab2.setLayout(self.tab2.layout)
        self.tabs.addTab(self.tab1,'Tab1')
        self.tabs.addTab(self.tab2,'Tab2')
        self.layout.addWidget(self.tabs)
        # Set tab to layout
        self.setLayout(self.layout)

    def createSummaryBox(self):
        # SummaryBox main　layout
        self.summaryLayout=QVBoxLayout()
        # Get current month from today's date
        today = datetime.date.today()
        current_month = today.month
        # Get aggregated data
        data = AggregateData()
        incomeData = data.incomeSum(current_month)
        expenseData = data.expenseSum(current_month)
        balanceData = data.Difference()
        # Layout for income data
        incomeLayout = QHBoxLayout()
        incomeLabel = QLabel('収入:')
        incomeText = QLabel(str(incomeData))
        incomeLayout.addWidget(incomeLabel)
        incomeLayout.addWidget(incomeText)
        # Layout for expense data
        expenseLayout = QHBoxLayout()
        expenseLabel = QLabel('支出:')
        expenseText = QLabel(str(expenseData))
        expenseLayout.addWidget(expenseLabel)
        expenseLayout.addWidget(expenseText)
        # Layout for balance data
        balanceLayout = QHBoxLayout()
        balanceLabel = QLabel('収支:')
        if balanceData==0:
            balanceText = QLabel('+-' + str(balanceData))
        elif balanceData>0:
            balanceText = QLabel('+' + str(balanceData))
        else:
            balanceText = QLabel(str(balanceData))
        balanceLayout.addWidget(balanceLabel)
        balanceLayout.addWidget(balanceText)
        # Layout for budget data
        budgetLayout = QHBoxLayout()
        budgetLabel = QLabel('予算:')
        budgetText = QLabel('0')
        budgetLayout.addWidget(budgetLabel)
        budgetLayout.addWidget(budgetText)
        # Add each layout to main layout
        self.summaryLayout.addLayout(incomeLayout)
        self.summaryLayout.addLayout(expenseLayout)
        self.summaryLayout.addLayout(balanceLayout)
        self.summaryLayout.addLayout(budgetLayout)

    def createInputBox(self):
        # Main layout
        self.inputLayout = QVBoxLayout()
        # Create widget for expence tab
        self.expenseCalendar = self.createCalendarWidget()
        expenseItem, self.expenseItemText = self.createItemWidget()
        expenseMoney, self.expenseMoneyText = self.createMoneyWidget()
        # Set value for the combobox from category database
        cursor = self.data.fetchQuery('SELECT name FROM category WHERE type = "支出"')
        expenseCategoryValues = cursor.fetchall()
        expenseCategory, self.expenseCategoryText = self.createCategoryWidget(expenseCategoryValues)
        cursor = self.data.fetchQuery('SELECT name FROM bank')
        expenseBankValues = cursor.fetchall()
        expenseBank, self.expenseBankText = self.createBankWidget(expenseBankValues)
        expenseButton = self.createButton()
        expenseButton.clicked.connect(self.expenseButtonClick)
        # Set widget to expence tab layout
        expenseLayout = QVBoxLayout()
        expenseLayout.addWidget(self.expenseCalendar)
        expenseLayout.addLayout(expenseItem)
        expenseLayout.addLayout(expenseMoney)
        expenseLayout.addLayout(expenseCategory)
        expenseLayout.addLayout(expenseBank)
        expenseLayout.addWidget(expenseButton)
        # Create widget for income tab
        self.incomeCalendar = self.createCalendarWidget()
        incomeItem, self.incomeItemText  = self.createItemWidget()
        incomeMoney, self.incomeMoneyText = self.createMoneyWidget()
        cursor = self.data.fetchQuery('SELECT name FROM category WHERE type = "収入"')
        incomeCategoryValues = cursor.fetchall()
        incomeCategory, self.incomeCategoryText = self.createCategoryWidget(incomeCategoryValues)
        cursor = self.data.fetchQuery('SELECT name FROM bank')
        incomeBankValues = cursor.fetchall()
        incomeBank, self.incomeBankText = self.createBankWidget(incomeBankValues)
        incomeButton = self.createButton()
        incomeButton.clicked.connect(self.incomeButtonClick)
        # Set widget to income layout
        incomeLayout=QVBoxLayout()
        incomeLayout.addWidget(self.incomeCalendar)
        incomeLayout.addLayout(incomeItem)
        incomeLayout.addLayout(incomeMoney)
        incomeLayout.addLayout(incomeCategory)
        incomeLayout.addLayout(incomeBank)
        incomeLayout.addWidget(incomeButton)
        # Set tab
        tabs = QTabWidget()
        tabs.resize(200,100)
        # Add layout to expense tab
        expense_tab = QWidget()
        expense_tab.setLayout(expenseLayout)
        # Add layout to income tab
        income_tab = QWidget()
        income_tab.setLayout(incomeLayout)
        #Add tab to UI
        tabs.addTab(expense_tab,'支出')
        tabs.addTab(income_tab,'収入')
        self.inputLayout.addWidget(tabs)

    def createCalendarWidget(self):
        # Set calendar view setting 
        calendar = QCalendarWidget()
        calendar.setFirstDayOfWeek(Qt.DayOfWeek(1))
        calendar.setGridVisible(True)

        return calendar

    def createItemWidget(self):
        # Create item widget
        itemLabel = QLabel('項目:')
        itemBox = QHBoxLayout()
        itemInput = QLineEdit()
        itemInput.setPlaceholderText('項目を入力')
        # Set widget to layout
        itemBox.addWidget(itemLabel)
        itemBox.addWidget(itemInput)

        return itemBox,itemInput

    def createMoneyWidget(self):
        # Create money widget
        moneyLabel = QLabel('金額:')
        moneyBox = QHBoxLayout()
        moneyInput = QLineEdit()
        validator = QIntValidator(self)
        moneyInput.setValidator(validator)
        # Set widget to layout
        moneyBox.addWidget(moneyLabel)
        moneyBox.addWidget(moneyInput)

        return moneyBox,moneyInput

    def createCategoryWidget(self, values):
        # Create category widget
        categoryLabel = QLabel('カテゴリー :')
        categoryBox = QHBoxLayout()
        categoryCombo = QComboBox()
        for value in values:
            categoryCombo.addItem(str(value[0]))
        categoryButton = QPushButton("+")
        # Set widget to layout
        categoryBox.addWidget(categoryLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        categoryBox.addWidget(categoryCombo, alignment=Qt.AlignmentFlag.AlignLeft)
        categoryBox.addWidget(categoryButton, alignment=Qt.AlignmentFlag.AlignLeft)

        return categoryBox, categoryCombo

    def createBankWidget(self, values):
        # Set expense bank layout
        bankLabel = QLabel('出入先:')
        bankBox = QHBoxLayout()
        bankCombo = QComboBox()
        for value in values:
            bankCombo.addItem(str(value[0]))
        bankButton = QPushButton('+')
        # Set widget to layout
        bankBox.addWidget(bankLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        bankBox.addWidget(bankCombo, alignment=Qt.AlignmentFlag.AlignLeft)
        bankBox.addWidget(bankButton, alignment=Qt.AlignmentFlag.AlignLeft)

        return bankBox, bankCombo

    def createButton(self):
        record_button = QPushButton('記録')

        return record_button
    
    def expenseButtonClick(self):
        # Get data from calendar
        calendar = self.expenseCalendar.selectedDate().toString('yyyy-MM-dd')
        print(str(calendar))
        # Get item name from textbox
        item = self.expenseItemText.text()
        print(item)
        # Get amount of money from textbox
        if(self.expenseMoneyText.text()):
            money = int(self.expenseMoneyText.text())
        else:
            money = 0.00
        print(money)
        # Get category name from textbox and find the ID for the name throgh category database 
        category_name = self.expenseCategoryText.currentText()
        print(category_name)
        cursor = self.data.exeQuery('SELECT id FROM category WHERE name = ?', (category_name,))
        category_id = cursor.fetchone()
        print(str(category_id[0]))
        # Get bank name from textbox and find the ID for the name throgh bank database 
        bank_name = self.expenseBankText.currentText()
        print(bank_name)
        cursor = self.data.exeQuery('SELECT id FROM bank WHERE name = ?', (bank_name,))
        bank_id = cursor.fetchone()
        print(str(category_id[0]))
        # Set expense as a value for balance
        balance = '支出'
        print(balance)
        # Insert data into database
        self.data.exeQuery('INSERT INTO report(date,description,amount,category_id,bank_id,balance) VALUES(?,?,?,?,?,?)', (calendar,item,money,str(category_id[0]),str(bank_id[0]),balance))
        # Clear out data from text box 
        self.expenseItemText.clear()
        self.expenseMoneyText.clear()

    def incomeButtonClick(self):
        # Get selected date from calendar widget and convert value to string 
        calendar = self.incomeCalendar.selectedDate().toString('yyyy-MM-dd')
        print(str(calendar))
        # Get user input for item
        item = self.incomeItemText.text()
        print(item)
        # Get user input for amount if empty, set 0
        if(self.incomeMoneyText.text()):
            money = int(self.incomeMoneyText.text())
        else:
            money = 0.00
        print(money)
        # Get category name from textbox and find the ID for the name throgh category database 
        category_name = self.expenseCategoryText.currentText()
        print(category_name)
        cursor = self.data.exeQuery('SELECT id FROM category WHERE name = ?', (category_name,))
        category_id = cursor.fetchone()
        print(str(category_id[0]))
        # Get bank name from textbox and find the ID for the name throgh bank database 
        bank_name = self.expenseBankText.currentText()
        print(bank_name)
        cursor = self.data.exeQuery('SELECT id FROM bank WHERE name = ?', (bank_name,))
        bank_id = cursor.fetchone()
        print(str(category_id[0]))
        # Set income as a value for balance
        balance = '収入'
        print(balance)
        # Insert data into database
        self.data.exeQuery('INSERT INTO report(date,description,amount,category_id,bank_id,balance) VALUES(?,?,?,?,?,?)', (calendar,item,money,str(category_id[0]),str(bank_id[0]),balance))
        # Clear out data from text box 
        self.expenseItemText.clear()
        # Clear text from textbox
        self.expenseItemText.clear()
        self.expenseMoneyText.clear()




       