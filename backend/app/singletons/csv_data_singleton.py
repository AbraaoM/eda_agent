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

    def search(self, query: str) -> str:
        """
        Executa uma busca simples no DataFrame, retornando linhas que contenham o termo em qualquer coluna.
        Retorna o resultado em formato string (CSV).
        """
        if self.df is None:
            return "Nenhum DataFrame carregado."
        mask = self.df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False)).any(axis=1)
        result_df = self.df[mask]
        if result_df.empty:
            return "Nenhum resultado encontrado."
        return result_df.to_csv(index=False)