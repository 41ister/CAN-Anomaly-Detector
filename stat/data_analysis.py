from factor_analyzer import FactorAnalyzer
from scipy.stats import f_oneway
from contextlib import redirect_stdout
import  pandas as pd
import  os
import  matplotlib.pyplot as plt


def drop_nulls_from_df(df:pd.DataFrame) -> pd.DataFrame:
  if(df.isna().sum().sum()):
   return df.dropna()
  else: return df

def plot_df(data:pd.Series, caption:str, ylabel:str, filename:str) -> pd.Series:
  plt.clf();
  data.plot(kind="bar")
  plt.title(caption)
  plt.ylabel(ylabel)
  plt.savefig(filename+".jpeg")
  return data
  
 

os.chdir('C:\\Users\\Кирилл\\Desktop\\Аномалии\\src')
pd.set_option('display.expand_frame_repr', False)

dateparse=lambda date: pd.to_datetime(date)

df_usual_drive=pd.read_csv('.\\data\\usual_drive.csv', index_col='timestamp', date_parser=dateparse)
df_usual_drive=drop_nulls_from_df(df_usual_drive)


df_long=pd.read_csv('.\\data\\long.csv', index_col='timestamp', date_parser=dateparse)
df_long=drop_nulls_from_df(df_long)

df_engine_start_minus16=pd.read_csv('.\\data\\engine_start_minus16.csv', index_col='timestamp', date_parser=dateparse)
df_engine_start_minus16=drop_nulls_from_df(df_engine_start_minus16)


df_dataset_usual_drive=pd.read_csv('.\\data\\dataset_usual_drive.csv', index_col='timestamp', date_parser=dateparse)
df_dataset_usual_drive=drop_nulls_from_df(df_dataset_usual_drive)


df_brakes_malfunction_tire=pd.read_csv('.\\data\\brakes_malfunction_tire.csv', index_col='timestamp', date_parser=dateparse)
df_brakes_malfunction_tire=drop_nulls_from_df(df_brakes_malfunction_tire)


df_AT_from_1_to_2=pd.read_csv('.\\data\\AT_from_1_to_2.csv', index_col='timestamp', date_parser=dateparse)
df_AT_from_1_to_2=drop_nulls_from_df(df_AT_from_1_to_2)



df_3_sudden_accelerate=pd.read_csv('.\\data\\3_sudden_accelerate.csv', index_col='timestamp', date_parser=dateparse)
df_3_sudden_accelerate=drop_nulls_from_df(df_3_sudden_accelerate)


with open('output.txt', 'w') as f:
    with redirect_stdout(f):
        print('Output:\n')
        print('usual_drive:\n')
        print(df_usual_drive.describe())
        print(df_usual_drive.cov())
        print('long:\n')
        print(df_long.describe())
        print(df_long.cov())
        print('engine_start_minus16:\n')
        print(df_engine_start_minus16.describe())
        print(df_engine_start_minus16.cov())
        print('dataset_usual_drive:\n')
        print(df_dataset_usual_drive.describe())
        print(df_dataset_usual_drive.cov())
        print('brakes_malfunction_tire:\n')
        print(df_brakes_malfunction_tire.describe())
        print(df_brakes_malfunction_tire.cov())
        print('AT_from_1_to_2:\n')
        print(df_AT_from_1_to_2.describe())
        print(df_AT_from_1_to_2.cov())
        print('3_sudden_accelerate:\n')
        print(df_3_sudden_accelerate.describe())
        print(df_3_sudden_accelerate.cov())
        
        print("vehicle_speed:")
        print(f_oneway(df_usual_drive["vehicle_speed"],df_long["vehicle_speed"], df_engine_start_minus16["vehicle_speed"],df_dataset_usual_drive["vehicle_speed"], df_brakes_malfunction_tire["vehicle_rpm"], df_AT_from_1_to_2["vehicle_rpm"], df_3_sudden_accelerate["vehicle_rpm"]))
        print("vehicle_rpm:")
        print(f_oneway(df_usual_drive["vehicle_rpm"],df_long["vehicle_rpm"], df_engine_start_minus16["vehicle_rpm"],df_dataset_usual_drive["vehicle_rpm"], df_brakes_malfunction_tire["vehicle_speed"], df_AT_from_1_to_2["vehicle_speed"], df_3_sudden_accelerate["vehicle_speed"]))
        print("lf_wheel_s:")
        print(f_oneway(df_usual_drive["lf_wheel_s"],df_long["lf_wheel_s"], df_engine_start_minus16["lf_wheel_s"], df_brakes_malfunction_tire["lf_wheel_s"], df_AT_from_1_to_2["lf_wheel_s"], df_3_sudden_accelerate["lf_wheel_s"]))
        print("rf_wheel_s:")
        print(f_oneway(df_usual_drive["rf_wheel_s"],df_long["rf_wheel_s"], df_engine_start_minus16["rf_wheel_s"], df_brakes_malfunction_tire["rf_wheel_s"], df_AT_from_1_to_2["rf_wheel_s"], df_3_sudden_accelerate["rf_wheel_s"]))
        print("lr_wheel_s:")
        print(f_oneway(df_usual_drive["lr_wheel_s"],df_long["lr_wheel_s"], df_engine_start_minus16["lr_wheel_s"], df_brakes_malfunction_tire["lr_wheel_s"], df_AT_from_1_to_2["rf_wheel_s"], df_3_sudden_accelerate["lr_wheel_s"]))
        print("rr_wheel_s:")
        print(f_oneway(df_usual_drive["rr_wheel_s"],df_long["rr_wheel_s"], df_engine_start_minus16["rr_wheel_s"], df_brakes_malfunction_tire["rr_wheel_s"], df_AT_from_1_to_2["rr_wheel_s"], df_3_sudden_accelerate["rr_wheel_s"]))
        print("gear:")
        print(f_oneway(df_usual_drive["gear"],df_long["gear"], df_engine_start_minus16["gear"], df_brakes_malfunction_tire["gear"], df_AT_from_1_to_2["gear"], df_3_sudden_accelerate["gear"]))
        print("accel_pedal:")
        print(f_oneway(df_usual_drive["accel_pedal"],df_long["accel_pedal"], df_engine_start_minus16["accel_pedal"], df_brakes_malfunction_tire["accel_pedal"], df_AT_from_1_to_2["accel_pedal"], df_3_sudden_accelerate["accel_pedal"]))
        print("engine_temp:")
        print(f_oneway(df_usual_drive["engine_temp"],df_long["engine_temp"], df_engine_start_minus16["engine_temp"], df_brakes_malfunction_tire["engine_temp"], df_AT_from_1_to_2["engine_temp"], df_3_sudden_accelerate["engine_temp"]))

                
