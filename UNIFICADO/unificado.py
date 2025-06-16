#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Unificado de Análise Global de Investimentos
Combina: Comparador, Analisador Global e Scanner
Versão Final Integrada
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
                    "AVGO": "Broadcom Inc.",
                    "COST": "Costco Wholesale",
                    "WMT": "Walmart Inc.",
                    "BAC": "Bank of America",
                    "DIS": "Walt Disney Co.",
                    "TMO": "Thermo Fisher Scientific",
                    "PEP": "PepsiCo Inc.",
                    "ABT": "Abbott Laboratories",
                    "LLY": "Eli Lilly and Co.",
                    "CRM": "Salesforce Inc.",
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
                    "AMAT": "Applied Materials",
                    "LRCX": "Lam Research",
                    "SHOP": "Shopify Inc.",
                    "SQ": "Block Inc.",
                    "ROKU": "Roku Inc.",
                    "ZM": "Zoom Video",
                    "PTON": "Peloton Interactive",
                    "SNAP": "Snap Inc.",
                    "UBER": "Uber Technologies",
                    "LYFT": "Lyft Inc.",
                    "PINS": "Pinterest Inc.",
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
                    "SQ": "Block Inc.",
                    "COIN": "Coinbase Global",
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
                    "^BVSP11": "IBrX 100",
                    "IFIX.SA": "IFIX (FIIs)",
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
                    "RAIL3.SA": "Rumo",
                    "VVAR3.SA": "Via Varejo",
                    "HAPV3.SA": "Hapvida",
                    "PCAR3.SA": "P&G Car",
                    "CSNA3.SA": "CSN",
                    "USIM5.SA": "Usiminas",
                    "AZUL4.SA": "Azul",
                    "MOVI3.SA": "Movida",
                    "RADL3.SA": "Raia Drogasil",
                    "COGN3.SA": "Cogna",
                },
                "fiis": {
                    "HGLG11.SA": "CSHG Logística",
                    "XPML11.SA": "XP Malls",
                    "BTLG11.SA": "BTG Logística",
                    "VILG11.SA": "Villagio",
                    "KNCR11.SA": "Kinea Rendimento",
                    "IRDM11.SA": "IRB Real Estate",
                    "MXRF11.SA": "Maxi Renda",
                    "BCFF11.SA": "BC Fund",
                    "HSML11.SA": "HSI Malls",
                    "RECT11.SA": "REC Recebíveis",
                    "VISC11.SA": "Vinci Shopping Centers",
                    "MALL11.SA": "Mall FII",
                },
            },
            "Europa": {
                "indices": {
                    "^GDAXI": "DAX (Alemanha)",
                    "^FCHI": "CAC 40 (França)",
                    "^FTSE": "FTSE 100 (Reino Unido)",
                    "^STOXX50E": "EURO STOXX 50",
                    "^AEX": "AEX (Holanda)",
                },
                "stocks": {
                    "ASML.AS": "ASML Holding (Holanda)",
                    "SAP.DE": "SAP SE (Alemanha)",
                    "LVMH.PA": "LVMH (França)",
                    "NVO": "Novo Nordisk",
                    "NESN.SW": "Nestlé (Suíça)",
                    "ROCHE.SW": "Roche (Suíça)",
                    "NOVN.SW": "Novartis (Suíça)",
                    "BAS.DE": "BASF (Alemanha)",
                    "SIE.DE": "Siemens (Alemanha)",
                    "ADYEN.AS": "Adyen (Holanda)",
                    "MC.PA": "LVMH (França)",
                    "OR.PA": "L'Oréal (França)",
                    "SAN.PA": "Sanofi (França)",
                    "TTE.PA": "TotalEnergies (França)",
                    "SHEL.L": "Shell (Reino Unido)",
                    "BP.L": "BP (Reino Unido)",
                    "VOD.L": "Vodafone (Reino Unido)",
                },
            },
            "Asia": {
                "indices": {
                    "^N225": "Nikkei 225 (Japão)",
                    "^HSI": "Hang Seng (Hong Kong)",
                    "000001.SS": "SSE Composite (China)",
                    "^KS11": "KOSPI (Coreia do Sul)",
                    "^STI": "Straits Times (Singapura)",
                },
                "stocks": {
                    "TSM": "Taiwan Semiconductor",
                    "BABA": "Alibaba Group",
                    "TCEHY": "Tencent Holdings",
                    "TM": "Toyota Motor",
                    "SONY": "Sony Group",
                    "7203.T": "Toyota (Tóquio)",
                    "6758.T": "Sony (Tóquio)",
                    "9984.T": "SoftBank Group",
                    "6861.T": "Keyence Corp",
                    "005930.KS": "Samsung Electronics",
                    "000660.KS": "SK Hynix",
                    "2330.TW": "Taiwan Semiconductor (Taiwan)",
                    "1810.HK": "Xiaomi Corp",
                    "9988.HK": "Alibaba (Hong Kong)",
                    "700.HK": "Tencent (Hong Kong)",
                },
            },
            "ETFs_Globais": {
                "spy": "SPDR S&P 500 ETF",
                "qqq": "Invesco QQQ Trust",
                "iwm": "iShares Russell 2000",
                "efa": "iShares MSCI EAFE",
                "eem": "iShares MSCI Emerging Markets",
                "vti": "Vanguard Total Stock Market",
                "vea": "Vanguard FTSE Developed Markets",
                "vwo": "Vanguard FTSE Emerging Markets",
                "gld": "SPDR Gold Shares",
                "slv": "iShares Silver Trust",
                "xle": "Energy Select Sector SPDR",
                "xlf": "Financial Select Sector SPDR",
                "xlk": "Technology Select Sector SPDR",
            },
            "Commodities": {
                "GC=F": "Ouro Futuro",
                "SI=F": "Prata Futuro",
                "CL=F": "Petróleo WTI",
                "BZ=F": "Petróleo Brent",
                "NG=F": "Gás Natural",
                "ZC=F": "Milho",
                "ZS=F": "Soja",
                "ZW=F": "Trigo",
                "KC=F": "Café",
                "SB=F": "Açúcar",
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
            "SHIB-USD": "Shiba Inu",
            "MATIC-USD": "Polygon",
            "LTC-USD": "Litecoin",
            "UNI-USD": "Uniswap",
            "LINK-USD": "Chainlink",
            "ALGO-USD": "Algorand",
        }

    def search_asset(self, query: str) -> List[Dict]:
        """Busca universal de ativos"""
        query = query.upper()
        results = []

        # Buscar em todas as categorias de ações
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
            elif category == "USA_Finance":
                if (
                    "USA" in self.global_assets
                    and "finance" in self.global_assets["USA"]
                ):
                    symbols.extend(self.global_assets["USA"]["finance"].keys())
            elif category == "USA_Energy":
                if (
                    "USA" in self.global_assets
                    and "energy" in self.global_assets["USA"]
                ):
                    symbols.extend(self.global_assets["USA"]["energy"].keys())
            elif category == "USA_Healthcare":
                if (
                    "USA" in self.global_assets
                    and "healthcare" in self.global_assets["USA"]
                ):
                    symbols.extend(self.global_assets["USA"]["healthcare"].keys())
            elif category == "Brazil_Stocks":
                if (
                    "Brasil" in self.global_assets
                    and "blue_chips" in self.global_assets["Brasil"]
                ):
                    symbols.extend(self.global_assets["Brasil"]["blue_chips"].keys())
            elif category == "Brazil_REITs":
                if (
                    "Brasil" in self.global_assets
                    and "fiis" in self.global_assets["Brasil"]
                ):
                    symbols.extend(self.global_assets["Brasil"]["fiis"].keys())
            elif category == "Europe_Stocks":
                if (
                    "Europa" in self.global_assets
                    and "stocks" in self.global_assets["Europa"]
                ):
                    symbols.extend(self.global_assets["Europa"]["stocks"].keys())
            elif category == "Asia_Stocks":
                if (
                    "Asia" in self.global_assets
                    and "stocks" in self.global_assets["Asia"]
                ):
                    symbols.extend(self.global_assets["Asia"]["stocks"].keys())
            elif category == "Indices":
                # Coletar índices de todas as regiões
                for region in ["USA", "Brasil", "Europa", "Asia"]:
                    if (
                        region in self.global_assets
                        and "indices" in self.global_assets[region]
                    ):
                        symbols.extend(self.global_assets[region]["indices"].keys())
            elif category == "ETFs":
                if "ETFs_Globais" in self.global_assets:
                    symbols.extend(self.global_assets["ETFs_Globais"].keys())
            elif category == "Commodities":
                if "Commodities" in self.global_assets:
                    symbols.extend(self.global_assets["Commodities"].keys())

        return list(set(symbols))

    def get_random_picks(self, count: int = 10) -> List[Dict]:
        """Seleção inteligente de ativos interessantes"""
        interesting_picks = [
            {
                "symbol": "AAPL",
                "reason": "Líder global em tecnologia com ecossistema robusto",
            },
            {"symbol": "NVDA", "reason": "Pioneira em IA e computação avançada"},
            {"symbol": "TSLA", "reason": "Revolução em veículos elétricos e energia"},
            {"symbol": "PETR4.SA", "reason": "Maior petrolífera da América Latina"},
            {"symbol": "BTC-USD", "reason": "Reserva de valor digital descentralizada"},
            {
                "symbol": "ASML.AS",
                "reason": "Monopólio global em equipamentos de chips",
            },
            {"symbol": "^GSPC", "reason": "Índice mais importante do mercado mundial"},
            {
                "symbol": "VALE3.SA",
                "reason": "Maior mineradora global de minério de ferro",
            },
            {
                "symbol": "ETH-USD",
                "reason": "Plataforma líder em contratos inteligentes",
            },
            {"symbol": "GOOGL", "reason": "Domínio absoluto em busca e IA"},
            {"symbol": "HGLG11.SA", "reason": "FII de logística com grande potencial"},
            {"symbol": "TSM", "reason": "Maior fabricante de semicondutores do mundo"},
        ]

        return interesting_picks[:count]


# ================================
# PROVEDOR DE DADOS SIMPLIFICADO
# ================================


class UnifiedDataProvider:
    """Provedor de dados simplificado e robusto"""

    def get_comprehensive_data(self, symbol: str, period: str = "1y") -> Dict:
        """Coleta dados de forma robusta"""
        try:
            # Limpar símbolo
            symbol = symbol.strip().upper()

            # Obter dados do yfinance
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                return None

            # Informações básicas da empresa
            try:
                info = ticker.info
                if not isinstance(info, dict):
                    info = {}
            except:
                info = {}

            # Preço atual
            current_price = float(hist["Close"][-1])

            # Calcular métricas básicas
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
            "9m": 189,
            "1y": 252,
            "2y": 504,
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

            # Volatilidade anualizada
            volatility = (
                float(returns.std() * np.sqrt(252) * 100) if len(returns) > 0 else 0
            )

            # Drawdown
            rolling_max = prices.expanding().max()
            drawdown = ((prices - rolling_max) / rolling_max) * 100
            max_drawdown = float(drawdown.min())
            current_drawdown = float(drawdown.iloc[-1])

            # Sharpe ratio simplificado
            if len(returns) > 0 and returns.std() > 0:
                excess_returns = returns.mean() * 252 - 0.02
                sharpe = excess_returns / (returns.std() * np.sqrt(252))
            else:
                sharpe = 0

            # Beta simplificado (assume 1 se não conseguir calcular)
            beta = 1.0

            return {
                "volatility": volatility,
                "max_drawdown": max_drawdown,
                "current_drawdown": current_drawdown,
                "sharpe_ratio": float(sharpe),
                "beta": beta,
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

            # RSI
            rsi = self._calculate_rsi(prices.values)

            # Médias móveis
            ma20 = (
                float(prices.rolling(20).mean().iloc[-1])
                if len(prices) >= 20
                else float(prices.iloc[-1])
            )
            ma50 = (
                float(prices.rolling(50).mean().iloc[-1])
                if len(prices) >= 50
                else float(prices.iloc[-1])
            )
            ma200 = (
                float(prices.rolling(200).mean().iloc[-1])
                if len(prices) >= 200
                else float(prices.iloc[-1])
            )

            # MACD
            macd_line, macd_signal, macd_histogram = self._calculate_macd(prices)

            # Bandas de Bollinger
            bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(prices)

            # Volume médio
            volume = hist.get("Volume", pd.Series([0]))
            avg_volume = (
                float(volume.rolling(20).mean().iloc[-1])
                if len(volume) >= 20
                else float(volume.iloc[-1] if len(volume) > 0 else 0)
            )

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
                "avg_volume": avg_volume,
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
                "peg_ratio": info.get("pegRatio", 0) or 0,
                "roe": info.get("returnOnEquity", 0) or 0,
                "roa": info.get("returnOnAssets", 0) or 0,
                "debt_to_equity": info.get("debtToEquity", 0) or 0,
                "current_ratio": info.get("currentRatio", 0) or 0,
                "profit_margin": info.get("profitMargins", 0) or 0,
                "operating_margin": info.get("operatingMargins", 0) or 0,
                "revenue_growth": info.get("revenueGrowth", 0) or 0,
                "earnings_growth": info.get("earningsGrowth", 0) or 0,
                "dividend_yield": info.get("dividendYield", 0) or 0,
                "payout_ratio": info.get("payoutRatio", 0) or 0,
                "sector": info.get("sector", "N/A") or "N/A",
                "industry": info.get("industry", "N/A") or "N/A",
                "employees": info.get("fullTimeEmployees", 0) or 0,
                "country": info.get("country", "N/A") or "N/A",
                "website": info.get("website", "N/A") or "N/A",
                "business_summary": info.get("longBusinessSummary", "N/A") or "N/A",
            }
        except:
            return {
                "market_cap": 0,
                "pe_ratio": 0,
                "pb_ratio": 0,
                "ps_ratio": 0,
                "peg_ratio": 0,
                "roe": 0,
                "roa": 0,
                "debt_to_equity": 0,
                "current_ratio": 0,
                "profit_margin": 0,
                "operating_margin": 0,
                "revenue_growth": 0,
                "earnings_growth": 0,
                "dividend_yield": 0,
                "payout_ratio": 0,
                "sector": "N/A",
                "industry": "N/A",
                "employees": 0,
                "country": "N/A",
                "website": "N/A",
                "business_summary": "N/A",
            }


# ================================
# ANALISADOR AVANÇADO COM IA
# ================================


