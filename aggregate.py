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
        self.incomeSum = data[data.index.month == current_month]['amount'].sum()

        return self.incomeSum

    def expenseSum(self,current_month):
        data = self.setData()
        data = data[data['balance'] == '支出']
        self.expenseSum = data[data.index.month == current_month]['amount'].sum()
        
        return self.expenseSum

    def Difference(self):
        diff = self.incomeSum - self.expenseSum   
        
        return diff
