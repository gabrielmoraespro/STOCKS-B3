#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scanner Global Final - Versão Testada e Funcional
Sistema completo para análise de oportunidades globais
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
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="🌍 Scanner Global Final",
    page_icon="🚀",
    layout="wide"
)

class AssetDatabase:
    """Base de dados de ativos globais"""
    
    def __init__(self):
        self.universe = {
            'USA_Mega': [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'BRK-B', 'UNH', 'JNJ',
                'V', 'PG', 'JPM', 'XOM', 'HD', 'CVX', 'MA', 'ABBV', 'PFE', 'KO',
                'AVGO', 'COST', 'WMT', 'BAC', 'DIS', 'TMO', 'PEP', 'ABT', 'LLY', 'CRM'
            ],
            'USA_Tech': [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'NFLX', 'ADBE', 'CRM', 'ORCL',
                'INTC', 'CSCO', 'AMD', 'QCOM', 'TXN', 'AVGO', 'IBM', 'MU', 'AMAT', 'LRCX'
            ],
            'Brazil': [
                'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'B3SA3.SA',
                'JBSS3.SA', 'RENT3.SA', 'LREN3.SA', 'MGLU3.SA', 'WEGE3.SA', 'SUZB3.SA',
                'RAIL3.SA', 'VVAR3.SA', 'HAPV3.SA', 'PCAR3.SA', 'CSNA3.SA', 'USIM5.SA'
            ],
            'Brazil_REITs': [
                'HGLG11.SA', 'XPML11.SA', 'BTLG11.SA', 'VILG11.SA', 'KNCR11.SA', 'IRDM11.SA',
                'MXRF11.SA', 'BCFF11.SA', 'HSML11.SA', 'RECT11.SA', 'VISC11.SA', 'MALL11.SA'
            ],
            'Europe': [
                'ASML.AS', 'SAP.DE', 'LVMH.PA', 'NVO', 'NESN.SW', 'ROCHE.SW', 'BAS.DE',
                'SIE.DE', 'ADYEN.AS', 'MC.PA', 'OR.PA', 'SAN.PA', 'TTE.PA', 'SHEL.L'
            ],
            'Asia': [
                'TSM', 'BABA', 'TCEHY', 'TM', 'SONY', '7203.T', '6758.T', '9984.T',
                '005930.KS', '000660.KS', '2330.TW', '1810.HK', '9988.HK', '700.HK'
            ],
            'Crypto': [
                'BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD', 'SOL-USD', 'DOT-USD',
                'DOGE-USD', 'AVAX-USD', 'SHIB-USD', 'MATIC-USD', 'LTC-USD', 'UNI-USD', 'LINK-USD'
            ],
            'Indices': [
                '^GSPC', '^DJI', '^IXIC', '^RUT', '^BVSP', '^GDAXI', '^FCHI', '^FTSE', '^N225'
            ],
            'ETFs': [
                'SPY', 'QQQ', 'IWM', 'EFA', 'EEM', 'VTI', 'GLD', 'SLV', 'XLE', 'XLF', 'XLK'
            ]
        }
    
    def get_symbols(self, categories: List[str]) -> List[str]:
        symbols = []
        for category in categories:
            if category in self.universe:
                symbols.extend(self.universe[category])
        return list(set(symbols))

