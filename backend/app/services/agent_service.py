from app.singletons.csv_data_singleton import CSVDataSingleton
from app.services.plot_service import PlotService

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

    def handle_prompt(self, prompt: str) -> dict:
        """
        Recebe um prompt e executa operações no DataFrame ou repassa para a LLM via agente pandas.
        Retorna um dicionário com o resultado e informação se contém gráfico.
        """
        df = self.singleton.get_df()
        if df is None:
            return {"result": "Nenhum DataFrame carregado.", "has_plot": False}

        try:
            # Verifica se o prompt solicita um gráfico
            plot_keywords = [
                "gere um gráfico", "criar gráfico", "plot", "gráfico", 
                "visualizar", "mostrar gráfico", "plotar", "chart",
                "histograma", "scatter", "dispersão", "linha", "barra",
                "pizza", "boxplot", "heatmap", "mapa de calor"
            ]
            
            should_generate_plot = any(keyword in prompt.lower() for keyword in plot_keywords)
            
            if should_generate_plot:
                # Gera o gráfico
                plot_base64 = PlotService.generate_plot(df, prompt)
                if plot_base64:
                    # Também gera uma análise textual usando o agente
                    agent = create_pandas_dataframe_agent(self.llm, df, verbose=False, allow_dangerous_code=True)
                    analysis_prompt = f"Analise os dados e forneça insights sobre o que foi solicitado: {prompt}. Seja breve e objetivo."
                    text_result = agent.run(analysis_prompt)
                    
                    return {
                        "result": str(text_result),
                        "has_plot": True,
                        "plot_image": plot_base64
                    }
                else:
                    return {"result": "Erro ao gerar o gráfico solicitado.", "has_plot": False}
            else:
                # Processamento normal sem gráfico
                agent = create_pandas_dataframe_agent(self.llm, df, verbose=False, allow_dangerous_code=True)
                result = agent.run(prompt)
                return {"result": str(result), "has_plot": False}
                
        except Exception as e:
            return {"result": f"Erro ao processar com LLM: {e}", "has_plot": False}

# Instância global do agente para uso nos endpoints
agent = DataFrameAgent()