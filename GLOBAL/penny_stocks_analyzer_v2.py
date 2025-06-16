#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 PENNY STOCKS B3 HUNTER - VERSÃO MELHORADA 🚀
Sistema Inteligente para Identificar Oportunidades de Baixo Preço

✅ Correções implementadas:
- Filtros de preço mais realistas para o mercado brasileiro atual
- Tratamento robusto de erros de dados
- Interface Streamlit integrada
- Análise adaptativa baseada no cenário atual
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import warnings
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import concurrent.futures
from dataclasses import dataclass

warnings.filterwarnings("ignore")

# Configuração da página Streamlit
st.set_page_config(
    page_title="🚀 Penny Stocks B3 Hunter",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class StockAnalysis:
    """Estrutura para análise de ações"""
    ticker: str
    nome: str
    preco_atual: float
    rsi: float
    volume_medio: int
    volatilidade: float
    tendencia_ma: str
    liquidez_score: int
    potencial_score: float
    nivel_risco: str
    entrada_sugerida: float
    alvo_conservador: float
    alvo_agressivo: float
    razao_entrada: str
    alertas: List[str]
    desconto_maxima: float
    setor: str

class BrazilianStockHunter:
    """🎯 Caçador de Oportunidades B3 - Versão Inteligente"""
    
    def __init__(self, price_range="flexible"):
        """
        price_range: 'penny' (R$0,10-2,00), 'low' (R$0,50-5,00), 'flexible' (R$0,10-10,00)
        """
        self.stocks_b3 = self._load_brazilian_stocks()
        self.price_range = price_range
        self._set_price_filters()
        self.min_volume_diario = 50000  # R$ 50k mínimo
        
    def _set_price_filters(self):
        """Define filtros de preço baseado no range selecionado"""
        if self.price_range == "penny":
            self.min_price = 0.10
            self.max_price = 2.00
        elif self.price_range == "low":
            self.min_price = 0.50
            self.max_price = 5.00
        else:  # flexible
            self.min_price = 0.10
            self.max_price = 10.00
        
    def _load_brazilian_stocks(self) -> List[str]:
        """🔍 Base de ações brasileiras - Focado em liquidez e disponibilidade"""
        return [
            # Blue Chips com maior probabilidade de dados
            "PETR4.SA", "PETR3.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA",
            "ABEV3.SA", "B3SA3.SA", "WEGE3.SA", "RENT3.SA", "LREN3.SA", "MGLU3.SA",
            
            # Mid Caps
            "CSNA3.SA", "USIM5.SA", "GGBR4.SA", "GOAU4.SA", "CYRE3.SA", "MRFG3.SA",
            "COGN3.SA", "YDUQ3.SA", "HAPV3.SA", "QUAL3.SA", "RDOR3.SA", "FLRY3.SA",
            
            # Small Caps e Recuperação
            "OIBR3.SA", "GOLL4.SA", "AZUL4.SA", "RECV3.SA", "AMER3.SA", "PCAR3.SA",
            "HYPE3.SA", "DESK3.SA", "LWSA3.SA", "MLAS3.SA", "PGMN3.SA", "LOGN3.SA",
            
            # Setores Específicos
            "JBSS3.SA", "BEEF3.SA", "SUZB3.SA", "RAIL3.SA", "CCRO3.SA", "SBSP3.SA",
            "CPFE3.SA", "ELET3.SA", "KLBN11.SA", "RADL3.SA", "PSSA3.SA", "MULT3.SA",
            
            # Telecom e Tech
            "TIMS3.SA", "VIVT3.SA", "TOTS3.SA", "TFCO4.SA", "TGMA3.SA",
            
            # Construção e Imobiliário
            "EVEN3.SA", "HBOR3.SA", "JHSF3.SA", "EZTC3.SA", "DIRR3.SA", "TCSA3.SA",
            
            # Outros promissores
            "SHOW3.SA", "MEAL3.SA", "NGRD3.SA", "LUPA3.SA", "CRFB3.SA", "BRFS3.SA",
            "JSLG3.SA", "TTEN3.SA", "LIGT3.SA", "VULC3.SA", "FIQE3.SA", "TUPY3.SA"
        ]
    
    def get_stock_data(self, ticker: str) -> Dict:
        """📊 Obtém dados com tratamento robusto de erros"""
        try:
            stock = yf.Ticker(ticker)
            
            # Tentar diferentes períodos se 1y falhar
            for period in ["1y", "6mo", "3mo"]:
                try:
                    hist = stock.history(period=period)
                    if not hist.empty and len(hist) > 30:  # Mínimo 30 dias
                        break
                except:
                    continue
            else:
                return None
                
            if hist.empty:
                return None
                
            # Informações da empresa
            try:
                info = stock.info
                if not isinstance(info, dict):
                    info = {}
            except:
                info = {}
            
            current_price = float(hist['Close'].iloc[-1])
            
            # Verificar se está na faixa de preço
            if not (self.min_price <= current_price <= self.max_price):
                return None
                
            # Volume médio dos últimos 20 dias
            volume_medio = int(hist['Volume'].rolling(min(20, len(hist))).mean().iloc[-1])
            volume_financeiro = volume_medio * current_price
            
            # Filtro de liquidez mais flexível
            if volume_financeiro < self.min_volume_diario:
                return None
                
            return {
                'ticker': ticker,
                'nome': info.get('longName', info.get('shortName', ticker.replace('.SA', ''))),
                'preco_atual': current_price,
                'hist_data': hist,
                'volume_medio': volume_medio,
                'volume_financeiro': volume_financeiro,
                'info': info,
                'market_cap': info.get('marketCap', 0),
                'setor': info.get('sector', 'N/A'),
                'industria': info.get('industry', 'N/A')
            }
            
        except Exception as e:
            return None
    
    def calculate_technical_indicators(self, hist_data: pd.DataFrame) -> Dict:
        """📈 Calcula indicadores com tratamento seguro de erros"""
        try:
            close = hist_data['Close']
            volume = hist_data['Volume']
            high = hist_data['High']
            low = hist_data['Low']
            
            # Garantir que temos dados suficientes
            if len(close) < 10:
                return self._get_default_indicators(float(close.iloc[-1]))
            
            # RSI
            rsi = self._safe_calculate_rsi(close)
            
            # Médias móveis (adaptadas ao tamanho dos dados)
            periods = min(len(close) // 3, 21)
            ma_short = close.rolling(min(7, periods)).mean().iloc[-1] if len(close) >= 7 else close.iloc[-1]
            ma_medium = close.rolling(min(21, periods)).mean().iloc[-1] if len(close) >= 21 else close.iloc[-1]
            ma_long = close.rolling(min(50, len(close))).mean().iloc[-1] if len(close) >= 50 else close.iloc[-1]
            
            current_price = close.iloc[-1]
            
            # Análise de tendência
            tendencia_ma = self._analyze_trend(current_price, ma_short, ma_medium, ma_long)
            
            # Volatilidade
            returns = close.pct_change().dropna()
            if len(returns) > 5:
                volatilidade = float(returns.std() * np.sqrt(252) * 100)
            else:
                volatilidade = 50.0
            
            # MACD simplificado
            macd_line, macd_signal = self._safe_calculate_macd(close)
            
            # Bandas de Bollinger
            bb_upper, bb_middle, bb_lower = self._safe_calculate_bollinger(close)
            
            # Volume
            volume_atual = volume.iloc[-1] if len(volume) > 0 else 1
            volume_medio = volume.rolling(min(10, len(volume))).mean().iloc[-1] if len(volume) >= 10 else volume_atual
            volume_ratio = volume_atual / volume_medio if volume_medio > 0 else 1
            
            # Máximas e mínimas
            max_periodo = high.max()
            min_periodo = low.min()
            distancia_maxima = ((current_price - max_periodo) / max_periodo) * 100
            
            return {
                'rsi': rsi,
                'ma_short': float(ma_short),
                'ma_medium': float(ma_medium),
                'ma_long': float(ma_long),
                'tendencia_ma': tendencia_ma,
                'volatilidade': volatilidade,
                'macd_line': macd_line,
                'macd_signal': macd_signal,
                'bb_upper': bb_upper,
                'bb_middle': bb_middle,
                'bb_lower': bb_lower,
                'volume_ratio': float(volume_ratio),
                'max_periodo': float(max_periodo),
                'min_periodo': float(min_periodo),
                'distancia_maxima': distancia_maxima,
            }
            
        except Exception as e:
            return self._get_default_indicators(float(hist_data['Close'].iloc[-1]))
    
    def _safe_calculate_rsi(self, prices, period=14):
        """RSI com tratamento de erro"""
        try:
            if len(prices) < period:
                period = max(2, len(prices) // 2)
            
            delta = prices.diff()
            gain = delta.where(delta > 0, 0).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return float(rsi.iloc[-1]) if not np.isnan(rsi.iloc[-1]) else 50.0
        except:
            return 50.0
    
    def _safe_calculate_macd(self, prices):
        """MACD simplificado"""
        try:
            if len(prices) < 26:
                return 0.0, 0.0
            
            exp1 = prices.ewm(span=12).mean()
            exp2 = prices.ewm(span=26).mean()
            macd_line = exp1 - exp2
            macd_signal = macd_line.ewm(span=9).mean()
            
            return float(macd_line.iloc[-1]), float(macd_signal.iloc[-1])
        except:
            return 0.0, 0.0
    
    def _safe_calculate_bollinger(self, prices, period=20):
        """Bandas de Bollinger adaptativas"""
        try:
            period = min(period, len(prices) // 2) if len(prices) > 10 else len(prices)
            if period < 2:
                current = float(prices.iloc[-1])
                return current * 1.02, current, current * 0.98
            
            sma = prices.rolling(period).mean()
            std = prices.rolling(period).std()
            
            upper = sma + (std * 2)
            lower = sma - (std * 2)
            
            return float(upper.iloc[-1]), float(sma.iloc[-1]), float(lower.iloc[-1])
        except:
            current = float(prices.iloc[-1])
            return current * 1.02, current, current * 0.98
    
    def _analyze_trend(self, current, ma_short, ma_medium, ma_long):
        """Análise de tendência"""
        if current > ma_short > ma_medium > ma_long:
            return "🟢 FORTE ALTA"
        elif current > ma_short > ma_medium:
            return "🔵 ALTA MODERADA"
        elif current > ma_medium:
            return "🟡 LATERAL ALTA"
        elif current < ma_short < ma_medium < ma_long:
            return "🔴 FORTE BAIXA"
        elif current < ma_short < ma_medium:
            return "🟠 BAIXA MODERADA"
        else:
            return "⚪ LATERAL"
    
    def _get_default_indicators(self, current_price):
        """Indicadores padrão"""
        return {
            'rsi': 50.0,
            'ma_short': current_price,
            'ma_medium': current_price,
            'ma_long': current_price,
            'tendencia_ma': "⚪ INDEFINIDA",
            'volatilidade': 50.0,
            'macd_line': 0.0,
            'macd_signal': 0.0,
            'bb_upper': current_price * 1.02,
            'bb_middle': current_price,
            'bb_lower': current_price * 0.98,
            'volume_ratio': 1.0,
            'max_periodo': current_price,
            'min_periodo': current_price,
            'distancia_maxima': 0.0,
        }
    
    def calculate_opportunity_score(self, data: Dict, indicators: Dict) -> Tuple[float, str, List[str]]:
        """🚀 Calcula score de oportunidade (0-100)"""
        score = 0
        reasons = []
        alerts = []
        
        preco = data['preco_atual']
        rsi = indicators['rsi']
        volatilidade = indicators['volatilidade']
        volume_ratio = indicators['volume_ratio']
        distancia_maxima = indicators['distancia_maxima']
        
        # 1. Análise de RSI (25 pontos)
        if rsi < 30:
            score += 25
            reasons.append("RSI em oversold extremo - oportunidade")
        elif rsi < 40:
            score += 20
            reasons.append("RSI oversold - entrada favorável")
        elif rsi > 70:
            score -= 10
            alerts.append("⚠️ RSI em overbought")
        
        # 2. Desconto vs máxima do período (25 pontos)
        if distancia_maxima < -60:
            score += 25
            reasons.append("MEGA DESCONTO: 60%+ abaixo da máxima")
        elif distancia_maxima < -40:
            score += 20
            reasons.append("Grande desconto: 40%+ abaixo da máxima")
        elif distancia_maxima < -20:
            score += 15
            reasons.append("Desconto interessante")
        
        # 3. Volume e interesse (20 pontos)
        if volume_ratio > 2.0:
            score += 20
            reasons.append("Volume explosivo - alto interesse")
        elif volume_ratio > 1.5:
            score += 15
            reasons.append("Volume acima da média")
        elif volume_ratio < 0.5:
            score -= 10
            alerts.append("⚠️ Volume baixo")
        
        # 4. Tendência técnica (15 pontos)
        tendencia = indicators['tendencia_ma']
        if "FORTE ALTA" in tendencia:
            score += 15
            reasons.append("Tendência de alta confirmada")
        elif "ALTA" in tendencia:
            score += 10
            reasons.append("Tendência positiva")
        elif "FORTE BAIXA" in tendencia:
            score -= 15
            alerts.append("⚠️ Tendência de baixa forte")
        
        # 5. MACD (10 pontos)
        if indicators['macd_line'] > indicators['macd_signal']:
            score += 10
            reasons.append("MACD positivo")
        
        # 6. Preço baixo (bônus)
        if preco < 1.00:
            score += 10
            reasons.append("💎 Preço muito baixo - potencial multiplicador")
        elif preco < 2.00:
            score += 5
            reasons.append("Preço baixo")
        
        # Penalizações
        if data['volume_financeiro'] < 30000:
            score -= 20
            alerts.append("🚨 Liquidez muito baixa")
        
        if volatilidade > 100:
            alerts.append("⚠️ Volatilidade extrema")
        
        # Classificação de risco
        final_score = max(0, min(100, score))
        
        if final_score >= 80:
            nivel_risco = "🟢 BAIXO"
        elif final_score >= 65:
            nivel_risco = "🟡 MÉDIO"
        elif final_score >= 45:
            nivel_risco = "🟠 ALTO"
        else:
            nivel_risco = "🔴 MUITO ALTO"
        
        return final_score, nivel_risco, reasons[:3], alerts
    
    def calculate_targets(self, data: Dict, indicators: Dict, score: float) -> Tuple[float, float, float]:
        """🎯 Calcula alvos de preço"""
        preco_atual = data['preco_atual']
        
        # Entrada conservadora (5% abaixo do atual)
        entrada = preco_atual * 0.95
        
        # Alvos baseados no score e preço atual
        if score >= 80:
            mult_conservador = 3.0
            mult_agressivo = 6.0
        elif score >= 65:
            mult_conservador = 2.5
            mult_agressivo = 4.5
        elif score >= 50:
            mult_conservador = 2.0
            mult_agressivo = 3.5
        else:
            mult_conservador = 1.5
            mult_agressivo = 2.5
        
        alvo_conservador = preco_atual * mult_conservador
        alvo_agressivo = preco_atual * mult_agressivo
        
        return entrada, alvo_conservador, alvo_agressivo
    
    def analyze_stock(self, ticker: str) -> StockAnalysis:
        """🔍 Análise completa de uma ação"""
        data = self.get_stock_data(ticker)
        if not data:
            return None
        
        indicators = self.calculate_technical_indicators(data['hist_data'])
        score, risco, reasons, alerts = self.calculate_opportunity_score(data, indicators)
        entrada, alvo_cons, alvo_agr = self.calculate_targets(data, indicators, score)
        
        # Score de liquidez
        vol_fin = data['volume_financeiro']
        if vol_fin > 500000:
            liquidez = 10
        elif vol_fin > 200000:
            liquidez = 8
        elif vol_fin > 100000:
            liquidez = 6
        elif vol_fin > 50000:
            liquidez = 4
        else:
            liquidez = 2
        
        return StockAnalysis(
            ticker=ticker,
            nome=data['nome'],
            preco_atual=data['preco_atual'],
            rsi=indicators['rsi'],
            volume_medio=data['volume_medio'],
            volatilidade=indicators['volatilidade'],
            tendencia_ma=indicators['tendencia_ma'],
            liquidez_score=liquidez,
            potencial_score=score,
            nivel_risco=risco,
            entrada_sugerida=entrada,
            alvo_conservador=alvo_cons,
            alvo_agressivo=alvo_agr,
            razao_entrada="; ".join(reasons) if reasons else "Análise técnica",
            alertas=alerts,
            desconto_maxima=indicators['distancia_maxima'],
            setor=data['setor']
        )
    
    def scan_opportunities(self, min_score=40, max_workers=10):
        """🚀 Escaneia oportunidades"""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ticker = {
                executor.submit(self.analyze_stock, ticker): ticker 
                for ticker in self.stocks_b3
            }
            
            for future in concurrent.futures.as_completed(future_to_ticker):
                try:
                    analysis = future.result()
                    if analysis and analysis.potencial_score >= min_score:
                        results.append(analysis)
                except:
                    continue
        
        return sorted(results, key=lambda x: x.potencial_score, reverse=True)

def create_opportunity_chart(analyses):
    """📊 Cria gráfico de oportunidades"""
    if not analyses:
        return None
    
    df = pd.DataFrame([{
        'Ticker': a.ticker,
        'Score': a.potencial_score,
        'Preço': a.preco_atual,
        'Desconto': abs(a.desconto_maxima),
        'Volatilidade': a.volatilidade,
        'Setor': a.setor,
        'Potencial': f"{a.alvo_agressivo/a.preco_atual:.1f}x"
    } for a in analyses])
    
    fig = px.scatter(
        df, 
        x='Desconto', 
        y='Score', 
        size='Preço',
        color='Setor',
        hover_data=['Ticker', 'Potencial'],
        title="🗺️ Mapa de Oportunidades - Score vs Desconto",
        labels={'Desconto': 'Desconto da Máxima (%)', 'Score': 'Score de Oportunidade'}
    )
    
    return fig

def main():
    """🚀 Interface principal Streamlit"""
    st.title("🚀 Penny Stocks B3 Hunter")
    st.subheader("💎 Descobrindo Oportunidades de Baixo Preço no Mercado Brasileiro")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        price_range = st.selectbox(
            "📊 Faixa de Preço:",
            ["flexible", "penny", "low"],
            format_func=lambda x: {
                "penny": "Penny Stocks (R$0,10 - R$2,00)",
                "low": "Low Price (R$0,50 - R$5,00)", 
                "flexible": "Flexível (R$0,10 - R$10,00)"
            }[x]
        )
        
        min_score = st.slider("🎯 Score Mínimo:", 0, 100, 40, 5)
        
        st.info("💡 Scores mais altos = melhores oportunidades")
        st.warning("⚠️ Sempre faça sua própria análise!")
    
    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["🔍 Scanner", "📊 Análise Individual", "📚 Educacional"])
    
    with tab1:
        st.header("🔍 Scanner de Oportunidades")
        
        if st.button("🚀 EXECUTAR SCANNER", type="primary"):
            with st.spinner("🤖 Analisando ações brasileiras..."):
                hunter = BrazilianStockHunter(price_range)
                opportunities = hunter.scan_opportunities(min_score)
            
            if opportunities:
                st.success(f"🎉 Encontradas {len(opportunities)} oportunidades!")
                
                # Métricas principais
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🎯 Total", len(opportunities))
                col2.metric("📊 Score Médio", f"{np.mean([o.potencial_score for o in opportunities]):.1f}")
                col3.metric("💰 Preço Médio", f"R$ {np.mean([o.preco_atual for o in opportunities]):.2f}")
                col4.metric("🏆 Melhor Score", f"{opportunities[0].potencial_score:.0f}/100")
                
                # Gráfico
                chart = create_opportunity_chart(opportunities)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
                
                # Tabela de resultados
                st.subheader("🏆 Top Oportunidades")
                
                results_data = []
                for opp in opportunities[:15]:
                    mult_agr = opp.alvo_agressivo / opp.preco_atual
                    
                    results_data.append({
                        "Ticker": opp.ticker,
                        "Preço": f"R$ {opp.preco_atual:.2f}",
                        "Score": f"{opp.potencial_score:.0f}/100",
                        "Alvo": f"R$ {opp.alvo_agressivo:.2f} ({mult_agr:.1f}x)",
                        "Risco": opp.nivel_risco,
                        "Desconto": f"{abs(opp.desconto_maxima):.1f}%",
                        "Razão": opp.razao_entrada[:50] + "..."
                    })
                
                df_results = pd.DataFrame(results_data)
                st.dataframe(df_results, use_container_width=True, hide_index=True)
                
                # Análise detalhada do top 3
                st.subheader("🔍 Análise Detalhada - Top 3")
                
                for i, opp in enumerate(opportunities[:3], 1):
                    with st.expander(f"#{i} - {opp.ticker} | Score: {opp.potencial_score:.0f}/100"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**💰 Preço Atual:** R$ {opp.preco_atual:.2f}")
                            st.write(f"**🎯 Entrada até:** R$ {opp.entrada_sugerida:.2f}")
                            st.write(f"**📈 Alvo Conservador:** R$ {opp.alvo_conservador:.2f}")
                            st.write(f"**🚀 Alvo Agressivo:** R$ {opp.alvo_agressivo:.2f}")
                            st.write(f"**🎪 Setor:** {opp.setor}")
                        
                        with col2:
                            st.write(f"**📊 RSI:** {opp.rsi:.1f}")
                            st.write(f"**📈 Tendência:** {opp.tendencia_ma}")
                            st.write(f"**⚡ Volatilidade:** {opp.volatilidade:.1f}%")
                            st.write(f"**💧 Liquidez:** {opp.liquidez_score}/10")
                            st.write(f"**🔴 Desconto:** {abs(opp.desconto_maxima):.1f}%")
                        
                        st.info(f"💡 **Razão:** {opp.razao_entrada}")
                        
                        if opp.alertas:
                            st.warning(f"⚠️ **Alertas:** {'; '.join(opp.alertas)}")
            
            else:
                st.warning("❌ Nenhuma oportunidade encontrada com os critérios atuais.")
                st.info("💡 Tente ajustar a faixa de preço ou score mínimo.")
    
    with tab2:
        st.header("📊 Análise Individual")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            ticker_input = st.text_input(
                "Digite o ticker:",
                placeholder="Ex: MGLU3.SA, OIBR3.SA, GOLL4.SA"
            )
        
        with col2:
            analyze_btn = st.button("🔍 ANALISAR", type="primary")
        
        if analyze_btn and ticker_input:
            ticker = ticker_input.upper().strip()
            if not ticker.endswith('.SA'):
                ticker += '.SA'
            
            with st.spinner(f"🤖 Analisando {ticker}..."):
                hunter = BrazilianStockHunter("flexible")
                analysis = hunter.analyze_stock(ticker)
            
            if analysis:
                st.success(f"✅ Análise de {analysis.ticker}")
                
                # Métricas principais
                col1, col2, col3, col4 = st.columns(4)
                
                mult_agr = analysis.alvo_agressivo / analysis.preco_atual
                
                col1.metric("💰 Preço", f"R$ {analysis.preco_atual:.2f}")
                col2.metric("🎯 Score", f"{analysis.potencial_score:.0f}/100")
                col3.metric("🚀 Potencial", f"{mult_agr:.1f}x")
                col4.metric("⚠️ Risco", analysis.nivel_risco.split()[1])
                
                # Recomendação principal
                if analysis.potencial_score >= 80:
                    st.success(f"## 🚀 RECOMENDAÇÃO: OPORTUNIDADE EXCEPCIONAL")
                elif analysis.potencial_score >= 65:
                    st.success(f"## ✅ RECOMENDAÇÃO: BOA OPORTUNIDADE")
                elif analysis.potencial_score >= 50:
                    st.warning(f"## 🟡 RECOMENDAÇÃO: OPORTUNIDADE MODERADA")
                else:
                    st.error(f"## ⚠️ RECOMENDAÇÃO: ALTO RISCO")
                
                # Análise detalhada
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Dados Técnicos")
                    st.write(f"**RSI:** {analysis.rsi:.1f}")
                    st.write(f"**Tendência:** {analysis.tendencia_ma}")
                    st.write(f"**Volatilidade:** {analysis.volatilidade:.1f}%")
                    st.write(f"**Volume Médio:** {analysis.volume_medio:,}")
                    st.write(f"**Liquidez:** {analysis.liquidez_score}/10")
                
                with col2:
                    st.subheader("🎯 Estratégia")
                    st.write(f"**Entrada até:** R$ {analysis.entrada_sugerida:.2f}")
                    st.write(f"**Alvo Conservador:** R$ {analysis.alvo_conservador:.2f}")
                    st.write(f"**Alvo Agressivo:** R$ {analysis.alvo_agressivo:.2f}")
                    st.write(f"**Desconto:** {abs(analysis.desconto_maxima):.1f}%")
                    st.write(f"**Setor:** {analysis.setor}")
                
                st.info(f"💡 **Razão de Entrada:** {analysis.razao_entrada}")
                
                if analysis.alertas:
                    st.warning(f"⚠️ **Alertas:** {'; '.join(analysis.alertas)}")
            
            else:
                st.error(f"❌ Não foi possível analisar {ticker}")
    
    with tab3:
        st.header("📚 Guia Educacional")
        
        st.markdown("""
        ### 🎯 Como Interpretar os Scores
        
        **🚀 80-100:** Oportunidade excepcional com múltiplos fatores positivos
        **✅ 65-79:** Boa oportunidade com fundamentos sólidos
        **🟡 50-64:** Oportunidade moderada, requer análise adicional
        **⚠️ 40-49:** Alto risco, apenas para investidores experientes
        **❌ 0-39:** Evitar no momento atual
        
        ### 📊 Componentes do Score
        
        - **RSI Oversold (25pts):** Condições de sobrevenda técnica
        - **Desconto vs Máxima (25pts):** Distância da máxima histórica
        - **Volume (20pts):** Interesse e liquidez do mercado
        - **Tendência (15pts):** Direção das médias móveis
        - **MACD (10pts):** Momentum positivo
        - **Preço Baixo (5-10pts):** Bônus por potencial multiplicador
        
        ### 💡 Estratégias Recomendadas
        
        **🛡️ Conservador:**
        - Foque em scores 70+
        - Diversifique em 5-8 ações
        - Use stop loss de 15%
        - Alvos conservadores
        
        **⚖️ Moderado:**
        - Scores 60+ aceitáveis
        - 3-5 ações diferentes
        - Stop loss de 20%
        - Mix de alvos conservadores e agressivos
        
        **🚀 Agressivo:**
        - Scores 50+ para maior seleção
        - Posições concentradas
        - Stop loss de 25%
        - Foco nos alvos agressivos
        
        ### ⚠️ Gestão de Risco
        
        1. **Nunca invista tudo** em uma única ação
        2. **Use stop loss** sempre
        3. **Diversifique setores** diferentes
        4. **Reavalie mensalmente** suas posições
        5. **Mantenha reserva** para oportunidades
        
        ### 🎪 Setores Promissores Atuais
        
        - **Telecomunicações:** Recuperação pós-crise
        - **Varejo:** Adaptação digital
        - **Educação:** Transformação do setor
        - **Logística:** E-commerce em crescimento
        - **Construção:** Ciclo de recuperação
        
        ---
        
        **⚠️ AVISO LEGAL:** Este sistema é uma ferramenta educacional de análise técnica.
        Não constitui recomendação de investimento. Sempre consulte profissionais
        qualificados e faça sua própria pesquisa antes de investir.
        """)
        
        # FAQ
        with st.expander("❓ Perguntas Frequentes"):
            st.markdown("""
            **Q: Por que não encontro penny stocks "clássicas" (abaixo de R$2)?**
            A: O mercado brasileiro atual tem poucas ações nessa faixa com boa liquidez. 
            Use a opção "Flexível" para encontrar mais oportunidades.
            
            **Q: Os dados são atualizados?**
            A: Sim, obtemos dados em tempo real do Yahoo Finance.
            
            **Q: Posso confiar 100% nos scores?**
            A: Não. Use como ferramenta de triagem, mas sempre faça análise adicional.
            
            **Q: Com que frequência devo executar o scanner?**
            A: Recomendamos semanalmente ou quando há mudanças significativas no mercado.
            
            **Q: E se uma ação não aparecer no scanner?**
            A: Use a análise individual para verificar ações específicas.
            """)

if __name__ == "__main__":
    # Interface Streamlit
    main()
    
    # Rodapé
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("🚀 **Penny Stocks B3 Hunter**")
    with col2:
        st.write("💎 **Desenvolvido para o mercado brasileiro**")
    with col3:
        st.write(f"📅 **{datetime.now().strftime('%d/%m/%Y')}**")
    
    # Versão para linha de comando
    st.sidebar.markdown("---")
    if st.sidebar.button("💻 Executar via Terminal"):
        st.sidebar.code("""
# Para usar via terminal:
python penny_stocks_analyzer_v2.py

# Ou análise individual:
from penny_stocks_analyzer_v2 import BrazilianStockHunter
hunter = BrazilianStockHunter('flexible')
analysis = hunter.analyze_stock('MGLU3.SA')
print(analysis)
        """)

# Função para uso em linha de comando
def command_line_analysis():
    """🖥️ Versão para linha de comando"""
    print("🚀 PENNY STOCKS B3 HUNTER - Versão Terminal")
    print("=" * 50)
    
    try:
        hunter = BrazilianStockHunter('flexible')
        print("🔍 Executando scanner...")
        
        opportunities = hunter.scan_opportunities(min_score=45)
        
        if opportunities:
            print(f"\n🎉 Encontradas {len(opportunities)} oportunidades!\n")
            
            print("🏆 TOP 10 OPORTUNIDADES:")
            print("-" * 50)
            
            for i, opp in enumerate(opportunities[:10], 1):
                mult = opp.alvo_agressivo / opp.preco_atual
                print(f"{i:2d}. {opp.ticker:10} | R$ {opp.preco_atual:6.2f} | Score: {opp.potencial_score:5.1f}/100")
                print(f"    🎯 Alvo: R$ {opp.alvo_agressivo:6.2f} ({mult:.1f}x) | {opp.nivel_risco}")
                print(f"    💡 {opp.razao_entrada[:60]}...")
                print()
        else:
            print("❌ Nenhuma oportunidade encontrada.")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

# Executar se chamado diretamente
if __name__ == "__main__" and len(__import__('sys').argv) > 1 and __import__('sys').argv[1] == '--cli':
    command_line_analysis()