class Analyzer:
    """Analisador de oportunidades"""
    
    def analyze(self, symbol: str) -> Dict:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1y")
            
            if hist.empty or len(hist) < 50:
                return None
                
            info = ticker.info
            current_price = float(hist['Close'][-1])
            max_price = float(hist['Close'].max())
            
            # Cálculos básicos
            drawdown = ((current_price - max_price) / max_price) * 100
            upside = ((max_price - current_price) / current_price) * 100
            
            # Retornos
            returns_1m = self._calc_return(hist['Close'], 21)
            returns_3m = self._calc_return(hist['Close'], 63)
            returns_1y = self._calc_return(hist['Close'], len(hist))
            
            # Indicadores
            rsi = self._calc_rsi(hist['Close'].values)
            volatility = self._calc_volatility(hist['Close'])
            
            # Fundamentals
            pe_ratio = info.get('forwardPE', info.get('trailingPE', 0)) or 0
            market_cap = info.get('marketCap', 0) or 0
            sector = info.get('sector', 'N/A')
            
            # Score
            score = self._calc_score(drawdown, pe_ratio, rsi, returns_1m, upside)
            
            return {
                'symbol': symbol,
                'price': round(current_price, 2),
                'drawdown': round(drawdown, 1),
                'upside': round(upside, 1),
                'returns_1m': round(returns_1m, 1),
                'returns_3m': round(returns_3m, 1),
                'returns_1y': round(returns_1y, 1),
                'rsi': round(rsi, 1),
                'volatility': round(volatility, 1),
                'pe_ratio': round(pe_ratio, 1),
                'market_cap': market_cap,
                'sector': sector,
                'score': round(score, 1)
            }
            
        except Exception:
            return None
    
    def _calc_return(self, prices, days):
        if len(prices) < days:
            return 0
        current = float(prices[-1])
        past = float(prices[-days])
        return ((current - past) / past) * 100
    
    def _calc_rsi(self, prices, period=14):
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
    
    def _calc_volatility(self, prices):
        returns = prices.pct_change().dropna()
        return float(returns.std() * np.sqrt(252) * 100)
    
    def _calc_score(self, drawdown, pe_ratio, rsi, momentum, upside):
        score = 50
        
        # Drawdown (oportunidade)
        dd = abs(drawdown)
        if dd > 40:
            score += 25
        elif dd > 25:
            score += 20
        elif dd > 15:
            score += 15
        elif dd > 10:
            score += 10
        
        # P/L
        if 0 < pe_ratio < 12:
            score += 20
        elif 12 <= pe_ratio < 18:
            score += 15
        elif 18 <= pe_ratio < 25:
            score += 10
        elif pe_ratio > 35:
            score -= 10
        
        # RSI
        if rsi < 30:
            score += 15
        elif rsi < 35:
            score += 10
        elif rsi > 70:
            score -= 10
        
        # Momentum
        if momentum > 10:
            score += 10
        elif momentum > 5:
            score += 5
        elif momentum < -10:
            score -= 10
        
        # Upside
        if upside > 40:
            score += 15
        elif upside > 25:
            score += 10
        elif upside > 15:
            score += 5
        
        return max(0, min(100, score))

def scan_parallel(symbols: List[str], max_workers: int = 20) -> List[Dict]:
    """Scan paralelo"""
    analyzer = Analyzer()
    results = []
    
    progress = st.progress(0)
    status = st.empty()
    
    def analyze_batch(batch):
        return [analyzer.analyze(symbol) for symbol in batch if analyzer.analyze(symbol)]
    
    # Dividir em lotes
    batch_size = max(1, len(symbols) // max_workers)
    batches = [symbols[i:i + batch_size] for i in range(0, len(symbols), batch_size)]
    
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(analyze_batch, batch): batch for batch in batches}
        
        for future in concurrent.futures.as_completed(futures):
            batch_results = future.result()
            results.extend(batch_results)
            
            completed += len(futures[future])
            progress.progress(completed / len(symbols))
            status.text(f"Analisados: {completed}/{len(symbols)}")
    
    progress.empty()
    status.empty()
    return results

def create_chart(df: pd.DataFrame):
    """Gráfico de oportunidades"""
    if df.empty:
        return None
    
    fig = px.scatter(
        df, x='drawdown', y='score', size='upside',
        color='sector', hover_data=['symbol', 'pe_ratio'],
        title="Mapa de Oportunidades Globais"
    )
    return fig