class AdvancedAnalyzer:
    """Analisador avançado com algoritmos de IA"""

    def __init__(self):
        self.data_provider = UnifiedDataProvider()
        self.asset_db = GlobalAssetDatabase()

    def analyze_single_asset(self, symbol: str, period: str = "1y") -> Dict:
        """Análise completa de um único ativo"""
        data = self.data_provider.get_comprehensive_data(symbol, period)
        if not data:
            return None

        # Análise com IA
        ai_analysis = self.calculate_ai_scores(data)

        # Análise de sentimento
        sentiment = self.analyze_sentiment(data.get("news", []))

        # Potencial de crescimento
        growth_potential = self.calculate_growth_potential(data)

        # Metas de preço
        price_targets = self.calculate_price_targets(data)

        # Recomendação final
        recommendation = self.generate_recommendation(ai_analysis, data)

        # Feedback detalhado
        feedback = self.generate_detailed_feedback(data, ai_analysis)

        return {
            "data": data,
            "ai_analysis": ai_analysis,
            "sentiment": sentiment,
            "growth_potential": growth_potential,
            "price_targets": price_targets,
            "recommendation": recommendation,
            "feedback": feedback,
        }

    def calculate_ai_scores(self, data: Dict) -> Dict:
        """Calcula scores com algoritmos de IA"""
        # Scores por categoria
        technical_score = self._calculate_technical_score(data)
        fundamental_score = self._calculate_fundamental_score(data)
        momentum_score = self._calculate_momentum_score(data)
        risk_score = self._calculate_risk_score(data)
        value_score = self._calculate_value_score(data)
        quality_score = self._calculate_quality_score(data)

        # Score final ponderado com IA
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
        if macd["histogram"] > 0:
            score += 5

        # Bandas de Bollinger
        bb = technical["bollinger"]
        bb_position = (price - bb["lower"]) / (bb["upper"] - bb["lower"])
        if bb_position < 0.2:  # Próximo da banda inferior
            score += 15
        elif bb_position > 0.8:  # Próximo da banda superior
            score -= 10

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

        # P/L (Price to Earnings)
        pe = fund["pe_ratio"]
        if 0 < pe < 8:
            score += 30
        elif 8 <= pe < 12:
            score += 25
        elif 12 <= pe < 15:
            score += 20
        elif 15 <= pe < 18:
            score += 15
        elif 18 <= pe < 22:
            score += 10
        elif 22 <= pe < 30:
            score += 5
        elif pe > 40:
            score -= 15

        # ROE (Return on Equity)
        roe = fund["roe"]
        if roe > 0.30:
            score += 25
        elif roe > 0.25:
            score += 20
        elif roe > 0.20:
            score += 15
        elif roe > 0.15:
            score += 10
        elif roe > 0.10:
            score += 5
        elif roe < 0:
            score -= 25

        # Debt to Equity
        debt = fund["debt_to_equity"]
        if debt < 0.2:
            score += 20
        elif debt < 0.4:
            score += 15
        elif debt < 0.6:
            score += 10
        elif debt < 1.0:
            score += 5
        elif debt > 3.0:
            score -= 25

        # Crescimento de receita
        growth = fund["revenue_growth"]
        if growth > 0.30:
            score += 25
        elif growth > 0.20:
            score += 20
        elif growth > 0.15:
            score += 15
        elif growth > 0.10:
            score += 10
        elif growth > 0.05:
            score += 5
        elif growth < -0.10:
            score -= 20

        # Margem de lucro
        margin = fund["profit_margin"]
        if margin > 0.25:
            score += 20
        elif margin > 0.20:
            score += 15
        elif margin > 0.15:
            score += 10
        elif margin > 0.10:
            score += 5
        elif margin < 0:
            score -= 20

        return max(0, min(100, score))

    def _calculate_momentum_score(self, data: Dict) -> float:
        """Score de momentum"""
        score = 50
        returns = data["returns"]

        # Pesos por período
        weights = {"1w": 0.1, "1m": 0.2, "3m": 0.3, "6m": 0.25, "1y": 0.15}

        for period, weight in weights.items():
            ret = returns.get(period, 0)
            if ret > 20:
                score += 20 * weight
            elif ret > 15:
                score += 15 * weight
            elif ret > 10:
                score += 10 * weight
            elif ret > 5:
                score += 5 * weight
            elif ret < -15:
                score -= 15 * weight
            elif ret < -10:
                score -= 10 * weight

        return max(0, min(100, score))

    def _calculate_value_score(self, data: Dict) -> float:
        """Score de valor"""
        score = 50
        fund = data["fundamentals"]

        # P/B (Price to Book)
        pb = fund["pb_ratio"]
        if 0 < pb < 1:
            score += 25
        elif 1 <= pb < 1.5:
            score += 20
        elif 1.5 <= pb < 2:
            score += 15
        elif 2 <= pb < 3:
            score += 10
        elif pb > 5:
            score -= 15

        # P/S (Price to Sales)
        ps = fund["ps_ratio"]
        if 0 < ps < 1:
            score += 20
        elif 1 <= ps < 2:
            score += 15
        elif 2 <= ps < 3:
            score += 10
        elif ps > 10:
            score -= 15

        # PEG Ratio
        peg = fund["peg_ratio"]
        if 0 < peg < 0.5:
            score += 25
        elif 0.5 <= peg < 1:
            score += 20
        elif 1 <= peg < 1.5:
            score += 10
        elif peg > 2:
            score -= 10

        # Dividend Yield
        div_yield = fund["dividend_yield"]
        if div_yield > 0.05:
            score += 15
        elif div_yield > 0.03:
            score += 10
        elif div_yield > 0.02:
            score += 5

        return max(0, min(100, score))

    def _calculate_quality_score(self, data: Dict) -> float:
        """Score de qualidade"""
        score = 50
        fund = data["fundamentals"]

        # ROA (Return on Assets)
        roa = fund["roa"]
        if roa > 0.15:
            score += 25
        elif roa > 0.10:
            score += 20
        elif roa > 0.08:
            score += 15
        elif roa > 0.05:
            score += 10
        elif roa < 0:
            score -= 20

        # Current Ratio
        current_ratio = fund["current_ratio"]
        if 1.5 <= current_ratio <= 3:
            score += 15
        elif 1.2 <= current_ratio < 1.5:
            score += 10
        elif current_ratio < 1:
            score -= 15

        # Operating Margin
        op_margin = fund["operating_margin"]
        if op_margin > 0.20:
            score += 20
        elif op_margin > 0.15:
            score += 15
        elif op_margin > 0.10:
            score += 10
        elif op_margin < 0:
            score -= 15

        # Earnings Growth
        earnings_growth = fund["earnings_growth"]
        if earnings_growth > 0.25:
            score += 15
        elif earnings_growth > 0.15:
            score += 10
        elif earnings_growth > 0.10:
            score += 5
        elif earnings_growth < -0.15:
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

        # Beta
        beta = data["risk_metrics"]["beta"]
        if beta > 2:
            risk += 20
        elif beta > 1.5:
            risk += 15
        elif beta > 1.2:
            risk += 10

        # Debt to Equity
        debt = data["fundamentals"]["debt_to_equity"]
        if debt > 5:
            risk += 30
        elif debt > 3:
            risk += 20
        elif debt > 2:
            risk += 15
        elif debt > 1:
            risk += 10

        # ROE negativo
        if data["fundamentals"]["roe"] < 0:
            risk += 25

        # Margem negativa
        if data["fundamentals"]["profit_margin"] < 0:
            risk += 20

        # Max Drawdown
        max_dd = abs(data["risk_metrics"]["max_drawdown"])
        if max_dd > 80:
            risk += 25
        elif max_dd > 60:
            risk += 20
        elif max_dd > 40:
            risk += 15

        return min(100, risk)

    def analyze_sentiment(self, news: List[Dict]) -> Dict:
        """Análise de sentimento das notícias"""
        if not news:
            return {"score": 0, "trend": "Neutro", "summary": "Sem notícias recentes"}

        positive_words = {
            "growth",
            "profit",
            "gain",
            "increase",
            "strong",
            "beat",
            "exceed",
            "positive",
            "bullish",
            "upgrade",
            "buy",
            "outperform",
            "record",
            "success",
            "expansion",
            "innovation",
            "breakthrough",
            "milestone",
        }

        negative_words = {
            "loss",
            "decline",
            "fall",
            "weak",
            "miss",
            "below",
            "negative",
            "bearish",
            "downgrade",
            "sell",
            "underperform",
            "concern",
            "risk",
            "challenge",
            "problem",
            "crisis",
            "lawsuit",
            "investigation",
        }

        sentiment_scores = []

        for article in news[:5]:
            title = article.get("title", "").lower()
            summary = article.get("summary", "").lower()
            text = f"{title} {summary}"
            words = text.split()

            pos_count = sum(1 for word in words if word in positive_words)
            neg_count = sum(1 for word in words if word in negative_words)

            if pos_count + neg_count > 0:
                score = (pos_count - neg_count) / (pos_count + neg_count)
                sentiment_scores.append(score)

        if sentiment_scores:
            avg_sentiment = np.mean(sentiment_scores)
        else:
            avg_sentiment = 0

        if avg_sentiment > 0.4:
            trend = "Muito Positivo"
        elif avg_sentiment > 0.2:
            trend = "Positivo"
        elif avg_sentiment > -0.2:
            trend = "Neutro"
        elif avg_sentiment > -0.4:
            trend = "Negativo"
        else:
            trend = "Muito Negativo"

        return {
            "score": round(avg_sentiment, 2),
            "trend": trend,
            "summary": f"Baseado em {len(news)} notícias recentes",
        }

    def calculate_growth_potential(self, data: Dict) -> Dict:
        """Calcula potencial de crescimento com IA"""
        current_price = data["current_price"]

        # Análise técnica
        max_1y = max(data["price_data"]) if data["price_data"] else current_price
        technical_upside = ((max_1y - current_price) / current_price) * 100

        # Análise fundamentalista
        pe = data["fundamentals"]["pe_ratio"]
        sector_avg_pe = 18  # Média do mercado

        if pe > 0:
            multiple_upside = (
                ((sector_avg_pe - pe) / pe) * 100 if pe < sector_avg_pe else 0
            )
        else:
            multiple_upside = 0

        # Crescimento orgânico
        revenue_growth = data["fundamentals"]["revenue_growth"]
        earnings_growth = data["fundamentals"]["earnings_growth"]
        organic_potential = (revenue_growth + earnings_growth) * 100

        # Cenários
        conservative = max(0, min(technical_upside * 0.4, 20))
        moderate = max(0, min((technical_upside + multiple_upside) * 0.6, 40))
        optimistic = max(
            0, min(technical_upside + multiple_upside + organic_potential, 80)
        )

        return {
            "conservative": round(conservative, 1),
            "moderate": round(moderate, 1),
            "optimistic": round(optimistic, 1),
            "timeframe": "12-24 meses",
        }

    def calculate_price_targets(self, data: Dict) -> Dict:
        """Calcula metas de preço avançadas"""
        current_price = data["current_price"]
        prices = data["price_data"]

        # Support e Resistance
        support = np.percentile(prices, 20)
        resistance = np.percentile(prices, 80)

        # Metas baseadas em médias móveis
        ma200 = data["technical"]["ma200"]

        # Bandas de Bollinger
        bb_upper = data["technical"]["bollinger"]["upper"]
        bb_lower = data["technical"]["bollinger"]["lower"]

        # Metas conservadora, moderada e otimista
        conservative_target = min(resistance, current_price * 1.15)
        moderate_target = min(bb_upper, current_price * 1.25)
        optimistic_target = min(max(prices) * 1.05, current_price * 1.40)

        # Stop loss inteligente
        stop_loss = max(bb_lower, support * 0.95, current_price * 0.85)

        return {
            "current": round(current_price, 2),
            "support": round(support, 2),
            "resistance": round(resistance, 2),
            "ma200": round(ma200, 2),
            "targets": {
                "conservative": round(conservative_target, 2),
                "moderate": round(moderate_target, 2),
                "optimistic": round(optimistic_target, 2),
            },
            "stop_loss": round(stop_loss, 2),
        }

    def generate_recommendation(self, ai_analysis: Dict, data: Dict) -> Dict:
        """Gera recomendação final com IA"""
        final_score = ai_analysis["final"]
        risk_score = ai_analysis["risk"]

        # Ajustar score com base no risco
        risk_adjusted_score = final_score - (risk_score * 0.15)

        if risk_adjusted_score >= 85:
            action = "COMPRA FORTE"
            confidence = "Muito Alta"
            emoji = "🚀"
        elif risk_adjusted_score >= 75:
            action = "COMPRAR"
            confidence = "Alta"
            emoji = "✅"
        elif risk_adjusted_score >= 65:
            action = "COMPRA MODERADA"
            confidence = "Boa"
            emoji = "🟢"
        elif risk_adjusted_score >= 55:
            action = "AGUARDAR MELHOR ENTRADA"
            confidence = "Moderada"
            emoji = "🟡"
        elif risk_adjusted_score >= 40:
            action = "EVITAR"
            confidence = "Baixa"
            emoji = "⚠️"
        else:
            action = "VENDER/EVITAR"
            confidence = "Alta"
            emoji = "❌"

        # Horizonte de investimento
        volatility = data["risk_metrics"]["volatility"]
        if volatility > 60:
            horizon = "Longo prazo (2+ anos)"
        elif volatility > 35:
            horizon = "Médio prazo (6-18 meses)"
        else:
            horizon = "Curto-médio prazo (3-12 meses)"

        # Nível de risco
        if risk_score > 70:
            risk_level = "Muito Alto"
        elif risk_score > 50:
            risk_level = "Alto"
        elif risk_score > 30:
            risk_level = "Médio"
        else:
            risk_level = "Baixo"

        return {
            "action": action,
            "confidence": confidence,
            "emoji": emoji,
            "score": round(risk_adjusted_score, 1),
            "horizon": horizon,
            "risk_level": risk_level,
        }

    def generate_detailed_feedback(self, data: Dict, ai_analysis: Dict) -> Dict:
        """Gera feedback detalhado com IA"""
        feedback = {
            "strengths": [],
            "weaknesses": [],
            "opportunities": [],
            "threats": [],
            "summary": "",
        }

        # Analisar pontos fortes
        if ai_analysis["technical"] > 75:
            feedback["strengths"].append("📈 Excelente performance técnica")
        if ai_analysis["fundamental"] > 75:
            feedback["strengths"].append("💪 Fundamentos muito sólidos")
        if ai_analysis["momentum"] > 75:
            feedback["strengths"].append("🚀 Forte momentum positivo")
        if ai_analysis["value"] > 75:
            feedback["strengths"].append("💎 Excelente oportunidade de valor")
        if ai_analysis["quality"] > 75:
            feedback["strengths"].append("⭐ Alta qualidade operacional")

        if data["fundamentals"]["roe"] > 0.20:
            feedback["strengths"].append("💰 ROE excepcional")
        if data["fundamentals"]["debt_to_equity"] < 0.3:
            feedback["strengths"].append("🛡️ Estrutura financeira conservadora")
        if data["fundamentals"]["revenue_growth"] > 0.15:
            feedback["strengths"].append("📊 Crescimento robusto")

        # Analisar pontos fracos
        if ai_analysis["risk"] > 70:
            feedback["weaknesses"].append("⚠️ Perfil de risco elevado")
        if data["risk_metrics"]["volatility"] > 60:
            feedback["weaknesses"].append("📊 Alta volatilidade histórica")
        if data["fundamentals"]["pe_ratio"] > 35:
            feedback["weaknesses"].append("💸 Múltiplo de valuation elevado")
        if data["returns"]["1y"] < -25:
            feedback["weaknesses"].append("📉 Performance ruim no último ano")
        if data["fundamentals"]["debt_to_equity"] > 2:
            feedback["weaknesses"].append("💳 Endividamento preocupante")

        # Analisar oportunidades
        current_dd = abs(data["risk_metrics"]["current_drawdown"])
        if current_dd > 25:
            feedback["opportunities"].append(
                f"🎯 Grande desconto: {current_dd:.1f}% abaixo do pico"
            )
        if data["technical"]["rsi"] < 35:
            feedback["opportunities"].append("📈 Condição técnica de oversold")
        if ai_analysis["value"] > 70:
            feedback["opportunities"].append("💎 Oportunidade de valor identificada")
        if data["fundamentals"]["dividend_yield"] > 0.04:
            feedback["opportunities"].append("💵 Boa rentabilidade em dividendos")

        # Analisar ameaças
        if data["fundamentals"]["profit_margin"] < 0.03:
            feedback["threats"].append("📉 Margem de lucro comprimida")
        if ai_analysis["momentum"] < 30:
            feedback["threats"].append("🐌 Momentum técnico negativo")
        if data["fundamentals"]["revenue_growth"] < -0.05:
            feedback["threats"].append("📉 Receita em declínio")
        if data["risk_metrics"]["beta"] > 1.8:
            feedback["threats"].append("⚡ Alta sensibilidade ao mercado")

        # Gerar resumo
        total_strengths = len(feedback["strengths"])
        total_weaknesses = len(feedback["weaknesses"])
        final_score = ai_analysis["final"]

        if final_score > 75:
            feedback["summary"] = "✅ Ativo com perfil muito atrativo para investimento"
        elif final_score > 60:
            feedback["summary"] = "🟢 Ativo com boa perspectiva de investimento"
        elif final_score > 45:
            feedback["summary"] = "🟡 Ativo neutro, requer análise mais detalhada"
        else:
            feedback["summary"] = "⚠️ Ativo apresenta muitos riscos no momento"

        return feedback


# ================================
# SCANNER GLOBAL DE OPORTUNIDADES
# ================================


