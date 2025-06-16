#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparador Global de Ativos - Versão Simplificada e Funcional
Sistema completo para comparação de investimentos
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from typing import List, Dict
import warnings
warnings.filterwarnings("ignore")

# Configuração da página
st.set_page_config(page_title="📊 Comparador de Ativos", page_icon="⚖️", layout="wide")


class AssetDatabase:
    """Base de dados simplificada de ativos"""

    def __init__(self):
        self.assets = {
            "USA_Stocks": [
                "AAPL",
                "MSFT",
                "GOOGL",
                "AMZN",
                "NVDA",
                "TSLA",
                "META",
                "NFLX",
                "ADBE",
                "CRM",
                "JPM",
                "BAC",
                "WFC",
                "GS",
                "MS",
                "V",
                "MA",
                "PYPL",
                "SQ",
                "COIN",
                "XOM",
                "CVX",
                "COP",
                "SLB",
                "HAL",
                "JNJ",
                "PFE",
                "MRK",
                "ABBV",
                "LLY",
            ],
            "Brazil_Stocks": [
                "PETR4.SA",
                "VALE3.SA",
                "ITUB4.SA",
                "BBDC4.SA",
                "ABEV3.SA",
                "B3SA3.SA",
                "JBSS3.SA",
                "RENT3.SA",
                "LREN3.SA",
                "MGLU3.SA",
                "WEGE3.SA",
                "SUZB3.SA",
                "RAIL3.SA",
                "VVAR3.SA",
                "HAPV3.SA",
                "PCAR3.SA",
                "CSNA3.SA",
                "USIM5.SA",
            ],
            "Brazil_REITs": [
                "HGLG11.SA",
                "XPML11.SA",
                "BTLG11.SA",
                "VILG11.SA",
                "KNCR11.SA",
                "IRDM11.SA",
                "MXRF11.SA",
                "BCFF11.SA",
                "HSML11.SA",
                "RECT11.SA",
                "VISC11.SA",
                "MALL11.SA",
            ],
            "Europe_Stocks": [
                "ASML.AS",
                "SAP.DE",
                "LVMH.PA",
                "NVO",
                "NESN.SW",
                "ROCHE.SW",
                "BAS.DE",
                "SIE.DE",
                "ADYEN.AS",
                "MC.PA",
                "OR.PA",
                "SHEL.L",
                "BP.L",
                "VOD.L",
            ],
            "Crypto": [
                "BTC-USD",
                "ETH-USD",
                "BNB-USD",
                "XRP-USD",
                "ADA-USD",
                "SOL-USD",
                "DOT-USD",
                "DOGE-USD",
                "AVAX-USD",
                "MATIC-USD",
                "LTC-USD",
                "UNI-USD",
                "LINK-USD",
            ],
            "Indices": [
                "^GSPC",
                "^DJI",
                "^IXIC",
                "^RUT",
                "^BVSP",
                "^GDAXI",
                "^FCHI",
                "^FTSE",
                "^N225",
            ],
            "ETFs": [
                "SPY",
                "QQQ",
                "IWM",
                "EFA",
                "EEM",
                "VTI",
                "GLD",
                "SLV",
                "XLE",
                "XLF",
                "XLK",
            ],
        }

    def get_all_symbols(self):
        all_symbols = []
        for category in self.assets.values():
            all_symbols.extend(category)
        return list(set(all_symbols))

    def search_assets(self, query):
        results = []
        query_upper = query.upper()

        for category, symbols in self.assets.items():
            for symbol in symbols:
                if query_upper in symbol or symbol.startswith(query_upper):
                    results.append({"symbol": symbol, "category": category})

        return results[:10]


