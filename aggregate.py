import pandas as pd
from database import DataBase


class AggregateData:
    def set_data(self):
        data = DataBase()
        conn = data.conn

        df = pd.read_sql('SELECT * FROM report', conn)
        df_date = df.copy()
        df_date['date'] = pd.to_datetime(df_date['date'], format='mixed')
        df_date = df_date.sort_values('date')
        df_date.set_index('date', inplace=True)

        data.close()

        return df_date

    def income_sum(self, current_month):
        data = self.set_data()
        data = data[data['balance'] == '収入']
        income_sum = data[data.index.month == current_month]['amount'].sum()

        return income_sum

    def expense_sum(self, current_month):
        data = self.set_data()
        data = data[data['balance'] == '支出']
        expense_sum = data[data.index.month == current_month]['amount'].sum()

        return expense_sum

    def difference(self, income, expense):
        diff = income - expense

        return diff
