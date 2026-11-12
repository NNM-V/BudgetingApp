import pandas as pd
import sqlite3
from database import DataBase


class AggregateData:
    def __init__(self):
        self.data_base = DataBase()

    def set_data(self, query):
        # Connect to database.DataBase
        conn = self.data_base.conn
        # Read SQL table and set to dataframe
        with conn:
            try:
                df = pd.read_sql(query, conn)
            except sqlite3.Error as e:
                print(f"An error occured: {e}")
                self.conn.rollback()

        return df

    def monthly_sum(self, year_month, balance_text):
        # Set dataframe from report table
        data = self.set_data('SELECT * FROM report')
        data = self.filter_data(data, year_month, balance_text)
        sum_data = data['amount'].sum()

        return sum_data

    def monthly_category_sum(self, year_month, balance_text):
        # Set dataframe from report table and category table
        data = self.set_data(
            'SELECT report.date, report.amount, report.balance, category.name FROM report JOIN category ON report.category_id = category.id'
        )
        # Filter dataframe from date and balance category
        data = self.filter_data(data, year_month, balance_text)
        # Get the amount of sum for each category
        category_data = data.groupby('name')['amount'].sum()
        # Convert dataframe to dictionary
        category_dict = category_data.to_dict()
        # Set default data if month has no data
        empty_dict = {}
        if category_dict == empty_dict:
            category_dict = {'No data': 0}
        
        return category_dict

    def filter_data(self, data, year_month, balance_text=None):
        # Set datetime data format
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        # Sort data by date
        data = data.sort_values('date')
        data.set_index('date', inplace=True)
        # Filter data by balance category
        data = data[data['balance'] == balance_text]
        # Filter data by year and month
        data = data[data.index.year == year_month.year]
        data = data[data.index.month == year_month.month]

        return data

    def monthly_budget_sum(self, year, month):
        # Set dataframe from report table
        data = self.set_data('SELECT * FROM budget')
        # Set datetime data format
        data['year_month'] = pd.to_datetime(data['year_month'], format='%Y-%m')
        data.set_index('year_month', inplace=True)
        # Filter data by year and month
        data = data[data.index.year == year]
        data = data[data.index.month == month]
        sum_data = data['amount'].sum()
        
        return sum_data

    def difference(self, income, expense):
        # Get difference between income and expence
        diff = income - expense

        return diff
