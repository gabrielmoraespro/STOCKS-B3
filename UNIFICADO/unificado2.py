#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Unificado de Análise Global de Investimentos
Versão Corrigida e Funcional
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import concurrent.futures
import time
from typing import List, Dict, Tuple
import warnings

warnings.filterwarnings("ignore")

# Configuração da página
st.set_page_config(
    page_title="🌍 Sistema Global de Investimentos",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================
# BASE DE DADOS UNIFICADA
# ================================


class GlobalAssetDatabase:
    """Base de dados global unificada de todos os ativos"""

    def __init__(self):
        self.global_assets = self._load_comprehensive_database()
        self.crypto_symbols = self._load_crypto_database()

    def _load_comprehensive_database(self):
        """Base de dados completa e unificada"""
        return {
            "USA": {
                "indices": {
                    "^GSPC": "S&P 500",
                    "^DJI": "Dow Jones",
                    "^IXIC": "NASDAQ",
                    "^RUT": "Russell 2000",
                    "^VIX": "VIX (Volatilidade)",
                },
                "mega_caps": {
                    "AAPL": "Apple Inc.",
                    "MSFT": "Microsoft Corp.",
                    "GOOGL": "Alphabet Inc.",
                    "AMZN": "Amazon.com Inc.",
                    "NVDA": "NVIDIA Corp.",
                    "TSLA": "Tesla Inc.",
                    "META": "Meta Platforms",
                    "BRK-B": "Berkshire Hathaway",
                    "UNH": "UnitedHealth Group",
                    "JNJ": "Johnson & Johnson",
                    "V": "Visa Inc.",
                    "PG": "Procter & Gamble",
                    "JPM": "JPMorgan Chase",
                    "XOM": "Exxon Mobil",
                    "HD": "Home Depot",
                    "CVX": "Chevron Corp.",
                    "MA": "Mastercard Inc.",
                    "ABBV": "AbbVie Inc.",
                    "PFE": "Pfizer Inc.",
                    "KO": "Coca-Cola Co.",
                },
                "tech_stocks": {
                    "NFLX": "Netflix Inc.",
                    "ADBE": "Adobe Inc.",
                    "ORCL": "Oracle Corp.",
                    "INTC": "Intel Corp.",
                    "CSCO": "Cisco Systems",
                    "AMD": "Advanced Micro Devices",
                    "QCOM": "Qualcomm Inc.",
                    "TXN": "Texas Instruments",
                    "IBM": "IBM Corp.",
                    "MU": "Micron Technology",
                },
                "finance": {
                    "JPM": "JPMorgan Chase",
                    "BAC": "Bank of America",
                    "WFC": "Wells Fargo",
                    "GS": "Goldman Sachs",
                    "MS": "Morgan Stanley",
                    "V": "Visa Inc.",
                    "MA": "Mastercard Inc.",
                    "PYPL": "PayPal Holdings",
                },
                "energy": {
                    "XOM": "Exxon Mobil",
                    "CVX": "Chevron Corp.",
                    "COP": "ConocoPhillips",
                    "SLB": "Schlumberger",
                    "HAL": "Halliburton",
                },
                "healthcare": {
                    "JNJ": "Johnson & Johnson",
                    "PFE": "Pfizer Inc.",
                    "MRK": "Merck & Co.",
                    "ABBV": "AbbVie Inc.",
                    "LLY": "Eli Lilly and Co.",
                },
            },
            "Brasil": {
                "indices": {
                    "^BVSP": "Ibovespa",
                },
                "blue_chips": {
                    "PETR4.SA": "Petrobras",
                    "VALE3.SA": "Vale",
                    "ITUB4.SA": "Itaú Unibanco",
                    "BBDC4.SA": "Bradesco",
                    "ABEV3.SA": "Ambev",
                    "B3SA3.SA": "B3",
                    "JBSS3.SA": "JBS",
                    "RENT3.SA": "Localiza",
                    "LREN3.SA": "Lojas Renner",
                    "MGLU3.SA": "Magazine Luiza",
                    "WEGE3.SA": "WEG",
                    "SUZB3.SA": "Suzano",
                },
                "fiis": {
                    "HGLG11.SA": "CSHG Logística",
                    "XPML11.SA": "XP Malls",
                    "BTLG11.SA": "BTG Logística",
                    "VILG11.SA": "Villagio",
                    "KNCR11.SA": "Kinea Rendimento",
                    "MXRF11.SA": "Maxi Renda",
                },
            },
            "Europa": {
                "indices": {
                    "^GDAXI": "DAX (Alemanha)",
                    "^FCHI": "CAC 40 (França)",
                    "^FTSE": "FTSE 100 (Reino Unido)",
                },
                "stocks": {
                    "ASML.AS": "ASML Holding (Holanda)",
                    "SAP.DE": "SAP SE (Alemanha)",
                    "NVO": "Novo Nordisk",
                    "NESN.SW": "Nestlé (Suíça)",
                },
            },
            "Asia": {
                "indices": {
                    "^N225": "Nikkei 225 (Japão)",
                    "^HSI": "Hang Seng (Hong Kong)",
                },
                "stocks": {
                    "TSM": "Taiwan Semiconductor",
                    "BABA": "Alibaba Group",
                    "TM": "Toyota Motor",
                    "SONY": "Sony Group",
                },
            },
            "ETFs_Globais": {
                "SPY": "SPDR S&P 500 ETF",
                "QQQ": "Invesco QQQ Trust",
                "IWM": "iShares Russell 2000",
                "EFA": "iShares MSCI EAFE",
                "GLD": "SPDR Gold Shares",
                "SLV": "iShares Silver Trust",
            },
            "Commodities": {
                "GC=F": "Ouro Futuro",
                "SI=F": "Prata Futuro",
                "CL=F": "Petróleo WTI",
                "BZ=F": "Petróleo Brent",
            },
        }

    def _load_crypto_database(self):
        """Base de dados de criptomoedas"""
        return {
            "BTC-USD": "Bitcoin",
            "ETH-USD": "Ethereum",
            "BNB-USD": "Binance Coin",
            "ADA-USD": "Cardano",
            "XRP-USD": "Ripple",
            "SOL-USD": "Solana",
            "DOT-USD": "Polkadot",
            "DOGE-USD": "Dogecoin",
            "AVAX-USD": "Avalanche",
            "MATIC-USD": "Polygon",
            "LTC-USD": "Litecoin",
            "UNI-USD": "Uniswap",
            "LINK-USD": "Chainlink",
        }

    def search_asset(self, query: str) -> List[Dict]:
        """Busca universal de ativos"""
        query = query.upper()
        results = []

        # Buscar em todas as categorias
        for region, categories in self.global_assets.items():
            for category, assets in categories.items():
                for symbol, name in assets.items():
                    if (
                        query in symbol.upper()
                        or query in name.upper()
                        or symbol.upper().startswith(query)
                    ):
                        results.append(
                            {
                                "symbol": symbol,
                                "name": name,
                                "region": region,
                                "category": category,
                                "type": "stock",
                            }
                        )

        # Buscar criptomoedas
        for symbol, name in self.crypto_symbols.items():
            if (
                query in symbol.upper()
                or query in name.upper()
                or symbol.upper().startswith(query)
            ):
                results.append(
                    {
                        "symbol": symbol,
                        "name": name,
                        "region": "Global",
                        "category": "cryptocurrency",
                        "type": "crypto",
                    }
                )

        return results[:20]

    def get_all_symbols(self) -> List[str]:
        """Retorna todos os símbolos disponíveis"""
        symbols = []

        for region, categories in self.global_assets.items():
            for category, assets in categories.items():
                symbols.extend(assets.keys())

        symbols.extend(self.crypto_symbols.keys())
        return symbols

    def get_symbols_by_category(self, categories: List[str]) -> List[str]:
        """Retorna símbolos por categoria"""
        symbols = []

        for category in categories:
            if category == "Crypto":
                symbols.extend(self.crypto_symbols.keys())
            elif category == "USA_Mega":
                if (
                    "USA" in self.global_assets
                    and "mega_caps" in self.global_assets["USA"]
                ):
                    symbols.extend(self.global_assets["USA"]["mega_caps"].keys())
            elif category == "USA_Tech":
                if (
                    "USA" in self.global_assets
                    and "tech_stocks" in self.global_assets["USA"]
                ):
                    symbols.extend(self.global_assets["USA"]["tech_stocks"].keys())
            elif category == "Brazil_Stocks":
                if (
                    "Brasil" in self.global_assets
                    and "blue_chips" in self.global_assets["Brasil"]
                ):
                    symbols.extend(self.global_assets["Brasil"]["blue_chips"].keys())
            elif category == "ETFs":
                if "ETFs_Globais" in self.global_assets:
                    symbols.extend(self.global_assets["ETFs_Globais"].keys())

        return list(set(symbols))

    def get_random_picks(self, count: int = 10) -> List[Dict]:
        """Seleção inteligente de ativos interessantes"""
        picks = [
            {"symbol": "AAPL", "reason": "Líder global em tecnologia"},
            {"symbol": "NVDA", "reason": "Pioneira em IA e chips"},
            {"symbol": "PETR4.SA", "reason": "Maior petrolífera da América Latina"},
            {"symbol": "BTC-USD", "reason": "Reserva de valor digital"},
            {"symbol": "^GSPC", "reason": "Índice mais importante do mundo"},
            {"symbol": "VALE3.SA", "reason": "Maior mineradora de ferro"},
        ]
        return picks[:count]


# ================================
# PROVEDOR DE DADOS SIMPLIFICADO
# ================================


class UnifiedDataProvider:
    """Provedor de dados simplificado e robusto"""

    def get_comprehensive_data(self, symbol: str, period: str = "1y") -> Dict:
        """Coleta dados de forma robusta"""
        try:
            symbol = symbol.strip().upper()
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                return None

            # Informações básicas
            try:
                info = ticker.info
                if not isinstance(info, dict):
                    info = {}
            except:
                info = {}

            current_price = float(hist["Close"][-1])

            # Calcular métricas
            returns = self._calculate_returns(hist["Close"])
            risk_metrics = self._calculate_risk_metrics(hist["Close"])
            technical = self._calculate_technical_indicators(hist)
            fundamentals = self._extract_fundamentals(info)

            return {
                "symbol": symbol,
                "current_price": current_price,
                "hist_data": hist.reset_index(),
                "returns": returns,
                "risk_metrics": risk_metrics,
                "technical": technical,
                "fundamentals": fundamentals,
                "price_data": hist["Close"].tolist(),
                "volume_data": hist["Volume"].tolist(),
                "last_updated": datetime.now().isoformat(),
            }

        except Exception as e:
            print(f"Erro ao obter dados de {symbol}: {str(e)}")
            return None

    def _calculate_returns(self, prices):
        """Calcula retornos por período"""
        current = float(prices[-1])
        returns = {}

        periods = {
            "1d": 1,
            "1w": 5,
            "2w": 10,
            "1m": 21,
            "2m": 42,
            "3m": 63,
            "6m": 126,
            "1y": 252,
        }

        for label, days in periods.items():
            if len(prices) >= days:
                past = float(prices[-days])
                returns[label] = ((current - past) / past) * 100 if past != 0 else 0
            else:
                returns[label] = 0

        return returns

    def _calculate_risk_metrics(self, prices):
        """Calcula métricas de risco"""
        try:
            returns = prices.pct_change().dropna()
            volatility = (
                float(returns.std() * np.sqrt(252) * 100) if len(returns) > 0 else 0
            )

            # Drawdown
            rolling_max = prices.expanding().max()
            drawdown = ((prices - rolling_max) / rolling_max) * 100
            max_drawdown = float(drawdown.min())
            current_drawdown = float(drawdown.iloc[-1])

            # Sharpe ratio
            if len(returns) > 0 and returns.std() > 0:
                excess_returns = returns.mean() * 252 - 0.02
                sharpe = excess_returns / (returns.std() * np.sqrt(252))
            else:
                sharpe = 0

            return {
                "volatility": volatility,
                "max_drawdown": max_drawdown,
                "current_drawdown": current_drawdown,
                "sharpe_ratio": float(sharpe),
                "beta": 1.0,
            }
        except:
            return {
                "volatility": 0,
                "max_drawdown": 0,
                "current_drawdown": 0,
                "sharpe_ratio": 0,
                "beta": 1.0,
            }

    def _calculate_technical_indicators(self, hist):
        """Calcula indicadores técnicos"""
        try:
            prices = hist["Close"]
            current_price = float(prices.iloc[-1])

            # RSI
            rsi = self._calculate_rsi(prices.values)

            # Médias móveis
            ma20 = (
                float(prices.rolling(20).mean().iloc[-1])
                if len(prices) >= 20
                else current_price
            )
            ma50 = (
                float(prices.rolling(50).mean().iloc[-1])
                if len(prices) >= 50
                else current_price
            )
            ma200 = (
                float(prices.rolling(200).mean().iloc[-1])
                if len(prices) >= 200
                else current_price
            )

            # MACD
            macd_line, macd_signal, macd_histogram = self._calculate_macd(prices)

            # Bandas de Bollinger
            bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(prices)

            return {
                "rsi": rsi,
                "ma20": ma20,
                "ma50": ma50,
                "ma200": ma200,
                "macd": {
                    "line": macd_line,
                    "signal": macd_signal,
                    "histogram": macd_histogram,
                },
                "bollinger": {
                    "upper": bb_upper,
                    "middle": bb_middle,
                    "lower": bb_lower,
                },
                "avg_volume": 0,
            }
        except:
            current_price = float(hist["Close"].iloc[-1])
            return {
                "rsi": 50,
                "ma20": current_price,
                "ma50": current_price,
                "ma200": current_price,
                "macd": {"line": 0, "signal": 0, "histogram": 0},
                "bollinger": {
                    "upper": current_price * 1.02,
                    "middle": current_price,
                    "lower": current_price * 0.98,
                },
                "avg_volume": 0,
            }

    def _calculate_rsi(self, prices, period=14):
        """Calcula RSI"""
        if len(prices) < period + 1:
            return 50

        try:
            deltas = np.diff(prices)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)

            avg_gain = np.mean(gains[-period:])
            avg_loss = np.mean(losses[-period:])

            if avg_loss == 0:
                return 100

            rs = avg_gain / avg_loss
            return 100 - (100 / (1 + rs))
        except:
            return 50

    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calcula MACD"""
        try:
            if len(prices) < slow:
                return 0, 0, 0

            exp1 = prices.ewm(span=fast).mean()
            exp2 = prices.ewm(span=slow).mean()
            macd_line = exp1 - exp2
            macd_signal = macd_line.ewm(span=signal).mean()
            macd_histogram = macd_line - macd_signal

            return (
                float(macd_line.iloc[-1]),
                float(macd_signal.iloc[-1]),
                float(macd_histogram.iloc[-1]),
            )
        except:
            return 0, 0, 0

    def _calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calcula Bandas de Bollinger"""
        try:
            if len(prices) < period:
                current = float(prices.iloc[-1])
                return current * 1.02, current, current * 0.98

            sma = prices.rolling(period).mean()
            std = prices.rolling(period).std()

            upper = sma + (std * std_dev)
            lower = sma - (std * std_dev)

            return (float(upper.iloc[-1]), float(sma.iloc[-1]), float(lower.iloc[-1]))
        except:
            current = float(prices.iloc[-1])
            return current * 1.02, current, current * 0.98

    def _extract_fundamentals(self, info):
        """Extrai dados fundamentalistas básicos"""
        try:
            return {
                "market_cap": info.get("marketCap", 0) or 0,
                "pe_ratio": info.get("forwardPE", info.get("trailingPE", 0)) or 0,
                "pb_ratio": info.get("priceToBook", 0) or 0,
                "ps_ratio": info.get("priceToSalesTrailing12Months", 0) or 0,
                "roe": info.get("returnOnEquity", 0) or 0,
                "roa": info.get("returnOnAssets", 0) or 0,
                "debt_to_equity": info.get("debtToEquity", 0) or 0,
                "current_ratio": info.get("currentRatio", 0) or 0,
                "profit_margin": info.get("profitMargins", 0) or 0,
                "operating_margin": info.get("operatingMargins", 0) or 0,
                "revenue_growth": info.get("revenueGrowth", 0) or 0,
                "earnings_growth": info.get("earningsGrowth", 0) or 0,
                "dividend_yield": info.get("dividendYield", 0) or 0,
                "sector": info.get("sector", "N/A") or "N/A",
                "industry": info.get("industry", "N/A") or "N/A",
                "country": info.get("country", "N/A") or "N/A",
            }
        except:
            return {
                "market_cap": 0,
                "pe_ratio": 0,
                "pb_ratio": 0,
                "ps_ratio": 0,
                "roe": 0,
                "roa": 0,
                "debt_to_equity": 0,
                "current_ratio": 0,
                "profit_margin": 0,
                "operating_margin": 0,
                "revenue_growth": 0,
                "earnings_growth": 0,
                "dividend_yield": 0,
                "sector": "N/A",
                "industry": "N/A",
                "country": "N/A",
            }


