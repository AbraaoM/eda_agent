from app.singletons.csv_data_singleton import CSVDataSingleton

from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

class DataFrameAgent:
    """
    Agente que opera sobre um DataFrame carregado em tempo de execução via singleton.
    Permite executar comandos e consultas sobre os dados, com suporte a LLM Google Generative AI.
    """

    def __init__(self):
        load_dotenv()
        GEMINI_KEY = os.getenv("GEMINI_KEY")

        self.singleton = CSVDataSingleton()
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=GEMINI_KEY)

    def handle_prompt(self, prompt: str) -> str:
        """
        Recebe um prompt e executa operações no DataFrame ou repassa para a LLM via agente pandas.
        """
        df = self.singleton.get_df()
        if df is None:
            return "Nenhum DataFrame carregado."

        try:
            agent = create_pandas_dataframe_agent(self.llm, df, verbose=False)
            result = agent.run(prompt)
            return str(result)
        except Exception as e:
            return f"Erro ao processar com LLM: {e}"

# Instância global do agente para uso nos endpoints
agent = DataFrameAgent()