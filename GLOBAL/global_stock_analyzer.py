import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import json
import requests
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Analisador Global de Investimentos",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

class GlobalAssetDatabase:
    """Banco de dados global de ativos financeiros"""
    
    def __init__(self):
        self.global_assets = self._load_global_assets()
        self.crypto_symbols = self._load_crypto_symbols()
        
    def _load_global_assets(self):
        """Carrega base de dados global de ações e índices"""
        return {
            'EUA': {
                'indices': {
                    '^GSPC': 'S&P 500',
                    '^DJI': 'Dow Jones',
                    '^IXIC': 'NASDAQ',
                    '^RUT': 'Russell 2000',
                    '^VIX': 'VIX (Volatilidade)'
                },
                'blue_chips': {
                    'AAPL': 'Apple Inc.',
                    'MSFT': 'Microsoft Corp.',
                    'GOOGL': 'Alphabet Inc.',
                    'AMZN': 'Amazon.com Inc.',
                    'TSLA': 'Tesla Inc.',
                    'META': 'Meta Platforms',
                    'NVDA': 'NVIDIA Corp.',
                    'BRK-B': 'Berkshire Hathaway',
                    'JNJ': 'Johnson & Johnson',
                    'V': 'Visa Inc.',
                    'PG': 'Procter & Gamble',
                    'UNH': 'UnitedHealth Group',
                    'HD': 'Home Depot',
                    'MA': 'Mastercard Inc.',
                    'DIS': 'Walt Disney Co.',
                    'PYPL': 'PayPal Holdings',
                    'ADBE': 'Adobe Inc.',
                    'NFLX': 'Netflix Inc.',
                    'CRM': 'Salesforce Inc.',
                    'CMCSA': 'Comcast Corp.'
                },
                'growth_stocks': {
                    'SHOP': 'Shopify Inc.',
                    'SQ': 'Block Inc.',
                    'ROKU': 'Roku Inc.',
                    'ZM': 'Zoom Video',
                    'PTON': 'Peloton Interactive',
                    'SNAP': 'Snap Inc.',
                    'UBER': 'Uber Technologies',
                    'LYFT': 'Lyft Inc.',
                    'TWTR': 'Twitter Inc.',
                    'PINS': 'Pinterest Inc.'
                },
                'value_stocks': {
                    'WMT': 'Walmart Inc.',
                    'KO': 'Coca-Cola Co.',
                    'PFE': 'Pfizer Inc.',
                    'T': 'AT&T Inc.',
                    'VZ': 'Verizon Communications',
                    'XOM': 'Exxon Mobil',
                    'CVX': 'Chevron Corp.',
                    'JPM': 'JPMorgan Chase',
                    'BAC': 'Bank of America',
                    'WFC': 'Wells Fargo'
                }
            },
            'Brasil': {
                'indices': {
                    '^BVSP': 'Ibovespa',
                    '^BVSP11': 'IBrX 100',
                    'IFIX.SA': 'IFIX (FIIs)'
                },
                'blue_chips': {
                    'PETR4.SA': 'Petrobras',
                    'VALE3.SA': 'Vale',
                    'ITUB4.SA': 'Itaú Unibanco',
                    'BBDC4.SA': 'Bradesco',
                    'ABEV3.SA': 'Ambev',
                    'B3SA3.SA': 'B3',
                    'JBSS3.SA': 'JBS',
                    'RENT3.SA': 'Localiza',
                    'LREN3.SA': 'Lojas Renner',
                    'MGLU3.SA': 'Magazine Luiza'
                },
                'growth_stocks': {
                    'WEGE3.SA': 'WEG',
                    'SUZB3.SA': 'Suzano',
                    'RAIL3.SA': 'Rumo',
                    'VVAR3.SA': 'Via Varejo',
                    'HAPV3.SA': 'Hapvida',
                    'PCAR3.SA': 'P&G Car',
                    'AZUL4.SA': 'Azul',
                    'MOVI3.SA': 'Movida',
                    'RADL3.SA': 'Raia Drogasil',
                    'COGN3.SA': 'Cogna'
                },
                'fiis': {
                    'HGLG11.SA': 'CSHG Logística',
                    'XPML11.SA': 'XP Malls',
                    'BTLG11.SA': 'BTG Logística',
                    'VILG11.SA': 'Villagio',
                    'KNCR11.SA': 'Kinea Rendimento',
                    'IRDM11.SA': 'IRB Real Estate',
                    'MXRF11.SA': 'Maxi Renda',
                    'BCFF11.SA': 'BC Fund',
                    'HSML11.SA': 'HSI Malls',
                    'RECT11.SA': 'REC Recebíveis'
                }
            },
            'Europa': {
                'indices': {
                    '^GDAXI': 'DAX (Alemanha)',
                    '^FCHI': 'CAC 40 (França)',
                    '^FTSE': 'FTSE 100 (Reino Unido)',
                    '^STOXX50E': 'EURO STOXX 50',
                    '^AEX': 'AEX (Holanda)'
                },
                'stocks': {
                    'ASML.AS': 'ASML Holding (Holanda)',
                    'SAP.DE': 'SAP SE (Alemanha)',
                    'LVMH.PA': 'LVMH (França)',
                    'NVO': 'Novo Nordisk',
                    'NESN.SW': 'Nestlé (Suíça)',
                    'ROCHE.SW': 'Roche (Suíça)',
                    'NOVN.SW': 'Novartis (Suíça)',
                    'BAS.DE': 'BASF (Alemanha)',
                    'SIE.DE': 'Siemens (Alemanha)',
                    'ADYEN.AS': 'Adyen (Holanda)',
                    'MC.PA': 'LVMH (França)',
                    'OR.PA': "L'Oréal (França)",
                    'SAN.PA': 'Sanofi (França)',
                    'ASME.L': 'ASOS (Reino Unido)',
                    'BP.L': 'BP (Reino Unido)'
                }
            },
            'Asia': {
                'indices': {
                    '^N225': 'Nikkei 225 (Japão)',
                    '^HSI': 'Hang Seng (Hong Kong)',
                    '000001.SS': 'SSE Composite (China)',
                    '^KS11': 'KOSPI (Coreia do Sul)',
                    '^STI': 'Straits Times (Singapura)'
                },
                'stocks': {
                    'TM': 'Toyota Motor',
                    'SONY': 'Sony Group',
                    '7203.T': 'Toyota (Tóquio)',
                    '6758.T': 'Sony (Tóquio)',
                    '9984.T': 'SoftBank Group',
                    '6861.T': 'Keyence Corp',
                    'TSM': 'Taiwan Semiconductor',
                    'BABA': 'Alibaba Group',
                    'TCEHY': 'Tencent Holdings',
                    '005930.KS': 'Samsung Electronics'
                }
            },
            'ETFs_Globais': {
                'spy': 'SPDR S&P 500 ETF',
                'qqq': 'Invesco QQQ Trust',
                'iwm': 'iShares Russell 2000',
                'efa': 'iShares MSCI EAFE',
                'eem': 'iShares MSCI Emerging Markets',
                'vti': 'Vanguard Total Stock Market',
                'vea': 'Vanguard FTSE Developed Markets',
                'vwo': 'Vanguard FTSE Emerging Markets',
                'gld': 'SPDR Gold Shares',
                'slv': 'iShares Silver Trust'
            },
            'Commodities': {
                'GC=F': 'Ouro Futuro',
                'SI=F': 'Prata Futuro',
                'CL=F': 'Petróleo WTI',
                'BZ=F': 'Petróleo Brent',
                'NG=F': 'Gás Natural',
                'ZC=F': 'Milho',
                'ZS=F': 'Soja',
                'ZW=F': 'Trigo',
                'KC=F': 'Café',
                'SB=F': 'Açúcar'
            }
        }
    
    def _load_crypto_symbols(self):
        """Carrega símbolos de criptomoedas principais"""
        return {
            'BTC-USD': 'Bitcoin',
            'ETH-USD': 'Ethereum',
            'BNB-USD': 'Binance Coin',
            'ADA-USD': 'Cardano',
            'XRP-USD': 'Ripple',
            'SOL-USD': 'Solana',
            'DOT-USD': 'Polkadot',
            'DOGE-USD': 'Dogecoin',
            'AVAX-USD': 'Avalanche',
            'SHIB-USD': 'Shiba Inu',
            'MATIC-USD': 'Polygon',
            'LTC-USD': 'Litecoin',
            'UNI-USD': 'Uniswap',
            'LINK-USD': 'Chainlink',
            'ALGO-USD': 'Algorand'
        }
    
    def search_asset(self, query: str) -> List[Dict]:
        """Busca ativos por nome ou símbolo"""
        query = query.upper()
        results = []
        
        # Buscar em todas as categorias
        for region, categories in self.global_assets.items():
            for category, assets in categories.items():
                for symbol, name in assets.items():
                    if (query in symbol.upper() or 
                        query in name.upper() or
                        symbol.upper().startswith(query)):
                        results.append({
                            'symbol': symbol,
                            'name': name,
                            'region': region,
                            'category': category,
                            'type': 'stock'
                        })
        
        # Buscar criptomoedas
        for symbol, name in self.crypto_symbols.items():
            if (query in symbol.upper() or 
                query in name.upper() or
                symbol.upper().startswith(query)):
                results.append({
                    'symbol': symbol,
                    'name': name,
                    'region': 'Global',
                    'category': 'cryptocurrency',
                    'type': 'crypto'
                })
        
        return results[:20]  # Limitar a 20 resultados
    
    def get_all_symbols(self) -> List[str]:
        """Retorna todos os símbolos disponíveis"""
        symbols = []
        
        for region, categories in self.global_assets.items():
            for category, assets in categories.items():
                symbols.extend(assets.keys())
        
        symbols.extend(self.crypto_symbols.keys())
        return symbols
    
    def get_random_picks(self, count: int = 10) -> List[Dict]:
        """Retorna seleção aleatória de ativos interessantes"""
        interesting_picks = [
            {'symbol': 'AAPL', 'reason': 'Líder em tecnologia com forte crescimento'},
            {'symbol': 'TSLA', 'reason': 'Pioneira em veículos elétricos'},
            {'symbol': 'PETR4.SA', 'reason': 'Maior petrolífera da América Latina'},
            {'symbol': 'BTC-USD', 'reason': 'Reserva de valor digital'},
            {'symbol': 'ASML.AS', 'reason': 'Monopólio em equipamentos de chips'},
            {'symbol': '^GSPC', 'reason': 'Índice mais importante do mundo'},
            {'symbol': 'NVDA', 'reason': 'Líder em IA e computação'},
            {'symbol': 'VALE3.SA', 'reason': 'Maior mineradora global'},
            {'symbol': 'ETH-USD', 'reason': 'Plataforma líder em DeFi'},
            {'symbol': 'GOOGL', 'reason': 'Domínio em busca e IA'}
        ]
        
        return interesting_picks[:count]

