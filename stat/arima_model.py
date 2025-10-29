import pandas
import itertools
from statsmodels.tsa.arima.model import ARIMA
from abstract_model import AbstractModel
class ArimaModel(AbstractModel):
    def __init__(self, historical_data: pandas.Series, std:float=0, p:int=0, d:int=0, q:int=0):
        super().__init__(historical_data, std)
        self.p=p
        self.d=d
        self.q=q        
        if(self.p==0 and self.d==0 and self.q==0):
            self.max_p_q=50
            self.max_d=2
            self.fit_hyper_parameters()          
    def fit_hyper_parameters(self):
        p=q=range(0,self.max_p_q+1)        
        d=range(0,self.max_d+1)
        aics =[]
        combs={}
        pdq = list(itertools.product(p,d,q))
        for combination in pdq:
            try:
                model=ARIMA(self.historical_data, order=combination)
                model=model.fit()
                combs.update({model.aic : combination})
                aics.append(model.aic)
            except:
               continue
        best_aic = min(aics)
        self.p=combs[best_aic][0]
        self.q=combs[best_aic][2]      
    def fit_parameters(self):
        model = ARIMA(self.historical_data, order=(self.p,self.d,self.q))
        self.model_fit = model.fit()   
        self.resid=self.model_fit.resid
        self.historical_data_diff=[]
        self.historical_data_diff.append(self.historical_data)
        for i in range(0, self.d):
            self.historical_data_diff.append(self.historical_data_diff[i].diff())  
    def predict(self):
        self.delta=0
        for i in range(0, self.d):
            self.delta+=self.historical_data_diff[i][-1]
        self.prediction_diff=0       
        for i in range(1, self.p+1):
            self.prediction_diff += self.model_fit.arparams[i-1]*self.historical_data_diff[-1][-i]
        for i in range(1, self.q+1):
            self.prediction_diff += self.model_fit.maparams[i-1]*self.resid[-i]
        self.prediction=self.prediction_diff+self.delta
        self.calc_interval()
        self.time_delta=self.historical_data.index[-1]-self.historical_data.index[-2]
        return pandas.Series([self.prediction],[self.historical_data.index[-1]+self.time_delta])
    def update_data(self, observation):
        super().update_data(observation)
        error=observation[0]-self.prediction        
        self.resid=pandas.concat([self.resid, pandas.Series([error],[self.resid.index[-1]+self.time_delta])])
        self.resid=self.resid[1:]
        self.historical_data_diff[0]=self.historical_data
        for i in range(0, self.d):
            diff=self.historical_data_diff[i][-1]-self.historical_data_diff[i][-2]
            self.historical_data_diff[i+1]=pandas.concat([self.historical_data_diff[i+1], pandas.Series([diff],[self.historical_data_diff[i+1].index[-1]+self.time_delta])])
            self.historical_data_diff[i+1]=self.historical_data_diff[i+1][1:]

    def old_predict(self):
        prediction=self.model_fit.forecast(1)
        self.prediction=prediction[0]
        self.calc_interval()
        return prediction
    def old_update_data(self, observation):
        super().update_data(observation)
        self.model_fit=self.model_fit.append(observation)
   
    