import  pandas as pd
import  os
import  matplotlib.pyplot as plt
from timeit import default_timer as timer
from arima_model import ArimaModel
from arma_model import ArmaModel
from white_nose_model import WhiteNoiseModel
from abstract_model import AbstractModel
from ma_model import MaModel
from ar_model import ArModel

def drop_nulls_from_df(df:pd.DataFrame) -> pd.DataFrame:
  if(df.isna().sum().sum()):
   return df.dropna()
  else: return df




# os.chdir('C:\\Users\\Кирилл\\Desktop\\Аномалии\\src')
pd.set_option('display.expand_frame_repr', False)

dateparse=lambda date: pd.to_datetime(date)

n=1000

df_usual_drive=pd.read_csv('./data/AT_from_1_to_2.csv', index_col='timestamp', date_parser=dateparse)
df_usual_drive=drop_nulls_from_df(df_usual_drive)

sr_vehicle_speed=df_usual_drive["vehicle_speed"]
dates = pd.date_range('2019-06-01 19:15:16', periods=len(df_usual_drive), freq='S')
sr_vehicle_speed.index=dates
sr_vehicle_speed_test=sr_vehicle_speed[n:]
historical_data=sr_vehicle_speed[0:n]

#std=sr_vehicle_speed.std()
std=2.5

model_number=int(input("0:White Noise Model\n1:MA Model\n2:AR Model\n3:ARMA Model\n4:ARIMA model\n5:Optimal Model\n Enter model:"))
model=AbstractModel
if(model_number<0 or model_number>5):
  exit(-1)
elif(model_number==0):
 model=WhiteNoiseModel(historical_data, std)
elif(model_number==1):
 q=int(input("Enter  parameter q:"))
 model=MaModel(historical_data, std, q=q)
elif(model_number==2):
 p=int(input("Enter  parameter p:"))
 model=ArModel(historical_data,std, p=p)
elif(model_number==3):
 p=int(input("Enter  parameter p:"))
 q=int(input("Enter  parameter q:"))
 model=ArmaModel(historical_data,std, p=p,q=q)
elif(model_number==4):
 p=int(input("Enter  parameter p:"))
 d=int(input("Enter  parameter d:"))
 q=int(input("Enter  parameter q:"))
 model=ArimaModel(historical_data,std, p=p,d=d,q=q)
elif(model_number==5):
 model=ArimaModel(historical_data, std)


prediction=pd.Series()

model.fit_parameters()
start=timer()
percents_prev=0
print("anomaly detection started...")
for i in range(0,len(sr_vehicle_speed_test)):    
        #yhat=model.predict()  
        yhat=model.old_predict()
        prediction=pd.concat([prediction,yhat])
        obs=sr_vehicle_speed_test[i:i+1]
        #print("reported: {}, expected: {}".format(obs[0], yhat[0]))
        if(model.anomaly_detect(obs[0])):
          print("anomaly detected at {:%Y-%m-%d %H:%M:%S}. reported: {}, expected: {}".format(obs.index[0], obs[0], yhat[0]))
        percents=round(100*i/len(sr_vehicle_speed_test))
        if(percents%10==0 and percents_prev!=percents and percents!=100): 
          print("{}  % processed".format(percents))
          percents_prev=percents          
          end=timer()
          print("{} seconds passed".format(end-start))       
        #model.update_data(obs)
        model.old_update_data(obs)



print("{} % processed".format(100))
end=timer()
print("{} seconds passed".format(end-start))    
print("{} anomalies was found".format(len(prediction)))
plt.clf()
prediction.plot(color="blue")
sr_vehicle_speed_test.plot(color="red")
plt.show()
        