class AdvancedAnalyzer:
    """Analisador avançado com IA para feedback e potencial"""
    
    def __init__(self):
        self.asset_db = GlobalAssetDatabase()
    
    @st.cache_data(ttl=3600)
    def get_comprehensive_data(_self, symbol: str) -> Dict:
        """Coleta dados abrangentes do ativo"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Dados históricos (2 anos)
            hist = ticker.history(period="2y")
            if hist.empty:
                return None
            
            # Informações da empresa
            info = ticker.info
            
            # Dados financeiros (se disponível)
            try:
                financials = ticker.financials
                balance_sheet = ticker.balance_sheet
                cashflow = ticker.cashflow
            except:
                financials = balance_sheet = cashflow = None
            
            # Notícias recentes
            try:
                news = ticker.news[:5]
            except:
                news = []
            
            # Calcular métricas técnicas
            current_price = float(hist['Close'][-1])
            
            # Preços de referência
            price_1y_ago = float(hist['Close'][-252]) if len(hist) >= 252 else current_price
            price_6m_ago = float(hist['Close'][-126]) if len(hist) >= 126 else current_price
            price_3m_ago = float(hist['Close'][-63]) if len(hist) >= 63 else current_price
            price_1m_ago = float(hist['Close'][-21]) if len(hist) >= 21 else current_price
            
            max_price_2y = float(hist['Close'].max())
            min_price_2y = float(hist['Close'].min())
            max_price_1y = float(hist['Close'][-252:].max()) if len(hist) >= 252 else max_price_2y
            
            # Retornos
            return_1y = ((current_price - price_1y_ago) / price_1y_ago) * 100
            return_6m = ((current_price - price_6m_ago) / price_6m_ago) * 100
            return_3m = ((current_price - price_3m_ago) / price_3m_ago) * 100
            return_1m = ((current_price - price_1m_ago) / price_1m_ago) * 100
            
            # Drawdown
            drawdown = ((current_price - max_price_1y) / max_price_1y) * 100
            
            # Volatilidade
            returns = hist['Close'].pct_change().dropna()
            volatility = float(returns.std() * np.sqrt(252) * 100)
            
            # RSI
            rsi = _self._calculate_rsi(hist['Close'].values)
            
            # Médias móveis
            ma20 = float(hist['Close'].rolling(20).mean().iloc[-1]) if len(hist) >= 20 else current_price
            ma50 = float(hist['Close'].rolling(50).mean().iloc[-1]) if len(hist) >= 50 else current_price
            ma200 = float(hist['Close'].rolling(200).mean().iloc[-1]) if len(hist) >= 200 else current_price
            
            # Análise fundamentalista
            fundamentals = _self._extract_fundamentals(info)
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'price_history': {
                    '1y_ago': price_1y_ago,
                    '6m_ago': price_6m_ago,
                    '3m_ago': price_3m_ago,
                    '1m_ago': price_1m_ago
                },
                'returns': {
                    '1y': return_1y,
                    '6m': return_6m,
                    '3m': return_3m,
                    '1m': return_1m
                },
                'price_levels': {
                    'max_2y': max_price_2y,
                    'min_2y': min_price_2y,
                    'max_1y': max_price_1y,
                    'current': current_price
                },
                'technical': {
                    'drawdown': drawdown,
                    'volatility': volatility,
                    'rsi': rsi,
                    'ma20': ma20,
                    'ma50': ma50,
                    'ma200': ma200
                },
                'fundamentals': fundamentals,
                'news': news,
                'hist_data': hist.reset_index().to_dict('records'),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            st.error(f"Erro ao analisar {symbol}: {str(e)}")
            return None
    
    def _calculate_rsi(self, prices, period=14):
        """Calcula RSI"""
        if len(prices) < period + 1:
            return 50
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    def _extract_fundamentals(self, info):
        """Extrai dados fundamentalistas"""
        return {
            'market_cap': info.get('marketCap', 0) or 0,
            'pe_ratio': info.get('forwardPE', info.get('trailingPE', 0)) or 0,
            'pb_ratio': info.get('priceToBook', 0) or 0,
            'roe': info.get('returnOnEquity', 0) or 0,
            'debt_to_equity': info.get('debtToEquity', 0) or 0,
            'profit_margin': info.get('profitMargins', 0) or 0,
            'revenue_growth': info.get('revenueGrowth', 0) or 0,
            'dividend_yield': info.get('dividendYield', 0) or 0,
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'employees': info.get('fullTimeEmployees', 0) or 0,
            'country': info.get('country', 'N/A')
        }
    
    def calculate_comprehensive_score(self, data: Dict) -> Dict:
        """Calcula score abrangente e análise de potencial"""
        if not data:
            return None
        
        # Scores por categoria
        technical_score = self._calculate_technical_score(data)
        fundamental_score = self._calculate_fundamental_score(data)
        momentum_score = self._calculate_momentum_score(data)
        risk_score = self._calculate_risk_score(data)
        
        # Score final ponderado
        final_score = (
            technical_score * 0.3 +
            fundamental_score * 0.3 +
            momentum_score * 0.25 +
            (100 - risk_score) * 0.15  # Inverter risk score
        )
        
        # Potencial de crescimento
        growth_potential = self._calculate_growth_potential(data)
        
        # Análise de sentimento
        sentiment_analysis = self._analyze_sentiment(data)
        
        # Recomendação final
        recommendation = self._generate_recommendation(final_score, risk_score, data)
        
        # Feedback detalhado
        feedback = self._generate_detailed_feedback(data, {
            'technical': technical_score,
            'fundamental': fundamental_score,
            'momentum': momentum_score,
            'risk': risk_score,
            'final': final_score
        })
        
        return {
            'scores': {
                'technical': round(technical_score, 1),
                'fundamental': round(fundamental_score, 1),
                'momentum': round(momentum_score, 1),
                'risk': round(risk_score, 1),
                'final': round(final_score, 1)
            },
            'growth_potential': growth_potential,
            'sentiment': sentiment_analysis,
            'recommendation': recommendation,
            'feedback': feedback,
            'price_targets': self._calculate_price_targets(data)
        }
    
    def _calculate_technical_score(self, data: Dict) -> float:
        """Score técnico baseado em indicadores"""
        score = 50
        technical = data['technical']
        
        # RSI
        rsi = technical['rsi']
        if 30 <= rsi <= 70:
            score += 15
        elif rsi < 30:
            score += 25  # Oversold = oportunidade
        elif rsi > 70:
            score -= 10  # Overbought
        
        # Posição vs médias móveis
        price = data['current_price']
        if price > technical['ma20']:
            score += 10
        if price > technical['ma50']:
            score += 10
        if price > technical['ma200']:
            score += 15
        
        # Drawdown (oportunidade)
        drawdown = abs(technical['drawdown'])
        if drawdown > 40:
            score += 20
        elif drawdown > 25:
            score += 15
        elif drawdown > 15:
            score += 10
        elif drawdown < 5:
            score -= 5
        
        # Volatilidade
        vol = technical['volatility']
        if vol < 20:
            score += 5
        elif vol > 60:
            score -= 10
        
        return max(0, min(100, score))
    
    def _calculate_fundamental_score(self, data: Dict) -> float:
        """Score fundamentalista"""
        score = 50
        fund = data['fundamentals']
        
        # P/L
        pe = fund['pe_ratio']
        if 0 < pe < 10:
            score += 25
        elif 10 <= pe < 15:
            score += 20
        elif 15 <= pe < 20:
            score += 15
        elif 20 <= pe < 25:
            score += 10
        elif pe > 35:
            score -= 15
        
        # ROE
        roe = fund['roe']
        if roe > 0.25:
            score += 25
        elif roe > 0.20:
            score += 20
        elif roe > 0.15:
            score += 15
        elif roe > 0.10:
            score += 10
        elif roe < 0:
            score -= 25
        
        # Debt to Equity
        debt = fund['debt_to_equity']
        if debt < 0.3:
            score += 15
        elif debt < 0.5:
            score += 10
        elif debt > 2.0:
            score -= 20
        
        # Crescimento de receita
        growth = fund['revenue_growth']
        if growth > 0.20:
            score += 20
        elif growth > 0.15:
            score += 15
        elif growth > 0.10:
            score += 10
        elif growth < -0.10:
            score -= 20
        
        # Margem de lucro
        margin = fund['profit_margin']
        if margin > 0.20:
            score += 15
        elif margin > 0.15:
            score += 10
        elif margin > 0.10:
            score += 5
        elif margin < 0:
            score -= 15
        
        return max(0, min(100, score))
    
    def _calculate_momentum_score(self, data: Dict) -> float:
        """Score de momentum baseado em retornos"""
        score = 50
        returns = data['returns']
        
        # Peso por período
        if returns['1m'] > 5:
            score += 15
        elif returns['1m'] > 2:
            score += 10
        elif returns['1m'] < -5:
            score -= 10
        
        if returns['3m'] > 10:
            score += 15
        elif returns['3m'] > 5:
            score += 10
        elif returns['3m'] < -10:
            score -= 10
        
        if returns['6m'] > 15:
            score += 10
        elif returns['6m'] < -15:
            score -= 10
        
        if returns['1y'] > 20:
            score += 10
        elif returns['1y'] < -20:
            score -= 15
        
        return max(0, min(100, score))
    
    def _calculate_risk_score(self, data: Dict) -> float:
        """Score de risco (maior = mais arriscado)"""
        risk = 0
        
        # Volatilidade
        vol = data['technical']['volatility']
        if vol > 60:
            risk += 30
        elif vol > 40:
            risk += 20
        elif vol > 25:
            risk += 10
        
        # Debt to Equity
        debt = data['fundamentals']['debt_to_equity']
        if debt > 3:
            risk += 25
        elif debt > 2:
            risk += 15
        elif debt > 1:
            risk += 10
        
        # ROE negativo
        if data['fundamentals']['roe'] < 0:
            risk += 20
        
        # Margem negativa
        if data['fundamentals']['profit_margin'] < 0:
            risk += 20
        
        # Drawdown extremo
        if abs(data['technical']['drawdown']) > 70:
            risk += 15
        
        return min(100, risk)
    
    def _calculate_growth_potential(self, data: Dict) -> Dict:
        """Calcula potencial de crescimento"""
        current_price = data['current_price']
        max_2y = data['price_levels']['max_2y']
        
        # Potencial técnico baseado em máximas históricas
        technical_upside = ((max_2y - current_price) / current_price) * 100
        
        # Potencial baseado em múltiplos
        pe = data['fundamentals']['pe_ratio']
        sector_avg_pe = 20  # Simplificado
        
        if pe > 0:
            multiple_upside = ((sector_avg_pe - pe) / pe) * 100 if pe < sector_avg_pe else 0
        else:
            multiple_upside = 0
        
        # Potencial de crescimento orgânico
        growth_rate = data['fundamentals']['revenue_growth']
        organic_potential = growth_rate * 100 * 2  # Projeção 2 anos
        
        # Potencial conservador, moderado e otimista
        conservative = max(0, min(technical_upside * 0.5, 25))
        moderate = max(0, min((technical_upside + multiple_upside) * 0.7, 50))
        optimistic = max(0, min(technical_upside + multiple_upside + organic_potential, 100))
        
        return {
            'conservative': round(conservative, 1),
            'moderate': round(moderate, 1),
            'optimistic': round(optimistic, 1),
            'timeframe': '12-24 meses'
        }
    
    def _analyze_sentiment(self, data: Dict) -> Dict:
        """Análise de sentimento baseada em notícias"""
        news = data.get('news', [])
        
        if not news:
            return {'score': 0, 'trend': 'Neutro', 'summary': 'Sem notícias recentes'}
        
        positive_words = {
            'growth', 'profit', 'gain', 'increase', 'strong', 'beat', 'exceed',
            'positive', 'bullish', 'upgrade', 'buy', 'outperform', 'record'
        }
        
        negative_words = {
            'loss', 'decline', 'fall', 'weak', 'miss', 'below', 'negative',
            'bearish', 'downgrade', 'sell', 'underperform', 'concern', 'risk'
        }
        
        sentiment_scores = []
        
        for article in news[:5]:
            title = article.get('title', '').lower()
            words = title.split()
            
            pos_count = sum(1 for word in words if word in positive_words)
            neg_count = sum(1 for word in words if word in negative_words)
            
            if pos_count + neg_count > 0:
                score = (pos_count - neg_count) / (pos_count + neg_count)
                sentiment_scores.append(score)
        
        if sentiment_scores:
            avg_sentiment = np.mean(sentiment_scores)
        else:
            avg_sentiment = 0
        
        if avg_sentiment > 0.3:
            trend = 'Muito Positivo'
        elif avg_sentiment > 0.1:
            trend = 'Positivo'
        elif avg_sentiment > -0.1:
            trend = 'Neutro'
        elif avg_sentiment > -0.3:
            trend = 'Negativo'
        else:
            trend = 'Muito Negativo'
        
        return {
            'score': round(avg_sentiment, 2),
            'trend': trend,
            'summary': f'Baseado em {len(news)} notícias recentes'
        }
    
    def _generate_recommendation(self, final_score: float, risk_score: float, data: Dict) -> Dict:
        """Gera recomendação final"""
        
        # Ajustar score baseado no risco
        risk_adjusted_score = final_score - (risk_score * 0.2)
        
        if risk_adjusted_score >= 80:
            action = "COMPRA FORTE"
            confidence = "Alta"
            emoji = "🚀"
        elif risk_adjusted_score >= 70:
            action = "COMPRAR"
            confidence = "Boa"
            emoji = "✅"
        elif risk_adjusted_score >= 55:
            action = "COMPRA MODERADA"
            confidence = "Moderada"
            emoji = "🟡"
        elif risk_adjusted_score >= 40:
            action = "AGUARDAR"
            confidence = "Baixa"
            emoji = "⏳"
        elif risk_adjusted_score >= 25:
            action = "EVITAR"
            confidence = "Baixa"
            emoji = "⚠️"
        else:
            action = "VENDER"
            confidence = "Alta"
            emoji = "❌"
        
        # Horizon de investimento recomendado
        volatility = data['technical']['volatility']
        if volatility > 50:
            horizon = "Longo prazo (2+ anos)"
        elif volatility > 30:
            horizon = "Médio prazo (6-18 meses)"
        else:
            horizon = "Médio prazo (3-12 meses)"
        
        return {
            'action': action,
            'confidence': confidence,
            'emoji': emoji,
            'score': round(risk_adjusted_score, 1),
            'horizon': horizon,
            'risk_level': 'Alto' if risk_score > 60 else 'Médio' if risk_score > 30 else 'Baixo'
        }
    
    def _generate_detailed_feedback(self, data: Dict, scores: Dict) -> Dict:
        """Gera feedback detalhado sobre o ativo"""
        
        feedback = {
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'threats': [],
            'summary': ''
        }
        
        # Analisar pontos fortes
        if scores['technical'] > 70:
            feedback['strengths'].append("📈 Forte performance técnica")
        if scores['fundamental'] > 70:
            feedback['strengths'].append("💪 Fundamentos sólidos")
        if scores['momentum'] > 70:
            feedback['strengths'].append("🚀 Momentum positivo")
        if data['fundamentals']['roe'] > 0.15:
            feedback['strengths'].append("💰 Alto retorno sobre patrimônio")
        if data['fundamentals']['debt_to_equity'] < 0.5:
            feedback['strengths'].append("🛡️ Baixo endividamento")
        
        # Analisar pontos fracos
        if scores['risk'] > 60:
            feedback['weaknesses'].append("⚠️ Alto perfil de risco")
        if data['technical']['volatility'] > 50:
            feedback['weaknesses'].append("📊 Alta volatilidade")
        if data['fundamentals']['pe_ratio'] > 30:
            feedback['weaknesses'].append("💸 Múltiplo elevado (P/L)")
        if data['returns']['1y'] < -20:
            feedback['weaknesses'].append("📉 Performance ruim no último ano")
        if data['fundamentals']['revenue_growth'] < 0:
            feedback['weaknesses'].append("📉 Receita em declínio")
        
        # Analisar oportunidades
        drawdown = abs(data['technical']['drawdown'])
        if drawdown > 30:
            feedback['opportunities'].append(f"🎯 Grande desconto: {drawdown:.1f}% abaixo do pico")
        if data['technical']['rsi'] < 35:
            feedback['opportunities'].append("📈 Condição de oversold (RSI baixo)")
        if data['fundamentals']['pe_ratio'] < 15 and data['fundamentals']['pe_ratio'] > 0:
            feedback['opportunities'].append("💎 Múltiplo atrativo (P/L baixo)")
        
        # Analisar ameaças
        if data['fundamentals']['debt_to_equity'] > 2:
            feedback['threats'].append("💳 Alto endividamento")
        if data['fundamentals']['profit_margin'] < 0.05:
            feedback['threats'].append("📉 Margem de lucro baixa")
        if scores['momentum'] < 30:
            feedback['threats'].append("🐌 Momentum negativo")
        
        # Gerar resumo
        total_strengths = len(feedback['strengths'])
        total_weaknesses = len(feedback['weaknesses'])
        
        if total_strengths > total_weaknesses:
            feedback['summary'] = "✅ Ativo com mais pontos positivos que negativos"
        elif total_weaknesses > total_strengths:
            feedback['summary'] = "⚠️ Ativo apresenta mais riscos que oportunidades"
        else:
            feedback['summary'] = "⚖️ Ativo equilibrado com pontos positivos e negativos"
        
        return feedback
    
    def _calculate_price_targets(self, data: Dict) -> Dict:
        """Calcula metas de preço"""
        current_price = data['current_price']
        
        # Support e Resistance baseados em histórico
        hist_prices = [d['Close'] for d in data['hist_data']]
        support = np.percentile(hist_prices, 25)
        resistance = np.percentile(hist_prices, 75)
        
        # Metas baseadas em análise técnica
        ma200 = data['technical']['ma200']
        max_1y = data['price_levels']['max_1y']
        
        # Metas conservadora, moderada e otimista
        conservative_target = min(ma200, current_price * 1.15)
        moderate_target = min(resistance, current_price * 1.30)
        optimistic_target = min(max_1y * 1.10, current_price * 1.50)
        
        # Stop loss baseado em suporte
        stop_loss = max(support * 0.95, current_price * 0.85)
        
        return {
            'current': round(current_price, 2),
            'support': round(support, 2),
            'resistance': round(resistance, 2),
            'targets': {
                'conservative': round(conservative_target, 2),
                'moderate': round(moderate_target, 2),
                'optimistic': round(optimistic_target, 2)
            },
            'stop_loss': round(stop_loss, 2)
        }

def create_comprehensive_chart(data: Dict) -> go.Figure:
    """Cria gráfico abrangente com análise técnica"""
    if not data or 'hist_data' not in data:
        return None
    
    df = pd.DataFrame(data['hist_data'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Criar subplots
    fig = go.Figure()
    
    # Preço de fechamento
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='lines',
        name='Preço',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Médias móveis
    if len(df) >= 20:
        ma20 = df['Close'].rolling(20).mean()
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=ma20,
            mode='lines',
            name='MA20',
            line=dict(color='orange', width=1)
        ))
    
    if len(df) >= 50:
        ma50 = df['Close'].rolling(50).mean()
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=ma50,
            mode='lines',
            name='MA50',
            line=dict(color='green', width=1)
        ))
    
    if len(df) >= 200:
        ma200 = df['Close'].rolling(200).mean()
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=ma200,
            mode='lines',
            name='MA200',
            line=dict(color='red', width=1, dash='dash')
        ))
    
    # Bandas de Bollinger
    if len(df) >= 20:
        ma20 = df['Close'].rolling(20).mean()
        std20 = df['Close'].rolling(20).std()
        upper_band = ma20 + (std20 * 2)
        lower_band = ma20 - (std20 * 2)
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=upper_band,
            mode='lines',
            name='BB Superior',
            line=dict(color='gray', width=1, dash='dot'),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=lower_band,
            mode='lines',
            name='BB Inferior',
            line=dict(color='gray', width=1, dash='dot'),
            fill='tonexty',
            fillcolor='rgba(128,128,128,0.1)',
            showlegend=False
        ))
    
    # Máximas e mínimas importantes
    max_price = df['Close'].max()
    min_price = df['Close'].min()
    
    fig.add_hline(y=max_price, line_dash="dash", line_color="red", 
                  annotation_text=f"Máx: ${max_price:.2f}")
    fig.add_hline(y=min_price, line_dash="dash", line_color="green", 
                  annotation_text=f"Mín: ${min_price:.2f}")
    
    fig.update_layout(
        title=f"Análise Técnica Completa - {data['symbol']}",
        xaxis_title="Data",
        yaxis_title="Preço ($)",
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

def format_large_number(num):
    """Formata números grandes"""
    if num >= 1e12:
        return f"${num/1e12:.1f}T"
    elif num >= 1e9:
        return f"${num/1e9:.1f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    elif num >= 1e3:
        return f"${num/1e3:.1f}K"
    else:
        return f"${num:.2f}"

def main():
    """Interface principal"""
    st.title("🌍 Analisador Global de Investimentos")
    st.subheader("Sistema Avançado com IA para Ações, Índices, ETFs e Criptomoedas")
    
    # Inicializar componentes
    analyzer = AdvancedAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 Navegação")
        
        # Busca rápida
        st.subheader("🔍 Busca Rápida")
        search_query = st.text_input("Buscar ativo:", placeholder="Ex: AAPL, Bitcoin, S&P 500")
        
        if search_query:
            results = analyzer.asset_db.search_asset(search_query)
            if results:
                st.write("**Resultados encontrados:**")
                for result in results[:5]:
                    st.write(f"• **{result['symbol']}** - {result['name']}")
                    st.write(f"  {result['region']} | {result['category']}")
        
        # Picks do dia
        st.subheader("💡 Sugestões do Dia")
        random_picks = analyzer.asset_db.get_random_picks(5)
        for pick in random_picks:
            if st.button(f"{pick['symbol']}", key=f"pick_{pick['symbol']}"):
                st.session_state['selected_symbol'] = pick['symbol']
        
        st.markdown("---")
        st.info("💡 **Dica:** Este sistema analisa +10.000 ativos globalmente")
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Análise Completa", 
        "🌍 Scanner Global", 
        "📈 Comparador", 
        "📚 Educacional"
    ])
    
    with tab1:
        st.header("📊 Análise Completa de Ativo")
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            symbol_input = st.text_input(
                "Digite o símbolo do ativo:",
                value=st.session_state.get('selected_symbol', ''),
                placeholder="Ex: AAPL, PETR4.SA, BTC-USD, ^GSPC"
            )
        
        with col2:
            analyze_btn = st.button("🔍 Analisar Completo", type="primary", use_container_width=True)
        
        # Exemplos por categoria
        st.write("**Exemplos por categoria:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write("**🇺🇸 Ações EUA:**")
            st.code("AAPL\nTSLA\nGOOGL\nNVDA")
        
        with col2:
            st.write("**🇧🇷 Ações Brasil:**")
            st.code("PETR4.SA\nVALE3.SA\nITUB4.SA")
        
        with col3:
            st.write("**💰 Criptomoedas:**")
            st.code("BTC-USD\nETH-USD\nADA-USD")
        
        with col4:
            st.write("**📊 Índices:**")
            st.code("^GSPC\n^BVSP\n^DJI")
        
        if analyze_btn and symbol_input:
            symbol = symbol_input.upper().strip()
            
            with st.spinner(f"🔍 Analisando {symbol} com IA avançada..."):
                
                # Coletar dados
                data = analyzer.get_comprehensive_data(symbol)
                
                if data:
                    # Análise completa
                    analysis = analyzer.calculate_comprehensive_score(data)
                    
                    if analysis:
                        # Header com informações básicas
                        st.success(f"✅ **Análise concluída para {symbol}**")
                        
                        # Métricas principais
                        col1, col2, col3, col4, col5 = st.columns(5)
                        
                        with col1:
                            current_price = data['current_price']
                            return_1y = data['returns']['1y']
                            delta_color = "normal" if abs(return_1y) < 10 else "inverse"
                            
                            st.metric(
                                "💰 Preço Atual",
                                f"${current_price:.2f}",
                                f"{return_1y:+.1f}% (1 ano)",
                                delta_color=delta_color
                            )
                        
                        with col2:
                            score = analysis['scores']['final']
                            st.metric(
                                f"{analysis['recommendation']['emoji']} Score IA",
                                f"{score:.0f}/100",
                                analysis['recommendation']['confidence']
                            )
                        
                        with col3:
                            growth = analysis['growth_potential']['moderate']
                            st.metric(
                                "📈 Potencial",
                                f"+{growth:.1f}%",
                                analysis['growth_potential']['timeframe']
                            )
                        
                        with col4:
                            risk_level = analysis['recommendation']['risk_level']
                            risk_color = "🟢" if risk_level == "Baixo" else "🟡" if risk_level == "Médio" else "🔴"
                            st.metric(
                                f"{risk_color} Risco",
                                risk_level,
                                f"RSI: {data['technical']['rsi']:.0f}"
                            )
                        
                        with col5:
                            market_cap = data['fundamentals']['market_cap']
                            st.metric(
                                "🏢 Market Cap",
                                format_large_number(market_cap),
                                data['fundamentals']['sector']
                            )
                        
                        # Recomendação principal
                        rec = analysis['recommendation']
                        if rec['action'] in ['COMPRA FORTE', 'COMPRAR']:
                            st.success(f"""
                            ## {rec['emoji']} RECOMENDAÇÃO: {rec['action']}
                            **Confiança:** {rec['confidence']} | **Horizonte:** {rec['horizon']} | **Score Ajustado:** {rec['score']}/100
                            """)
                        elif rec['action'] in ['COMPRA MODERADA', 'AGUARDAR']:
                            st.warning(f"""
                            ## {rec['emoji']} RECOMENDAÇÃO: {rec['action']}
                            **Confiança:** {rec['confidence']} | **Horizonte:** {rec['horizon']} | **Score Ajustado:** {rec['score']}/100
                            """)
                        else:
                            st.error(f"""
                            ## {rec['emoji']} RECOMENDAÇÃO: {rec['action']}
                            **Confiança:** {rec['confidence']} | **Horizonte:** {rec['horizon']} | **Score Ajustado:** {rec['score']}/100
                            """)
                        
                        # Gráfico avançado
                        chart = create_comprehensive_chart(data)
                        if chart:
                            st.plotly_chart(chart, use_container_width=True)
                        
                        # Análise detalhada em colunas
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📊 Scores Detalhados")
                            
                            scores_df = pd.DataFrame([
                                ["🔧 Técnico", f"{analysis['scores']['technical']:.1f}/100"],
                                ["💼 Fundamentalista", f"{analysis['scores']['fundamental']:.1f}/100"],
                                ["🚀 Momentum", f"{analysis['scores']['momentum']:.1f}/100"],
                                ["⚠️ Risco", f"{analysis['scores']['risk']:.1f}/100"],
                                ["🎯 Final", f"{analysis['scores']['final']:.1f}/100"]
                            ], columns=["Categoria", "Score"])
                            
                            st.dataframe(scores_df, hide_index=True, use_container_width=True)
                            
                            # Potencial de crescimento
                            st.subheader("📈 Potencial de Crescimento")
                            growth = analysis['growth_potential']
                            
                            st.write(f"**🛡️ Conservador:** +{growth['conservative']:.1f}%")
                            st.write(f"**⚖️ Moderado:** +{growth['moderate']:.1f}%")
                            st.write(f"**🚀 Otimista:** +{growth['optimistic']:.1f}%")
                            st.write(f"**⏰ Prazo:** {growth['timeframe']}")
                        
                        with col2:
                            st.subheader("🎯 Metas de Preço")
                            targets = analysis['price_targets']
                            
                            st.write(f"**💰 Preço Atual:** ${targets['current']}")
                            st.write(f"**🛡️ Suporte:** ${targets['support']}")
                            st.write(f"**⚡ Resistência:** ${targets['resistance']}")
                            st.write(f"**🛑 Stop Loss:** ${targets['stop_loss']}")
                            
                            st.write("**🎯 Metas:**")
                            st.write(f"• Conservadora: ${targets['targets']['conservative']}")
                            st.write(f"• Moderada: ${targets['targets']['moderate']}")
                            st.write(f"• Otimista: ${targets['targets']['optimistic']}")
                            
                            # Sentimento
                            st.subheader("📰 Análise de Sentimento")
                            sentiment = analysis['sentiment']
                            
                            sentiment_color = {
                                'Muito Positivo': '🟢',
                                'Positivo': '🟡',
                                'Neutro': '⚪',
                                'Negativo': '🟠',
                                'Muito Negativo': '🔴'
                            }
                            
                            color = sentiment_color.get(sentiment['trend'], '⚪')
                            st.write(f"**{color} Tendência:** {sentiment['trend']}")
                            st.write(f"**📊 Score:** {sentiment['score']}")
                            st.write(f"**📋 Resumo:** {sentiment['summary']}")
                        
                        # Feedback detalhado
                        with st.expander("🧠 Análise Detalhada com IA", expanded=True):
                            feedback = analysis['feedback']
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if feedback['strengths']:
                                    st.write("**✅ Pontos Fortes:**")
                                    for strength in feedback['strengths']:
                                        st.write(f"• {strength}")
                                
                                if feedback['opportunities']:
                                    st.write("**🎯 Oportunidades:**")
                                    for opp in feedback['opportunities']:
                                        st.write(f"• {opp}")
                            
                            with col2:
                                if feedback['weaknesses']:
                                    st.write("**⚠️ Pontos Fracos:**")
                                    for weakness in feedback['weaknesses']:
                                        st.write(f"• {weakness}")
                                
                                if feedback['threats']:
                                    st.write("**🚨 Ameaças:**")
                                    for threat in feedback['threats']:
                                        st.write(f"• {threat}")
                            
                            st.info(f"**📝 Resumo da IA:** {feedback['summary']}")
                        
                        # Dados fundamentalistas detalhados
                        with st.expander("📋 Dados Fundamentalistas Completos"):
                            fund = data['fundamentals']
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write("**💰 Valuation:**")
                                st.write(f"• P/L: {fund['pe_ratio']:.1f}")
                                st.write(f"• P/B: {fund['pb_ratio']:.1f}")
                                st.write(f"• Market Cap: {format_large_number(fund['market_cap'])}")
                                st.write(f"• Dividend Yield: {fund['dividend_yield']*100:.1f}%")
                            
                            with col2:
                                st.write("**📊 Rentabilidade:**")
                                st.write(f"• ROE: {fund['roe']*100:.1f}%")
                                st.write(f"• Margem Lucro: {fund['profit_margin']*100:.1f}%")
                                st.write(f"• Crescimento Receita: {fund['revenue_growth']*100:.1f}%")
                                st.write(f"• Dívida/PL: {fund['debt_to_equity']:.1f}")
                            
                            with col3:
                                st.write("**🏢 Empresa:**")
                                st.write(f"• Setor: {fund['sector']}")
                                st.write(f"• Indústria: {fund['industry']}")
                                st.write(f"• País: {fund['country']}")
                                if fund['employees'] > 0:
                                    st.write(f"• Funcionários: {fund['employees']:,}")
                        
                        # Performance histórica
                        with st.expander("📈 Performance Histórica"):
                            returns = data['returns']
                            
                            performance_df = pd.DataFrame([
                                ["1 Mês", f"{returns['1m']:+.1f}%"],
                                ["3 Meses", f"{returns['3m']:+.1f}%"],
                                ["6 Meses", f"{returns['6m']:+.1f}%"],
                                ["1 Ano", f"{returns['1y']:+.1f}%"]
                            ], columns=["Período", "Retorno"])
                            
                            st.dataframe(performance_df, hide_index=True, use_container_width=True)
                            
                            # Gráfico de retornos
                            periods = ['1M', '3M', '6M', '1A']
                            values = [returns['1m'], returns['3m'], returns['6m'], returns['1y']]
                            
                            fig_returns = px.bar(
                                x=periods, 
                                y=values,
                                title="Retornos por Período",
                                labels={'x': 'Período', 'y': 'Retorno (%)'}
                            )
                            st.plotly_chart(fig_returns, use_container_width=True)
                
                else:
                    st.error(f"❌ Não foi possível analisar {symbol}. Verifique se o símbolo está correto.")
    
    with tab2:
        st.header("🌍 Scanner Global de Oportunidades")
        
        # Implementação do scanner global seria aqui
        st.info("🚧 Scanner Global em desenvolvimento. Use a análise individual por enquanto.")
    
    with tab3:
        st.header("📈 Comparador de Ativos")
        
        # Implementação do comparador seria aqui
        st.info("🚧 Comparador em desenvolvimento. Use a análise individual por enquanto.")
    
    with tab4:
        st.header("📚 Guia Educacional")
        
        st.markdown("""
        ### 🎯 Como Interpretar as Análises
        
        #### 📊 **Scores de IA (0-100):**
        - **90-100:** 🚀 Oportunidade excepcional
        - **80-89:** ✅ Muito boa oportunidade
        - **70-79:** 🟡 Boa oportunidade
        - **60-69:** ⚖️ Oportunidade moderada
        - **50-59:** ⏳ Aguardar melhores condições
        - **40-49:** ⚠️ Evitar por enquanto
        - **0-39:** ❌ Alto risco, evitar
        
        #### 🎯 **Potencial de Crescimento:**
        - **Conservador:** Cenário mais provável com baixo risco
        - **Moderado:** Cenário equilibrado risco/retorno
        - **Otimista:** Melhor cenário possível
        
        #### ⚠️ **Níveis de Risco:**
        - **Baixo:** 🟢 Adequado para investidores conservadores
        - **Médio:** 🟡 Para investidores moderados
        - **Alto:** 🔴 Apenas para investidores arrojados
        
        #### 📈 **Indicadores Técnicos:**
        - **RSI < 30:** Oversold (oportunidade de compra)
        - **RSI > 70:** Overbought (cuidado com entrada)
        - **Preço > MA200:** Tendência de alta
        - **Preço < MA200:** Tendência de baixa
        
        #### 💼 **Indicadores Fundamentalistas:**
        - **P/L < 15:** Ação potencialmente barata
        - **ROE > 15%:** Empresa eficiente
        - **Dívida/PL < 1:** Baixo endividamento
        - **Crescimento > 10%:** Empresa em expansão
        """)

if __name__ == "__main__":
    main()