import pandas as pd
from io import StringIO
from app.singletons.csv_data_singleton import CSVDataSingleton

def process_csv(content: bytes) -> dict:
    """
    Processa o conteúdo de um arquivo CSV, salva em singleton como DataFrame e retorna info básica.
    """
    decoded = content.decode('utf-8')
    df = pd.read_csv(StringIO(decoded))
    CSVDataSingleton().set_df(df)
    return {
        "columns": df.columns.tolist(),
        "rows": df.shape[0],
        "preview": df.head(5).to_dict(orient="records")
    }