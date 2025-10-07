import pandas as pd
from typing import Optional, Dict, Any

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

    def create_row(self, data: Dict[str, Any]) -> str:
        """
        Adiciona uma nova linha ao DataFrame.
        """
        if self.df is None:
            return "Nenhum DataFrame carregado."
        self.df = pd.concat([self.df, pd.DataFrame([data])], ignore_index=True)
        return "Linha adicionada com sucesso."

    def read_row(self, index: int) -> Dict[str, Any]:
        """
        Retorna uma linha do DataFrame pelo índice.
        """
        if self.df is None:
            return {"error": "Nenhum DataFrame carregado."}
        if index < 0 or index >= len(self.df):
            return {"error": "Índice fora do intervalo."}
        return self.df.iloc[index].to_dict()

    def update_row(self, index: int, data: Dict[str, Any]) -> str:
        """
        Atualiza uma linha do DataFrame pelo índice.
        """
        if self.df is None:
            return "Nenhum DataFrame carregado."
        if index < 0 or index >= len(self.df):
            return "Índice fora do intervalo."
        for key, value in data.items():
            if key in self.df.columns:
                self.df.at[index, key] = value
        return "Linha atualizada com sucesso."

    def delete_row(self, index: int) -> str:
        """
        Remove uma linha do DataFrame pelo índice.
        """
        if self.df is None:
            return "Nenhum DataFrame carregado."
        if index < 0 or index >= len(self.df):
            return "Índice fora do intervalo."
        self.df = self.df.drop(self.df.index[index]).reset_index(drop=True)
        return "Linha removida com sucesso."

    def execute_query(self, query: str) -> str:
        """
        Executa uma query no DataFrame em memória usando pandas.DataFrame.query().
        Retorna o resultado formatado como string (tabela).
        Exemplo de query: "coluna1 > 10 and coluna2 == 'valor'"
        """
        if self.df is None:
            return "Nenhum DataFrame carregado."
        try:
            result = self.df.query(query)
            if result.empty:
                return "Nenhum resultado encontrado."
            return result.to_string(index=False)
        except Exception as e:
            return f"Erro ao executar a query: {str(e)}"