# ================================
# ANALISADOR AVANÇADO
# ================================


class AdvancedAnalyzer:
    """Analisador avançado com algoritmos de IA"""

    def __init__(self):
        self.data_provider = UnifiedDataProvider()

    def calculate_ai_scores(self, data: Dict) -> Dict:
        """Calcula scores com algoritmos de IA"""
        technical_score = self._calculate_technical_score(data)
        fundamental_score = self._calculate_fundamental_score(data)
        momentum_score = self._calculate_momentum_score(data)
        risk_score = self._calculate_risk_score(data)
        value_score = self._calculate_value_score(data)
        quality_score = self._calculate_quality_score(data)

        # Score final ponderado
        weights = {
            "technical": 0.20,
            "fundamental": 0.25,
            "momentum": 0.15,
            "value": 0.20,
            "quality": 0.15,
            "risk_penalty": 0.05,
        }

        final_score = (
            technical_score * weights["technical"]
            + fundamental_score * weights["fundamental"]
            + momentum_score * weights["momentum"]
            + value_score * weights["value"]
            + quality_score * weights["quality"]
            - (risk_score * weights["risk_penalty"])
        )

        return {
            "technical": round(technical_score, 1),
            "fundamental": round(fundamental_score, 1),
            "momentum": round(momentum_score, 1),
            "value": round(value_score, 1),
            "quality": round(quality_score, 1),
            "risk": round(risk_score, 1),
            "final": round(max(0, min(100, final_score)), 1),
        }

    def _calculate_technical_score(self, data: Dict) -> float:
        """Score técnico avançado"""
        score = 50
        technical = data["technical"]
        price = data["current_price"]

        # RSI
        rsi = technical["rsi"]
        if 30 <= rsi <= 70:
            score += 15
        elif rsi < 30:
            score += 25  # Oversold = oportunidade
        elif rsi > 70:
            score -= 10  # Overbought

        # Posição vs médias móveis
        if price > technical["ma20"]:
            score += 8
        if price > technical["ma50"]:
            score += 12
        if price > technical["ma200"]:
            score += 15

        # MACD
        macd = technical["macd"]
        if macd["line"] > macd["signal"]:
            score += 10

        # Drawdown atual (oportunidade)
        current_dd = abs(data["risk_metrics"]["current_drawdown"])
        if current_dd > 30:
            score += 20
        elif current_dd > 20:
            score += 15
        elif current_dd > 10:
            score += 10

        return max(0, min(100, score))

    def _calculate_fundamental_score(self, data: Dict) -> float:
        """Score fundamentalista avançado"""
        score = 50
        fund = data["fundamentals"]

        # P/L
        pe = fund["pe_ratio"]
        if 0 < pe < 8:
            score += 30
        elif 8 <= pe < 15:
            score += 20
        elif 15 <= pe < 25:
            score += 10
        elif pe > 40:
            score -= 15

        # ROE
        roe = fund["roe"]
        if roe > 0.30:
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
        debt = fund["debt_to_equity"]
        if debt < 0.2:
            score += 20
        elif debt < 0.4:
            score += 15
        elif debt < 1.0:
            score += 10
        elif debt > 3.0:
            score -= 25

        # Crescimento
        growth = fund["revenue_growth"]
        if growth > 0.20:
            score += 20
        elif growth > 0.10:
            score += 15
        elif growth > 0.05:
            score += 10
        elif growth < -0.10:
            score -= 20

        return max(0, min(100, score))

    def _calculate_momentum_score(self, data: Dict) -> float:
        """Score de momentum"""
        score = 50
        returns = data["returns"]

        weights = {"1w": 0.1, "1m": 0.2, "3m": 0.3, "6m": 0.25, "1y": 0.15}

        for period, weight in weights.items():
            ret = returns.get(period, 0)
            if ret > 20:
                score += 20 * weight
            elif ret > 10:
                score += 15 * weight
            elif ret > 5:
                score += 10 * weight
            elif ret < -15:
                score -= 15 * weight

        return max(0, min(100, score))

    def _calculate_value_score(self, data: Dict) -> float:
        """Score de valor"""
        score = 50
        fund = data["fundamentals"]

        # P/B
        pb = fund["pb_ratio"]
        if 0 < pb < 1:
            score += 25
        elif 1 <= pb < 2:
            score += 15
        elif pb > 5:
            score -= 15

        # Dividend Yield
        div_yield = fund["dividend_yield"]
        if div_yield > 0.05:
            score += 15
        elif div_yield > 0.03:
            score += 10

        return max(0, min(100, score))

    def _calculate_quality_score(self, data: Dict) -> float:
        """Score de qualidade"""
        score = 50
        fund = data["fundamentals"]

        # ROA
        roa = fund["roa"]
        if roa > 0.15:
            score += 25
        elif roa > 0.10:
            score += 20
        elif roa > 0.05:
            score += 10
        elif roa < 0:
            score -= 20

        # Margem de lucro
        margin = fund["profit_margin"]
        if margin > 0.20:
            score += 20
        elif margin > 0.10:
            score += 10
        elif margin < 0:
            score -= 15

        return max(0, min(100, score))

    def _calculate_risk_score(self, data: Dict) -> float:
        """Score de risco (maior = mais arriscado)"""
        risk = 0

        # Volatilidade
        vol = data["risk_metrics"]["volatility"]
        if vol > 80:
            risk += 40
        elif vol > 60:
            risk += 30
        elif vol > 40:
            risk += 20
        elif vol > 25:
            risk += 10

        # Debt to Equity
        debt = data["fundamentals"]["debt_to_equity"]
        if debt > 5:
            risk += 30
        elif debt > 3:
            risk += 20
        elif debt > 1:
            risk += 10

        # ROE negativo
        if data["fundamentals"]["roe"] < 0:
            risk += 25

        return min(100, risk)


