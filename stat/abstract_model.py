import pandas
class AbstractModel:
    def __init__(self, historical_data:pandas.Series, std:float=0):
        self.historical_data=historical_data.copy()
        self.critical_std_deviations=2
        self.is_std_provided=False  
        self.std=std        
        if(self.std>0):
            self.is_std_provided=True
    def fit_hyper_parameters(self):
        pass          
    def fit_parameters(self):
        pass    
    def calc_interval(self):
        if(not self.is_std_provided):
            self.std=self.historical_data.std()
        self.upper_bound=self.prediction+self.critical_std_deviations*self.std
        self.lower_bound=self.prediction-self.critical_std_deviations*self.std    
    def update_data(self, observation):  
        self.historical_data=pandas.concat([self.historical_data, observation])
        self.historical_data=self.historical_data[1:]   
    def predict(self):
        pass    
    def anomaly_detect(self, observation):
        return observation>self.upper_bound or observation<self.lower_bound