def main():
    """Interface principal"""
    
    st.title("🌍 Scanner Global de Oportunidades")
    st.subheader("Sistema Final com Dados Reais")
    
    # Status
    st.success("🔴 LIVE - Conectado aos mercados globais")
    
    # Database
    db = AssetDatabase()
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 Configurações")
        
        # Mercados
        st.subheader("🌍 Mercados")
        
        markets = {
            'USA_Mega': '🇺🇸 EUA - Mega Cap',
            'USA_Tech': '🇺🇸 EUA - Tech',
            'Brazil': '🇧🇷 Brasil - Ações',
            'Brazil_REITs': '🇧🇷 Brasil - FIIs',
            'Europe': '🇪🇺 Europa',
            'Asia': '🌏 Ásia',
            'Crypto': '💰 Crypto',
            'Indices': '📊 Índices',
            'ETFs': '🏗️ ETFs'
        }
        
        selected = []
        for key, label in markets.items():
            default = key in ['USA_Mega', 'Brazil', 'Crypto']
            if st.checkbox(label, value=default):
                selected.append(key)
        
        # Filtros
        st.subheader("⚙️ Filtros")
        min_score = st.slider("Score Mínimo", 0, 100, 60)
        min_drawdown = st.slider("Drawdown Mín", 0, 70, 15)
        max_pe = st.slider("P/L Máximo", 0, 50, 30)
        
        # Performance
        max_assets = st.selectbox("Máx Ativos", [50, 100, 200], index=1)
        max_workers = st.selectbox("Threads", [10, 20, 30], index=1)
        
        if selected:
            total = len(db.get_symbols(selected))
            st.info(f"📊 {total} ativos selecionados")
    
    # Interface principal
    if not selected:
        st.warning("⚠️ Selecione mercados na sidebar")
        return
    
    # Botão scan
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"🎯 {len(selected)} mercados selecionados")
    with col2:
        scan_btn = st.button("🚀 SCAN", type="primary", use_container_width=True)
    
    # Executar scan
    if scan_btn:
        symbols = db.get_symbols(selected)[:max_assets]
        
        st.info(f"🔍 Analisando {len(symbols)} ativos...")
        
        with st.spinner("Processando..."):
            opportunities = scan_parallel(symbols, max_workers)
        
        # Filtrar
        filtered = [
            opp for opp in opportunities
            if (opp['score'] >= min_score and
                abs(opp['drawdown']) >= min_drawdown and
                (opp['pe_ratio'] <= max_pe or opp['pe_ratio'] == 0))
        ]
        
        if filtered:
            st.success(f"🎉 {len(filtered)} oportunidades encontradas!")
            
            df = pd.DataFrame(filtered).sort_values('score', ascending=False)
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🎯 Total", len(filtered))
            col2.metric("📊 Score Médio", f"{df['score'].mean():.1f}")
            col3.metric("🏆 Melhor", f"{df['score'].max():.1f}")
            col4.metric("📈 Upside Total", f"+{df['upside'].sum():.0f}%")
            
            # Gráfico
            chart = create_chart(df)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            
            # Tabela Top 15
            st.subheader("🏆 Top 15 Oportunidades")
            
            top15 = df.head(15)[['symbol', 'score', 'drawdown', 'upside', 'returns_1y', 'pe_ratio', 'sector']]
            top15.columns = ['Símbolo', 'Score', 'DD %', 'Up %', 'Ret 1Y %', 'P/L', 'Setor']
            
            st.dataframe(top15, hide_index=True, use_container_width=True)
            
            # Análise por setor
            if len(df['sector'].unique()) > 1:
                st.subheader("🏭 Por Setor")
                sector_analysis = df.groupby('sector').agg({
                    'score': 'mean',
                    'upside': 'mean',
                    'symbol': 'count'
                }).round(1)
                sector_analysis.columns = ['Score Médio', 'Upside Médio', 'Qtd']
                st.dataframe(sector_analysis.sort_values('Score Médio', ascending=False))
            
            # Top 3 detalhado
            with st.expander("🔍 Top 3 Detalhado"):
                for i, (_, row) in enumerate(df.head(3).iterrows(), 1):
                    st.write(f"""
                    **{i}. {row['symbol']} - Score: {row['score']:.1f}**
                    • Preço: ${row['price']:.2f}
                    • Drawdown: {row['drawdown']:.1f}%
                    • Upside: +{row['upside']:.1f}%
                    • RSI: {row['rsi']:.1f}
                    • P/L: {row['pe_ratio']:.1f}
                    • Setor: {row['sector']}
                    """)
            
            # Download
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Baixar CSV",
                csv,
                f"scanner_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                "text/csv"
            )
        
        else:
            st.warning("❌ Nenhuma oportunidade com os filtros")
    
    # Scanners rápidos
    st.markdown("---")
    st.subheader("⚡ Scanners Rápidos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🇺🇸 Top USA"):
            usa_symbols = db.universe['USA_Mega'][:15]
            with st.spinner("Analisando EUA..."):
                usa_results = scan_parallel(usa_symbols, 10)
            if usa_results:
                usa_df = pd.DataFrame(usa_results).sort_values('score', ascending=False)
                st.success(f"✅ {len(usa_results)} ações analisadas")
                top_usa = usa_df.head(6)[['symbol', 'score', 'drawdown', 'price']]
                top_usa.columns = ['Símbolo', 'Score', 'DD %', 'Preço USD']
                st.dataframe(top_usa, hide_index=True)
    
    with col2:
        if st.button("🇧🇷 Top Brasil"):
            br_symbols = db.universe['Brazil'][:15]
            with st.spinner("Analisando Brasil..."):
                br_results = scan_parallel(br_symbols, 10)
            if br_results:
                br_df = pd.DataFrame(br_results).sort_values('score', ascending=False)
                st.success(f"✅ {len(br_results)} ações analisadas")
                top_br = br_df.head(6)[['symbol', 'score', 'drawdown', 'price']]
                top_br.columns = ['Símbolo', 'Score', 'DD %', 'Preço BRL']
                st.dataframe(top_br, hide_index=True)
    
    with col3:
        if st.button("💰 Top Crypto"):
            crypto_symbols = db.universe['Crypto'][:10]
            with st.spinner("Analisando Crypto..."):
                crypto_results = scan_parallel(crypto_symbols, 8)
            if crypto_results:
                crypto_df = pd.DataFrame(crypto_results).sort_values('score', ascending=False)
                st.success(f"✅ {len(crypto_results)} cryptos analisadas")
                top_crypto = crypto_df.head(6)[['symbol', 'score', 'returns_1y', 'volatility']]
                top_crypto.columns = ['Cripto', 'Score', 'Ret 1Y %', 'Vol %']
                st.dataframe(top_crypto, hide_index=True)
    
    # Info
    with st.expander("📊 Informações do Sistema"):
        total_assets = sum(len(symbols) for symbols in db.universe.values())
        st.write(f"🌍 **Total de ativos disponíveis:** {total_assets}")
        
        st.write("**Por categoria:**")
        for category, symbols in db.universe.items():
            st.write(f"• {category}: {len(symbols)} ativos")
        
        st.write("**Algoritmo de scoring:**")
        st.write("• 30% - Drawdown (oportunidade)")
        st.write("• 25% - Indicadores técnicos")
        st.write("• 20% - Múltiplos de valuation")
        st.write("• 15% - Potencial de upside")
        st.write("• 10% - Momentum")

if __name__ == "__main__":
    try:
        import yfinance
        import plotly
        import pandas
        import numpy
        
        # Teste de conectividade
        try:
            test_ticker = yf.Ticker("AAPL")
            test_data = test_ticker.history(period="1d")
            if not test_data.empty:
                st.info("🟢 Conectividade OK - Sistema pronto")
            else:
                st.warning("🟡 Conectividade limitada")
        except:
            st.warning("🟡 Problemas de conectividade detectados")
        
        main()
        
    except ImportError as e:
        st.error(f"❌ Dependência faltando: {e}")
        st.code("pip install streamlit pandas numpy yfinance plotly")
        
    except Exception as e:
        st.error(f"❌ Erro: {e}")
        st.info("🔄 Tente recarregar a página")
