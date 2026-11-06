import pandas as pd
import sqlite3
from database import DataBase


class AggregateData:
    def __init__(self):
        self.data_base = DataBase()

    def set_data(self, query):
        conn = self.data_base.conn
        with conn:
            try:
                df = pd.read_sql(query, conn)
            except sqlite3.Error as e:
                print(f"An error occured: {e}")
                self.conn.rollback()

        return df

    def update_data(self):
        return self.data_base

    def monthly_sum(self, year_month, balance_text):
        data = self.set_data('SELECT * FROM report')
        data = self.filter_data(data, year_month, balance_text)
        data = data[data.index.month == year_month.month]
        sum_data = data['amount'].sum()

        return sum_data

    def monthly_category(self, year_month, balance_text):
        data = self.set_data(
            'SELECT report.date, report.amount, report.balance, category.name FROM report Join category ON report.category_id = category.id'
        )
        data = self.filter_data(data, year_month, balance_text)
        data = data[data.index.month == year_month.month]
        category_data = data.groupby('name')['amount'].sum()
        category_dict = category_data.to_dict()

        return category_dict

    def yearly_sum(self, year_month, balance_text):
        data = self.set_data('SELECT * FROM report')
        data = self.filter_data(data, year_month, balance_text)
        sum_data = data['amount'].sum()

        return sum_data

    def yearly_category(self, year_month, balance_text):
        data = self.set_data(
            'SELECT report.date, report.amount, report.balance, category.name FROM report Join category ON report.category_id = category.id'
        )
        data = self.filter_data(data, year_month, balance_text)
        category_data = data.groupby('name')['amount'].sum()

        return category_data

    def filter_data(self, data, year_month, balance_text):
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        data = data.sort_values('date')
        data.set_index('date', inplace=True)
        data = data[data['balance'] == balance_text]
        data = data[data.index.year == year_month.year]

        return data

    def difference(self, income, expense):
        diff = income - expense

        return diff
