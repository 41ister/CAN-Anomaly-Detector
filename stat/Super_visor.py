import pandas
from statsmodels.tsa.stattools import adfuller
class SuperVisor:
    def __init__(self, data:pandas.Series):
        self.data=data      

    def stationarotyTest(self):
         try:
            pvalue = adfuller(self.data, autolag='AIC')[1]        
            return (pvalue<0.05)           
         except:
            return False