class DataProvider:
    """Provedor de dados simplificado"""

    @st.cache_data(ttl=1800)
    def get_asset_data(_self, symbol: str, period: str = "1y"):
        """Obtém dados de um ativo"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                return None

            info = ticker.info
            current_price = float(hist["Close"][-1])

            # Retornos
            returns = _self._calculate_returns(hist["Close"])

            # Métricas de risco
            volatility = _self._calculate_volatility(hist["Close"])
            max_dd = _self._calculate_max_drawdown(hist["Close"])

            # Indicadores técnicos
            rsi = _self._calculate_rsi(hist["Close"].values)

            # Dados fundamentais
            pe_ratio = info.get("forwardPE", info.get("trailingPE", 0)) or 0
            market_cap = info.get("marketCap", 0) or 0
            sector = info.get("sector", "N/A")

            return {
                "symbol": symbol,
                "current_price": current_price,
                "hist_data": hist.reset_index(),
                "returns": returns,
                "volatility": volatility,
                "max_drawdown": max_dd,
                "rsi": rsi,
                "pe_ratio": pe_ratio,
                "market_cap": market_cap,
                "sector": sector,
                "price_data": hist["Close"].tolist(),
            }

        except Exception as e:
            st.error(f"Erro ao obter dados de {symbol}: {str(e)}")
            return None

    def _calculate_returns(self, prices):
        """Calcula retornos por período"""
        current = float(prices[-1])

        returns = {}
        periods = {"1d": 1, "1w": 5, "1m": 21, "3m": 63, "6m": 126, "1y": 252}

        for label, days in periods.items():
            if len(prices) >= days:
                past = float(prices[-days])
                returns[label] = ((current - past) / past) * 100
            else:
                returns[label] = 0

        return returns

    def _calculate_volatility(self, prices):
        """Calcula volatilidade anualizada"""
        returns = prices.pct_change().dropna()
        return float(returns.std() * np.sqrt(252) * 100)

    def _calculate_max_drawdown(self, prices):
        """Calcula drawdown máximo"""
        rolling_max = prices.expanding().max()
        drawdown = ((prices - rolling_max) / rolling_max) * 100
        return float(drawdown.min())

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


class AssetComparator:
    """Comparador de ativos"""

    def __init__(self):
        self.data_provider = DataProvider()

    def compare_assets(self, symbols: List[str], period: str = "1y"):
        """Compara múltiplos ativos"""
        assets_data = {}

        progress = st.progress(0)
        status = st.empty()

        for i, symbol in enumerate(symbols):
            status.text(f"Carregando {symbol}...")
            progress.progress((i + 1) / len(symbols))

            data = self.data_provider.get_asset_data(symbol, period)
            if data:
                assets_data[symbol] = data

        progress.empty()
        status.empty()

        if not assets_data:
            return None

        # Análises comparativas
        comparison = {
            "performance": self._compare_performance(assets_data),
            "risk": self._compare_risk(assets_data),
            "fundamentals": self._compare_fundamentals(assets_data),
            "correlation": self._calculate_correlation(assets_data),
            "summary": self._create_summary(assets_data),
        }

        return comparison

    def _compare_performance(self, assets_data):
        """Compara performance"""
        perf_data = []

        for symbol, data in assets_data.items():
            row = {"Symbol": symbol}
            row.update(data["returns"])
            row["Current_Price"] = data["current_price"]
            perf_data.append(row)

        return pd.DataFrame(perf_data)

    def _compare_risk(self, assets_data):
        """Compara métricas de risco"""
        risk_data = []

        for symbol, data in assets_data.items():
            risk_data.append(
                {
                    "Symbol": symbol,
                    "Volatility": round(data["volatility"], 2),
                    "Max_Drawdown": round(data["max_drawdown"], 2),
                    "RSI": round(data["rsi"], 1),
                }
            )

        return pd.DataFrame(risk_data)

    def _compare_fundamentals(self, assets_data):
        """Compara dados fundamentais"""
        fund_data = []

        for symbol, data in assets_data.items():
            market_cap = data["market_cap"]
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
                    "PE_Ratio": round(data["pe_ratio"], 1),
                    "Sector": data["sector"],
                }
            )

        return pd.DataFrame(fund_data)

    def _calculate_correlation(self, assets_data):
        """Calcula correlação entre ativos"""
        if len(assets_data) < 2:
            return pd.DataFrame()

        try:
            # Alinhar dados de preços
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

    def _create_summary(self, assets_data):
        """Cria resumo com scores"""
        summary_data = []

        for symbol, data in assets_data.items():
            # Score simples baseado em retorno 1y e risco
            return_1y = data["returns"].get("1y", 0)
            volatility = data["volatility"]

            # Score de performance (0-100)
            perf_score = min(100, max(0, (return_1y + 50) * 2))

            # Score de risco (inverso da volatilidade)
            risk_score = max(0, 100 - volatility)

            # Score final
            final_score = (perf_score + risk_score) / 2

            # Recomendação
            if final_score >= 75:
                recommendation = "COMPRAR"
            elif final_score >= 60:
                recommendation = "MANTER"
            elif final_score >= 40:
                recommendation = "AGUARDAR"
            else:
                recommendation = "EVITAR"

            summary_data.append(
                {
                    "Symbol": symbol,
                    "Performance_Score": round(perf_score, 1),
                    "Risk_Score": round(risk_score, 1),
                    "Final_Score": round(final_score, 1),
                    "Recommendation": recommendation,
                }
            )

        return pd.DataFrame(summary_data).sort_values("Final_Score", ascending=False)


def create_charts(comparison_data, assets_data):
    """Cria gráficos de comparação"""
    charts = []

    # 1. Gráfico de performance
    perf_df = comparison_data["performance"]
    if not perf_df.empty:
        fig_perf = px.bar(
            perf_df,
            x="Symbol",
            y=["1d", "1w", "1m", "3m", "6m", "1y"],
            title="📈 Performance por Período",
            labels={"value": "Retorno (%)", "Symbol": "Ativo"},
        )
        charts.append(fig_perf)

    # 2. Gráfico risco vs retorno
    risk_df = comparison_data["risk"]
    if not risk_df.empty and not perf_df.empty:
        combined = pd.merge(
            risk_df[["Symbol", "Volatility"]], perf_df[["Symbol", "1y"]], on="Symbol"
        )

        fig_risk = px.scatter(
            combined,
            x="Volatility",
            y="1y",
            text="Symbol",
            title="⚖️ Risco vs Retorno",
            labels={"Volatility": "Volatilidade (%)", "1y": "Retorno 1 Ano (%)"},
        )
        fig_risk.update_traces(textposition="top center")
        charts.append(fig_risk)

    # 3. Preços normalizados
    if assets_data:
        fig_prices = go.Figure()

        for symbol, data in assets_data.items():
            hist_df = data["hist_data"]
            if not hist_df.empty:
                prices = hist_df["Close"]
                normalized = (prices / prices.iloc[0]) * 100

                fig_prices.add_trace(
                    go.Scatter(
                        x=hist_df["Date"],
                        y=normalized,
                        mode="lines",
                        name=symbol,
                        line=dict(width=2),
                    )
                )

        fig_prices.update_layout(
            title="📊 Preços Normalizados (Base 100)",
            xaxis_title="Data",
            yaxis_title="Preço Normalizado",
            height=400,
        )
        charts.append(fig_prices)

    return charts


def main():
    """Interface principal"""

    st.title("📊 Comparador Global de Ativos")
    st.subheader("Sistema Simplificado para Comparação de Investimentos")

    # Status
    st.success("🟢 Sistema carregado com sucesso!")

    # Inicializar componentes
    try:
        asset_db = AssetDatabase()
        comparator = AssetComparator()

        st.info("✅ Componentes inicializados corretamente")

    except Exception as e:
        st.error(f"❌ Erro na inicialização: {e}")
        return

    # Sidebar
    with st.sidebar:
        st.title("🎯 Configurações")

        # Busca
        st.subheader("🔍 Buscar Ativos")
        search_query = st.text_input("Pesquisar:", placeholder="Ex: AAPL, PETR4")

        if search_query:
            results = asset_db.search_assets(search_query)
            if results:
                for result in results[:5]:
                    st.write(f"• {result['symbol']} ({result['category']})")

        # Categorias
        st.subheader("📂 Categorias")
        categories = {
            "USA_Stocks": "🇺🇸 Ações EUA",
            "Brazil_Stocks": "🇧🇷 Ações Brasil",
            "Brazil_REITs": "🇧🇷 FIIs Brasil",
            "Europe_Stocks": "🇪🇺 Ações Europa",
            "Crypto": "💰 Criptomoedas",
            "Indices": "📊 Índices",
            "ETFs": "🏗️ ETFs",
        }

        selected_cat = st.selectbox(
            "Escolha categoria:",
            [""] + list(categories.keys()),
            format_func=lambda x: categories.get(x, "Selecione..."),
        )

        if selected_cat:
            cat_symbols = asset_db.assets[selected_cat]
            st.write(f"📊 {len(cat_symbols)} ativos disponíveis")

        # Configurações
        st.subheader("⚙️ Configurações")
        period = st.selectbox("Período:", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)
        max_assets = st.slider("Máx ativos:", 2, 8, 4)

    # Interface principal
    st.subheader("🎯 Comparação de Ativos")

    # Input de símbolos
    col1, col2 = st.columns([3, 1])

    with col1:
        symbols_input = st.text_input(
            "Digite símbolos separados por vírgula:",
            placeholder="Ex: AAPL,MSFT,GOOGL,PETR4.SA",
            help="Máximo 8 ativos",
        )

    with col2:
        compare_btn = st.button("🔍 COMPARAR", type="primary", use_container_width=True)

    # Comparações populares
    st.write("**🚀 Comparações Populares:**")

    popular = {
        "Tech EUA": "AAPL,MSFT,GOOGL,AMZN",
        "Brasil Top": "PETR4.SA,VALE3.SA,ITUB4.SA",
        "Crypto": "BTC-USD,ETH-USD,BNB-USD",
        "Índices": "^GSPC,^DJI,^BVSP",
    }

    cols = st.columns(len(popular))
    for i, (name, symbols) in enumerate(popular.items()):
        with cols[i]:
            if st.button(name, key=f"pop_{i}"):
                symbols_input = symbols
                compare_btn = True

    # Executar comparação
    if compare_btn and symbols_input:
        symbols = [s.strip().upper() for s in symbols_input.split(",")]
        symbols = [s for s in symbols if s]

        if len(symbols) < 2:
            st.error("❌ Mínimo 2 ativos")
            return

        if len(symbols) > max_assets:
            st.warning(f"⚠️ Limitado a {max_assets} ativos")
            symbols = symbols[:max_assets]

        st.info(f"🔍 Comparando: {', '.join(symbols)}")

        # Executar análise
        with st.spinner("Processando..."):
            try:
                # Obter dados individuais
                assets_data = {}
                for symbol in symbols:
                    data = comparator.data_provider.get_asset_data(symbol, period)
                    if data:
                        assets_data[symbol] = data

                if not assets_data:
                    st.error("❌ Nenhum dado obtido")
                    return

                # Fazer comparação
                comparison = comparator.compare_assets(list(assets_data.keys()), period)

                if not comparison:
                    st.error("❌ Erro na comparação")
                    return

                st.success(f"✅ Comparação de {len(assets_data)} ativos concluída!")

                # Resultados
                tab1, tab2, tab3, tab4 = st.tabs(
                    ["📈 Performance", "⚖️ Risco", "💼 Fundamentals", "📊 Resumo"]
                )

                with tab1:
                    st.subheader("📈 Análise de Performance")

                    perf_df = comparison["performance"]
                    if not perf_df.empty:
                        st.dataframe(perf_df, use_container_width=True, hide_index=True)

                        # Gráfico de performance
                        fig_perf = px.bar(
                            perf_df,
                            x="Symbol",
                            y=["1d", "1w", "1m", "3m", "6m", "1y"],
                            title="Performance por Período",
                        )
                        st.plotly_chart(fig_perf, use_container_width=True)

                with tab2:
                    st.subheader("⚖️ Análise de Risco")

                    risk_df = comparison["risk"]
                    if not risk_df.empty:
                        st.dataframe(risk_df, use_container_width=True, hide_index=True)

                        # Risco vs Retorno
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
                                title="Risco vs Retorno",
                                labels={
                                    "Volatility": "Volatilidade (%)",
                                    "1y": "Retorno 1Y (%)",
                                },
                            )
                            fig_risk.update_traces(textposition="top center")
                            st.plotly_chart(fig_risk, use_container_width=True)

                with tab3:
                    st.subheader("💼 Dados Fundamentais")

                    fund_df = comparison["fundamentals"]
                    if not fund_df.empty:
                        st.dataframe(fund_df, use_container_width=True, hide_index=True)

                    # Correlação
                    corr_df = comparison["correlation"]
                    if not corr_df.empty:
                        st.subheader("🔗 Matriz de Correlação")

                        fig_corr = px.imshow(
                            corr_df,
                            title="Correlação entre Ativos",
                            color_continuous_scale="RdBu",
                        )
                        st.plotly_chart(fig_corr, use_container_width=True)

                with tab4:
                    st.subheader("📊 Resumo Executivo")

                    summary_df = comparison["summary"]
                    if not summary_df.empty:
                        # Scores
                        st.subheader("🏆 Ranking por Score")
                        st.dataframe(
                            summary_df, use_container_width=True, hide_index=True
                        )

                        # Gráfico de scores
                        fig_scores = px.bar(
                            summary_df,
                            x="Symbol",
                            y="Final_Score",
                            color="Final_Score",
                            title="Score Final por Ativo",
                            color_continuous_scale="RdYlGn",
                        )
                        st.plotly_chart(fig_scores, use_container_width=True)

                        # Melhor ativo
                        best = summary_df.iloc[0]
                        st.success(
                            f"""
                        🏆 **MELHOR ATIVO: {best['Symbol']}**
                        • Score Final: {best['Final_Score']}/100
                        • Recomendação: {best['Recommendation']}
                        """
                        )

                # Gráfico de preços
                st.subheader("📊 Comparação de Preços (Normalizado)")

                fig_prices = go.Figure()
                for symbol, data in assets_data.items():
                    hist_df = data["hist_data"]
                    if not hist_df.empty:
                        prices = hist_df["Close"]
                        normalized = (prices / prices.iloc[0]) * 100

                        fig_prices.add_trace(
                            go.Scatter(
                                x=hist_df["Date"],
                                y=normalized,
                                mode="lines",
                                name=symbol,
                                line=dict(width=2),
                            )
                        )

                fig_prices.update_layout(
                    title="Preços Normalizados (Base 100)",
                    xaxis_title="Data",
                    yaxis_title="Preço Normalizado",
                    height=400,
                )
                st.plotly_chart(fig_prices, use_container_width=True)

                # Download
                st.subheader("📥 Download")

                if not summary_df.empty:
                    csv = summary_df.to_csv(index=False)
                    st.download_button(
                        "Baixar Resumo (CSV)",
                        csv,
                        f"comparacao_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        "text/csv",
                    )

            except Exception as e:
                st.error(f"❌ Erro durante análise: {str(e)}")
                st.info("🔄 Tente novamente ou verifique os símbolos")


if __name__ == "__main__":
    try:
        # Verificar dependências básicas
        import yfinance
        import plotly
        import pandas
        import numpy

        # Teste básico
        test_ticker = yf.Ticker("AAPL")
        test_data = test_ticker.history(period="1d")

        if not test_data.empty:
            st.sidebar.success("🟢 Conectividade OK")
        else:
            st.sidebar.warning("🟡 Conectividade limitada")

        # Executar aplicação
        main()

    except ImportError as e:
        st.error(f"❌ Dependência faltando: {e}")
        st.code("pip install streamlit pandas numpy yfinance plotly")

    except Exception as e:
        st.error(f"❌ Erro na inicialização: {e}")
        st.info("🔄 Recarregue a página")

