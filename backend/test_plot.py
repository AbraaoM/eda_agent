import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.plot_service import PlotService
import pandas as pd
import numpy as np

# Criar dados de teste
np.random.seed(42)
test_data = {
    'coluna_numerica_1': np.random.normal(100, 15, 1000),
    'coluna_numerica_2': np.random.normal(50, 10, 1000),
    'categoria': np.random.choice(['A', 'B', 'C', 'D'], 1000),
    'vendas': np.random.uniform(10, 1000, 1000)
}

df = pd.DataFrame(test_data)

# Testar geração de gráfico
print("Testando geração de gráfico...")
plot_base64 = PlotService.generate_plot(df, "gere um histograma")

if plot_base64:
    print("✅ Gráfico gerado com sucesso!")
    print(f"Tamanho da string base64: {len(plot_base64)} caracteres")
else:
    print("❌ Erro ao gerar gráfico")