means_vehicle_speed=pd.Series([df_usual_drive["vehicle_speed"].mean(),df_long["vehicle_speed"].mean(), df_engine_start_minus16["vehicle_speed"].mean() ,df_dataset_usual_drive["vehicle_speed"].mean(), df_brakes_malfunction_tire["vehicle_speed"].mean(), df_AT_from_1_to_2["vehicle_speed"].mean(), df_3_sudden_accelerate["vehicle_speed"].mean()],["uDr", "long", "start", "uDr2", "mlfc", "AT12", "acc"])
means_vehicle_rpm=pd.Series([df_usual_drive["vehicle_rpm"].mean(),df_long["vehicle_rpm"].mean(), df_engine_start_minus16["vehicle_rpm"].mean() ,df_dataset_usual_drive["vehicle_rpm"].mean(), df_brakes_malfunction_tire["vehicle_rpm"].mean(), df_AT_from_1_to_2["vehicle_rpm"].mean(), df_3_sudden_accelerate["vehicle_rpm"].mean()],["uDr", "long", "start", "uDr2", "mlfc", "AT12", "acc"])
means_lf_wheel_s=pd.Series([df_usual_drive["lf_wheel_s"].mean(),df_long["lf_wheel_s"].mean(), df_engine_start_minus16["lf_wheel_s"].mean() ,df_brakes_malfunction_tire["lf_wheel_s"].mean(), df_AT_from_1_to_2["lf_wheel_s"].mean(), df_3_sudden_accelerate["lf_wheel_s"].mean()],["uDr", "long", "start", "mlfc", "AT12", "acc"])
means_rf_wheel_s=pd.Series([df_usual_drive["rf_wheel_s"].mean(),df_long["rf_wheel_s"].mean(), df_engine_start_minus16["rf_wheel_s"].mean() ,df_brakes_malfunction_tire["rf_wheel_s"].mean(), df_AT_from_1_to_2["rf_wheel_s"].mean(), df_3_sudden_accelerate["rf_wheel_s"].mean()],["uDr", "long", "start", "mlfc", "AT12", "acc"])
means_lr_wheel_s=pd.Series([df_usual_drive["lr_wheel_s"].mean(),df_long["lr_wheel_s"].mean(), df_engine_start_minus16["lr_wheel_s"].mean() ,df_brakes_malfunction_tire["lr_wheel_s"].mean(), df_AT_from_1_to_2["lr_wheel_s"].mean(), df_3_sudden_accelerate["lr_wheel_s"].mean()],["uDr", "long", "start", "mlfc", "AT12", "acc"])
means_rr_wheel_s=pd.Series([df_usual_drive["rr_wheel_s"].mean(),df_long["rr_wheel_s"].mean(), df_engine_start_minus16["rr_wheel_s"].mean() ,df_brakes_malfunction_tire["rr_wheel_s"].mean(), df_AT_from_1_to_2["rr_wheel_s"].mean(), df_3_sudden_accelerate["rr_wheel_s"].mean()],["uDr", "long", "start", "mlfc", "AT12", "acc"])
means_gear=pd.Series([df_usual_drive["gear"].mean(),df_long["gear"].mean(), df_engine_start_minus16["gear"].mean() ,df_brakes_malfunction_tire["gear"].mean(), df_AT_from_1_to_2["gear"].mean(), df_3_sudden_accelerate["gear"].mean()],["uDr", "long", "start", "mlfc", "AT12", "acc"])
means_accel_pedal=pd.Series([df_usual_drive["accel_pedal"].mean(),df_long["accel_pedal"].mean(), df_engine_start_minus16["accel_pedal"].mean() ,df_brakes_malfunction_tire["accel_pedal"].mean(), df_AT_from_1_to_2["accel_pedal"].mean(), df_3_sudden_accelerate["accel_pedal"].mean()],["uDr", "long", "start", "mlfc", "AT12", "acc"])
means_engine_temp=pd.Series([df_usual_drive["engine_temp"].mean(),df_long["engine_temp"].mean(), df_engine_start_minus16["engine_temp"].mean() ,df_brakes_malfunction_tire["engine_temp"].mean(), df_AT_from_1_to_2["engine_temp"].mean(), df_3_sudden_accelerate["engine_temp"].mean()],["uDr", "long", "start", "mlfc", "AT12", "acc"])

