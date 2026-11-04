import pandas as pd
from database import DataBase


class AggregateData:
    def set_data(self):
        data = DataBase()
        conn = data.conn

        df = pd.read_sql('SELECT * FROM report', conn)
        df_date = df.copy()
        df_date['date'] = pd.to_datetime(df_date['date'], format='%Y-%m-%d')
        df_date = df_date.sort_values('date')
        df_date.set_index('date', inplace=True)

        data.close()

        return df_date

    def monthly_sum(self, year_month, balance_text):
        year = year_month.year
        month = year_month.month

        data = self.set_data()
        data = data[data['balance'] == balance_text]
        data = data[data.index.year == year]
        sum_data = data[data.index.month == month]['amount'].sum()

        return sum_data

    def difference(self, income, expense):
        diff = income - expense

        return diff
