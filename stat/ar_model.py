import pandas
import itertools
from statsmodels.tsa.arima.model import ARIMA
from abstract_model import AbstractModel
class ArModel(AbstractModel):
    def __init__(self, historical_data: pandas.Series, std:float=0, p:int=0):
        super().__init__(historical_data, std)
        self.p=p
        if(self.p==0):
            self.max_p=50
            self.fit_hyper_parameters()          
    def fit_hyper_parameters(self):
        p=range(0,self.max_p+1)
        d=range(0,1)
        q=range(0,1)
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
    def fit_parameters(self):
        model = ARIMA(self.historical_data, order=(self.p,0,0))
        self.model_fit = model.fit()               
        self.const=self.model_fit.params[0]
    def predict(self):        
        self.prediction=self.const
        for i in range(1, self.p+1):
            self.prediction += self.model_fit.arparams[i-1]*(self.historical_data[-i]-self.const)        
        self.calc_interval()
        time_delta=self.historical_data.index[-1]-self.historical_data.index[-2]
        return pandas.Series([self.prediction],[self.historical_data.index[-1]+time_delta])
    def old_predict(self):
        self.prediction=self.model_fit.forecast(1)[0]
        self.calc_interval()
        time_delta=self.historical_data.index[-1]-self.historical_data.index[-2]
        return pandas.Series([self.prediction],[self.historical_data.index[-1]+time_delta])
    def old_update_data(self, observation):
        self.update_data(observation)
        self.model_fit=self.model_fit.append(observation)


    
    