plot_df(means_vehicle_speed, "Среднее выборочные значения скорости", "Скорость","means_vehicle_speed")
plot_df(means_vehicle_rpm, "Среднее выборочные значения оборотов двигателя", "Обороты двигателя","means_vehicle_rpm")
plot_df(means_lf_wheel_s,"Means lf wheel s","lf_wheel_s","means_lf_wheel_s")
plot_df(means_rf_wheel_s,"Means rf wheel s","rf_wheel_s","means_rf_wheel_s")
plot_df(means_lr_wheel_s,"Means lr wheel s","lr_wheel_s","means_lr_wheel_s")
plot_df(means_rr_wheel_s,"Means rr wheel s","rr_wheel_s","means_rr_wheel_s")
plot_df(means_gear,"Средее выборочное значение передачи","Передача","means_gear")
plot_df(means_accel_pedal,"Means accel pedal","Ускорение","means_accel_pedal")
plot_df(means_engine_temp,"Средее выборочное значение температуры двигателя","Температура двигателя","means_engine_temp")

fa_model_usual_drive=FactorAnalyzer(n_factors=3,rotation="varimax").fit(df_usual_drive)
fa_model_long=FactorAnalyzer(n_factors=3,rotation="varimax").fit(df_long)
fa_model_brakes_malfunction_tire=FactorAnalyzer(n_factors=3,rotation="varimax").fit(df_brakes_malfunction_tire)
fa_model_AT_from_1_to_2=FactorAnalyzer(n_factors=3,rotation="varimax").fit(df_AT_from_1_to_2)
fa_model_3_sudden_accelerate=FactorAnalyzer(n_factors=3,rotation="varimax").fit(df_3_sudden_accelerate)

ev_usual_drive,v_usual_drive=fa_model_usual_drive.get_eigenvalues()
ev_long,v_long=fa_model_long.get_eigenvalues()
ev_brakes_malfunction_tire,v_brakes_malfunction_tire=fa_model_brakes_malfunction_tire.get_eigenvalues()
ev_AT_from_1_to_2,v_AT_from_1_to_2=fa_model_AT_from_1_to_2.get_eigenvalues()
ev_3_sudden_accelerate,v_3_sudden_accelerate=fa_model_3_sudden_accelerate.get_eigenvalues()



series_factors_usual_drive=pd.Series(ev_usual_drive, range(1,10))
series_factors_long=pd.Series(ev_long, range(1,10))
series_factors_brakes_malfunction_tire=pd.Series(ev_brakes_malfunction_tire, range(1,10))
series_factors_AT_from_1_to_2=pd.Series(ev_AT_from_1_to_2, range(1,10))
series_factors_3_sudden_accelerate=pd.Series(ev_3_sudden_accelerate, range(1,10))



plot_df(series_factors_usual_drive, "Собственные значения факторов. Набор данных 'usual_drive'", "Собственное значение","factors_usual_drive")
plot_df(series_factors_long, "Собственные значения факторов. Набор данных 'long'", "Собственное значение","factors_long")
plot_df(series_factors_brakes_malfunction_tire, "Собственные значения факторов. Набор данных 'brakes_malfunction_tire'", "Собственное значение","factors_brakes_malfunction_tire")
plot_df(series_factors_AT_from_1_to_2, "Собственные значения факторов. Набор данных 'AT_from_1_to_2'", "Собственное значение","factors_AT_from_1_to_2")
plot_df(series_factors_3_sudden_accelerate, "Собственные значения факторов. Набор данных 'sudden_accelerate'", "Собственное значение","factors_3_sudden_accelerate")


sr_vehicle_speed=df_usual_drive["vehicle_speed"]
dates = pd.date_range('1900-1-1', periods=len(sr_vehicle_speed), freq='D')
sr_vehicle_speed.index=dates
sr_vehicle_speed_train=sr_vehicle_speed[:int(sr_vehicle_speed.size*0.5)]
sr_vehicle_speed_test=sr_vehicle_speed[int(sr_vehicle_speed.size*0.5):]
historical_data=sr_vehicle_speed_train[-100:]





