import pandas
import itertools
from statsmodels.tsa.arima.model import ARIMA
from abstract_model import AbstractModel
class MaModel(AbstractModel):
    def __init__(self, historical_data: pandas.Series, std:float=0, q:int=0):
        super().__init__(historical_data, std)
        self.q=q          
        if(self.q==0):
            self.max_q=50
            self.fit_hyper_parameters()          
    def fit_hyper_parameters(self):
        q=range(0,self.max_q+1)
        p=range(0,1)
        d=range(0,1)        
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
        self.q=combs[best_aic][2]      
    def fit_parameters(self):
        model = ARIMA(self.historical_data, order=(0,0,self.q))
        self.model_fit = model.fit()   
        self.resid=self.model_fit.resid
    def predict(self):
        self.prediction=self.model_fit.params[0]       
        for i in range(1, self.q+1):
            self.prediction += self.model_fit.maparams[i-1]*self.resid[-i]            
        self.calc_interval()
        self.time_delta=self.historical_data.index[-1]-self.historical_data.index[-2]
        return pandas.Series([self.prediction],[self.historical_data.index[-1]+self.time_delta])
    def update_data(self, observation):
        super().update_data(observation)
        error=observation[0]-self.prediction
        self.resid=pandas.concat([self.resid, pandas.Series([error],[self.resid.index[-1]+self.time_delta])])
        self.resid=self.resid[1:]   
    def old_predict(self):
        self.prediction=self.model_fit.forecast(1)[0]
        self.calc_interval()
        time_delta=self.historical_data.index[-1]-self.historical_data.index[-2]
        return pandas.Series([self.prediction],[self.historical_data.index[-1]+time_delta])
    def old_update_data(self, observation):
        super().update_data(observation)
        self.model_fit=self.model_fit.append(observation)

    

