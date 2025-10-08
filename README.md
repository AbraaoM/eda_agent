# EDA Agent - Sistema de Análise Exploratória de Dados com Gráficos

Este projeto implementa um sistema de análise exploratória de dados que permite gerar gráficos automaticamente através de comandos em linguagem natural.

## Funcionalidades Implementadas

### 📊 Geração de Gráficos
O sistema agora detecta automaticamente quando o usuário solicita um gráfico e gera visualizações baseadas nos dados carregados.

**Comandos suportados:**
- `gere um gráfico`
- `criar gráfico` 
- `mostrar histograma`
- `gráfico de dispersão`
- `gráfico de barras`
- `gráfico de pizza`
- `boxplot`
- `mapa de calor`
- `gráfico de linha`

### 🎨 Tipos de Gráficos Disponíveis

1. **Histograma** - Para distribuição de dados numéricos
2. **Dispersão (Scatter)** - Para relação entre duas variáveis
3. **Linha** - Para dados temporais ou sequenciais  
4. **Barras** - Para dados categóricos
5. **Pizza** - Para proporções de categorias
6. **Boxplot** - Para análise de distribuição e outliers
7. **Mapa de Calor** - Para correlações entre variáveis

## Configuração

### Backend
1. Instale as dependências:
```bash
cd backend
pip install -r requirements.txt
```

2. Configure a API Key do Google Gemini:
```bash
cp .env.example .env
# Edite o arquivo .env e adicione sua GEMINI_KEY
```

3. Execute o servidor:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Frontend
1. Instale as dependências:
```bash
cd frontend
npm install
```

2. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

## Como Usar

1. **Upload de Dados**: Faça upload de um arquivo CSV através da interface
2. **Análise com Gráficos**: Digite comandos como:
   - "Gere um histograma da coluna idade"
   - "Mostrar gráfico de barras das vendas por categoria"
   - "Criar um scatter plot entre preço e quantidade"
   - "Gere um mapa de calor das correlações"

3. **Análise Textual**: Continue usando comandos normais para análises textuais:
   - "Qual a média das vendas?"
   - "Quantos registros temos?"
   - "Descreva os dados"

## Arquitetura

### Backend (`/backend`)
- **`services/plot_service.py`**: Serviço responsável pela geração de gráficos
- **`services/agent_service.py`**: Agente principal que detecta quando gerar gráficos
- **`controllers/prompt_controller.py`**: Endpoint que processa prompts
- **`services/csv_service.py`**: Serviço de upload de CSV
- **`singletons/csv_data_singleton.py`**: Singleton para dados CSV

### Frontend (`/frontend`)
- **`components/Chat.tsx`**: Interface de chat que suporta exibição de imagens
- **`services/promptService.ts`**: Serviço que comunica com o backend

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web
- **LangChain**: Para agentes LLM
- **Google Gemini**: Modelo de linguagem
- **Matplotlib/Seaborn**: Geração de gráficos
- **Pandas**: Manipulação de dados

### Frontend  
- **Next.js**: Framework React
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Estilização

## Exemplo de Uso

```
Usuário: "Gere um gráfico de barras das vendas por região"

Sistema:
1. Detecta a palavra-chave "gráfico"
2. Identifica o tipo (barras)
3. Gera visualização usando matplotlib
4. Retorna análise textual + imagem base64
5. Frontend exibe texto + gráfico na interface
```

## Melhorias Futuras

- [ ] Suporte a mais tipos de gráficos (violin plot, área, etc.)
- [ ] Personalização de cores e estilos
- [ ] Export de gráficos em diferentes formatos
- [ ] Gráficos interativos com Plotly
- [ ] Análise de múltiplos datasets simultaneamente