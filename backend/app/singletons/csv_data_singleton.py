import pandas as pd
from typing import Optional

class CSVDataSingleton:
    _instance = None
    df: Optional[pd.DataFrame] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CSVDataSingleton, cls).__new__(cls)
        return cls._instance

    def set_df(self, df: pd.DataFrame):
        self.df = df

    def get_df(self) -> Optional[pd.DataFrame]:
        return self.df