import pandas
import math
from abstract_model import AbstractModel
class WhiteNoiseModel(AbstractModel):                     
    def predict(self):
       self.prediction=self.historical_data.mean()
       time_delta=self.historical_data.index[-1]-self.historical_data.index[-2]
       self.calc_interval()
       return pandas.Series([self.prediction],[self.historical_data.index[-1]+time_delta])
   
        
        
  