# ================================
# FUNÇÕES DE VISUALIZAÇÃO
# ================================


def create_price_chart(data: Dict) -> go.Figure:
    """Cria gráfico avançado de preços"""
    if not data or "hist_data" not in data:
        return None

    df = pd.DataFrame(data["hist_data"])
    df["Date"] = pd.to_datetime(df["Date"])

    fig = go.Figure()

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Preço",
        )
    )

    # Médias móveis
    if len(df) >= 20:
        ma20 = df["Close"].rolling(20).mean()
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=ma20,
                mode="lines",
                name="MA20",
                line=dict(color="orange", width=1),
            )
        )

    if len(df) >= 50:
        ma50 = df["Close"].rolling(50).mean()
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=ma50,
                mode="lines",
                name="MA50",
                line=dict(color="blue", width=1),
            )
        )

    # Configurações do layout
    fig.update_layout(
        title=f"📊 Análise Técnica - {data['symbol']}",
        xaxis_title="Data",
        yaxis_title="Preço ($)",
        height=600,
        showlegend=True,
        xaxis_rangeslider_visible=False,
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


# ================================
# INTERFACE PRINCIPAL
# ================================


def main():
    """Interface principal"""

    # Header
    st.title("🌍 Sistema Global de Análise de Investimentos")
    st.subheader("Plataforma Unificada com IA Avançada")

    # Inicializar componentes
    try:
        # Teste de conectividade
        test_ticker = yf.Ticker("AAPL")
        test_data = test_ticker.history(period="1d")

        if test_data.empty:
            st.error("❌ Problema de conectividade com dados financeiros")
            return

        # Inicializar sistema
        asset_db = GlobalAssetDatabase()
        data_provider = UnifiedDataProvider()
        analyzer = AdvancedAnalyzer()

        all_symbols = asset_db.get_all_symbols()

        if len(all_symbols) == 0:
            st.error("❌ Erro ao carregar base de dados")
            return

        st.sidebar.success(f"✅ Sistema pronto: {len(all_symbols)} ativos")

    except Exception as e:
        st.error(f"❌ Erro na inicialização: {str(e)}")
        st.info("💡 Soluções:")
        st.write("• Verifique sua conexão com internet")
        st.write("• Recarregue a página (F5)")
        return

    # Sidebar
    with st.sidebar:
        st.title("🎯 Navegação")

        # Busca universal
        st.subheader("🔍 Busca Universal")
        search_query = st.text_input(
            "Buscar ativo:", placeholder="Ex: AAPL, Bitcoin, S&P 500"
        )

        if search_query and len(search_query) >= 2:
            try:
                results = asset_db.search_asset(search_query)
                if results:
                    st.write("**🎯 Resultados:**")
                    for result in results[:5]:
                        if st.button(
                            f"{result['symbol']} - {result['name'][:20]}",
                            key=f"search_{result['symbol']}",
                        ):
                            st.session_state["selected_symbol"] = result["symbol"]
            except:
                st.write("⚠️ Erro na busca")

        # Picks inteligentes
        st.subheader("💡 Picks Rápidos")
        try:
            picks = asset_db.get_random_picks(6)
            for pick in picks:
                if st.button(
                    f"{pick['symbol']}",
                    key=f"pick_{pick['symbol']}",
                    help=pick["reason"],
                ):
                    st.session_state["selected_symbol"] = pick["symbol"]
        except:
            st.write("Picks indisponíveis")

        # Info do sistema
        st.markdown("---")
        st.subheader("ℹ️ Sistema")
        st.metric("Ativos", f"{len(all_symbols):,}")
        st.write("🇺🇸 **EUA:** Ações, ETFs")
        st.write("🇧🇷 **Brasil:** Ações, FIIs")
        st.write("💰 **Crypto:** Top moedas")

    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🔍 Análise Individual",
            "🌍 Scanner Global",
            "📊 Comparador",
            "📚 Educacional",
        ]
    )

    # ================================
    # TAB 1: ANÁLISE INDIVIDUAL
    # ================================
    with tab1:
        st.header("🔍 Análise Individual Completa")

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            symbol_input = st.text_input(
                "Digite o símbolo:",
                value=st.session_state.get("selected_symbol", ""),
                placeholder="Ex: AAPL, PETR4.SA, BTC-USD",
            )

        with col2:
            period = st.selectbox("Período:", ["3mo", "6mo", "1y", "2y"], index=2)

        with col3:
            analyze_btn = st.button("🚀 ANALISAR", type="primary")

        # Exemplos rápidos
        st.write("**⚡ Exemplos:**")
        cols = st.columns(5)
        examples = [
            ("🇺🇸 AAPL", "AAPL"),
            ("🇺🇸 NVDA", "NVDA"),
            ("🇧🇷 PETR4.SA", "PETR4.SA"),
            ("💰 BTC-USD", "BTC-USD"),
            ("📊 ^GSPC", "^GSPC"),
        ]

        for i, (label, symbol) in enumerate(examples):
            with cols[i]:
                if st.button(label, key=f"ex_{symbol}"):
                    st.session_state["selected_symbol"] = symbol
                    st.rerun()

        if analyze_btn and symbol_input:
            symbol = symbol_input.upper().strip()

            with st.spinner(f"🤖 Analisando {symbol}..."):
                try:
                    # Obter dados
                    data = data_provider.get_comprehensive_data(symbol, period)

                    if data:
                        # Calcular scores IA
                        ai_scores = analyzer.calculate_ai_scores(data)

                        # Métricas principais
                        current_price = data["current_price"]
                        return_1y = data["returns"]["1y"]
                        final_score = ai_scores["final"]

                        # Recomendação
                        if final_score >= 80:
                            rec = {
                                "action": "COMPRA FORTE",
                                "emoji": "🚀",
                                "color": "success",
                            }
                        elif final_score >= 70:
                            rec = {
                                "action": "COMPRAR",
                                "emoji": "✅",
                                "color": "success",
                            }
                        elif final_score >= 60:
                            rec = {
                                "action": "COMPRA MODERADA",
                                "emoji": "🟢",
                                "color": "info",
                            }
                        elif final_score >= 50:
                            rec = {
                                "action": "AGUARDAR",
                                "emoji": "🟡",
                                "color": "warning",
                            }
                        else:
                            rec = {"action": "EVITAR", "emoji": "⚠️", "color": "error"}

                        # Exibir resultados
                        st.success(f"✅ **Análise completa para {symbol}**")

                        # Métricas em colunas
                        col1, col2, col3, col4, col5 = st.columns(5)

                        with col1:
                            st.metric(
                                "💰 Preço",
                                f"${current_price:.2f}",
                                f"{return_1y:+.1f}% (1Y)",
                            )

                        with col2:
                            st.metric(
                                f"{rec['emoji']} Score IA",
                                f"{final_score:.0f}/100",
                                rec["action"],
                            )

                        with col3:
                            volatility = data["risk_metrics"]["volatility"]
                            st.metric(
                                "📊 Volatilidade",
                                f"{volatility:.1f}%",
                                f"RSI: {data['technical']['rsi']:.0f}",
                            )

                        with col4:
                            market_cap = data["fundamentals"]["market_cap"]
                            st.metric(
                                "🏢 Market Cap",
                                format_large_number(market_cap),
                                data["fundamentals"]["sector"][:15],
                            )

                        with col5:
                            drawdown = data["risk_metrics"]["current_drawdown"]
                            st.metric("📉 Drawdown", f"{drawdown:.1f}%", "vs Pico")

                        # Recomendação principal
                        if rec["color"] == "success":
                            st.success(
                                f"## {rec['emoji']} RECOMENDAÇÃO: {rec['action']}"
                            )
                        elif rec["color"] == "warning":
                            st.warning(
                                f"## {rec['emoji']} RECOMENDAÇÃO: {rec['action']}"
                            )
                        else:
                            st.error(f"## {rec['emoji']} RECOMENDAÇÃO: {rec['action']}")

                        # Gráfico de preços
                        try:
                            chart = create_price_chart(data)
                            if chart:
                                st.plotly_chart(chart, use_container_width=True)
                        except:
                            st.info("📊 Gráfico temporariamente indisponível")

                        # Análise detalhada
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("📊 Scores IA")
                            scores_df = pd.DataFrame(
                                [
                                    ["🔧 Técnico", f"{ai_scores['technical']:.1f}/100"],
                                    [
                                        "💼 Fundamental",
                                        f"{ai_scores['fundamental']:.1f}/100",
                                    ],
                                    ["🚀 Momentum", f"{ai_scores['momentum']:.1f}/100"],
                                    ["💎 Valor", f"{ai_scores['value']:.1f}/100"],
                                    ["⭐ Qualidade", f"{ai_scores['quality']:.1f}/100"],
                                    ["⚠️ Risco", f"{ai_scores['risk']:.1f}/100"],
                                    [
                                        "🎯 **Final**",
                                        f"**{ai_scores['final']:.1f}/100**",
                                    ],
                                ],
                                columns=["Categoria", "Score"],
                            )

                            st.dataframe(
                                scores_df, hide_index=True, use_container_width=True
                            )

                        with col2:
                            st.subheader("💼 Fundamentals")
                            fund = data["fundamentals"]
                            st.write(f"**P/L:** {fund['pe_ratio']:.1f}")
                            st.write(f"**P/B:** {fund['pb_ratio']:.1f}")
                            st.write(f"**ROE:** {fund['roe']*100:.1f}%")
                            st.write(f"**Margem:** {fund['profit_margin']*100:.1f}%")
                            st.write(
                                f"**Crescimento:** {fund['revenue_growth']*100:.1f}%"
                            )
                            st.write(
                                f"**Div. Yield:** {fund['dividend_yield']*100:.1f}%"
                            )
                            st.write(f"**Setor:** {fund['sector']}")

                        # Performance histórica
                        with st.expander("📈 Performance Histórica"):
                            returns = data["returns"]
                            perf_df = pd.DataFrame(
                                [
                                    ["1 Mês", f"{returns['1m']:+.1f}%"],
                                    ["3 Meses", f"{returns['3m']:+.1f}%"],
                                    ["6 Meses", f"{returns['6m']:+.1f}%"],
                                    ["1 Ano", f"{returns['1y']:+.1f}%"],
                                ],
                                columns=["Período", "Retorno"],
                            )

                            st.dataframe(
                                perf_df, hide_index=True, use_container_width=True
                            )

                    else:
                        st.error(f"❌ Não foi possível analisar {symbol}")

                except Exception as e:
                    st.error(f"❌ Erro na análise: {str(e)}")

    # ================================
    # TAB 2: SCANNER GLOBAL
    # ================================
    with tab2:
        st.header("🌍 Scanner Global")
        st.info("⚡ Scanner simplificado para melhor performance")

        # Scanners rápidos
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🇺🇸 Top EUA", use_container_width=True):
                with st.spinner("Analisando EUA..."):
                    try:
                        usa_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA"]
                        results = []

                        for symbol in usa_symbols:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, "6mo"
                                )
                                if data:
                                    scores = analyzer.calculate_ai_scores(data)
                                    results.append(
                                        {
                                            "Symbol": symbol,
                                            "Score": scores["final"],
                                            "Price": f"${data['current_price']:.2f}",
                                            "Return_1Y": f"{data['returns']['1y']:.1f}%",
                                        }
                                    )
                            except:
                                continue

                        if results:
                            df = pd.DataFrame(results).sort_values(
                                "Score", ascending=False
                            )
                            st.success("✅ Top EUA")
                            st.dataframe(df, hide_index=True, use_container_width=True)
                    except:
                        st.error("❌ Erro no scanner EUA")

        with col2:
            if st.button("🇧🇷 Top Brasil", use_container_width=True):
                with st.spinner("Analisando Brasil..."):
                    try:
                        br_symbols = [
                            "PETR4.SA",
                            "VALE3.SA",
                            "ITUB4.SA",
                            "BBDC4.SA",
                            "WEGE3.SA",
                        ]
                        results = []

                        for symbol in br_symbols:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, "6mo"
                                )
                                if data:
                                    scores = analyzer.calculate_ai_scores(data)
                                    results.append(
                                        {
                                            "Symbol": symbol,
                                            "Score": scores["final"],
                                            "Price": f"R${data['current_price']:.2f}",
                                            "Return_1Y": f"{data['returns']['1y']:.1f}%",
                                        }
                                    )
                            except:
                                continue

                        if results:
                            df = pd.DataFrame(results).sort_values(
                                "Score", ascending=False
                            )
                            st.success("✅ Top Brasil")
                            st.dataframe(df, hide_index=True, use_container_width=True)
                    except:
                        st.error("❌ Erro no scanner Brasil")

        with col3:
            if st.button("💰 Top Crypto", use_container_width=True):
                with st.spinner("Analisando Crypto..."):
                    try:
                        crypto_symbols = [
                            "BTC-USD",
                            "ETH-USD",
                            "BNB-USD",
                            "ADA-USD",
                            "SOL-USD",
                        ]
                        results = []

                        for symbol in crypto_symbols:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, "6mo"
                                )
                                if data:
                                    scores = analyzer.calculate_ai_scores(data)
                                    results.append(
                                        {
                                            "Symbol": symbol,
                                            "Score": scores["final"],
                                            "Price": f"${data['current_price']:.2f}",
                                            "Volatility": f"{data['risk_metrics']['volatility']:.1f}%",
                                        }
                                    )
                            except:
                                continue

                        if results:
                            df = pd.DataFrame(results).sort_values(
                                "Score", ascending=False
                            )
                            st.success("✅ Top Crypto")
                            st.dataframe(df, hide_index=True, use_container_width=True)
                    except:
                        st.error("❌ Erro no scanner Crypto")

    # ================================
    # TAB 3: COMPARADOR
    # ================================
    with tab3:
        st.header("📊 Comparador de Ativos")

        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            symbols_input = st.text_input(
                "Símbolos separados por vírgula:",
                placeholder="Ex: AAPL,MSFT,GOOGL,PETR4.SA",
            )

        with col2:
            comp_period = st.selectbox("Período:", ["3mo", "6mo", "1y"], index=1)

        with col3:
            compare_btn = st.button("⚖️ COMPARAR", type="primary")

        # Comparações populares
        st.write("**🔥 Populares:**")
        popular = {
            "🏆 Big Tech": "AAPL,MSFT,GOOGL,NVDA",
            "💎 Brasil": "PETR4.SA,VALE3.SA,ITUB4.SA",
            "💰 Crypto": "BTC-USD,ETH-USD,BNB-USD",
            "📊 Índices": "^GSPC,^DJI,^BVSP",
        }

        cols = st.columns(len(popular))
        for i, (name, symbols) in enumerate(popular.items()):
            with cols[i]:
                if st.button(name, key=f"pop_{i}"):
                    symbols_input = symbols
                    compare_btn = True

        if compare_btn and symbols_input:
            symbols = [s.strip().upper() for s in symbols_input.split(",")]
            symbols = [s for s in symbols if s]

            if len(symbols) < 2:
                st.error("❌ Mínimo 2 ativos")
            elif len(symbols) > 5:
                st.warning("⚠️ Limitado a 5 ativos")
                symbols = symbols[:5]
            else:
                with st.spinner("🤖 Comparando..."):
                    try:
                        results = []

                        for symbol in symbols:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, comp_period
                                )
                                if data:
                                    scores = analyzer.calculate_ai_scores(data)
                                    results.append(
                                        {
                                            "Symbol": symbol,
                                            "Price": data["current_price"],
                                            "Score_IA": scores["final"],
                                            "Return_1Y": data["returns"]["1y"],
                                            "Volatility": data["risk_metrics"][
                                                "volatility"
                                            ],
                                            "PE_Ratio": data["fundamentals"][
                                                "pe_ratio"
                                            ],
                                            "Sector": data["fundamentals"]["sector"],
                                        }
                                    )
                            except:
                                continue

                        if results:
                            st.success(f"✅ Comparação de {len(results)} ativos!")

                            df = pd.DataFrame(results).sort_values(
                                "Score_IA", ascending=False
                            )

                            # Formatação para exibição
                            display_df = df.copy()
                            display_df["Price"] = display_df["Price"].apply(
                                lambda x: f"${x:.2f}"
                            )
                            display_df["Return_1Y"] = display_df["Return_1Y"].apply(
                                lambda x: f"{x:.1f}%"
                            )
                            display_df["Volatility"] = display_df["Volatility"].apply(
                                lambda x: f"{x:.1f}%"
                            )
                            display_df["PE_Ratio"] = display_df["PE_Ratio"].apply(
                                lambda x: f"{x:.1f}"
                            )

                            st.dataframe(
                                display_df, hide_index=True, use_container_width=True
                            )

                            # Melhor ativo
                            best = df.iloc[0]
                            st.success(
                                f"""
                            🏆 **MELHOR: {best['Symbol']}**
                            • Score: {best['Score_IA']:.1f}/100
                            • Preço: ${best['Price']:.2f}
                            • Retorno 1Y: {best['Return_1Y']:.1f}%
                            """
                            )

                            # Gráfico
                            try:
                                fig = px.bar(
                                    df,
                                    x="Symbol",
                                    y="Score_IA",
                                    color="Score_IA",
                                    title="Scores de IA",
                                    color_continuous_scale="RdYlGn",
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            except:
                                st.info("Gráfico indisponível")

                        else:
                            st.error("❌ Erro nos dados")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")

    # ================================
    # TAB 4: EDUCACIONAL
    # ================================
    with tab4:
        st.header("📚 Centro Educacional")

        st.markdown(
            """
        ### 🎯 Interpretação dos Scores IA
        
        **🚀 90-100:** Oportunidade excepcional
        **✅ 80-89:** Muito boa oportunidade  
        **🟢 70-79:** Boa oportunidade
        **🟡 60-69:** Moderada
        **⚠️ 50-59:** Aguardar
        **❌ 0-49:** Evitar
        
        ### 📊 Componentes
        - **Técnico (20%):** RSI, médias móveis, drawdown
        - **Fundamental (25%):** P/L, ROE, crescimento
        - **Momentum (15%):** Performance recente
        - **Valor (20%):** P/B, dividend yield
        - **Qualidade (15%):** ROA, margens
        - **Risco (5%):** Volatilidade, endividamento
        
        ### 💡 Dicas
        - Use símbolos corretos (AAPL, PETR4.SA)
        - Combine múltiplas análises
        - Considere seu perfil de risco
        - Diversifique investimentos
        
        ### ⚠️ Aviso
        Este sistema é uma ferramenta de análise educacional.
        Não constitui recomendação de investimento.
        Sempre consulte profissionais qualificados.
        """
        )

        with st.expander("❓ FAQ"):
            st.markdown(
                """
            **Q: Como usar o sistema?**
            A: Digite símbolos na análise individual ou use scanners rápidos.
            
            **Q: Dados são confiáveis?**
            A: Usamos Yahoo Finance, mas sempre faça sua pesquisa.
            
            **Q: Funciona para todos mercados?**
            A: Sim, EUA, Brasil, Europa, Ásia e criptomoedas.
            
            **Q: Posso confiar nas recomendações?**
            A: Use como base, mas tome suas próprias decisões.
            """
            )


if __name__ == "__main__":
    try:
        # Verificar dependências
        import yfinance
        import plotly

        # Executar app
        main()

        # Footer
        st.markdown("---")
        cols = st.columns(3)
        with cols[0]:
            st.write("🌍 **Sistema Global**")
        with cols[1]:
            st.write("🤖 **Powered by AI**")
        with cols[2]:
            st.write(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    except ImportError as e:
        st.error(f"❌ Faltando: {e}")
        st.code("pip install streamlit pandas numpy yfinance plotly")

    except Exception as e:
        st.error(f"❌ Erro: {e}")
        st.info("🔄 Recarregue a página")
