# 🚀 Instruções de Instalação e Execução

## Pré-requisitos
- Python 3.8+
- Node.js 18+
- npm ou yarn

## 📦 Instalação

### 1. Backend (Python/FastAPI)

```bash
cd backend
pip install -r requirements.txt
```

### 2. Frontend (Next.js/React)

```bash
cd frontend
npm install
```

## ⚙️ Configuração

### 1. Configurar API Key do Google Gemini

```bash
cd backend
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da API do Google Gemini:
```
GEMINI_KEY=sua_chave_api_aqui
```

### 2. Obter Chave da API Google Gemini
1. Acesse [Google AI Studio](https://aistudio.google.com/)
2. Crie uma nova API key
3. Copie a chave para o arquivo `.env`

## 🏃‍♂️ Execução

### 1. Iniciar Backend

```bash
cd backend
uvicorn app.main:app --reload
```

O backend estará disponível em: `http://localhost:8000`

### 2. Iniciar Frontend

```bash
cd frontend
npm run dev
```

O frontend estará disponível em: `http://localhost:3000`

## 🧪 Testando a Funcionalidade de Gráficos

### 1. Teste Rápido do Backend

```bash
cd backend
python demo.py
```

### 2. Teste Completo via Interface

1. Acesse `http://localhost:3000`
2. Faça upload de um arquivo CSV
3. Digite comandos como:
   - "Gere um gráfico"
   - "Criar histograma"
   - "Mostrar gráfico de barras"
   - "Gráfico de dispersão"

## 📊 Comandos de Gráficos Suportados

- **Histograma**: "gere um histograma", "distribuição"
- **Dispersão**: "scatter plot", "gráfico de dispersão"
- **Barras**: "gráfico de barras", "bar chart"
- **Pizza**: "gráfico de pizza", "pie chart"
- **Linha**: "gráfico de linha", "line plot"
- **Boxplot**: "boxplot", "diagrama de caixa"
- **Mapa de Calor**: "heatmap", "mapa de calor", "correlação"

## 🛠️ Solução de Problemas

### Erro: "Cannot find module 'react'"
```bash
cd frontend
npm install
```

### Erro: "ModuleNotFoundError: No module named 'matplotlib'"
```bash
cd backend
pip install matplotlib seaborn
```

### Erro: "GEMINI_KEY not found"
- Verifique se o arquivo `.env` existe no diretório `backend`
- Confirme se a variável `GEMINI_KEY` está definida

### Erro: "No DataFrame loaded"
- Primeiro faça upload de um arquivo CSV via interface
- O arquivo deve estar em formato CSV válido

## 📁 Estrutura do Projeto

```
eda_agent/
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── services/
│   │   └── singletons/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   └── app/
│   └── package.json
└── README.md
```

## 🎯 Próximos Passos

Após a instalação bem-sucedida:

1. **Upload de Dados**: Teste com diferentes tipos de CSV
2. **Comandos Variados**: Experimente diferentes formas de solicitar gráficos
3. **Análise Combinada**: Use análises textuais junto com gráficos
4. **Performance**: Teste com datasets maiores

## 🐛 Reportar Problemas

Se encontrar algum problema:
1. Verifique se todas as dependências estão instaladas
2. Confirme se ambos os servidores estão rodando
3. Verifique os logs no terminal para mais detalhes