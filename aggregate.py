import pandas as pd 
import sqlite3
import datetime
from dataBase import dataBase

class AggregateData:
    def setData(self):
        data = dataBase()
        conn = data.conn

        df = pd.read_sql('SELECT * FROM report', conn)
        df_date = df.copy()
        df_date['date'] = pd.to_datetime(df_date['date'])
        df_date = df_date.sort_values('date')
        df_date.set_index('date', inplace = True)

        data.close()

        return df_date

    def incomeSum(self,current_month):
        data = self.setData()
        data = data[data['balance'] == '収入']
        incomeSum = data[data.index.month == current_month]['amount'].sum()

        return incomeSum

    def expenseSum(self,current_month):
        data = self.setData()
        data = data[data['balance'] == '支出']
        expenseSum = data[data.index.month == current_month]['amount'].sum()
        
        return expenseSum

    def Difference(self, income, expense):
        diff = income - expense   
        
        return diff