class GlobalScanner:
    """Scanner global de oportunidades"""

    def __init__(self):
        self.analyzer = AdvancedAnalyzer()
        self.db = GlobalAssetDatabase()

    def scan_opportunities(
        self, categories: List[str], filters: Dict, max_assets: int = 100
    ) -> List[Dict]:
        """Scan paralelo de oportunidades"""
        symbols = self.db.get_symbols_by_category(categories)[:max_assets]

        if not symbols:
            return []

        results = []
        progress = st.progress(0)
        status = st.empty()

        def analyze_batch(batch):
            batch_results = []
            for symbol in batch:
                try:
                    data = self.analyzer.data_provider.get_comprehensive_data(
                        symbol, "1y"
                    )
                    if data and data.get("current_price") and data.get("risk_metrics"):
                        scores = self.analyzer.calculate_ai_scores(data)

                        # Criar resultado simplificado para o scanner
                        result = {
                            "symbol": symbol,
                            "price": data["current_price"],
                            "score": scores["final"],
                            "technical_score": scores["technical"],
                            "fundamental_score": scores["fundamental"],
                            "risk_score": scores["risk"],
                            "drawdown": data["risk_metrics"]["current_drawdown"],
                            "upside_potential": self._calculate_upside(data),
                            "returns_1y": data["returns"]["1y"],
                            "returns_3m": data["returns"]["3m"],
                            "returns_1m": data["returns"]["1m"],
                            "pe_ratio": data["fundamentals"]["pe_ratio"],
                            "market_cap": data["fundamentals"]["market_cap"],
                            "sector": data["fundamentals"]["sector"],
                            "volatility": data["risk_metrics"]["volatility"],
                            "rsi": data["technical"]["rsi"],
                        }
                        batch_results.append(result)
                except Exception as e:
                    # Log do erro para debug, mas continua processamento
                    continue
            return batch_results

        # Processar em paralelo
        batch_size = max(1, len(symbols) // 20)  # 20 threads
        batches = [
            symbols[i : i + batch_size] for i in range(0, len(symbols), batch_size)
        ]

        completed = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {
                executor.submit(analyze_batch, batch): batch for batch in batches
            }

            for future in concurrent.futures.as_completed(futures):
                batch_results = future.result()
                results.extend(batch_results)

                completed += len(futures[future])
                progress.progress(completed / len(symbols))
                status.text(f"Analisados: {completed}/{len(symbols)}")

        progress.empty()
        status.empty()

        # Aplicar filtros
        filtered_results = self._apply_filters(results, filters)

        return sorted(filtered_results, key=lambda x: x["score"], reverse=True)

    def _calculate_upside(self, data: Dict) -> float:
        """Calcula potencial de upside"""
        current_price = data["current_price"]
        max_price = max(data["price_data"]) if data["price_data"] else current_price
        return ((max_price - current_price) / current_price) * 100

    def _apply_filters(self, results: List[Dict], filters: Dict) -> List[Dict]:
        """Aplica filtros aos resultados"""
        filtered = []

        for result in results:
            # Filtro de score mínimo
            if result["score"] < filters.get("min_score", 0):
                continue

            # Filtro de drawdown mínimo
            if abs(result["drawdown"]) < filters.get("min_drawdown", 0):
                continue

            # Filtro de P/L máximo
            max_pe = filters.get("max_pe", 999)
            if result["pe_ratio"] > max_pe and result["pe_ratio"] > 0:
                continue

            # Filtro de volatilidade máxima
            if result["volatility"] > filters.get("max_volatility", 999):
                continue

            # Filtro de market cap mínimo
            if result["market_cap"] < filters.get("min_market_cap", 0):
                continue

            filtered.append(result)

        return filtered


# ================================
# COMPARADOR DE ATIVOS
# ================================


class AssetComparator:
    """Comparador avançado de múltiplos ativos"""

    def __init__(self):
        self.analyzer = AdvancedAnalyzer()

    def compare_assets(self, symbols: List[str], period: str = "1y") -> Dict:
        """Compara múltiplos ativos de forma abrangente"""
        if not symbols:
            return None

        assets_data = {}
        progress = st.progress(0)
        status = st.empty()

        for i, symbol in enumerate(symbols):
            status.text(f"Carregando dados de {symbol}...")
            progress.progress((i + 1) / len(symbols))

            data = self.analyzer.data_provider.get_comprehensive_data(symbol, period)
            if data:
                # Adicionar análise completa
                analysis = self.analyzer.calculate_ai_scores(data)
                data["ai_analysis"] = analysis
                assets_data[symbol] = data

        progress.empty()
        status.empty()

        if not assets_data:
            return None

        # Criar comparações
        comparison = {
            "performance": self._compare_performance(assets_data),
            "risk": self._compare_risk(assets_data),
            "fundamentals": self._compare_fundamentals(assets_data),
            "technical": self._compare_technical(assets_data),
            "ai_scores": self._compare_ai_scores(assets_data),
            "correlation": self._calculate_correlation(assets_data),
            "summary": self._create_summary(assets_data),
        }

        return comparison

    def _compare_performance(self, assets_data: Dict) -> pd.DataFrame:
        """Compara performance entre ativos"""
        perf_data = []

        for symbol, data in assets_data.items():
            row = {"Symbol": symbol}
            row.update(data["returns"])
            row["Current_Price"] = data["current_price"]
            perf_data.append(row)

        return pd.DataFrame(perf_data)

    def _compare_risk(self, assets_data: Dict) -> pd.DataFrame:
        """Compara métricas de risco"""
        risk_data = []

        for symbol, data in assets_data.items():
            risk_metrics = data["risk_metrics"]
            technical = data["technical"]

            risk_data.append(
                {
                    "Symbol": symbol,
                    "Volatility": round(risk_metrics["volatility"], 2),
                    "Max_Drawdown": round(risk_metrics["max_drawdown"], 2),
                    "Current_Drawdown": round(risk_metrics["current_drawdown"], 2),
                    "Beta": round(risk_metrics["beta"], 2),
                    "Sharpe_Ratio": round(risk_metrics["sharpe_ratio"], 2),
                    "RSI": round(technical["rsi"], 1),
                }
            )

        return pd.DataFrame(risk_data)

    def _compare_fundamentals(self, assets_data: Dict) -> pd.DataFrame:
        """Compara dados fundamentalistas"""
        fund_data = []

        for symbol, data in assets_data.items():
            fund = data["fundamentals"]
            market_cap = fund["market_cap"]

            if market_cap >= 1e12:
                mc_str = f"${market_cap/1e12:.1f}T"
            elif market_cap >= 1e9:
                mc_str = f"${market_cap/1e9:.1f}B"
            else:
                mc_str = f"${market_cap/1e6:.1f}M"

            fund_data.append(
                {
                    "Symbol": symbol,
                    "Market_Cap": mc_str,
                    "PE_Ratio": round(fund["pe_ratio"], 1),
                    "PB_Ratio": round(fund["pb_ratio"], 1),
                    "ROE": f"{fund['roe']*100:.1f}%",
                    "Debt_to_Equity": round(fund["debt_to_equity"], 1),
                    "Profit_Margin": f"{fund['profit_margin']*100:.1f}%",
                    "Revenue_Growth": f"{fund['revenue_growth']*100:.1f}%",
                    "Dividend_Yield": f"{fund['dividend_yield']*100:.1f}%",
                    "Sector": fund["sector"],
                }
            )

        return pd.DataFrame(fund_data)

    def _compare_technical(self, assets_data: Dict) -> pd.DataFrame:
        """Compara indicadores técnicos"""
        tech_data = []

        for symbol, data in assets_data.items():
            tech = data["technical"]
            price = data["current_price"]

            tech_data.append(
                {
                    "Symbol": symbol,
                    "RSI": round(tech["rsi"], 1),
                    "Price_vs_MA20": round(
                        ((price - tech["ma20"]) / tech["ma20"]) * 100, 1
                    ),
                    "Price_vs_MA50": round(
                        ((price - tech["ma50"]) / tech["ma50"]) * 100, 1
                    ),
                    "Price_vs_MA200": round(
                        ((price - tech["ma200"]) / tech["ma200"]) * 100, 1
                    ),
                    "MACD_Signal": (
                        "Positivo"
                        if tech["macd"]["line"] > tech["macd"]["signal"]
                        else "Negativo"
                    ),
                    "BB_Position": self._calculate_bb_position(
                        price, tech["bollinger"]
                    ),
                }
            )

        return pd.DataFrame(tech_data)

    def _calculate_bb_position(self, price, bollinger):
        """Calcula posição nas Bandas de Bollinger"""
        upper, middle, lower = (
            bollinger["upper"],
            bollinger["middle"],
            bollinger["lower"],
        )
        position = (price - lower) / (upper - lower)

        if position < 0.2:
            return "Oversold"
        elif position > 0.8:
            return "Overbought"
        else:
            return "Neutro"

    def _compare_ai_scores(self, assets_data: Dict) -> pd.DataFrame:
        """Compara scores de IA"""
        ai_data = []

        for symbol, data in assets_data.items():
            scores = data["ai_analysis"]

            ai_data.append(
                {
                    "Symbol": symbol,
                    "Final_Score": scores["final"],
                    "Technical": scores["technical"],
                    "Fundamental": scores["fundamental"],
                    "Momentum": scores["momentum"],
                    "Value": scores["value"],
                    "Quality": scores["quality"],
                    "Risk": scores["risk"],
                }
            )

        return pd.DataFrame(ai_data).sort_values("Final_Score", ascending=False)

    def _calculate_correlation(self, assets_data: Dict) -> pd.DataFrame:
        """Calcula correlação entre ativos"""
        if len(assets_data) < 2:
            return pd.DataFrame()

        try:
            price_data = {}
            min_length = min(len(data["price_data"]) for data in assets_data.values())

            for symbol, data in assets_data.items():
                prices = data["price_data"]
                if len(prices) >= min_length:
                    price_data[symbol] = prices[-min_length:]

            if len(price_data) < 2:
                return pd.DataFrame()

            df = pd.DataFrame(price_data)
            returns_df = df.pct_change().dropna()

            return returns_df.corr()

        except:
            return pd.DataFrame()

    def _create_summary(self, assets_data: Dict) -> pd.DataFrame:
        """Cria resumo com rankings"""
        summary_data = []

        for symbol, data in assets_data.items():
            scores = data["ai_analysis"]

            # Recomendação baseada no score final
            final_score = scores["final"]
            risk_score = scores["risk"]

            if final_score >= 80:
                recommendation = "COMPRA FORTE"
                emoji = "🚀"
            elif final_score >= 70:
                recommendation = "COMPRAR"
                emoji = "✅"
            elif final_score >= 60:
                recommendation = "COMPRA MODERADA"
                emoji = "🟢"
            elif final_score >= 50:
                recommendation = "AGUARDAR"
                emoji = "🟡"
            elif final_score >= 35:
                recommendation = "EVITAR"
                emoji = "⚠️"
            else:
                recommendation = "VENDER"
                emoji = "❌"

            # Potencial de upside
            current_price = data["current_price"]
            max_price = max(data["price_data"]) if data["price_data"] else current_price
            upside = ((max_price - current_price) / current_price) * 100

            summary_data.append(
                {
                    "Symbol": symbol,
                    "Final_Score": final_score,
                    "Recommendation": f"{emoji} {recommendation}",
                    "Upside_Potential": f"{upside:.1f}%",
                    "Risk_Level": (
                        "Alto"
                        if risk_score > 60
                        else "Médio" if risk_score > 30 else "Baixo"
                    ),
                    "Price": f"${current_price:.2f}",
                    "Returns_1Y": f"{data['returns']['1y']:.1f}%",
                }
            )

        return pd.DataFrame(summary_data).sort_values("Final_Score", ascending=False)


# ================================
# FUNÇÕES DE VISUALIZAÇÃO
# ================================


def create_comprehensive_charts(
    data: Dict, comparison_data: Dict = None
) -> List[go.Figure]:
    """Cria gráficos abrangentes"""
    charts = []

    if data:
        # 1. Gráfico de preços com análise técnica
        fig_price = create_price_chart(data)
        if fig_price:
            charts.append(fig_price)

    if comparison_data:
        # 2. Gráfico de performance comparativa
        perf_df = comparison_data.get("performance")
        if perf_df is not None and not perf_df.empty:
            fig_perf = px.bar(
                perf_df,
                x="Symbol",
                y=["1d", "1w", "1m", "3m", "6m", "1y"],
                title="📈 Performance Comparativa por Período",
                labels={"value": "Retorno (%)", "Symbol": "Ativo"},
                barmode="group",
            )
            charts.append(fig_perf)

        # 3. Gráfico risco vs retorno
        risk_df = comparison_data.get("risk")
        if risk_df is not None and not risk_df.empty and perf_df is not None:
            combined = pd.merge(
                risk_df[["Symbol", "Volatility"]],
                perf_df[["Symbol", "1y"]],
                on="Symbol",
            )

            fig_risk = px.scatter(
                combined,
                x="Volatility",
                y="1y",
                text="Symbol",
                title="⚖️ Risco vs Retorno (1 Ano)",
                labels={"Volatility": "Volatilidade (%)", "1y": "Retorno 1 Ano (%)"},
                size_max=15,
            )
            fig_risk.update_traces(textposition="top center")
            charts.append(fig_risk)

        # 4. Scores de IA
        ai_df = comparison_data.get("ai_scores")
        if ai_df is not None and not ai_df.empty:
            fig_scores = px.bar(
                ai_df,
                x="Symbol",
                y="Final_Score",
                color="Final_Score",
                title="🧠 Scores de IA por Ativo",
                color_continuous_scale="RdYlGn",
                range_color=[0, 100],
            )
            charts.append(fig_scores)

    return charts


def create_price_chart(data: Dict) -> go.Figure:
    """Cria gráfico avançado de preços"""
    if not data or "hist_data" not in data:
        return None

    df = pd.DataFrame(data["hist_data"])
    df["Date"] = pd.to_datetime(df["Date"])

    # Criar gráfico principal
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
            increasing_line_color="green",
            decreasing_line_color="red",
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

    if len(df) >= 200:
        ma200 = df["Close"].rolling(200).mean()
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=ma200,
                mode="lines",
                name="MA200",
                line=dict(color="red", width=1, dash="dash"),
            )
        )

    # Bandas de Bollinger
    if len(df) >= 20:
        ma20 = df["Close"].rolling(20).mean()
        std20 = df["Close"].rolling(20).std()
        upper_band = ma20 + (std20 * 2)
        lower_band = ma20 - (std20 * 2)

        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=upper_band,
                mode="lines",
                name="BB Superior",
                line=dict(color="gray", width=1, dash="dot"),
                showlegend=False,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=lower_band,
                mode="lines",
                name="BB Inferior",
                line=dict(color="gray", width=1, dash="dot"),
                fill="tonexty",
                fillcolor="rgba(128,128,128,0.1)",
                showlegend=False,
            )
        )

    # Configurações do layout
    fig.update_layout(
        title=f"📊 Análise Técnica Completa - {data['symbol']}",
        xaxis_title="Data",
        yaxis_title="Preço ($)",
        height=600,
        showlegend=True,
        hovermode="x unified",
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
# INTERFACE PRINCIPAL UNIFICADA
# ================================


def main():
    """Interface principal unificada"""

    # Inicializar componentes principais
    global scanner
    scanner = GlobalScanner()
    comparator = AssetComparator()
    analyzer = AdvancedAnalyzer()

    # Header principal
    st.title("🌍 Sistema Global de Análise de Investimentos")
    st.subheader(
        "Plataforma Unificada: Análise Individual | Scanner Global | Comparador"
    )

    # Status do sistema
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("🟢 Sistema Online")
    with col2:
        st.info("📊 Ativos Globais Disponíveis")
    with col3:
        st.warning("🤖 IA Avançada Ativa")

    # Inicializar componentes de forma simples e robusta
    try:
        # Teste básico de conectividade
        test_ticker = yf.Ticker("AAPL")
        test_data = test_ticker.history(period="1d")

        if test_data.empty:
            st.error("❌ Problema de conectividade com dados financeiros")
            return

        # Inicializar base de dados
        asset_db = GlobalAssetDatabase()
        data_provider = UnifiedDataProvider()

        # Verificar se a base de dados foi carregada
        all_symbols = asset_db.get_all_symbols()
        if len(all_symbols) == 0:
            st.error("❌ Erro ao carregar base de dados")
            return

        st.sidebar.success(f"✅ Sistema pronto: {len(all_symbols)} ativos")

    except Exception as e:
        st.error(f"❌ Erro na inicialização: {str(e)}")
        st.info("🔧 Soluções:")
        st.write("• Verifique sua conexão com internet")
        st.write("• Recarregue a página (F5)")
        st.write("• Aguarde alguns minutos e tente novamente")
        return

    # Sidebar global
    with st.sidebar:
        st.title("🎯 Navegação Global")

        # Busca universal
        st.subheader("🔍 Busca Universal")
        search_query = st.text_input(
            "Buscar qualquer ativo:", placeholder="Ex: AAPL, Bitcoin, S&P 500"
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
            except Exception as e:
                st.write("⚠️ Erro na busca")

        # Picks inteligentes
        st.subheader("💡 Picks Inteligentes")
        try:
            random_picks = asset_db.get_random_picks(6)
            for pick in random_picks:
                if st.button(
                    f"{pick['symbol']}",
                    key=f"pick_{pick['symbol']}",
                    help=pick["reason"][:50],
                ):
                    st.session_state["selected_symbol"] = pick["symbol"]
        except:
            st.write("Picks temporariamente indisponíveis")

        # Informações do sistema
        st.markdown("---")
        st.subheader("ℹ️ Sistema")
        st.metric("Ativos Disponíveis", f"{len(all_symbols):,}")

        st.write("🇺🇸 **EUA:** Ações, ETFs, Índices")
        st.write("🇧🇷 **Brasil:** Ações, FIIs")
        st.write("🇪🇺 **Europa:** Principais mercados")
        st.write("🌏 **Ásia:** Ações globais")
        st.write("💰 **Crypto:** Top moedas")
        st.write("📊 **Commodities:** Futuros")
        st.write("💰 **Crypto:** Top moedas")
        st.write("📊 **Commodities:** Futuros")

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
        
        # Initialize data provider
        data_provider = UnifiedDataProvider()

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            symbol_input = st.text_input(
                "Digite o símbolo do ativo:",
                value=st.session_state.get("selected_symbol", ""),
                placeholder="Ex: AAPL, PETR4.SA, BTC-USD, ^GSPC",
            )

        with col2:
            period = st.selectbox(
                "Período:", ["1mo", "3mo", "6mo", "1y", "2y"], index=3
            )

        with col3:
            analyze_btn = st.button(
                "🚀 ANALISAR", type="primary", use_container_width=True
            )

        # Exemplos rápidos
        st.write("**⚡ Exemplos Rápidos:**")
        col1, col2, col3, col4, col5 = st.columns(5)

        examples = [
            ("🇺🇸 AAPL", "AAPL"),
            ("🇺🇸 NVDA", "NVDA"),
            ("🇧🇷 PETR4.SA", "PETR4.SA"),
            ("💰 BTC-USD", "BTC-USD"),
            ("📊 ^GSPC", "^GSPC"),
        ]

        for i, (label, symbol) in enumerate(examples):
            with [col1, col2, col3, col4, col5][i]:
                if st.button(label, key=f"example_{symbol}"):
                    st.session_state["selected_symbol"] = symbol
                    st.rerun()

        if analyze_btn and symbol_input:
            symbol = symbol_input.upper().strip()

            with st.spinner(f"🤖 Analisando {symbol}..."):
                try:
                    # Inicializar provedor de dados
                    data_provider = UnifiedDataProvider()
                    
                    # Obter dados básicos
                    data = data_provider.get_comprehensive_data(symbol, period)

                    if data:
                        # Criar analisador simples para este ativo
                        simple_analyzer = AdvancedAnalyzer()
                        simple_analyzer.data_provider = data_provider

                        # Calcular scores
                        ai_scores = simple_analyzer.calculate_ai_scores(data)

                        # Análise de sentimento simples
                        sentiment = {
                            "score": 0,
                            "trend": "Neutro",
                            "summary": "Análise básica",
                        }

                        # Potencial de crescimento
                        current_price = data["current_price"]
                        max_price = (
                            max(data["price_data"])
                            if data["price_data"]
                            else current_price
                        )
                        upside = ((max_price - current_price) / current_price) * 100

                        growth_potential = {
                            "conservative": min(upside * 0.4, 20),
                            "moderate": min(upside * 0.6, 35),
                            "optimistic": min(upside, 50),
                            "timeframe": "12-24 meses",
                        }

                        # Metas de preço
                        price_targets = {
                            "current": current_price,
                            "support": (
                                min(data["price_data"]) * 1.05
                                if data["price_data"]
                                else current_price * 0.9
                            ),
                            "resistance": (
                                max(data["price_data"]) * 0.95
                                if data["price_data"]
                                else current_price * 1.1
                            ),
                            "targets": {
                                "conservative": current_price * 1.15,
                                "moderate": current_price * 1.25,
                                "optimistic": current_price * 1.40,
                            },
                            "stop_loss": current_price * 0.85,
                        }

                        # Recomendação
                        final_score = ai_scores["final"]
                        if final_score >= 80:
                            recommendation = {
                                "action": "COMPRA FORTE",
                                "emoji": "🚀",
                                "confidence": "Alta",
                            }
                        elif final_score >= 70:
                            recommendation = {
                                "action": "COMPRAR",
                                "emoji": "✅",
                                "confidence": "Boa",
                            }
                        elif final_score >= 60:
                            recommendation = {
                                "action": "COMPRA MODERADA",
                                "emoji": "🟢",
                                "confidence": "Moderada",
                            }
                        elif final_score >= 50:
                            recommendation = {
                                "action": "AGUARDAR",
                                "emoji": "🟡",
                                "confidence": "Baixa",
                            }
                        else:
                            recommendation = {
                                "action": "EVITAR",
                                "emoji": "⚠️",
                                "confidence": "Alta",
                            }

                        # Exibir resultados
                        st.success(f"✅ **Análise completa para {symbol}**")

                        # Métricas principais
                        col1_m, col2_m, col3_m, col4_m, col5_m = st.columns(5)

                        with col1_m:
                            return_1y = data["returns"]["1y"]
                            st.metric(
                                "💰 Preço Atual",
                                f"${current_price:.2f}",
                                f"{return_1y:+.1f}% (1Y)",
                            )

                        with col2_m:
                            st.metric(
                                f"{recommendation['emoji']} Score IA",
                                f"{final_score:.0f}/100",
                                recommendation["confidence"],
                            )

                        with col3_m:
                            st.metric(
                                "📈 Potencial",
                                f"+{growth_potential['moderate']:.1f}%",
                                growth_potential["timeframe"],
                            )

                        with col4_m:
                            volatility = data["risk_metrics"]["volatility"]
                            st.metric(
                                "📊 Volatilidade",
                                f"{volatility:.1f}%",
                                f"RSI: {data['technical']['rsi']:.0f}",
                            )

                        with col5_m:
                            market_cap = data["fundamentals"]["market_cap"]
                            st.metric(
                                "🏢 Market Cap",
                                format_large_number(market_cap),
                                data["fundamentals"]["sector"][:15],
                            )

                        # Recomendação principal
                        if recommendation["action"] in ["COMPRA FORTE", "COMPRAR"]:
                            st.success(
                                f"## {recommendation['emoji']} RECOMENDAÇÃO: {recommendation['action']}"
                            )
                        elif recommendation["action"] in [
                            "COMPRA MODERADA",
                            "AGUARDAR",
                        ]:
                            st.warning(
                                f"## {recommendation['emoji']} RECOMENDAÇÃO: {recommendation['action']}"
                            )
                        else:
                            st.error(
                                f"## {recommendation['emoji']} RECOMENDAÇÃO: {recommendation['action']}"
                            )

                        st.write(
                            f"**Confiança:** {recommendation['confidence']} | **Score:** {final_score}/100"
                        )

                        # Gráfico de preços simples
                        try:
                            chart = create_price_chart(data)
                            if chart:
                                st.plotly_chart(chart, use_container_width=True)
                        except:
                            st.info("📊 Gráfico temporariamente indisponível")

                        # Análise detalhada em colunas
                        col1_d, col2_d = st.columns(2)

                        with col1_d:
                            st.subheader("📊 Scores Detalhados")

                            scores_df = pd.DataFrame(
                                [
                                    ["🔧 Técnico", f"{ai_scores['technical']:.1f}/100"],
                                    [
                                        "💼 Fundamentalista",
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

                            st.subheader("🎯 Metas de Preço")
                            st.write(f"**💰 Atual:** ${price_targets['current']:.2f}")
                            st.write(f"**🛡️ Suporte:** ${price_targets['support']:.2f}")
                            st.write(
                                f"**⚡ Resistência:** ${price_targets['resistance']:.2f}"
                            )
                            st.write(
                                f"**🛑 Stop Loss:** ${price_targets['stop_loss']:.2f}"
                            )

                        with col2_d:
                            st.subheader("📈 Potencial de Crescimento")

                            st.write(
                                f"**🛡️ Conservador:** +{growth_potential['conservative']:.1f}%"
                            )
                            st.progress(growth_potential["conservative"] / 50)

                            st.write(
                                f"**⚖️ Moderado:** +{growth_potential['moderate']:.1f}%"
                            )
                            st.progress(growth_potential["moderate"] / 50)

                            st.write(
                                f"**🚀 Otimista:** +{growth_potential['optimistic']:.1f}%"
                            )
                            st.progress(growth_potential["optimistic"] / 100)

                            st.subheader("💼 Dados Fundamentais")
                            fund = data["fundamentals"]
                            st.write(f"**P/L:** {fund['pe_ratio']:.1f}")
                            st.write(f"**ROE:** {fund['roe']*100:.1f}%")
                            st.write(f"**Margem:** {fund['profit_margin']*100:.1f}%")
                            st.write(
                                f"**Crescimento:** {fund['revenue_growth']*100:.1f}%"
                            )
                            st.write(f"**Setor:** {fund['sector']}")

                        # Performance histórica
                        with st.expander("📈 Performance Histórica"):
                            returns = data["returns"]

                            performance_df = pd.DataFrame(
                                [
                                    ["1 Mês", f"{returns['1m']:+.1f}%"],
                                    ["3 Meses", f"{returns['3m']:+.1f}%"],
                                    ["6 Meses", f"{returns['6m']:+.1f}%"],
                                    ["1 Ano", f"{returns['1y']:+.1f}%"],
                                ],
                                columns=["Período", "Retorno"],
                            )

                            st.dataframe(
                                performance_df,
                                hide_index=True,
                                use_container_width=True,
                            )

                    else:
                        st.error(
                            f"❌ Não foi possível analisar {symbol}. Verifique se o símbolo está correto."
                        )

                except Exception as e:
                    st.error(f"❌ Erro durante a análise: {str(e)}")
                    st.info("💡 Tente com outro símbolo ou aguarde alguns minutos")

    # ================================
    # TAB 2: SCANNER GLOBAL (SIMPLIFICADO)
    # ================================
    with tab2:
        st.header("🌍 Scanner Global de Oportunidades")

        st.info("⚡ **Scanner Rápido** - Versão simplificada para melhor performance")

        # Scanners predefinidos
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🇺🇸 Top EUA", use_container_width=True):
                with st.spinner("Analisando EUA..."):
                    try:
                        usa_symbols = [
                            "AAPL",
                            "MSFT",
                            "GOOGL",
                            "AMZN",
                            "NVDA",
                            "TSLA",
                            "META",
                            "NFLX",
                        ]
                        results = []

                        for symbol in usa_symbols[:6]:  # Limitar para performance
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, "6mo"
                                )
                                if data:
                                    analyzer = AdvancedAnalyzer()
                                    analyzer.data_provider = data_provider
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
                            results_df = pd.DataFrame(results).sort_values(
                                "Score", ascending=False
                            )
                            st.success("✅ Top EUA Analisados")
                            st.dataframe(
                                results_df, hide_index=True, use_container_width=True
                            )
                    except Exception as e:
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
                            "RENT3.SA",
                        ]
                        results = []

                        for symbol in br_symbols[:6]:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, "6mo"
                                )
                                if data:
                                    analyzer = AdvancedAnalyzer()
                                    analyzer.data_provider = data_provider
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
                            results_df = pd.DataFrame(results).sort_values(
                                "Score", ascending=False
                            )
                            st.success("✅ Top Brasil Analisados")
                            st.dataframe(
                                results_df, hide_index=True, use_container_width=True
                            )
                    except Exception as e:
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
                            "DOT-USD",
                        ]
                        results = []

                        for symbol in crypto_symbols[:6]:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, "6mo"
                                )
                                if data:
                                    analyzer = AdvancedAnalyzer()
                                    analyzer.data_provider = data_provider
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
                            results_df = pd.DataFrame(results).sort_values(
                                "Score", ascending=False
                            )
                            st.success("✅ Top Crypto Analisadas")
                            st.dataframe(
                                results_df, hide_index=True, use_container_width=True
                            )
                    except Exception as e:
                        st.error("❌ Erro no scanner Crypto")

        st.markdown("---")
        st.write(
            "💡 **Dica:** Use a análise individual para estudos mais detalhados dos ativos encontrados"
        )

    # ================================
    # TAB 3: COMPARADOR (SIMPLIFICADO)
    # ================================
    with tab3:
        st.header("📊 Comparador de Ativos")

        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            symbols_input = st.text_input(
                "Digite os símbolos separados por vírgula:",
                placeholder="Ex: AAPL,MSFT,GOOGL,PETR4.SA",
                help="Máximo 5 ativos para melhor performance",
            )

        with col2:
            comp_period = st.selectbox("Período:", ["3mo", "6mo", "1y"], index=1)

        with col3:
            compare_btn = st.button(
                "⚖️ COMPARAR", type="primary", use_container_width=True
            )
            
        # Initialize comparator
        comparator = AssetComparator()

        # Comparações populares
        st.write("**🔥 Comparações Populares:**")

        popular_comparisons = {
            "🏆 Big Tech": "AAPL,MSFT,GOOGL,NVDA",
            "💎 Brasil Top": "PETR4.SA,VALE3.SA,ITUB4.SA",
            "💰 Crypto": "BTC-USD,ETH-USD,BNB-USD",
            "📊 Índices": "^GSPC,^DJI,^BVSP",
        }

        cols = st.columns(len(popular_comparisons))
        for i, (name, symbols) in enumerate(popular_comparisons.items()):
            with cols[i]:
                if st.button(name, key=f"pop_comp_{i}"):
                    st.session_state["comparison_symbols"] = symbols
                    st.rerun()

        # Usar símbolos da sessão se disponível
        if "comparison_symbols" in st.session_state and not symbols_input:
            symbols_input = st.session_state["comparison_symbols"]
            compare_btn = True

        if compare_btn and symbols_input:
            symbols = [s.strip().upper() for s in symbols_input.split(",")]
            symbols = [s for s in symbols if s]

            if len(symbols) < 2:
                st.error("❌ Mínimo 2 ativos para comparação")
            elif len(symbols) > 5:
                st.warning("⚠️ Limitado a 5 ativos. Usando os primeiros 5.")
                symbols = symbols[:5]
            else:
                st.info(f"⚖️ Comparando: {', '.join(symbols)}")

                with st.spinner("🤖 Executando comparação..."):
                    try:
                        comparison_results = []

                        for symbol in symbols:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, comp_period
                                )
                                if data:
                                    analyzer = AdvancedAnalyzer()
                                    analyzer.data_provider = data_provider
                                    scores = analyzer.calculate_ai_scores(data)

                                    comparison_results.append(
                                        {
                                            "Symbol": symbol,
                                            "Price": data["current_price"],
                                            "Score_IA": scores["final"],
                                            "Return_1Y": data["returns"]["1y"],
                                            "Return_3M": data["returns"]["3m"],
                                            "Return_1M": data["returns"]["1m"],
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

                        if comparison_results:
                            st.success(
                                f"✅ Comparação de {len(comparison_results)} ativos concluída!"
                            )

                            df = pd.DataFrame(comparison_results).sort_values(
                                "Score_IA", ascending=False
                            )

                            # Resumo
                            st.subheader("📊 Resumo da Comparação")

                            display_df = df.copy()
                            display_df["Price"] = display_df["Price"].apply(
                                lambda x: f"${x:.2f}"
                            )
                            display_df["Return_1Y"] = display_df["Return_1Y"].apply(
                                lambda x: f"{x:.1f}%"
                            )
                            display_df["Return_3M"] = display_df["Return_3M"].apply(
                                lambda x: f"{x:.1f}%"
                            )
                            display_df["Return_1M"] = display_df["Return_1M"].apply(
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
                            🏆 **MELHOR ATIVO: {best['Symbol']}**
                            • Score IA: {best['Score_IA']:.1f}/100
                            • Preço: ${best['Price']:.2f}
                            • Retorno 1Y: {best['Return_1Y']:.1f}%
                            • Setor: {best['Sector']}
                            """
                            )

                            # Gráfico de scores
                            try:
                                fig_scores = px.bar(
                                    df,
                                    x="Symbol",
                                    y="Score_IA",
                                    color="Score_IA",
                                    title="🧠 Scores de IA por Ativo",
                                    color_continuous_scale="RdYlGn",
                                    range_color=[0, 100],
                                )
                                st.plotly_chart(fig_scores, use_container_width=True)
                            except:
                                st.info("📊 Gráfico temporariamente indisponível")

                        else:
                            st.error("❌ Não foi possível obter dados dos ativos")

                    except Exception as e:
                        st.error(f"❌ Erro na comparação: {str(e)}")

    # ================================
    # TAB 4: EDUCACIONAL (SIMPLIFICADO)
    # ================================
    with tab4:
        st.header("📚 Centro Educacional")

        st.markdown(
            """
        ### 🎯 Como Interpretar os Scores de IA
        
        **🚀 90-100:** Oportunidade excepcional - Alta probabilidade de retornos superiores
        
        **✅ 80-89:** Muito boa oportunidade - Bons fundamentos com catalisadores
        
        **🟢 70-79:** Boa oportunidade - Fundamentos razoáveis, adequado para perfil moderado
        
        **🟡 60-69:** Oportunidade moderada - Perfil neutro, requer análise detalhada
        
        **⚠️ 50-59:** Aguardar melhores condições - Muitas incertezas no momento
        
        **❌ 0-49:** Evitar/Vender - Fundamentos deteriorados, alto risco
        
        ---
        
        ### 📊 Componentes do Score
        
        **🔧 Score Técnico (20%):** RSI, médias móveis, MACD, drawdown atual
        
        **💼 Score Fundamental (25%):** P/L, ROE, crescimento, endividamento, margens
        
        **🚀 Score Momentum (15%):** Performance recente em múltiplos períodos
        
        **💎 Score Valor (20%):** P/B, P/S, PEG ratio, múltiplos vs setor
        
        **⭐ Score Qualidade (15%):** ROA, margens operacionais, estabilidade
        
        **⚠️ Penalização Risco (5%):** Volatilidade excessiva, endividamento alto
        
        ---
        
        ### 💡 Dicas de Uso
        
        **Para Análise Individual:**
        - Use símbolos exatos (ex: AAPL, PETR4.SA, BTC-USD)
        - Comece com períodos de 1 ano para análise completa
        - Verifique múltiplas métricas antes de decidir
        
        **Para Scanner:**
        - Use os scanners rápidos para descobrir oportunidades
        - Foque em ativos com score > 70 para menor risco
        - Analise individualmente os ativos interessantes
        
        **Para Comparação:**
        - Compare ativos do mesmo setor quando possível
        - Considere correlação para diversificação
        - Não se baseie apenas no score mais alto
        
        ---
        
        ### ⚠️ Aviso Importante
        
        Este sistema é uma ferramenta de análise e não constitui recomendação de investimento.
        Sempre consulte um profissional qualificado e faça sua própria pesquisa antes de investir.
        Investimentos envolvem riscos e podem resultar em perdas.
        """
        )

        # FAQ Rápido
        with st.expander("❓ Perguntas Frequentes"):
            st.markdown(
                """
            **Q: O sistema funciona para todos os mercados?**
            A: Sim, funciona para ações dos EUA, Brasil, Europa, Ásia, criptomoedas, ETFs e índices.
            
            **Q: Com que frequência os dados são atualizados?**
            A: Os dados são obtidos em tempo real do Yahoo Finance.
            
            **Q: Posso confiar 100% nas recomendações?**
            A: Não. O sistema é uma ferramenta de análise. Sempre faça sua própria pesquisa e consulte profissionais.
            
            **Q: Por que alguns ativos não funcionam?**
            A: Pode ser devido a problemas de conectividade, símbolos incorretos ou ativos com pouca liquidez.
            
            **Q: Como interpretar a volatilidade?**
            A: < 25% = Baixa, 25-50% = Moderada, > 50% = Alta. Crypto geralmente tem volatilidade muito alta.
            """
            )


if __name__ == "__main__":
    try:
        # Verificação básica de dependências
        import yfinance
        import plotly
        import pandas
        import numpy

        # Executar aplicação principal
        main()

        # Tabs principais
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🔍 Análise Individual",
                "🌍 Scanner Global",
                "📊 Comparador",
                "📚 Educacional",
            ]
        )

        # Footer
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("🌍 **Sistema Global de Investimentos**")
        with col2:
            st.write("🤖 **Powered by Advanced AI**")
        with col3:
            st.write(
                f"⏰ **Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )

    except ImportError as error:
        st.error(f"❌ Dependência faltando: {error}")
        st.markdown(
            """
        ### 📦 Instalação de Dependências:
        ```bash
        pip install streamlit pandas numpy yfinance plotly
        ```
        """
        )

    except Exception as error:
        st.error(f"❌ Erro na aplicação: {error}")
        st.info("🔄 Tente recarregar a página (F5) ou aguarde alguns minutos")

        # Diagnóstico simples
        if st.button("🔧 Diagnóstico Rápido"):
            st.write("**Verificando componentes...**")

            try:
                import streamlit

                st.success("✅ Streamlit OK")
            except:
                st.error("❌ Streamlit com problema")

            try:
                import yfinance

                test_data = yfinance.Ticker("AAPL").history(period="1d")
                if not test_data.empty:
                    st.success("✅ yfinance e conectividade OK")
                else:
                    st.warning("🟡 yfinance OK mas dados limitados")
            except:
                st.error("❌ yfinance ou conectividade com problema")

        # Exemplos rápidos
        st.write("**⚡ Exemplos Rápidos:**")
        col1, col2, col3, col4, col5 = st.columns(5)

        examples = [
            ("🇺🇸 AAPL", "AAPL"),
            ("🇺🇸 NVDA", "NVDA"),
            ("🇧🇷 PETR4.SA", "PETR4.SA"),
            ("💰 BTC-USD", "BTC-USD"),
            ("📊 ^GSPC", "^GSPC"),
        ]

        for i, (label, symbol) in enumerate(examples):
            with [col1, col2, col3, col4, col5][i]:
                if st.button(label, key=f"example_{symbol}"):
                    symbol_input = symbol
                    analyze_btn = True

        if analyze_btn and symbol_input:
            symbol = symbol_input.upper().strip()
            period = "1y"  # Default period
            data_provider = UnifiedDataProvider()

            with st.spinner(f"🤖 Analisando {symbol}..."):
                try:
                    # Obter dados básicos
                    data = data_provider.get_comprehensive_data(symbol, period)

                    if data:
                        # Criar analisador simples para este ativo
                        simple_analyzer = AdvancedAnalyzer()
                        simple_analyzer.data_provider = data_provider

                        # Calcular scores
                        ai_scores = simple_analyzer.calculate_ai_scores(data)

                        # Análise de sentimento simples
                        sentiment = {
                            "score": 0,
                            "trend": "Neutro",
                            "summary": "Análise básica",
                        }

                        # Potencial de crescimento
                        current_price = data["current_price"]
                        max_price = (
                            max(data["price_data"])
                            if data["price_data"]
                            else current_price
                        )
                        upside = ((max_price - current_price) / current_price) * 100

                        growth_potential = {
                            "conservative": min(upside * 0.4, 20),
                            "moderate": min(upside * 0.6, 35),
                            "optimistic": min(upside, 50),
                            "timeframe": "12-24 meses",
                        }

                        # Metas de preço
                        price_targets = {
                            "current": current_price,
                            "support": (
                                min(data["price_data"]) * 1.05
                                if data["price_data"]
                                else current_price * 0.9
                            ),
                            "resistance": (
                                max(data["price_data"]) * 0.95
                                if data["price_data"]
                                else current_price * 1.1
                            ),
                            "targets": {
                                "conservative": current_price * 1.15,
                                "moderate": current_price * 1.25,
                                "optimistic": current_price * 1.40,
                            },
                            "stop_loss": current_price * 0.85,
                        }

                        # Recomendação
                        final_score = ai_scores["final"]
                        if final_score >= 80:
                            recommendation = {
                                "action": "COMPRA FORTE",
                                "emoji": "🚀",
                                "confidence": "Alta",
                            }
                        elif final_score >= 70:
                            recommendation = {
                                "action": "COMPRAR",
                                "emoji": "✅",
                                "confidence": "Boa",
                            }
                        elif final_score >= 60:
                            recommendation = {
                                "action": "COMPRA MODERADA",
                                "emoji": "🟢",
                                "confidence": "Moderada",
                            }
                        elif final_score >= 50:
                            recommendation = {
                                "action": "AGUARDAR",
                                "emoji": "🟡",
                                "confidence": "Baixa",
                            }
                        else:
                            recommendation = {
                                "action": "EVITAR",
                                "emoji": "⚠️",
                                "confidence": "Alta",
                            }

                        # Exibir resultados
                        st.success(f"✅ **Análise completa para {symbol}**")

                        # Métricas principais
                        col1, col2, col3, col4, col5 = st.columns(5)

                        with col1:
                            return_1y = data["returns"]["1y"]
                            st.metric(
                                "💰 Preço Atual",
                                f"${current_price:.2f}",
                                f"{return_1y:+.1f}% (1Y)",
                            )

                        with col2:
                            st.metric(
                                f"{recommendation['emoji']} Score IA",
                                f"{final_score:.0f}/100",
                                recommendation["confidence"],
                            )

                        with col3:
                            st.metric(
                                "📈 Potencial",
                                f"+{growth_potential['moderate']:.1f}%",
                                growth_potential["timeframe"],
                            )

                        with col4:
                            volatility = data["risk_metrics"]["volatility"]
                            st.metric(
                                "📊 Volatilidade",
                                f"{volatility:.1f}%",
                                f"RSI: {data['technical']['rsi']:.0f}",
                            )

                        with col5:
                            market_cap = data["fundamentals"]["market_cap"]
                            st.metric(
                                "🏢 Market Cap",
                                format_large_number(market_cap),
                                data["fundamentals"]["sector"][:15],
                            )

                        # Recomendação principal
                        if recommendation["action"] in ["COMPRA FORTE", "COMPRAR"]:
                            st.success(
                                f"## {recommendation['emoji']} RECOMENDAÇÃO: {recommendation['action']}"
                            )
                        elif recommendation["action"] in [
                            "COMPRA MODERADA",
                            "AGUARDAR",
                        ]:
                            st.warning(
                                f"## {recommendation['emoji']} RECOMENDAÇÃO: {recommendation['action']}"
                            )
                        else:
                            st.error(
                                f"## {recommendation['emoji']} RECOMENDAÇÃO: {recommendation['action']}"
                            )

                        st.write(
                            f"**Confiança:** {recommendation['confidence']} | **Score:** {final_score}/100"
                        )

                        # Gráfico de preços simples
                        try:
                            chart = create_price_chart(data)
                            if chart:
                                st.plotly_chart(chart, use_container_width=True)
                        except:
                            st.info("📊 Gráfico temporariamente indisponível")

                        # Análise detalhada em colunas
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("📊 Scores Detalhados")

                            scores_df = pd.DataFrame(
                                [
                                    ["🔧 Técnico", f"{ai_scores['technical']:.1f}/100"],
                                    [
                                        "💼 Fundamentalista",
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

                            st.subheader("🎯 Metas de Preço")
                            st.write(f"**💰 Atual:** ${price_targets['current']:.2f}")
                            st.write(f"**🛡️ Suporte:** ${price_targets['support']:.2f}")
                            st.write(
                                f"**⚡ Resistência:** ${price_targets['resistance']:.2f}"
                            )
                            st.write(
                                f"**🛑 Stop Loss:** ${price_targets['stop_loss']:.2f}"
                            )

                        with col2:
                            st.subheader("📈 Potencial de Crescimento")

                            st.write(
                                f"**🛡️ Conservador:** +{growth_potential['conservative']:.1f}%"
                            )
                            st.progress(growth_potential["conservative"] / 50)

                            st.write(
                                f"**⚖️ Moderado:** +{growth_potential['moderate']:.1f}%"
                            )
                            st.progress(growth_potential["moderate"] / 50)

                            st.write(
                                f"**🚀 Otimista:** +{growth_potential['optimistic']:.1f}%"
                            )
                            st.progress(growth_potential["optimistic"] / 100)

                            st.subheader("💼 Dados Fundamentais")
                            fund = data["fundamentals"]
                            st.write(f"**P/L:** {fund['pe_ratio']:.1f}")
                            st.write(f"**ROE:** {fund['roe']*100:.1f}%")
                            st.write(f"**Margem:** {fund['profit_margin']*100:.1f}%")
                            st.write(
                                f"**Crescimento:** {fund['revenue_growth']*100:.1f}%"
                            )
                            st.write(f"**Setor:** {fund['sector']}")

                        # Performance histórica
                        with st.expander("📈 Performance Histórica"):
                            returns = data["returns"]

                            performance_df = pd.DataFrame(
                                [
                                    ["1 Mês", f"{returns['1m']:+.1f}%"],
                                    ["3 Meses", f"{returns['3m']:+.1f}%"],
                                    ["6 Meses", f"{returns['6m']:+.1f}%"],
                                    ["1 Ano", f"{returns['1y']:+.1f}%"],
                                ],
                                columns=["Período", "Retorno"],
                            )

                            st.dataframe(
                                performance_df,
                                hide_index=True,
                                use_container_width=True,
                            )

                    else:
                        st.error(
                            f"❌ Não foi possível analisar {symbol}. Verifique se o símbolo está correto."
                        )

                except Exception as e:
                    st.error(f"❌ Erro durante a análise: {str(e)}")
                    st.info("💡 Tente com outro símbolo ou aguarde alguns minutos")

    # ================================
    # TAB 2: SCANNER GLOBAL (SIMPLIFICADO)
    # ================================
    with tab2:
        st.header("🌍 Scanner Global de Oportunidades")

        st.info("⚡ **Scanner Rápido** - Versão simplificada para melhor performance")

        # Scanners predefinidos
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🇺🇸 Top EUA", use_container_width=True):
                with st.spinner("Analisando EUA..."):
                    try:
                        usa_symbols = [
                            "AAPL",
                            "MSFT",
                            "GOOGL",
                            "AMZN",
                            "NVDA",
                            "TSLA",
                            "META",
                            "NFLX",
                        ]
                        results = []

                        for symbol in usa_symbols[:6]:  # Limitar para performance
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, "6mo"
                                )
                                if data:
                                    analyzer = AdvancedAnalyzer()
                                    analyzer.data_provider = data_provider
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
                            results_df = pd.DataFrame(results).sort_values(
                                "Score", ascending=False
                            )
                            st.success("✅ Top EUA Analisados")
                            st.dataframe(
                                results_df, hide_index=True, use_container_width=True
                            )
                    except Exception as e:
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
                            "RENT3.SA",
                        ]
                        results = []

                        for symbol in br_symbols[:6]:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, "6mo"
                                )
                                if data:
                                    analyzer = AdvancedAnalyzer()
                                    analyzer.data_provider = data_provider
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
                            results_df = pd.DataFrame(results).sort_values(
                                "Score", ascending=False
                            )
                            st.success("✅ Top Brasil Analisados")
                            st.dataframe(
                                results_df, hide_index=True, use_container_width=True
                            )
                    except Exception as e:
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
                            "DOT-USD",
                        ]
                        results = []

                        for symbol in crypto_symbols[:6]:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, "6mo"
                                )
                                if data:
                                    analyzer = AdvancedAnalyzer()
                                    analyzer.data_provider = data_provider
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
                            results_df = pd.DataFrame(results).sort_values(
                                "Score", ascending=False
                            )
                            st.success("✅ Top Crypto Analisadas")
                            st.dataframe(
                                results_df, hide_index=True, use_container_width=True
                            )
                    except Exception as e:
                        st.error("❌ Erro no scanner Crypto")

        st.markdown("---")
        st.write(
            "💡 **Dica:** Use a análise individual para estudos mais detalhados dos ativos encontrados"
        )

    # ================================
    # TAB 3: COMPARADOR (SIMPLIFICADO)
    # ================================
    with tab3:
        st.header("📊 Comparador de Ativos")

        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            symbols_input = st.text_input(
                "Digite os símbolos separados por vírgula:",
                placeholder="Ex: AAPL,MSFT,GOOGL,PETR4.SA",
                help="Máximo 5 ativos para melhor performance",
            )

        with col2:
            comp_period = st.selectbox("Período:", ["3mo", "6mo", "1y"], index=1)

        with col3:
            compare_btn = st.button(
                "⚖️ COMPARAR", type="primary", use_container_width=True
            )

        # Comparações populares
        st.write("**🔥 Comparações Populares:**")

        popular_comparisons = {
            "🏆 Big Tech": "AAPL,MSFT,GOOGL,NVDA",
            "💎 Brasil Top": "PETR4.SA,VALE3.SA,ITUB4.SA",
            "💰 Crypto": "BTC-USD,ETH-USD,BNB-USD",
            "📊 Índices": "^GSPC,^DJI,^BVSP",
        }

        cols = st.columns(len(popular_comparisons))
        for i, (name, symbols) in enumerate(popular_comparisons.items()):
            with cols[i]:
                if st.button(name, key=f"pop_comp_{i}"):
                    symbols_input = symbols
                    compare_btn = True

        if compare_btn and symbols_input:
            symbols = [s.strip().upper() for s in symbols_input.split(",")]
            symbols = [s for s in symbols if s]

            if len(symbols) < 2:
                st.error("❌ Mínimo 2 ativos para comparação")
            elif len(symbols) > 5:
                st.warning("⚠️ Limitado a 5 ativos. Usando os primeiros 5.")
                symbols = symbols[:5]
            else:
                st.info(f"⚖️ Comparando: {', '.join(symbols)}")

                with st.spinner("🤖 Executando comparação..."):
                    try:
                        comparison_results = []

                        for symbol in symbols:
                            try:
                                data = data_provider.get_comprehensive_data(
                                    symbol, comp_period
                                )
                                if data:
                                    analyzer = AdvancedAnalyzer()
                                    analyzer.data_provider = data_provider
                                    scores = analyzer.calculate_ai_scores(data)

                                    comparison_results.append(
                                        {
                                            "Symbol": symbol,
                                            "Price": data["current_price"],
                                            "Score_IA": scores["final"],
                                            "Return_1Y": data["returns"]["1y"],
                                            "Return_3M": data["returns"]["3m"],
                                            "Return_1M": data["returns"]["1m"],
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

                        if comparison_results:
                            st.success(
                                f"✅ Comparação de {len(comparison_results)} ativos concluída!"
                            )

                            df = pd.DataFrame(comparison_results).sort_values(
                                "Score_IA", ascending=False
                            )

                            # Resumo
                            st.subheader("📊 Resumo da Comparação")

                            display_df = df.copy()
                            display_df["Price"] = display_df["Price"].apply(
                                lambda x: f"${x:.2f}"
                            )
                            display_df["Return_1Y"] = display_df["Return_1Y"].apply(
                                lambda x: f"{x:.1f}%"
                            )
                            display_df["Return_3M"] = display_df["Return_3M"].apply(
                                lambda x: f"{x:.1f}%"
                            )
                            display_df["Return_1M"] = display_df["Return_1M"].apply(
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
                            🏆 **MELHOR ATIVO: {best['Symbol']}**
                            • Score IA: {best['Score_IA']:.1f}/100
                            • Preço: ${best['Price']:.2f}
                            • Retorno 1Y: {best['Return_1Y']:.1f}%
                            • Setor: {best['Sector']}
                            """
                            )

                            # Gráfico de scores
                            try:
                                fig_scores = px.bar(
                                    df,
                                    x="Symbol",
                                    y="Score_IA",
                                    color="Score_IA",
                                    title="🧠 Scores de IA por Ativo",
                                    color_continuous_scale="RdYlGn",
                                    range_color=[0, 100],
                                )
                                st.plotly_chart(fig_scores, use_container_width=True)
                            except:
                                st.info("📊 Gráfico temporariamente indisponível")

                        else:
                            st.error("❌ Não foi possível obter dados dos ativos")

                    except Exception as e:
                        st.error(f"❌ Erro na comparação: {str(e)}")

    # ================================
    # TAB 4: EDUCACIONAL (SIMPLIFICADO)
    # ================================
    with tab4:
        st.header("📚 Centro Educacional")

        st.markdown(
            """
        ### 🎯 Como Interpretar os Scores de IA
        
        **🚀 90-100:** Oportunidade excepcional - Alta probabilidade de retornos superiores
        
        **✅ 80-89:** Muito boa oportunidade - Bons fundamentos com catalisadores
        
        **🟢 70-79:** Boa oportunidade - Fundamentos razoáveis, adequado para perfil moderado
        
        **🟡 60-69:** Oportunidade moderada - Perfil neutro, requer análise detalhada
        
        **⚠️ 50-59:** Aguardar melhores condições - Muitas incertezas no momento
        
        **❌ 0-49:** Evitar/Vender - Fundamentos deteriorados, alto risco
        
        ---
        
        ### 📊 Componentes do Score
        
        **🔧 Score Técnico (20%):** RSI, médias móveis, MACD, drawdown atual
        
        **💼 Score Fundamental (25%):** P/L, ROE, crescimento, endividamento, margens
        
        **🚀 Score Momentum (15%):** Performance recente em múltiplos períodos
        
        **💎 Score Valor (20%):** P/B, P/S, PEG ratio, múltiplos vs setor
        
        **⭐ Score Qualidade (15%):** ROA, margens operacionais, estabilidade
        
        **⚠️ Penalização Risco (5%):** Volatilidade excessiva, endividamento alto
        
        ---
        
        ### 💡 Dicas de Uso
        
        **Para Análise Individual:**
        - Use símbolos exatos (ex: AAPL, PETR4.SA, BTC-USD)
        - Comece com períodos de 1 ano para análise completa
        - Verifique múltiplas métricas antes de decidir
        
        **Para Scanner:**
        - Use os scanners rápidos para descobrir oportunidades
        - Foque em ativos com score > 70 para menor risco
        - Analise individualmente os ativos interessantes
        
        **Para Comparação:**
        - Compare ativos do mesmo setor quando possível
        - Considere correlação para diversificação
        - Não se baseie apenas no score mais alto
        
        ---
        
        ### ⚠️ Aviso Importante
        
        Este sistema é uma ferramenta de análise e não constitui recomendação de investimento.
        Sempre consulte um profissional qualificado e faça sua própria pesquisa antes de investir.
        Investimentos envolvem riscos e podem resultar em perdas.
        """
        )

        # FAQ Rápido
        with st.expander("❓ Perguntas Frequentes"):
            st.markdown(
                """
            **Q: O sistema funciona para todos os mercados?**
            A: Sim, funciona para ações dos EUA, Brasil, Europa, Ásia, criptomoedas, ETFs e índices.
            
            **Q: Com que frequência os dados são atualizados?**
            A: Os dados são obtidos em tempo real do Yahoo Finance, com cache de 30 minutos para otimizar performance.
            
            **Q: Posso confiar 100% nas recomendações?**
            A: Não. O sistema é uma ferramenta de análise. Sempre faça sua própria pesquisa e consulte profissionais.
            
            **Q: Por que alguns ativos não funcionam?**
            A: Pode ser devido a problemas de conectividade, símbolos incorretos ou ativos com pouca liquidez.
            
            **Q: Como interpretar a volatilidade?**
            A: < 25% = Baixa, 25-50% = Moderada, > 50% = Alta. Crypto geralmente tem volatilidade muito alta.
            """
            )

if __name__ == "__main__":
    try:
        # Verificação básica de dependências
        import yfinance
        import plotly
        import pandas
        import numpy

        # Executar aplicação principal
        main()

        # Footer
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("🌍 **Sistema Global de Investimentos**")
        with col2:
            st.write("🤖 **Powered by Advanced AI**")
        with col3:
            st.write(
                f"⏰ **Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )

    except ImportError as e:
        st.error(f"❌ Dependência faltando: {e}")
        st.markdown(
            """
        ### 📦 Instalação de Dependências:
        ```bash
        pip install streamlit pandas numpy yfinance plotly
        ```
        """
        )

    except Exception as e:
        st.error(f"❌ Erro na aplicação: {e}")
        st.info("🔄 Tente recarregar a página (F5) ou aguarde alguns minutos")

        # Diagnóstico simples
        if st.button("🔧 Diagnóstico Rápido"):
            st.write("**Verificando componentes...**")

            try:
                import streamlit

                st.success("✅ Streamlit OK")
            except:
                st.error("❌ Streamlit com problema")

            try:
                import yfinance

                test_data = yfinance.Ticker("AAPL").history(period="1d")
                if not test_data.empty:
                    st.success("✅ yfinance e conectividade OK")
                else:
                    st.warning("🟡 yfinance OK mas dados limitados")
            except:
                st.error("❌ yfinance ou conectividade com problema")

    # ================================
    # TAB 1: ANÁLISE INDIVIDUAL
    # ================================
    with tab1:
        st.header("🔍 Análise Individual Completa com IA")

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            symbol_input = st.text_input(
                "Digite o símbolo do ativo:",
                value=st.session_state.get("selected_symbol", ""),
                placeholder="Ex: AAPL, PETR4.SA, BTC-USD, ^GSPC, HGLG11.SA",
            )

        with col2:
            period = st.selectbox(
                "Período:", ["1mo", "3mo", "6mo", "1y", "2y"], index=3
            )

        with col3:
            analyze_btn = st.button(
                "🚀 ANALISAR", type="primary", use_container_width=True
            )

        # Exemplos rápidos
        st.write("**⚡ Exemplos Rápidos:**")
        col1, col2, col3, col4, col5 = st.columns(5)

        examples = [
            ("🇺🇸 AAPL", "AAPL"),
            ("🇺🇸 NVDA", "NVDA"),
            ("🇧🇷 PETR4.SA", "PETR4.SA"),
            ("💰 BTC-USD", "BTC-USD"),
            ("📊 ^GSPC", "^GSPC"),
        ]

        for i, (label, symbol) in enumerate(examples):
            with [col1, col2, col3, col4, col5][i]:
                if st.button(label, key=f"example_{symbol}"):
                    symbol_input = symbol
                    analyze_btn = True

        if analyze_btn and symbol_input:
            symbol = symbol_input.upper().strip()

            with st.spinner(f"🤖 Analisando {symbol} com IA avançada..."):
                analysis = analyzer.analyze_single_asset(symbol, period)

                if analysis:
                    data = analysis["data"]
                    ai_analysis = analysis["ai_analysis"]
                    recommendation = analysis["recommendation"]

                    # Header com métricas principais
                    st.success(f"✅ **Análise completa para {symbol}**")

                    col1, col2, col3, col4, col5 = st.columns(5)

                    with col1:
                        current_price = data["current_price"]
                        return_1y = data["returns"]["1y"]
                        st.metric(
                            "💰 Preço Atual",
                            f"${current_price:.2f}",
                            f"{return_1y:+.1f}% (1Y)",
                        )

                    with col2:
                        final_score = ai_analysis["final"]
                        st.metric(
                            f"{recommendation['emoji']} Score IA",
                            f"{final_score:.0f}/100",
                            recommendation["confidence"],
                        )

                    with col3:
                        growth = analysis["growth_potential"]["moderate"]
                        st.metric(
                            "📈 Potencial",
                            f"+{growth:.1f}%",
                            analysis["growth_potential"]["timeframe"],
                        )

                    with col4:
                        risk_level = recommendation["risk_level"]
                        risk_emoji = {
                            "Baixo": "🟢",
                            "Médio": "🟡",
                            "Alto": "🔴",
                            "Muito Alto": "🔴",
                        }.get(risk_level, "🟡")
                        st.metric(
                            f"{risk_emoji} Risco",
                            risk_level,
                            f"Vol: {data['risk_metrics']['volatility']:.1f}%",
                        )

                    with col5:
                        market_cap = data["fundamentals"]["market_cap"]
                        st.metric(
                            "🏢 Market Cap",
                            format_large_number(market_cap),
                            data["fundamentals"]["sector"][:15],
                        )

                    # Recomendação principal
                    rec = recommendation
                    rec_color = {
                        "COMPRA FORTE": "success",
                        "COMPRAR": "success",
                        "COMPRA MODERADA": "info",
                        "AGUARDAR MELHOR ENTRADA": "warning",
                        "EVITAR": "warning",
                        "VENDER/EVITAR": "error",
                    }.get(rec["action"], "info")

                    if rec_color == "success":
                        st.success(f"## {rec['emoji']} RECOMENDAÇÃO: {rec['action']}")
                    elif rec_color == "warning":
                        st.warning(f"## {rec['emoji']} RECOMENDAÇÃO: {rec['action']}")
                    else:
                        st.error(f"## {rec['emoji']} RECOMENDAÇÃO: {rec['action']}")

                    st.write(
                        f"**Confiança:** {rec['confidence']} | **Horizonte:** {rec['horizon']} | **Score Ajustado:** {rec['score']}/100"
                    )

                    # Gráfico de preços
                    chart = create_price_chart(data)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)

                    # Análise detalhada em abas
                    subtab1, subtab2, subtab3, subtab4 = st.tabs(
                        ["🧠 Scores IA", "💼 Fundamentals", "📈 Técnica", "🎯 Alvos"]
                    )

                    with subtab1:
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("📊 Scores Detalhados")

                            scores_df = pd.DataFrame(
                                [
                                    [
                                        "🔧 Técnico",
                                        f"{ai_analysis['technical']:.1f}/100",
                                    ],
                                    [
                                        "💼 Fundamentalista",
                                        f"{ai_analysis['fundamental']:.1f}/100",
                                    ],
                                    [
                                        "🚀 Momentum",
                                        f"{ai_analysis['momentum']:.1f}/100",
                                    ],
                                    ["💎 Valor", f"{ai_analysis['value']:.1f}/100"],
                                    [
                                        "⭐ Qualidade",
                                        f"{ai_analysis['quality']:.1f}/100",
                                    ],
                                    ["⚠️ Risco", f"{ai_analysis['risk']:.1f}/100"],
                                    [
                                        "🎯 **Final**",
                                        f"**{ai_analysis['final']:.1f}/100**",
                                    ],
                                ],
                                columns=["Categoria", "Score"],
                            )

                            st.dataframe(
                                scores_df, hide_index=True, use_container_width=True
                            )

                        with col2:
                            st.subheader("📈 Potencial de Crescimento")
                            growth = analysis["growth_potential"]

                            st.write(
                                f"**🛡️ Conservador:** +{growth['conservative']:.1f}%"
                            )
                            st.progress(growth["conservative"] / 50)

                            st.write(f"**⚖️ Moderado:** +{growth['moderate']:.1f}%")
                            st.progress(growth["moderate"] / 50)

                            st.write(f"**🚀 Otimista:** +{growth['optimistic']:.1f}%")
                            st.progress(growth["optimistic"] / 100)

                            st.write(f"**⏰ Prazo:** {growth['timeframe']}")

                            # Sentimento
                            st.subheader("📰 Sentimento")
                            sentiment = analysis["sentiment"]

                            sentiment_colors = {
                                "Muito Positivo": "🟢",
                                "Positivo": "🟡",
                                "Neutro": "⚪",
                                "Negativo": "🟠",
                                "Muito Negativo": "🔴",
                            }

                            color = sentiment_colors.get(sentiment["trend"], "⚪")
                            st.write(f"**{color} Tendência:** {sentiment['trend']}")
                            st.write(f"**📊 Score:** {sentiment['score']}")

                    with subtab2:
                        fund = data["fundamentals"]

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.subheader("💰 Valuation")
                            st.write(f"**P/L:** {fund['pe_ratio']:.1f}")
                            st.write(f"**P/B:** {fund['pb_ratio']:.1f}")
                            st.write(f"**P/S:** {fund['ps_ratio']:.1f}")
                            st.write(f"**PEG:** {fund['peg_ratio']:.1f}")
                            st.write(
                                f"**Market Cap:** {format_large_number(fund['market_cap'])}"
                            )

                        with col2:
                            st.subheader("📊 Rentabilidade")
                            st.write(f"**ROE:** {fund['roe']*100:.1f}%")
                            st.write(f"**ROA:** {fund['roa']*100:.1f}%")
                            st.write(
                                f"**Margem Líquida:** {fund['profit_margin']*100:.1f}%"
                            )
                            st.write(
                                f"**Margem Operacional:** {fund['operating_margin']*100:.1f}%"
                            )
                            st.write(
                                f"**Crescimento Receita:** {fund['revenue_growth']*100:.1f}%"
                            )

                        with col3:
                            st.subheader("🏢 Empresa")
                            st.write(f"**Setor:** {fund['sector']}")
                            st.write(f"**Indústria:** {fund['industry']}")
                            st.write(f"**País:** {fund['country']}")
                            st.write(
                                f"**Div. Yield:** {fund['dividend_yield']*100:.1f}%"
                            )
                            if fund["employees"] > 0:
                                st.write(f"**Funcionários:** {fund['employees']:,}")

                    with subtab3:
                        tech = data["technical"]
                        risk = data["risk_metrics"]

                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("📊 Indicadores Técnicos")
                            st.write(f"**RSI:** {tech['rsi']:.1f}")
                            st.write(f"**MA20:** ${tech['ma20']:.2f}")
                            st.write(f"**MA50:** ${tech['ma50']:.2f}")
                            st.write(f"**MA200:** ${tech['ma200']:.2f}")

                            macd = tech["macd"]
                            macd_signal = (
                                "Positivo"
                                if macd["line"] > macd["signal"]
                                else "Negativo"
                            )
                            st.write(f"**MACD:** {macd_signal}")

                        with col2:
                            st.subheader("⚠️ Métricas de Risco")
                            st.write(f"**Volatilidade:** {risk['volatility']:.1f}%")
                            st.write(f"**Max Drawdown:** {risk['max_drawdown']:.1f}%")
                            st.write(
                                f"**Drawdown Atual:** {risk['current_drawdown']:.1f}%"
                            )
                            st.write(f"**Beta:** {risk['beta']:.2f}")
                            st.write(f"**Sharpe Ratio:** {risk['sharpe_ratio']:.2f}")

                    with subtab4:
                        targets = analysis["price_targets"]

                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("🎯 Metas de Preço")
                            st.write(f"**💰 Preço Atual:** ${targets['current']}")
                            st.write(f"**🛡️ Suporte:** ${targets['support']}")
                            st.write(f"**⚡ Resistência:** ${targets['resistance']}")
                            st.write(f"**📊 MA200:** ${targets['ma200']}")

                        with col2:
                            st.subheader("🎯 Cenários de Preço")
                            st.write(
                                f"**🛡️ Conservador:** ${targets['targets']['conservative']}"
                            )
                            st.write(
                                f"**⚖️ Moderado:** ${targets['targets']['moderate']}"
                            )
                            st.write(
                                f"**🚀 Otimista:** ${targets['targets']['optimistic']}"
                            )
                            st.write(f"**🛑 Stop Loss:** ${targets['stop_loss']}")

                    # Feedback da IA
                    with st.expander("🤖 Análise Detalhada da IA", expanded=True):
                        feedback = analysis["feedback"]

                        col1, col2 = st.columns(2)

                        with col1:
                            if feedback["strengths"]:
                                st.write("**✅ Pontos Fortes:**")
                                for strength in feedback["strengths"]:
                                    st.write(f"• {strength}")

                            if feedback["opportunities"]:
                                st.write("**🎯 Oportunidades:**")
                                for opp in feedback["opportunities"]:
                                    st.write(f"• {opp}")

                        with col2:
                            if feedback["weaknesses"]:
                                st.write("**⚠️ Pontos Fracos:**")
                                for weakness in feedback["weaknesses"]:
                                    st.write(f"• {weakness}")

                            if feedback["threats"]:
                                st.write("**🚨 Ameaças:**")
                                for threat in feedback["threats"]:
                                    st.write(f"• {threat}")

                        st.info(f"**📝 Resumo da IA:** {feedback['summary']}")

                else:
                    st.error(
                        f"❌ Não foi possível analisar {symbol}. Verifique se o símbolo está correto."
                    )

    # ================================
    # TAB 2: SCANNER GLOBAL
    # ================================
    with tab2:
        st.header("🌍 Scanner Global de Oportunidades")

        # Configurações do scanner
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📊 Mercados para Scanear")

            col1a, col2a, col3a = st.columns(3)

            with col1a:
                st.write("**🇺🇸 Estados Unidos:**")
                usa_mega = st.checkbox("🏢 Mega Caps", value=True)
                usa_tech = st.checkbox("💻 Tech Stocks")
                usa_finance = st.checkbox("🏦 Financeiro")
                usa_energy = st.checkbox("⚡ Energia")
                usa_health = st.checkbox("🏥 Saúde")

            with col2a:
                st.write("**🇧🇷 Brasil:**")
                br_stocks = st.checkbox("🏭 Ações", value=True)
                br_reits = st.checkbox("🏢 FIIs")

                st.write("**🌍 Global:**")
                europe = st.checkbox("🇪🇺 Europa")
                asia = st.checkbox("🌏 Ásia")
                crypto = st.checkbox("💰 Crypto", value=True)

            with col3a:
                st.write("**📊 Outros:**")
                indices = st.checkbox("📈 Índices")
                etfs = st.checkbox("🏗️ ETFs")
                commodities = st.checkbox("🥇 Commodities")

        with col2:
            st.subheader("⚙️ Filtros")
            min_score = st.slider("Score IA Mínimo:", 0, 100, 65, 5)
            min_drawdown = st.slider("Drawdown Mínimo:", 0, 70, 15, 5)
            max_pe = st.slider("P/L Máximo:", 0, 50, 25, 5)
            max_vol = st.slider("Volatilidade Máx:", 20, 100, 60, 10)

            st.subheader("🔧 Performance")
            max_assets = st.selectbox("Máx Ativos:", [50, 100, 200, 300], index=1)

            # Contar ativos selecionados
            selected_categories = []
            if usa_mega:
                selected_categories.append("USA_Mega")
            if usa_tech:
                selected_categories.append("USA_Tech")
            if usa_finance:
                selected_categories.append("USA_Finance")
            if usa_energy:
                selected_categories.append("USA_Energy")
            if usa_health:
                selected_categories.append("USA_Healthcare")
            if br_stocks:
                selected_categories.append("Brazil_Stocks")
            if br_reits:
                selected_categories.append("Brazil_REITs")
            if europe:
                selected_categories.append("Europe_Stocks")
            if asia:
                selected_categories.append("Asia_Stocks")
            if crypto:
                selected_categories.append("Crypto")
            if indices:
                selected_categories.append("Indices")
            if etfs:
                selected_categories.append("ETFs")
            if commodities:
                selected_categories.append("Commodities")

            if selected_categories:
                total_symbols = len(
                    scanner.db.get_symbols_by_category(selected_categories)
                )
                st.info(f"📊 {min(total_symbols, max_assets)} ativos serão analisados")

        # Botão de scan
        scan_btn = st.button(
            "🚀 EXECUTAR SCANNER GLOBAL", type="primary", use_container_width=True
        )

        if scan_btn and selected_categories:
            filters = {
                "min_score": min_score,
                "min_drawdown": min_drawdown,
                "max_pe": max_pe,
                "max_volatility": max_vol,
                "min_market_cap": 0,
            }

            st.info(f"🔍 Iniciando scan de {len(selected_categories)} mercados...")

            with st.spinner("🤖 IA analisando oportunidades globais..."):
                opportunities = scanner.scan_opportunities(
                    selected_categories, filters, max_assets
                )

            if opportunities:
                st.success(f"🎉 {len(opportunities)} oportunidades encontradas!")

                df = pd.DataFrame(opportunities)

                # Métricas principais
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("🎯 Total", len(opportunities))
                col2.metric("📊 Score Médio", f"{df['score'].mean():.1f}")
                col3.metric("🏆 Melhor Score", f"{df['score'].max():.1f}")
                col4.metric("📈 Upside Médio", f"+{df['upside_potential'].mean():.1f}%")
                col5.metric("💰 Upside Total", f"+{df['upside_potential'].sum():.0f}%")

                # Gráfico principal
                fig_scanner = px.scatter(
                    df,
                    x="drawdown",
                    y="score",
                    size="upside_potential",
                    color="sector",
                    hover_data=["symbol", "pe_ratio", "returns_1y"],
                    title="🗺️ Mapa Global de Oportunidades",
                    labels={
                        "drawdown": "Drawdown Atual (%)",
                        "score": "Score IA",
                        "upside_potential": "Potencial Upside (%)",
                    },
                )
                fig_scanner.update_traces(marker=dict(sizemin=5))
                st.plotly_chart(fig_scanner, use_container_width=True)

                # Top 20 Oportunidades
                st.subheader("🏆 Top 20 Oportunidades Globais")

                top20 = df.head(20)[
                    [
                        "symbol",
                        "score",
                        "drawdown",
                        "upside_potential",
                        "returns_1y",
                        "pe_ratio",
                        "sector",
                        "price",
                    ]
                ]
                top20.columns = [
                    "Símbolo",
                    "Score IA",
                    "Drawdown %",
                    "Upside %",
                    "Ret 1Y %",
                    "P/L",
                    "Setor",
                    "Preço",
                ]

                # Colorir por score
                def color_score(val):
                    if val >= 80:
                        return "background-color: #90EE90"
                    elif val >= 70:
                        return "background-color: #FFFFE0"
                    elif val >= 60:
                        return "background-color: #FFE4B5"
                    else:
                        return "background-color: #FFB6C1"

                styled_df = top20.style.applymap(color_score, subset=["Score IA"])
                st.dataframe(styled_df, use_container_width=True, hide_index=True)

                # Análise por setor
                if len(df["sector"].unique()) > 1:
                    st.subheader("🏭 Oportunidades por Setor")

                    sector_analysis = (
                        df.groupby("sector")
                        .agg(
                            {
                                "score": "mean",
                                "upside_potential": "mean",
                                "returns_1y": "mean",
                                "symbol": "count",
                            }
                        )
                        .round(1)
                    )
                    sector_analysis.columns = [
                        "Score Médio",
                        "Upside Médio %",
                        "Ret 1Y Médio %",
                        "Qtd Ativos",
                    ]
                    sector_analysis = sector_analysis.sort_values(
                        "Score Médio", ascending=False
                    )

                    st.dataframe(sector_analysis, use_container_width=True)

                    # Gráfico por setor
                    fig_sector = px.bar(
                        sector_analysis.reset_index(),
                        x="sector",
                        y="Score Médio",
                        color="Score Médio",
                        title="📊 Score Médio por Setor",
                        color_continuous_scale="RdYlGn",
                    )
                    st.plotly_chart(fig_sector, use_container_width=True)

                # Top 5 detalhado
                with st.expander("🔍 Top 5 Análise Detalhada", expanded=True):
                    for i, (_, row) in enumerate(df.head(5).iterrows(), 1):
                        emoji = (
                            "🥇"
                            if i == 1
                            else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                        )

                        col1, col2, col3 = st.columns([1, 2, 1])

                        with col1:
                            st.write(f"### {emoji} {row['symbol']}")
                            st.write(f"**Score:** {row['score']:.1f}/100")
                            st.write(f"**Preço:** ${row['price']:.2f}")

                        with col2:
                            st.write(f"**Setor:** {row['sector']}")
                            st.write(f"**Drawdown:** {row['drawdown']:.1f}%")
                            st.write(
                                f"**Upside Potencial:** +{row['upside_potential']:.1f}%"
                            )
                            st.write(f"**Retorno 1Y:** {row['returns_1y']:.1f}%")

                        with col3:
                            st.write(f"**P/L:** {row['pe_ratio']:.1f}")
                            st.write(f"**RSI:** {row['rsi']:.1f}")
                            st.write(f"**Volatilidade:** {row['volatility']:.1f}%")

                        st.markdown("---")

                # Download
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Baixar Relatório Completo (CSV)",
                    csv,
                    f"scanner_global_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv",
                )

            else:
                st.warning(
                    "❌ Nenhuma oportunidade encontrada com os filtros aplicados"
                )

        elif scan_btn:
            st.error("⚠️ Selecione pelo menos um mercado para scan")

        # Scanners rápidos
        st.markdown("---")
        st.subheader("⚡ Scanners Rápidos Predefinidos")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🇺🇸 Top EUA", use_container_width=True):
                with st.spinner("Analisando EUA..."):
                    quick_filters = {
                        "min_score": 60,
                        "min_drawdown": 10,
                        "max_pe": 30,
                        "max_volatility": 50,
                    }
                    usa_results = scanner.scan_opportunities(
                        ["USA_Mega"], quick_filters, 50
                    )
                if usa_results:
                    usa_df = pd.DataFrame(usa_results).head(10)
                    st.success(f"✅ Top 10 EUA")
                    st.dataframe(
                        usa_df[["symbol", "score", "upside_potential", "price"]],
                        hide_index=True,
                    )

        with col2:
            if st.button("🇧🇷 Top Brasil", use_container_width=True):
                with st.spinner("Analisando Brasil..."):
                    quick_filters = {
                        "min_score": 60,
                        "min_drawdown": 10,
                        "max_pe": 25,
                        "max_volatility": 60,
                    }
                    br_results = scanner.scan_opportunities(
                        ["Brazil_Stocks"], quick_filters, 50
                    )
                if br_results:
                    br_df = pd.DataFrame(br_results).head(10)
                    st.success(f"✅ Top 10 Brasil")
                    st.dataframe(
                        br_df[["symbol", "score", "upside_potential", "price"]],
                        hide_index=True,
                    )

        with col3:
            if st.button("💰 Top Crypto", use_container_width=True):
                with st.spinner("Analisando Crypto..."):
                    quick_filters = {
                        "min_score": 55,
                        "min_drawdown": 15,
                        "max_pe": 999,
                        "max_volatility": 80,
                    }
                    crypto_results = scanner.scan_opportunities(
                        ["Crypto"], quick_filters, 30
                    )
                if crypto_results:
                    crypto_df = pd.DataFrame(crypto_results).head(10)
                    st.success(f"✅ Top 10 Crypto")
                    st.dataframe(
                        crypto_df[["symbol", "score", "returns_1y", "volatility"]],
                        hide_index=True,
                    )

        with col4:
            if st.button("🌍 Top Global", use_container_width=True):
                with st.spinner("Analisando Global..."):
                    quick_filters = {
                        "min_score": 70,
                        "min_drawdown": 15,
                        "max_pe": 25,
                        "max_volatility": 55,
                    }
                    global_results = scanner.scan_opportunities(
                        ["USA_Mega", "Brazil_Stocks", "Europe_Stocks"],
                        quick_filters,
                        100,
                    )
                if global_results:
                    global_df = pd.DataFrame(global_results).head(10)
                    st.success(f"✅ Top 10 Global")
                    st.dataframe(
                        global_df[["symbol", "score", "sector", "upside_potential"]],
                        hide_index=True,
                    )

    # ================================
    # TAB 3: COMPARADOR
    # ================================
    with tab3:
        st.header("📊 Comparador Avançado de Ativos")

        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            symbols_input = st.text_input(
                "Digite os símbolos separados por vírgula:",
                placeholder="Ex: AAPL,MSFT,GOOGL,PETR4.SA,BTC-USD",
                help="Máximo 8 ativos para melhor visualização",
            )

        with col2:
            comp_period = st.selectbox("Período:", ["3mo", "6mo", "1y", "2y"], index=2)

        with col3:
            compare_btn = st.button(
                "⚖️ COMPARAR", type="primary", use_container_width=True
            )

        # Comparações populares
        st.write("**🔥 Comparações Populares:**")

        popular_comparisons = {
            "🏆 Big Tech": "AAPL,MSFT,GOOGL,AMZN,META",
            "💎 Brasil Top": "PETR4.SA,VALE3.SA,ITUB4.SA,BBDC4.SA",
            "💰 Crypto Kings": "BTC-USD,ETH-USD,BNB-USD,SOL-USD",
            "📊 Índices Globais": "^GSPC,^DJI,^BVSP,^GDAXI",
            "🏢 FIIs Brasil": "HGLG11.SA,XPML11.SA,BTLG11.SA,VILG11.SA",
            "⚡ Energia Global": "XOM,CVX,PETR4.SA,TTE.PA",
        }

        cols = st.columns(len(popular_comparisons))
        for i, (name, symbols) in enumerate(popular_comparisons.items()):
            with cols[i]:
                if st.button(name, key=f"pop_comp_{i}"):
                    symbols_input = symbols
                    compare_btn = True

        if compare_btn and symbols_input:
            symbols = [s.strip().upper() for s in symbols_input.split(",")]
            symbols = [s for s in symbols if s]

            if len(symbols) < 2:
                st.error("❌ Mínimo 2 ativos para comparação")
            elif len(symbols) > 8:
                st.warning("⚠️ Limitado a 8 ativos. Usando os primeiros 8.")
                symbols = symbols[:8]
            else:
                st.info(f"⚖️ Comparando: {', '.join(symbols)}")

                with st.spinner("🤖 Executando comparação avançada..."):
                    comparison = comparator.compare_assets(symbols, comp_period)

                    if comparison:
                        st.success(f"✅ Comparação de {len(symbols)} ativos concluída!")

                        # Tabs de comparação
                        comp_tab1, comp_tab2, comp_tab3, comp_tab4, comp_tab5 = st.tabs(
                            [
                                "📈 Performance",
                                "⚖️ Risco",
                                "💼 Fundamentals",
                                "🧠 IA Scores",
                                "📊 Resumo",
                            ]
                        )

                        with comp_tab1:
                            st.subheader("📈 Análise de Performance")

                            perf_df = comparison["performance"]
                            if not perf_df.empty:
                                st.dataframe(
                                    perf_df, use_container_width=True, hide_index=True
                                )

                                # Gráfico de performance
                                fig_perf = px.bar(
                                    perf_df,
                                    x="Symbol",
                                    y=["1d", "1w", "1m", "3m", "6m", "1y"],
                                    title="Performance por Período",
                                    barmode="group",
                                )
                                st.plotly_chart(fig_perf, use_container_width=True)

                        with comp_tab2:
                            st.subheader("⚖️ Análise de Risco")

                            risk_df = comparison["risk"]
                            if not risk_df.empty:
                                st.dataframe(
                                    risk_df, use_container_width=True, hide_index=True
                                )

                                # Risco vs Retorno
                                perf_df = comparison["performance"]
                                if not perf_df.empty:
                                    combined = pd.merge(
                                        risk_df[["Symbol", "Volatility"]],
                                        perf_df[["Symbol", "1y"]],
                                        on="Symbol",
                                    )

                                    fig_risk = px.scatter(
                                        combined,
                                        x="Volatility",
                                        y="1y",
                                        text="Symbol",
                                        title="Risco vs Retorno (1 Ano)",
                                        labels={
                                            "Volatility": "Volatilidade (%)",
                                            "1y": "Retorno 1Y (%)",
                                        },
                                    )
                                    fig_risk.update_traces(textposition="top center")
                                    st.plotly_chart(fig_risk, use_container_width=True)

                        with comp_tab3:
                            st.subheader("💼 Dados Fundamentais")

                            fund_df = comparison["fundamentals"]
                            if not fund_df.empty:
                                st.dataframe(
                                    fund_df, use_container_width=True, hide_index=True
                                )

                            # Matriz de correlação
                            corr_df = comparison["correlation"]
                            if not corr_df.empty:
                                st.subheader("🔗 Matriz de Correlação")

                                fig_corr = px.imshow(
                                    corr_df,
                                    title="Correlação entre Ativos",
                                    color_continuous_scale="RdBu",
                                    aspect="auto",
                                )
                                st.plotly_chart(fig_corr, use_container_width=True)

                        with comp_tab4:
                            st.subheader("🧠 Scores de IA Comparados")

                            ai_df = comparison["ai_scores"]
                            if not ai_df.empty:
                                st.dataframe(
                                    ai_df, use_container_width=True, hide_index=True
                                )

                                # Gráfico radar dos scores
                                fig_radar = go.Figure()

                                categories = [
                                    "Technical",
                                    "Fundamental",
                                    "Momentum",
                                    "Value",
                                    "Quality",
                                ]

                                for _, row in ai_df.iterrows():
                                    values = [row[cat] for cat in categories]
                                    values += [values[0]]  # Fechar o radar

                                    fig_radar.add_trace(
                                        go.Scatterpolar(
                                            r=values,
                                            theta=categories + [categories[0]],
                                            fill="toself",
                                            name=row["Symbol"],
                                        )
                                    )

                                fig_radar.update_layout(
                                    polar=dict(
                                        radialaxis=dict(visible=True, range=[0, 100])
                                    ),
                                    title="Radar de Scores IA",
                                    showlegend=True,
                                )
                                st.plotly_chart(fig_radar, use_container_width=True)

                        with comp_tab5:
                            st.subheader("📊 Resumo Executivo")

                            summary_df = comparison["summary"]
                            if not summary_df.empty:
                                st.dataframe(
                                    summary_df,
                                    use_container_width=True,
                                    hide_index=True,
                                )

                                # Melhor ativo
                                best = summary_df.iloc[0]
                                st.success(
                                    f"""
                                🏆 **MELHOR ATIVO: {best['Symbol']}**
                                • Score Final: {best['Final_Score']:.1f}/100
                                • Recomendação: {best['Recommendation']}
                                • Potencial: {best['Upside_Potential']}
                                • Preço: {best['Price']}
                                """
                                )

                                # Ranking visual
                                fig_ranking = px.bar(
                                    summary_df,
                                    x="Symbol",
                                    y="Final_Score",
                                    color="Final_Score",
                                    title="Ranking Final por Score IA",
                                    color_continuous_scale="RdYlGn",
                                    range_color=[0, 100],
                                )
                                st.plotly_chart(fig_ranking, use_container_width=True)

                        # Gráfico de preços normalizados
                        st.subheader("📊 Comparação de Preços Normalizados")

                        # Initialize comparator
                        comparator = AssetComparator()

                        # Coletar dados de preços dos ativos comparados
                        fig_prices = go.Figure()

                        for symbol in symbols:
                            try:
                                data = comparator.analyzer.data_provider.get_comprehensive_data(
                                    symbol, comp_period
                                )
                                if data and data["hist_data"]:
                                    hist_df = pd.DataFrame(data["hist_data"])
                                    hist_df["Date"] = pd.to_datetime(hist_df["Date"])

                                    # Normalizar preços (base 100)
                                    normalized = (
                                        hist_df["Close"] / hist_df["Close"].iloc[0]
                                    ) * 100

                                    fig_prices.add_trace(
                                        go.Scatter(
                                            x=hist_df["Date"],
                                            y=normalized,
                                            mode="lines",
                                            name=symbol,
                                            line=dict(width=2),
                                        )
                                    )
                            except:
                                continue

                        fig_prices.update_layout(
                            title="Preços Normalizados (Base 100)",
                            xaxis_title="Data",
                            yaxis_title="Preço Normalizado",
                            height=500,
                        )
                        st.plotly_chart(fig_prices, use_container_width=True)

                        # Download
                        if not summary_df.empty:
                            csv = summary_df.to_csv(index=False)
                            st.download_button(
                                "📥 Baixar Comparação (CSV)",
                                csv,
                                f"comparacao_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                "text/csv",
                            )

                    else:
                        st.error("❌ Erro na comparação. Verifique os símbolos.")

    # ================================
    # TAB 4: EDUCACIONAL
    # ================================
    with tab4:
        st.header("📚 Centro Educacional de Investimentos")

        # Guias educacionais
        edu_tab1, edu_tab2, edu_tab3, edu_tab4 = st.tabs(
            ["🎯 Interpretação IA", "📊 Indicadores", "💡 Estratégias", "❓ FAQ"]
        )

        with edu_tab1:
            st.subheader("🎯 Como Interpretar os Scores de IA")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    """
                ### 🧠 **Sistema de Scoring (0-100)**
                
                **🚀 90-100:** Oportunidade excepcional
                - Alta probabilidade de retornos superiores
                - Fundamentos sólidos + momentum positivo
                - Risco controlado
                
                **✅ 80-89:** Muito boa oportunidade
                - Bons fundamentos com catalisadores
                - Tendência técnica favorável
                - Relação risco/retorno atrativa
                
                **🟢 70-79:** Boa oportunidade
                - Fundamentos razoáveis
                - Alguns pontos de atenção
                - Adequado para perfil moderado
                
                **🟡 60-69:** Oportunidade moderada
                - Perfil neutro
                - Requer análise mais detalhada
                - Considerar timing de entrada
                
                **⚠️ 50-59:** Aguardar melhores condições
                - Muitas incertezas
                - Risco elevado no momento
                - Monitorar desenvolvimentos
                
                **❌ 0-49:** Evitar/Vender
                - Fundamentos deteriorados
                - Tendência negativa
                - Alto risco de perdas
                """
                )

            with col2:
                st.markdown(
                    """
                ### 📊 **Componentes do Score**
                
                **🔧 Score Técnico (20%)**
                - RSI, médias móveis, MACD
                - Bandas de Bollinger
                - Drawdown atual (oportunidade)
                
                **💼 Score Fundamental (25%)**
                - P/L, ROE, crescimento
                - Endividamento, margens
                - Qualidade dos resultados
                
                **🚀 Score Momentum (15%)**
                - Performance recente
                - Aceleração/desaceleração
                - Tendências de curto prazo
                
                **💎 Score Valor (20%)**
                - P/B, P/S, PEG ratio
                - Múltiplos vs setor
                - Dividend yield
                
                **⭐ Score Qualidade (15%)**
                - ROA, margens operacionais
                - Estabilidade financeira
                - Crescimento sustentável
                
                **⚠️ Penalização Risco (5%)**
                - Volatilidade excessiva
                - Endividamento alto
                - Instabilidade operacional
                """
                )

        with edu_tab2:
            st.subheader("📊 Guia de Indicadores Técnicos e Fundamentais")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    """
                ### 📈 **Indicadores Técnicos**
                
                **RSI (Relative Strength Index)**
                - < 30: Oversold (oportunidade de compra)
                - 30-70: Zona neutra
                - > 70: Overbought (cuidado)
                
                **Médias Móveis**
                - MA20: Tendência de curto prazo
                - MA50: Tendência de médio prazo  
                - MA200: Tendência de longo prazo
                - Preço > MAs = Tendência de alta
                
                **MACD**
                - Linha > Signal: Momentum positivo
                - Linha < Signal: Momentum negativo
                - Histograma: Força do momentum
                
                **Bandas de Bollinger**
                - Banda superior: Resistência dinâmica
                - Banda inferior: Suporte dinâmico
                - Estreitamento: Possível breakout
                
                **Drawdown**
                - Mede queda desde o pico
                - > 20%: Possível oportunidade
                - > 40%: Grande desconto
                """
                )

            with col2:
                st.markdown(
                    """
                ### 💼 **Indicadores Fundamentais**
                
                **P/L (Price/Earnings)**
                - < 10: Muito barato
                - 10-15: Barato
                - 15-25: Justo
                - > 30: Caro
                
                **P/B (Price/Book)**
                - < 1: Abaixo do valor contábil
                - 1-2: Razoável
                - > 3: Premium
                
                **ROE (Return on Equity)**
                - > 20%: Excelente
                - 15-20%: Bom
                - 10-15%: Razoável
                - < 10%: Fraco
                
                **Debt/Equity**
                - < 0.3: Conservador
                - 0.3-1.0: Moderado
                - > 2.0: Alto risco
                
                **Margem Líquida**
                - > 20%: Excelente
                - 10-20%: Boa
                - 5-10%: Razoável
                - < 5%: Fraca
                
                **Crescimento de Receita**
                - > 20%: Alto crescimento
                - 10-20%: Bom crescimento
                - 5-10%: Crescimento moderado
                - < 0%: Declínio
                """
                )

        with edu_tab3:
            st.subheader("💡 Estratégias de Investimento")

            strategy_tab1, strategy_tab2, strategy_tab3 = st.tabs(
                ["🛡️ Conservador", "⚖️ Moderado", "🚀 Arrojado"]
            )

            with strategy_tab1:
                st.markdown(
                    """
                ## 🛡️ Perfil Conservador
                
                ### 🎯 **Objetivos**
                - Preservação de capital
                - Rendimento estável
                - Baixa volatilidade
                
                ### 📊 **Critérios de Seleção**
                - Score IA > 70
                - Risco < 30
                - Volatilidade < 25%
                - Dividend yield > 3%
                - Debt/Equity < 0.5
                
                ### 💰 **Alocação Sugerida**
                - 40% Ações blue chip
                - 30% FIIs/REITs
                - 20% Títulos/Renda fixa
                - 10% Reserva emergência
                
                ### ⏰ **Horizonte**
                - Médio a longo prazo (3+ anos)
                - Rebalanceamento semestral
                
                ### 🎯 **Ativos Recomendados**
                - Grandes bancos (ITUB4, BBDC4)
                - Utilities (ELET3, CMIG4)
                - FIIs de papel (HGLG11, XPML11)
                - ETFs de dividendos (SPYD, VYM)
                """
                )

            with strategy_tab2:
                st.markdown(
                    """
                ## ⚖️ Perfil Moderado
                
                ### 🎯 **Objetivos**
                - Crescimento do patrimônio
                - Equilibrio risco/retorno
                - Diversificação global
                
                ### 📊 **Critérios de Seleção**
                - Score IA > 65
                - Risco 30-60
                - Mix de valor e crescimento
                - P/L < 25
                - ROE > 15%
                
                ### 💰 **Alocação Sugerida**
                - 50% Ações diversificadas
                - 20% Internacional (ETFs)
                - 15% FIIs/REITs
                - 10% Crypto (Bitcoin/Ethereum)
                - 5% Reserva oportunidade
                
                ### ⏰ **Horizonte**
                - Médio prazo (2-5 anos)
                - Rebalanceamento trimestral
                
                ### 🎯 **Ativos Recomendados**
                - Tech growth (AAPL, MSFT, GOOGL)
                - Brasil (PETR4, VALE3, WEGE3)
                - ETFs globais (VTI, EFA, EEM)
                - Bitcoin para diversificação
                """
                )

            with strategy_tab3:
                st.markdown(
                    """
                ## 🚀 Perfil Arrojado
                
                ### 🎯 **Objetivos**
                - Máximo crescimento
                - Alpha generation
                - Oportunidades de turnaround
                
                ### 📊 **Critérios de Seleção**
                - Score IA > 60 (flexível)
                - Alto potencial upside
                - Drawdown > 30% (oportunidade)
                - Empresas disruptivas
                - Momentum positivo
                
                ### 💰 **Alocação Sugerida**
                - 60% Growth stocks
                - 20% Crypto portfolio
                - 10% Small caps
                - 5% Commodities
                - 5% Cash para timing
                
                ### ⏰ **Horizonte**
                - Longo prazo (5+ anos)
                - Trading ativo permitido
                
                ### 🎯 **Ativos Recomendados**
                - High growth (TSLA, NVDA, SHOP)
                - Crypto diversificado
                - Small caps brasileiras
                - Setores emergentes (IA, cleantech)
                """
                )

        with edu_tab4:
            st.subheader("❓ Perguntas Frequentes")

            faqs = [
                {
                    "q": "🤔 Como o Score de IA é calculado?",
                    "a": """O Score de IA combina 6 componentes principais:
                    
**1. Análise Técnica (20%):** RSI, médias móveis, MACD, drawdown
**2. Análise Fundamental (25%):** P/L, ROE, crescimento, endividamento  
**3. Momentum (15%):** Performance recente em múltiplos períodos
**4. Análise de Valor (20%):** P/B, P/S, PEG, dividend yield
**5. Qualidade (15%):** ROA, margens, estabilidade financeira
**6. Penalização de Risco (5%):** Volatilidade e instabilidade

Cada componente é pontuado de 0-100 e o score final é a média ponderada.""",
                },
                {
                    "q": "📊 Qual a diferença entre os mercados?",
                    "a": """**EUA:** Maior liquidez, empresas globais, moeda forte
**Brasil:** Maiores dividendos, ciclos econômicos, FIIs únicos  
**Europa:** Estabilidade, ESG, acesso a mercados desenvolvidos
**Ásia:** Alto crescimento, tecnologia, mercados emergentes
**Crypto:** 24/7, descentralizado, alta volatilidade, inovação""",
                },
                {
                    "q": "⏰ Qual o melhor timing para investir?",
                    "a": """**Para Ações:**
- RSI < 35: Ótimo timing de entrada
- Drawdown > 25%: Oportunidade de desconto
- Score IA > 75: Timing menos importante

**Para Crypto:**
- Maior volatilidade = mais oportunidades
- Dollar-cost averaging recomendado
- Nunca investir tudo de uma vez

**Geral:**
- Tempo no mercado > timing do mercado
- Diversificação temporal (DCA)
- Rebalanceamento regular""",
                },
                {
                    "q": "💰 Como definir o valor a investir?",
                    "a": """**Regra dos 3 Pilares:**

**1. Reserva de Emergência (6-12 meses)**
- 100% renda fixa líquida
- Antes de qualquer investimento

**2. Alocação por Perfil:**
- Conservador: 20-40% renda variável
- Moderado: 40-70% renda variável  
- Arrojado: 70-90% renda variável

**3. Diversificação:**
- Máximo 5% por ativo individual
- Máximo 20% por setor
- Máximo 10% em crypto (iniciantes)""",
                },
                {
                    "q": "📈 Como interpretar os gráficos?",
                    "a": """**Gráfico de Preços:**
- Candlesticks: OHLC do período
- Médias móveis: Tendências
- Bandas de Bollinger: Suporte/resistência

**Scatter Risco vs Retorno:**
- Eixo X: Volatilidade (risco)
- Eixo Y: Retorno histórico
- Quadrante ideal: Alto retorno, baixo risco

**Radar de Scores:**
- Cada eixo: Componente do score IA
- Área maior: Perfil mais completo
- Compare formatos entre ativos""",
                },
                {
                    "q": "🚨 Principais riscos a considerar?",
                    "a": """**Riscos do Sistema:**
- Dados históricos não garantem futuro
- IA pode ter vieses nos dados
- Mercados podem ser irracionais

**Riscos dos Ativos:**
- Volatilidade em crypto
- Risco cambial em ativos internacionais
- Concentração setorial no Brasil
- Liquidez em small caps

**Como Mitigar:**
- Diversificação ampla
- Horizonte de longo prazo
- Rebalanceamento regular
- Stop loss em posições especulativas
- Educação financeira contínua""",
                },
            ]

            for faq in faqs:
                with st.expander(faq["q"], expanded=False):
                    st.markdown(faq["a"])

        # Glossário
        st.markdown("---")

        with st.expander("📖 Glossário Completo", expanded=False):
            st.markdown(
                """
            ### 🔤 Termos Importantes
            
            **Alpha:** Retorno acima do benchmark/mercado
            **Beta:** Sensibilidade do ativo ao mercado (>1 = mais volátil)
            **Drawdown:** Queda percentual desde o pico histórico
            **EBITDA:** Lucros antes de juros, impostos, depreciação e amortização
            **Free Float:** Percentual de ações em circulação no mercado
            **Market Cap:** Valor de mercado (preço × quantidade de ações)
            **P/E (P/L):** Preço/Lucro - múltiplo de valuation
            **PEG:** P/E dividido pelo crescimento - valor ajustado
            **ROE:** Retorno sobre patrimônio líquido
            **ROI:** Retorno sobre investimento
            **Sharpe Ratio:** Retorno ajustado ao risco
            **Volatilidade:** Medida de oscilação de preços
            **Volume:** Quantidade de ações/ativos negociados
            **Yield:** Rendimento percentual (dividendos/preço)
            """
            )

