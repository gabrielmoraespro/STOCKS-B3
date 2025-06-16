import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import sqlite3
import requests
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Analisador Global de Ações",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DatabaseManager:
    """Gerenciador do banco de dados SQLite"""
    
    def __init__(self, db_path="stock_analysis.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa as tabelas do banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de cache de dados de ações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_cache (
                ticker TEXT PRIMARY KEY,
                data TEXT,
                last_updated TIMESTAMP
            )
        ''')
        
        # Tabela de análises
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT,
                analysis_date TIMESTAMP,
                recommendation TEXT,
                score REAL,
                fundamentals TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def cache_stock_data(self, ticker, data):
        """Armazena dados de ações no cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO stock_cache (ticker, data, last_updated)
            VALUES (?, ?, ?)
        ''', (ticker, json.dumps(data), datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_cached_data(self, ticker, max_age_hours=2):
        """Recupera dados do cache se ainda válidos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT data, last_updated FROM stock_cache WHERE ticker = ?
        ''', (ticker,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            data, last_updated = result
            last_updated = datetime.fromisoformat(last_updated)
            if datetime.now() - last_updated < timedelta(hours=max_age_hours):
                return json.loads(data)
        
        return None

class DataCollector:
    """Coletor de dados financeiros de múltiplas fontes"""
    
    def __init__(self):
        self.db = DatabaseManager()
        # Inicializar modelo de sentimento
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis", 
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                return_all_scores=True
            )
        except:
            # Fallback para modelo mais simples
            self.sentiment_analyzer = pipeline("sentiment-analysis")
    
    def get_stock_data(self, ticker):
        """Coleta dados completos de uma ação"""
        # Verificar cache primeiro
        cached_data = self.db.get_cached_data(ticker)
        if cached_data:
            return cached_data
        
        try:
            stock = yf.Ticker(ticker)
            
            # Dados históricos (2 anos)
            hist = stock.history(period="2y")
            if hist.empty:
                return None
            
            # Informações fundamentais
            info = stock.info
            
            # Dados financeiros
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cashflow = stock.cashflow
            
            # Calcular métricas
            current_price = hist['Close'][-1]
            max_price_1y = hist['Close'][-252:].max()  # Último ano
            drawdown = ((current_price - max_price_1y) / max_price_1y) * 100
            
            # Volatilidade
            volatility = hist['Close'].pct_change().std() * np.sqrt(252) * 100
            
            data = {
                'ticker': ticker,
                'current_price': current_price,
                'max_price_1y': max_price_1y,
                'drawdown': drawdown,
                'volatility': volatility,
                'volume_avg': hist['Volume'][-30:].mean(),
                'pe_ratio': info.get('forwardPE', info.get('trailingPE', 0)),
                'pb_ratio': info.get('priceToBook', 0),
                'roe': info.get('returnOnEquity', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'profit_margin': info.get('profitMargins', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'market_cap': info.get('marketCap', 0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'hist_data': hist.tail(252).to_dict('records'),  # Último ano
                'last_updated': datetime.now().isoformat()
            }
            
            # Cache dos dados
            self.db.cache_stock_data(ticker, data)
            return data
            
        except Exception as e:
            st.error(f"Erro ao coletar dados para {ticker}: {str(e)}")
            return None
    
    def get_news_sentiment(self, ticker, company_name=None):
        """Coleta notícias e analisa sentimento"""
        try:
            # Usar Google News RSS (gratuito)
            search_term = company_name if company_name else ticker
            url = f"https://news.google.com/rss/search?q={search_term}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
            
            import feedparser
            feed = feedparser.parse(url)
            
            news_data = []
            sentiments = []
            
            for entry in feed.entries[:5]:  # Últimas 5 notícias
                title = entry.title
                published = entry.published
                link = entry.link
                
                # Análise de sentimento
                sentiment = self.sentiment_analyzer(title)
                if isinstance(sentiment, list) and len(sentiment) > 0:
                    sentiment_score = sentiment[0]['score'] if sentiment[0]['label'] == 'POSITIVE' else -sentiment[0]['score']
                else:
                    sentiment_score = 0
                
                news_data.append({
                    'title': title,
                    'published': published,
                    'link': link,
                    'sentiment': sentiment_score
                })
                
                sentiments.append(sentiment_score)
            
            avg_sentiment = np.mean(sentiments) if sentiments else 0
            
            return {
                'news': news_data,
                'avg_sentiment': avg_sentiment,
                'sentiment_trend': 'Positivo' if avg_sentiment > 0.1 else 'Negativo' if avg_sentiment < -0.1 else 'Neutro'
            }
            
        except Exception as e:
            st.warning(f"Não foi possível coletar notícias para {ticker}: {str(e)}")
            return {
                'news': [],
                'avg_sentiment': 0,
                'sentiment_trend': 'Neutro'
            }
    
    def get_global_tickers(self):
        """Retorna lista de tickers para varredura global"""
        tickers = {
            'EUA': [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'JNJ', 'V',
                'PG', 'UNH', 'HD', 'MA', 'DIS', 'PYPL', 'ADBE', 'NFLX', 'CRM', 'CMCSA',
                'VZ', 'T', 'PFE', 'INTC', 'CSCO', 'ABT', 'TMO', 'COST', 'AVGO', 'TXN'
            ],
            'Brasil': [
                'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'B3SA3.SA',
                'RENT3.SA', 'LREN3.SA', 'MGLU3.SA', 'WEGE3.SA', 'SUZB3.SA', 'RAIL3.SA',
                'VVAR3.SA', 'HAPV3.SA', 'PCAR3.SA', 'CSNA3.SA', 'USIM5.SA', 'GOAU4.SA'
            ],
            'Europa': [
                'ASML.AS', 'SAP.DE', 'LVMH.PA', 'NVO', 'NESN.SW', 'ROCHE.SW', 'TM',
                'BAS.DE', 'INGA.AS', 'ING.AS', 'SIE.DE', 'ADYEN.AS', 'OR.PA'
            ]
        }
        
        return tickers

class StockAnalyzer:
    """Analisador principal de ações"""
    
    def __init__(self):
        self.collector = DataCollector()
    
    def analyze_stock(self, ticker):
        """Análise completa de uma ação"""
        # Coletar dados
        data = self.collector.get_stock_data(ticker)
        if not data:
            return None
        
        # Análise de notícias
        news_data = self.collector.get_news_sentiment(ticker)
        
        # Calcular score de oportunidade
        score = self.calculate_opportunity_score(data, news_data)
        
        # Gerar recomendação
        recommendation = self.generate_recommendation(score, data)
        
        return {
            'data': data,
            'news': news_data,
            'score': score,
            'recommendation': recommendation
        }
    
    def calculate_opportunity_score(self, data, news_data):
        """Calcula score de oportunidade (0-100)"""
        score = 50  # Score base
        
        # Penalizar/premiar por drawdown
        drawdown = abs(data.get('drawdown', 0))
        if drawdown > 50:
            score += 20  # Grande oportunidade
        elif drawdown > 30:
            score += 15
        elif drawdown > 20:
            score += 10
        elif drawdown < 5:
            score -= 10  # Pouco upside
        
        # Fundamentals
        pe_ratio = data.get('pe_ratio', 0)
        if 0 < pe_ratio < 15:
            score += 15
        elif 15 <= pe_ratio < 25:
            score += 10
        elif pe_ratio > 35:
            score -= 10
        
        # ROE
        roe = data.get('roe', 0)
        if roe > 0.20:
            score += 15
        elif roe > 0.15:
            score += 10
        elif roe > 0.10:
            score += 5
        elif roe < 0:
            score -= 20
        
        # Debt to Equity
        debt_ratio = data.get('debt_to_equity', 0)
        if debt_ratio < 0.3:
            score += 10
        elif debt_ratio > 1.0:
            score -= 15
        
        # Crescimento de receita
        revenue_growth = data.get('revenue_growth', 0)
        if revenue_growth > 0.10:
            score += 10
        elif revenue_growth < -0.05:
            score -= 10
        
        # Sentimento das notícias
        sentiment = news_data.get('avg_sentiment', 0)
        if sentiment > 0.2:
            score += 5
        elif sentiment < -0.2:
            score -= 5
        
        # Margem de lucro
        profit_margin = data.get('profit_margin', 0)
        if profit_margin > 0.15:
            score += 10
        elif profit_margin < 0.05:
            score -= 10
        
        return max(0, min(100, score))
    
    def generate_recommendation(self, score, data):
        """Gera recomendação baseada no score"""
        if score >= 75:
            return "COMPRAR FORTE"
        elif score >= 60:
            return "COMPRAR"
        elif score >= 45:
            return "AGUARDAR"
        elif score >= 30:
            return "EVITAR"
        else:
            return "VENDER"
    
    def global_screening(self, min_drawdown=20, max_pe=30, min_roe=0.10):
        """Varredura global de oportunidades"""
        tickers_dict = self.collector.get_global_tickers()
        all_tickers = []
        for region, tickers in tickers_dict.items():
            all_tickers.extend([(ticker, region) for ticker in tickers])
        
        opportunities = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, (ticker, region) in enumerate(all_tickers):
            status_text.text(f'Analisando {ticker} ({region})... {i+1}/{len(all_tickers)}')
            progress_bar.progress((i + 1) / len(all_tickers))
            
            try:
                analysis = self.analyze_stock(ticker)
                if analysis and analysis['data']:
                    data = analysis['data']
                    
                    # Filtros para varredura
                    drawdown = abs(data.get('drawdown', 0))
                    pe_ratio = data.get('pe_ratio', 999)
                    roe = data.get('roe', 0)
                    
                    if (drawdown >= min_drawdown and 
                        pe_ratio <= max_pe and pe_ratio > 0 and
                        roe >= min_roe):
                        
                        opportunities.append({
                            'ticker': ticker,
                            'region': region,
                            'score': analysis['score'],
                            'drawdown': drawdown,
                            'pe_ratio': pe_ratio,
                            'roe': roe * 100,
                            'recommendation': analysis['recommendation'],
                            'sector': data.get('sector', 'N/A'),
                            'current_price': data.get('current_price', 0),
                            'market_cap': data.get('market_cap', 0)
                        })
            except:
                continue
        
        # Ordenar por score
        opportunities.sort(key=lambda x: x['score'], reverse=True)
        return opportunities[:20]  # Top 20

def create_price_chart(data):
    """Cria gráfico de preços com drawdown"""
    if not data or 'hist_data' not in data:
        return None
    
    hist_df = pd.DataFrame(data['hist_data'])
    if hist_df.empty:
        return None
    
    hist_df['Date'] = pd.to_datetime(hist_df['Date'])
    
    fig = go.Figure()
    
    # Gráfico de preços
    fig.add_trace(go.Scatter(
        x=hist_df['Date'],
        y=hist_df['Close'],
        mode='lines',
        name='Preço',
        line=dict(color='blue', width=2)
    ))
    
    # Máximo do período
    max_price = hist_df['Close'].max()
    fig.add_hline(
        y=max_price,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Máximo: ${max_price:.2f}"
    )
    
    fig.update_layout(
        title=f"Histórico de Preços - {data['ticker']}",
        xaxis_title="Data",
        yaxis_title="Preço ($)",
        height=400,
        showlegend=True
    )
    
    return fig

def main():
    """Função principal da aplicação"""
    st.title("🎯 Analisador Global de Ações")
    st.subheader("Encontre oportunidades de recuperação assimétrica")
    
    analyzer = StockAnalyzer()
    
    # Sidebar
    st.sidebar.title("⚙️ Configurações")
    
    # Abas principais
    tab1, tab2 = st.tabs(["📊 Análise Individual", "🌍 Varredura Global"])
    
    with tab1:
        st.header("Análise Individual de Ação")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            ticker_input = st.text_input(
                "Digite o código da ação:", 
                placeholder="Ex: AAPL, PETR4.SA, ASML.AS"
            )
        with col2:
            analyze_button = st.button("🔍 Analisar", type="primary")
        
        if analyze_button and ticker_input:
            with st.spinner(f"Analisando {ticker_input.upper()}..."):
                analysis = analyzer.analyze_stock(ticker_input.upper())
                
                if analysis:
                    data = analysis['data']
                    
                    # Métricas principais
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Preço Atual", 
                            f"${data.get('current_price', 0):.2f}",
                            f"{data.get('drawdown', 0):.1f}%"
                        )
                    
                    with col2:
                        st.metric(
                            "Score Oportunidade", 
                            f"{analysis['score']:.0f}/100"
                        )
                    
                    with col3:
                        st.metric(
                            "P/L", 
                            f"{data.get('pe_ratio', 0):.1f}"
                        )
                    
                    with col4:
                        st.metric(
                            "ROE", 
                            f"{data.get('roe', 0)*100:.1f}%"
                        )
                    
                    # Recomendação
                    rec_color = {
                        "COMPRAR FORTE": "🟢",
                        "COMPRAR": "🟡", 
                        "AGUARDAR": "🟠",
                        "EVITAR": "🔴",
                        "VENDER": "⚫"
                    }
                    
                    st.subheader(f"{rec_color.get(analysis['recommendation'], '❓')} Recomendação: {analysis['recommendation']}")
                    
                    # Gráfico
                    chart = create_price_chart(data)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                    
                    # Detalhes fundamentalistas
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📈 Indicadores Fundamentalistas")
                        fundamentals_df = pd.DataFrame([
                            ["Drawdown", f"{data.get('drawdown', 0):.1f}%"],
                            ["P/L", f"{data.get('pe_ratio', 0):.1f}"],
                            ["P/B", f"{data.get('pb_ratio', 0):.1f}"],
                            ["ROE", f"{data.get('roe', 0)*100:.1f}%"],
                            ["Dívida/Patrimônio", f"{data.get('debt_to_equity', 0):.1f}"],
                            ["Margem Lucro", f"{data.get('profit_margin', 0)*100:.1f}%"],
                            ["Crescimento Receita", f"{data.get('revenue_growth', 0)*100:.1f}%"],
                            ["Dividend Yield", f"{data.get('dividend_yield', 0)*100:.1f}%"]
                        ], columns=["Indicador", "Valor"])
                        st.dataframe(fundamentals_df, hide_index=True)
                    
                    with col2:
                        st.subheader("📰 Sentimento das Notícias")
                        news = analysis['news']
                        st.write(f"**Tendência:** {news.get('sentiment_trend', 'Neutro')}")
                        st.write(f"**Score Médio:** {news.get('avg_sentiment', 0):.2f}")
                        
                        if news.get('news'):
                            st.write("**Últimas Notícias:**")
                            for article in news['news'][:3]:
                                st.write(f"• {article['title'][:100]}...")
                
                else:
                    st.error("Não foi possível analisar esta ação. Verifique o código inserido.")
    
    with tab2:
        st.header("Varredura Global de Oportunidades")
        
        # Filtros
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            min_drawdown = st.slider("Drawdown Mínimo (%)", 10, 70, 25)
        with col2:
            max_pe = st.slider("P/L Máximo", 5, 50, 25)
        with col3:
            min_roe = st.slider("ROE Mínimo (%)", 5, 30, 10) / 100
        with col4:
            scan_button = st.button("🌍 Iniciar Varredura", type="primary")
        
        if scan_button:
            with st.spinner("Realizando varredura global... Isso pode levar alguns minutos."):
                opportunities = analyzer.global_screening(min_drawdown, max_pe, min_roe)
                
                if opportunities:
                    st.success(f"Encontradas {len(opportunities)} oportunidades!")
                    
                    # Criar DataFrame para exibição
                    df = pd.DataFrame(opportunities)
                    df = df[['ticker', 'region', 'score', 'recommendation', 'drawdown', 
                            'pe_ratio', 'roe', 'sector', 'current_price']]
                    
                    df.columns = ['Ticker', 'Região', 'Score', 'Recomendação', 'Drawdown (%)', 
                                 'P/L', 'ROE (%)', 'Setor', 'Preço ($)']
                    
                    # Formatar colunas
                    df['Drawdown (%)'] = df['Drawdown (%)'].round(1)
                    df['P/L'] = df['P/L'].round(1)
                    df['ROE (%)'] = df['ROE (%)'].round(1)
                    df['Preço ($)'] = df['Preço ($)'].round(2)
                    
                    st.dataframe(df, use_container_width=True)
                    
                    # Gráfico de distribuição por região
                    region_counts = pd.DataFrame(opportunities)['region'].value_counts()
                    fig_region = px.pie(
                        values=region_counts.values, 
                        names=region_counts.index,
                        title="Distribuição de Oportunidades por Região"
                    )
                    st.plotly_chart(fig_region, use_container_width=True)
                    
                else:
                    st.warning("Nenhuma oportunidade encontrada com os filtros atuais. Tente ajustar os parâmetros.")

if __name__ == "__main__":
    main()