"""
Configurações e integrações de APIs gratuitas
"""

import os
import requests
import json
from datetime import datetime, timedelta

class APIConfig:
    """Configurações para APIs gratuitas"""
    
    # URLs das APIs gratuitas
    FRED_API_BASE = "https://api.stlouisfed.org/fred/series/observations"
    BCB_SGS_API = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados"
    YAHOO_FINANCE_API = "https://query1.finance.yahoo.com/v8/finance/chart/{}"
    
    # Parâmetros padrão
    DEFAULT_PERIOD = "2y"
    CACHE_DURATION_HOURS = 2
    
    @staticmethod
    def get_fred_data(series_id, api_key=None):
        """
        Coleta dados do FRED (Federal Reserve Economic Data)
        Exemplo de uso: get_fred_data('GDP')
        """
        if not api_key:
            # FRED API é gratuita mas requer registro
            # Para demo, usamos dados simulados
            return {
                'series_id': series_id,
                'data': [{'date': '2024-01-01', 'value': 100}],
                'status': 'simulated'
            }
        
        try:
            params = {
                'series_id': series_id,
                'api_key': api_key,
                'file_type': 'json'
            }
            response = requests.get(APIConfig.FRED_API_BASE, params=params)
            return response.json()
        except:
            return None
    
    @staticmethod
    def get_bcb_data(series_code):
        """
        Coleta dados do Banco Central do Brasil
        Séries importantes:
        - 432: Taxa Selic
        - 433: IPCA
        - 1: Dólar
        """
        try:
            url = APIConfig.BCB_SGS_API.format(series_code)
            response = requests.get(url)
            return response.json()
        except:
            return None
    
    @staticmethod
    def get_economic_indicators():
        """Coleta indicadores econômicos importantes"""
        indicators = {}
        
        # Brasil - dados do BC
        try:
            # Taxa Selic
            selic = APIConfig.get_bcb_data(432)
            if selic:
                indicators['selic'] = selic[-1]['valor'] if selic else 0
            
            # IPCA
            ipca = APIConfig.get_bcb_data(433)
            if ipca:
                indicators['ipca'] = ipca[-1]['valor'] if ipca else 0
                
            # Dólar
            dollar = APIConfig.get_bcb_data(1)
            if dollar:
                indicators['usd_brl'] = dollar[-1]['valor'] if dollar else 0
                
        except:
            pass
        
        return indicators

class NewsCollector:
    """Coletor de notícias usando fontes gratuitas"""
    
    @staticmethod
    def get_google_news(query, num_articles=10):
        """Coleta notícias do Google News via RSS"""
        try:
            import feedparser
            
            # URL do RSS do Google News
            url = f"https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
            
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:num_articles]:
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published,
                    'summary': entry.get('summary', ''),
                    'source': entry.get('source', {}).get('title', 'Google News')
                })
            
            return articles
        except Exception as e:
            print(f"Erro ao coletar notícias: {e}")
            return []
    
    @staticmethod
    def get_yahoo_finance_news(symbol):
        """Coleta notícias específicas de uma ação via Yahoo Finance"""
        try:
            import yfinance as yf
            
            stock = yf.Ticker(symbol)
            news = stock.news
            
            return [{
                'title': article.get('title', ''),
                'link': article.get('link', ''),
                'published': article.get('providerPublishTime', ''),
                'summary': article.get('summary', ''),
                'source': article.get('publisher', '')
            } for article in news[:5]]
            
        except:
            return []

class MarketDataCollector:
    """Coletor de dados de mercado usando APIs gratuitas"""
    
    @staticmethod
    def get_global_indices():
        """Coleta dados de índices globais principais"""
        indices = {
            'US': ['^GSPC', '^DJI', '^IXIC'],  # S&P500, Dow, Nasdaq
            'Brazil': ['^BVSP'],  # Ibovespa
            'Europe': ['^GDAXI', '^FCHI', '^FTSE'],  # DAX, CAC40, FTSE100
            'Asia': ['^N225', '^HSI', '399001.SZ']  # Nikkei, Hang Seng, Shenzhen
        }
        
        market_data = {}
        
        try:
            import yfinance as yf
            
            for region, tickers in indices.items():
                market_data[region] = {}
                for ticker in tickers:
                    try:
                        index = yf.Ticker(ticker)
                        hist = index.history(period='5d')
                        if not hist.empty:
                            current = hist['Close'][-1]
                            previous = hist['Close'][-2] if len(hist) > 1 else current
                            change = ((current - previous) / previous) * 100
                            
                            market_data[region][ticker] = {
                                'current': current,
                                'change': change,
                                'volume': hist['Volume'][-1]
                            }
                    except:
                        continue
        except:
            pass
        
        return market_data
    
    @staticmethod
    def get_sector_performance():
        """Análise de performance por setor"""
        sector_etfs = {
            'Technology': 'XLK',
            'Healthcare': 'XLV', 
            'Financial': 'XLF',
            'Energy': 'XLE',
            'Consumer Discretionary': 'XLY',
            'Consumer Staples': 'XLP',
            'Industrials': 'XLI',
            'Materials': 'XLB',
            'Utilities': 'XLU',
            'Real Estate': 'XLRE',
            'Communication': 'XLC'
        }
        
        sector_data = {}
        
        try:
            import yfinance as yf
            
            for sector, etf in sector_etfs.items():
                try:
                    ticker = yf.Ticker(etf)
                    hist = ticker.history(period='1mo')
                    if not hist.empty:
                        current = hist['Close'][-1]
                        month_ago = hist['Close'][0]
                        change = ((current - month_ago) / month_ago) * 100
                        
                        sector_data[sector] = {
                            'etf': etf,
                            'change_1m': change,
                            'current_price': current
                        }
                except:
                    continue
        except:
            pass
        
        return sector_data

