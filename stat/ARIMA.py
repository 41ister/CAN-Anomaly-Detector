import pandas
import itertools
from statsmodels.tsa.arima.model import ARIMA
from Abstract_model import AbstractModel
class ARIMA_Model(AbstractModel):
    def __init__(self, historicalData: pandas.Series, p=0,d=0,q=0):
        super().__init__(historicalData)
        self.p=p
        self.d=d
        self.q=q
        if(p==0 and d==0 and q==0):
            self.fitHyperParameters()
    def fitHyperParameters(self):
        p=d=q = range(0,3)        
        aics =[]
        combs={}
        pdq = list(itertools.product(p,d,q))
        for combination in pdq:
            try:
                model = ARIMA(self.historicalData, order=combination)
                model = model.fit()
                combs.update({model.aic : combination})
                aics.append(model.aic)
            except:
               continue
        best_aic = min(aics)
        self.p=combs[best_aic][0]
        self.d=combs[best_aic][1]
        self.q=combs[best_aic][2]
    def fitParameters(self):
        model = ARIMA(self.historicalData, order=(self.p,self.d,self.q))
        self.model_fit = model.fit()
    def predict(self):
        forecast=self.model_fit.get_forecast(1)
        conf_i_forecast=forecast.conf_int(alpha=0.05)    
        self.lowerBound= conf_i_forecast[conf_i_forecast.columns[0]][0]
        self.upperBound= conf_i_forecast[conf_i_forecast.columns[1]][0]
        return forecast.predicted_mean
    def updatelData(self, observation):
        self.model_fit=self.model_fit.append(observation)

    