if __name__ == "__main__":
    try:
        # Verificação de dependências
        import yfinance
        import plotly
        import pandas
        import numpy

        # Teste de conectividade
        try:
            test_ticker = yf.Ticker("AAPL")
            test_data = test_ticker.history(period="1d")
            if not test_data.empty:
                st.sidebar.info("🟢 Conectividade perfeita")
            else:
                st.sidebar.warning("🟡 Conectividade limitada")
        except Exception as e:
            st.sidebar.error(f"🔴 Problema de conectividade: {str(e)}")

        # Executar aplicação principal
        main()

        # Footer
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("🌍 **Sistema Global de Investimentos**")
        with col2:
            st.write("🤖 **Powered by Advanced AI**")
        with col3:
            st.write(
                f"⏰ **Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )

    except ImportError as e:
        st.error(f"❌ Dependência faltando: {e}")
        st.markdown(
            """
        ### 📦 Instalação de Dependências:
        ```bash
        pip install streamlit pandas numpy yfinance plotly
        ```
        """
        )

    except Exception as e:
        st.error(f"❌ Erro na aplicação: {e}")
        st.info("🔄 Tente recarregar a página ou verificar sua conexão com a internet")

        # Botão de diagnóstico
        if st.button("🔧 Executar Diagnóstico"):
            st.write("**Verificando sistema...**")

            # Verificar imports
            try:
                import streamlit

                st.success("✅ Streamlit OK")
            except:
                st.error("❌ Streamlit com problema")

            try:
                import pandas

                st.success("✅ Pandas OK")
            except:
                st.error("❌ Pandas com problema")

            try:
                import yfinance

                st.success("✅ yfinance OK")
            except:
                st.error("❌ yfinance com problema")

            try:
                import plotly

                st.success("✅ Plotly OK")
            except:
                st.error("❌ Plotly com problema")

            # Testar internet
            try:
                import requests

                response = requests.get("https://www.google.com", timeout=5)
                if response.status_code == 200:
                    st.success("✅ Conexão com internet OK")
                else:
                    st.warning("🟡 Internet lenta")
            except:
                st.error("❌ Sem conexão com internet")