class SentimentAnalyzer:
    """Analisador de sentimento usando modelos gratuitos"""
    
    def __init__(self):
        self.models = self._load_models()
    
    def _load_models(self):
        """Carrega modelos de sentimento disponíveis"""
        models = {}
        
        try:
            from transformers import pipeline
            
            # Modelo multilíngue leve
            models['multilingual'] = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
        except:
            try:
                # Fallback para modelo mais simples
                models['simple'] = pipeline("sentiment-analysis")
            except:
                models = {}
        
        return models
    
    def analyze_text(self, text):
        """Analisa sentimento de um texto"""
        if not self.models:
            return 0  # Sentimento neutro
        
        try:
            # Usar o melhor modelo disponível
            model_key = list(self.models.keys())[0]
            model = self.models[model_key]
            
            result = model(text)
            
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], list):
                    # Modelo com scores múltiplos
                    positive_score = 0
                    negative_score = 0
                    
                    for score_dict in result[0]:
                        if 'POSITIVE' in score_dict['label'].upper():
                            positive_score = score_dict['score']
                        elif 'NEGATIVE' in score_dict['label'].upper():
                            negative_score = score_dict['score']
                    
                    return positive_score - negative_score
                else:
                    # Modelo simples
                    if result[0]['label'] == 'POSITIVE':
                        return result[0]['score']
                    else:
                        return -result[0]['score']
            
            return 0
        except:
            return 0
    
    def analyze_news_batch(self, news_list):
        """Analisa sentimento de múltiplas notícias"""
        if not news_list:
            return {'avg_sentiment': 0, 'sentiment_trend': 'Neutro'}
        
        sentiments = []
        for news in news_list:
            title = news.get('title', '')
            summary = news.get('summary', '')
            text = f"{title} {summary}".strip()
            
            if text:
                sentiment = self.analyze_text(text)
                sentiments.append(sentiment)
        
        if not sentiments:
            return {'avg_sentiment': 0, 'sentiment_trend': 'Neutro'}
        
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        if avg_sentiment > 0.1:
            trend = 'Positivo'
        elif avg_sentiment < -0.1:
            trend = 'Negativo'
        else:
            trend = 'Neutro'
        
        return {
            'avg_sentiment': avg_sentiment,
            'sentiment_trend': trend,
            'individual_scores': sentiments
        }

class TechnicalIndicators:
    """Calculadora de indicadores técnicos"""
    
    @staticmethod
    def calculate_rsi(prices, period=14):
        """Calcula RSI (Relative Strength Index)"""
        try:
            import pandas as pd
            
            if len(prices) < period + 1:
                return 50  # RSI neutro
            
            prices_series = pd.Series(prices)
            delta = prices_series.diff()
            
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
        except:
            return 50
    
    @staticmethod
    def calculate_moving_averages(prices, periods=[20, 50, 200]):
        """Calcula médias móveis"""
        try:
            import pandas as pd
            
            prices_series = pd.Series(prices)
            mas = {}
            
            for period in periods:
                if len(prices) >= period:
                    ma = prices_series.rolling(window=period).mean().iloc[-1]
                    mas[f'MA{period}'] = ma
                else:
                    mas[f'MA{period}'] = prices[-1]  # Preço atual se não há dados suficientes
            
            return mas
        except:
            return {f'MA{p}': prices[-1] if prices else 0 for p in periods}
    
    @staticmethod
    def calculate_bollinger_bands(prices, period=20, std_dev=2):
        """Calcula Bandas de Bollinger"""
        try:
            import pandas as pd
            
            if len(prices) < period:
                current_price = prices[-1] if prices else 0
                return {
                    'upper_band': current_price * 1.1,
                    'middle_band': current_price,
                    'lower_band': current_price * 0.9
                }
            
            prices_series = pd.Series(prices)
            
            middle_band = prices_series.rolling(window=period).mean()
            std = prices_series.rolling(window=period).std()
            
            upper_band = middle_band + (std * std_dev)
            lower_band = middle_band - (std * std_dev)
            
            return {
                'upper_band': upper_band.iloc[-1],
                'middle_band': middle_band.iloc[-1], 
                'lower_band': lower_band.iloc[-1]
            }
        except:
            current_price = prices[-1] if prices else 0
            return {
                'upper_band': current_price * 1.1,
                'middle_band': current_price,
                'lower_band': current_price * 0.9
            }
    
    @staticmethod
    def calculate_macd(prices, fast=12, slow=26, signal=9):
        """Calcula MACD (Moving Average Convergence Divergence)"""
        try:
            import pandas as pd
            
            if len(prices) < slow + signal:
                return {'macd': 0, 'signal': 0, 'histogram': 0}
            
            prices_series = pd.Series(prices)
            
            ema_fast = prices_series.ewm(span=fast).mean()
            ema_slow = prices_series.ewm(span=slow).mean()
            
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line
            
            return {
                'macd': macd_line.iloc[-1],
                'signal': signal_line.iloc[-1],
                'histogram': histogram.iloc[-1]
            }
        except:
            return {'macd': 0, 'signal': 0, 'histogram': 0}

# Configurações globais da aplicação
APP_CONFIG = {
    'title': 'Analisador Global de Ações',
    'version': '1.0.0',
    'author': 'AI Stock Analyzer',
    'description': 'Sistema de análise e varredura global de ações com foco em oportunidades de recuperação assimétrica',
    'cache_duration': 2,  # horas
    'max_stocks_per_scan': 100,
    'default_filters': {
        'min_drawdown': 20,
        'max_pe': 30,
        'min_roe': 0.10,
        'min_market_cap': 1e9  # 1 bilhão
    }
}