import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64
from typing import Optional
import numpy as np

class PlotService:
    """
    Serviço responsável por gerar gráficos a partir de dados do DataFrame.
    """
    
    @staticmethod
    def generate_plot(df: pd.DataFrame, plot_command: str) -> Optional[str]:
        """
        Gera um gráfico baseado no comando fornecido e retorna como base64.
        
        Args:
            df: DataFrame com os dados
            plot_command: Comando de plotagem em linguagem natural
            
        Returns:
            String base64 da imagem do gráfico ou None em caso de erro
        """
        try:
            # Configura o estilo dos gráficos
            plt.style.use('dark_background')
            sns.set_palette("husl")
            
            # Cria figura com tamanho adequado
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#1f2937')
            ax.set_facecolor('#1f2937')
            
            # Detecta o tipo de gráfico baseado no comando
            command_lower = plot_command.lower()
            
            if any(word in command_lower for word in ['histograma', 'histogram', 'distribuição', 'distribution']):
                PlotService._create_histogram(df, ax, command_lower)
            elif any(word in command_lower for word in ['scatter', 'dispersão', 'pontos']):
                PlotService._create_scatter(df, ax, command_lower)
            elif any(word in command_lower for word in ['linha', 'line', 'temporal', 'tempo']):
                PlotService._create_line_plot(df, ax, command_lower)
            elif any(word in command_lower for word in ['barra', 'bar', 'coluna']):
                PlotService._create_bar_plot(df, ax, command_lower)
            elif any(word in command_lower for word in ['pizza', 'pie', 'setores']):
                PlotService._create_pie_chart(df, ax, command_lower)
            elif any(word in command_lower for word in ['boxplot', 'caixa', 'box']):
                PlotService._create_boxplot(df, ax, command_lower)
            elif any(word in command_lower for word in ['heatmap', 'mapa de calor', 'correlação']):
                PlotService._create_heatmap(df, ax, command_lower)
            else:
                # Gráfico padrão - histograma da primeira coluna numérica
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    df[numeric_cols[0]].hist(ax=ax, bins=20, alpha=0.7, color='skyblue')
                    ax.set_title(f'Histograma de {numeric_cols[0]}', color='white', fontsize=14)
                    ax.set_xlabel(numeric_cols[0], color='white')
                    ax.set_ylabel('Frequência', color='white')
                else:
                    ax.text(0.5, 0.5, 'Nenhuma coluna numérica encontrada', 
                           transform=ax.transAxes, ha='center', va='center', 
                           color='white', fontsize=12)
            
            # Ajusta layout e salva em buffer
            plt.tight_layout()
            
            # Converte para base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', facecolor='#1f2937', 
                       edgecolor='none', bbox_inches='tight', dpi=100)
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            plt.close(fig)
            buffer.close()
            
            return image_base64
            
        except Exception as e:
            print(f"Erro ao gerar gráfico: {e}")
            plt.close('all')
            return None
    
    @staticmethod
    def _create_histogram(df: pd.DataFrame, ax, command: str):
        """Cria histograma"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # Tenta identificar a coluna pelo comando
            col_name = numeric_cols[0]
            for col in numeric_cols:
                if col.lower() in command:
                    col_name = col
                    break
            
            df[col_name].hist(ax=ax, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax.set_title(f'Histograma de {col_name}', color='white', fontsize=14)
            ax.set_xlabel(col_name, color='white')
            ax.set_ylabel('Frequência', color='white')
            ax.tick_params(colors='white')
    
    @staticmethod
    def _create_scatter(df: pd.DataFrame, ax, command: str):
        """Cria gráfico de dispersão"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            x_col, y_col = numeric_cols[0], numeric_cols[1]
            ax.scatter(df[x_col], df[y_col], alpha=0.6, c='skyblue')
            ax.set_title(f'Dispersão: {x_col} vs {y_col}', color='white', fontsize=14)
            ax.set_xlabel(x_col, color='white')
            ax.set_ylabel(y_col, color='white')
            ax.tick_params(colors='white')
    
    @staticmethod
    def _create_line_plot(df: pd.DataFrame, ax, command: str):
        """Cria gráfico de linha"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col_name = numeric_cols[0]
            ax.plot(df.index, df[col_name], color='skyblue', linewidth=2)
            ax.set_title(f'Linha: {col_name}', color='white', fontsize=14)
            ax.set_xlabel('Índice', color='white')
            ax.set_ylabel(col_name, color='white')
            ax.tick_params(colors='white')
    
    @staticmethod
    def _create_bar_plot(df: pd.DataFrame, ax, command: str):
        """Cria gráfico de barras"""
        # Tenta encontrar uma coluna categórica e uma numérica
        cat_cols = df.select_dtypes(include=['object']).columns
        num_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(cat_cols) > 0 and len(num_cols) > 0:
            cat_col = cat_cols[0]
            num_col = num_cols[0]
            
            # Agrupa por categoria e soma
            grouped = df.groupby(cat_col)[num_col].sum().head(10)
            grouped.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title(f'Barras: {num_col} por {cat_col}', color='white', fontsize=14)
            ax.set_xlabel(cat_col, color='white')
            ax.set_ylabel(num_col, color='white')
            ax.tick_params(colors='white')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    @staticmethod
    def _create_pie_chart(df: pd.DataFrame, ax, command: str):
        """Cria gráfico de pizza"""
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            col_name = cat_cols[0]
            value_counts = df[col_name].value_counts().head(8)
            colors = plt.cm.Set3(np.linspace(0, 1, len(value_counts)))
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', 
                   colors=colors, textprops={'color': 'white'})
            ax.set_title(f'Pizza: {col_name}', color='white', fontsize=14)
    
    @staticmethod
    def _create_boxplot(df: pd.DataFrame, ax, command: str):
        """Cria boxplot"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col_name = numeric_cols[0]
            bp = ax.boxplot(df[col_name].dropna(), patch_artist=True)
            bp['boxes'][0].set_facecolor('skyblue')
            ax.set_title(f'Boxplot: {col_name}', color='white', fontsize=14)
            ax.set_ylabel(col_name, color='white')
            ax.tick_params(colors='white')
    
    @staticmethod
    def _create_heatmap(df: pd.DataFrame, ax, command: str):
        """Cria mapa de calor de correlação"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu', center=0, 
                       ax=ax, cbar_kws={'label': 'Correlação'})
            ax.set_title('Mapa de Calor - Correlação', color='white', fontsize=14)
            ax.tick_params(colors='white')