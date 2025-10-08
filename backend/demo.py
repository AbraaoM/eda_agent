"""
Script de demonstração das funcionalidades de plotagem implementadas.
Execute este script para testar se tudo está funcionando corretamente.
"""

import sys
import os

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_plot_detection():
    """Testa a detecção de comandos de plotagem"""
    from app.services.agent_service import DataFrameAgent
    
    agent = DataFrameAgent()
    
    # Comandos que devem gerar gráficos
    plot_commands = [
        "gere um gráfico",
        "criar gráfico de barras", 
        "mostrar histograma",
        "gráfico de dispersão",
        "plotar dados",
        "visualizar correlação"
    ]
    
    # Comandos que NÃO devem gerar gráficos
    normal_commands = [
        "qual a média?",
        "quantos registros temos?",
        "descreva os dados",
        "análise estatística"
    ]
    
    print("🧪 Testando detecção de comandos de plotagem...")
    
    # Simula a detecção (sem precisar de dados reais)
    plot_keywords = [
        "gere um gráfico", "criar gráfico", "plot", "gráfico", 
        "visualizar", "mostrar gráfico", "plotar", "chart",
        "histograma", "scatter", "dispersão", "linha", "barra",
        "pizza", "boxplot", "heatmap", "mapa de calor"
    ]
    
    print("\n✅ Comandos que DEVEM gerar gráficos:")
    for cmd in plot_commands:
        should_plot = any(keyword in cmd.lower() for keyword in plot_keywords)
        status = "✅" if should_plot else "❌"
        print(f"  {status} '{cmd}' -> {should_plot}")
    
    print("\n❌ Comandos que NÃO devem gerar gráficos:")
    for cmd in normal_commands:
        should_plot = any(keyword in cmd.lower() for keyword in plot_keywords)
        status = "❌" if not should_plot else "✅"
        print(f"  {status} '{cmd}' -> {should_plot}")

def test_plot_service():
    """Testa o serviço de plotagem com dados simulados"""
    try:
        import pandas as pd
        import numpy as np
        from app.services.plot_service import PlotService
        
        print("\n📊 Testando geração de gráficos...")
        
        # Cria dados de teste
        np.random.seed(42)
        test_data = {
            'vendas': np.random.uniform(100, 1000, 100),
            'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], 100),
            'idade': np.random.randint(18, 65, 100),
            'salario': np.random.normal(5000, 1500, 100)
        }
        
        df = pd.DataFrame(test_data)
        print(f"  📋 Dataset de teste criado: {df.shape}")
        
        # Testa diferentes tipos de gráfico
        plot_tests = [
            ("histograma", "gere um histograma"),
            ("barras", "gráfico de barras"),
            ("dispersão", "scatter plot"),
            ("pizza", "gráfico de pizza"),
            ("boxplot", "criar boxplot")
        ]
        
        success_count = 0
        for plot_type, command in plot_tests:
            try:
                result = PlotService.generate_plot(df, command)
                if result and len(result) > 1000:  # Base64 deve ter tamanho razoável
                    print(f"  ✅ {plot_type}: OK ({len(result)} chars)")
                    success_count += 1
                else:
                    print(f"  ❌ {plot_type}: Falhou")
            except Exception as e:
                print(f"  ❌ {plot_type}: Erro - {e}")
        
        print(f"\n📈 Resultado: {success_count}/{len(plot_tests)} gráficos gerados com sucesso")
        
        if success_count == len(plot_tests):
            print("🎉 Todos os tipos de gráfico funcionaram!")
        elif success_count > 0:
            print("⚠️  Alguns gráficos funcionaram, verifique as dependências")
        else:
            print("🚨 Nenhum gráfico foi gerado. Verifique as dependências matplotlib/seaborn")
            
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Instale as dependências: pip install matplotlib seaborn pandas numpy")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def main():
    print("🚀 Demonstração do Sistema EDA Agent com Gráficos")
    print("=" * 50)
    
    # Testa detecção de comandos
    test_plot_detection()
    
    # Testa geração de gráficos
    test_plot_service()
    
    print("\n" + "=" * 50)
    print("✨ Para testar completamente:")
    print("1. Execute o backend: uvicorn app.main:app --reload")
    print("2. Execute o frontend: npm run dev")
    print("3. Faça upload de um CSV")
    print("4. Digite: 'gere um gráfico'")

if __name__ == "__main__":
    main()