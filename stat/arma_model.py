import pandas
import itertools
from statsmodels.tsa.arima.model import ARIMA
from abstract_model import AbstractModel
class ArmaModel(AbstractModel):
    def __init__(self, historical_data: pandas.Series, std:float=0, p:int=0, q:int=0):
        super().__init__(historical_data, std)
        self.p=p
        self.q=q          
        if(self.p==0 and self.q==0):
            self.max_p_q=50
            self.fit_hyper_parameters()          
    def fit_hyper_parameters(self):
        p=q=range(0,self.max_p_q+1)
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
        self.p=combs[best_aic][0]
        self.q=combs[best_aic][2]      
    def fit_parameters(self):
        model = ARIMA(self.historical_data, order=(self.p,0,self.q))
        self.model_fit = model.fit()   
        self.resid=self.model_fit.resid
        self.const=self.model_fit.params[0]
    def predict(self):
        self.prediction=self.const
        for i in range(1, self.p+1):
            self.prediction += self.model_fit.arparams[i-1]*(self.historical_data[-i]-self.const) 
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

    

