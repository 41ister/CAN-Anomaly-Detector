from factor_analyzer import FactorAnalyzer
from scipy.stats import f_oneway
from contextlib import redirect_stdout
import  pandas as pd
import  os
import  matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.varmax import VARMAX
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import grangercausalitytests


def drop_nulls_from_df(df:pd.DataFrame) -> pd.DataFrame:
  if(df.isna().sum().sum()):
   return df.dropna()
  else: return df


os.chdir('C:\\Users\\Кирилл\\Desktop\\Аномалии\\src')
pd.set_option('display.expand_frame_repr', False)

dateparse=lambda date: pd.to_datetime(date)

N=100

df_usual_drive=pd.read_csv('.\\data\\usual_drive.csv', index_col='timestamp', date_parser=dateparse)
df_usual_drive=drop_nulls_from_df(df_usual_drive)


#dates = pd.date_range('2019-06-01 19:15:16', periods=len(df_usual_drive), freq='S')

#df_usual_drive.index=dates
#historical_data=df_usual_drive[-N:]
#test_data=df_usual_drive[N+1:]

#prediction=pd.Series()



