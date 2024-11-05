import os
import pandas as pd
import pyreadstat

from utils import MetaData

class FileReader:
    def __init__(self):
        pass

    def read_stata(self, path:str):
        df, pyreadstat_metadata = pyreadstat.read_dta(path)
        return (df, MetaData.wrap(pyreadstat_metadata))

class DataManager:
    def __init__(self):
        self.file_reader = FileReader()

        self.data_path:str = None
        self.df:pd.DataFrame = None
        self.metadata:MetaData = None

        self.results = None
        self.matrix = None

        #self.read("sysuse/auto.dta")

    def read(self, path):
        stata_data = self.file_reader.read_stata(path=path)
        self.df, self.metadata = stata_data
        self.data_path = path

    def clear(self):
        self.data_path = None
        self.df = None
        self.metadata = None

    @property
    def file_size(self):
        return os.path.getsize(self.data_path)
    
    @property
    def memory_usage(self):
        return self.df.memory_usage(deep=True).sum()



    