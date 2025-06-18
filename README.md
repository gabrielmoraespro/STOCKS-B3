# 🎯 Analisador Global de Ações

Sistema completo de análise e varredura global de ações com foco em identificar oportunidades de recuperação assimétrica.

![Dashboard Amplo](https://github.com/gabrielmoraespro/STOCKS-B3/blob/main/stocks-img-1.PNG)


## 🚀 Características Principais

- **100% Gratuito**: Utiliza apenas APIs e ferramentas gratuitas
- **Análise Individual**: Diagnóstico completo de qualquer ação
- **Varredura Global**: Identifica automaticamente as melhores oportunidades mundiais
- **IA Integrada**: Análise de sentimento de notícias
- **Interface Moderna**: Dashboard intuitivo via Streamlit
- **Cache Inteligente**: Otimização de performance com banco SQLite


![Dashboard Amplo](https://github.com/gabrielmoraespro/STOCKS-B3/blob/main/stocks-img-2.PNG)



## 📊 Funcionalidades

### Análise Individual
- Inserir código da ação → Análise completa instantânea
- Indicadores fundamentalistas (P/L, ROE, Dívida/Patrimônio, etc.)
- Análise técnica (Drawdown, Volatilidade, RSI)
- Sentimento de notícias com IA
- Recomendação final: COMPRAR/AGUARDAR/EVITAR
- Gráficos interativos de preços


![Dashboard Amplo](https://github.com/gabrielmoraespro/STOCKS-B3/blob/main/stocks-img-3.PNG)




### Varredura Global
- Análise automática de milhares de ações mundiais
- Filtros personalizáveis (Drawdown, P/L, ROE)
- Ranking das melhores oportunidades
- Cobertura global: EUA, Brasil, Europa, Ásia
- Análise por setores

### Métricas Avançadas
- Score de Oportunidade (0-100)
- Análise de risco fundamentalista
- Potencial de recuperação assimétrica
- Correlação entre ativos
- Sugestão de pesos para portfólio


![Dashboard Amplo](https://github.com/gabrielmoraespro/STOCKS-B3/blob/main/stocks-img-4.PNG)




## 🛠️ Tecnologias Utilizadas

### APIs Gratuitas
- **Yahoo Finance**: Dados de ações globais
- **Google News RSS**: Notícias financeiras
- **Banco Central Brasil**: Indicadores macroeconômicos
- **FRED API**: Dados econômicos dos EUA

### IA e Machine Learning
- **HuggingFace Transformers**: Análise de sentimento
- **Modelos locais**: Processamento offline
- **OpenRouter**: Modelos gratuitos (opcional)

### Stack Técnica
- **Python 3.8+**: Linguagem principal
- **Streamlit**: Interface web
- **SQLite**: Banco de dados local
- **Pandas/NumPy**: Processamento de dados
- **Plotly**: Visualizações interativas
- **yfinance**: Dados financeiros

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conexão com internet

### Instalação Automática

```bash
# Clone o repositório
git clone <repository-url>
cd analisador-acoes

# Execute a instalação
python setup.py install
```

### Instalação Manual

```bash
# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados
python -c "from main import DatabaseManager; DatabaseManager().init_database()"
```

## 🚀 Como Usar

### Execução Rápida
```bash
# Método 1: Script de execução
python run.py

# Método 2: Streamlit direto
streamlit run main.py

# Método 3: Windows (batch file)
run.bat
```

### Acesso ao Sistema
Após executar, acesse: `http://localhost:8501`

### Análise Individual
1. Digite o código da ação (ex: AAPL, PETR4.SA, ASML.AS)
2. Clique em "Analisar"
3. Visualize os resultados completos

### Varredura Global
1. Ajuste os filtros (Drawdown, P/L, ROE)
2. Clique em "Iniciar Varredura"
3. Aguarde a análise (pode levar alguns minutos)
4. Visualize o ranking de oportunidades

## 📈 Códigos de Ações Suportados

### Estados Unidos
- Nasdaq: AAPL, MSFT, GOOGL, AMZN, TSLA
- NYSE: JPM, JNJ, V, PG, UNH

### Brasil
- Bovespa: PETR4.SA, VALE3.SA, ITUB4.SA, BBDC4.SA

### Europa
- Holanda: ASML.AS, ADYEN.AS
- Alemanha: SAP.DE, BAS.DE, SIE.DE
- França: LVMH.PA, OR.PA

### Outros Mercados
- Suíça: NESN.SW, ROCHE.SW
- Reino Unido: Vários códigos .L

## ⚙️ Configurações Avançadas

### Filtros de Varredura
- **Drawdown Mínimo**: 10-70% (padrão: 25%)
- **P/L Máximo**: 5-50 (padrão: 25)
- **ROE Mínimo**: 5-30% (padrão: 10%)

### Cache e Performance
- Cache de dados: 2 horas (configurável)
- Máximo de ações por varredura: 100
- Timeout de API: 30 segundos

### Personalização
Edite o arquivo `config.py` para:
- Adicionar novos tickers
- Modificar indicadores
- Ajustar algoritmos de score

## 📊 Interpretação dos Resultados

### Score de Oportunidade (0-100)
- **80-100**: Oportunidade excepcional
- **60-79**: Boa oportunidade
- **40-59**: Oportunidade moderada
- **20-39**: Baixa oportunidade
- **0-19**: Evitar

### Recomendações
- **COMPRAR FORTE**: Score ≥ 75
- **COMPRAR**: Score 60-74
- **AGUARDAR**: Score 45-59
- **EVITAR**: Score 30-44
- **VENDER**: Score < 30

### Indicadores Chave
- **Drawdown**: Queda desde o pico (quanto maior, maior a oportunidade)
- **P/L**: Preço/Lucro (menor = mais barato)
- **ROE**: Retorno sobre patrimônio (maior = mais eficiente)
- **Dívida/Patrimônio**: Alavancagem (menor = mais seguro)

## 🔧 Solução de Problemas

### Erros Comuns

**Erro de instalação de dependências**
```bash
# Atualize pip primeiro
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Erro "Module not found"**
```bash
# Verifique se está no diretório correto
cd analisador-acoes
python -c "import sys; print(sys.path)"
```

**Timeout de API**
- Aguarde alguns minutos entre varreduras
- Verifique conexão com internet
- Reduza número de ações analisadas

**Problemas com modelos de IA**
```bash
# Instale transformers manualmente
pip install transformers torch --upgrade
```

### Performance

**Varredura muito lenta**
- Reduza filtros para analisar menos ações
- Use cache (aguarde entre varreduras)
- Feche outros programas

**Alto uso de memória**
- Reinicie a aplicação periodicamente
- Limpe cache do navegador
- Verifique disponibilidade de RAM

## 📋 Estrutura do Projeto

```
analisador-acoes/
├── main.py              # Aplicação principal
├── config.py            # Configurações e APIs
├── utils.py             # Funções utilitárias
├── setup.py             # Script de instalação
├── requirements.txt     # Dependências
├── README.md           # Esta documentação
├── run.py              # Script de execução
├── run.bat             # Execução Windows
└── stock_analysis.db   # Banco de dados (criado automaticamente)
```

## 🤝 Contribuições

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### Áreas para Contribuição
- Novos indicadores técnicos
- Suporte a mais mercados
- Melhorias na interface
- Otimizações de performance
- Documentação

## 📄 Licença

Este projeto é open-source e está disponível sob a licença MIT.

## 🆘 Suporte

### Documentação
- Acesse a ajuda integrada no sistema
- Consulte os comentários no código
- Verifique logs de erro

### Reportar Problemas
1. Descreva o erro detalhadamente
2. Inclua logs de erro
3. Especifique sistema operacional
4. Mencione versão do Python

## 🎯 Roadmap

### Versão 1.1
- [ ] Suporte a criptomoedas
- [ ] Análise de commodities
- [ ] Backtesting de estratégias
- [ ] Alertas por email

### Versão 1.2
- [ ] API própria
- [ ] Mobile app
- [ ] Mais indicadores técnicos
- [ ] Integração com brokers

### Versão 2.0
- [ ] Machine Learning avançado
- [ ] Predições de preços
- [ ] Portfolio tracking
- [ ] Social trading

## 🏆 Créditos

Desenvolvido com foco em democratizar análise financeira profissional usando apenas ferramentas gratuitas e open-source.

**Fontes de Dados:**
- Yahoo Finance (dados financeiros)
- Google News (notícias)
- Banco Central do Brasil (indicadores BR)
- Federal Reserve (indicadores EUA)

**Tecnologias:**
- Streamlit (interface)
- HuggingFace (IA)
- Plotly (gráficos)
- Pandas (análise de dados)

---

💡 **Lembre-se**: Este sistema é para fins educacionais e de pesquisa. Sempre consulte um consultor financeiro antes de investir.
