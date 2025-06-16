"""
Funções utilitárias para o sistema de análise de ações
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sqlite3
import logging
from typing import Dict, List, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataValidator:
    """Validador de dados financeiros"""
    
    @staticmethod
    def validate_ticker(ticker: str) -> bool:
        """Valida formato do ticker"""
        if not ticker or not isinstance(ticker, str):
            return False
        
        ticker = ticker.upper().strip()
        
        # Regras básicas de validação
        if len(ticker) < 1 or len(ticker) > 10:
            return False
        
        # Caracteres permitidos
        allowed_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-')
        if not all(c in allowed_chars for c in ticker):
            return False
        
        return True
    
    @staticmethod
    def validate_stock_data(data: Dict) -> bool:
        """Valida integridade dos dados da ação"""
        required_fields = ['current_price', 'ticker', 'last_updated']
        
        if not isinstance(data, dict):
            return False
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validar valores numéricos
        numeric_fields = ['current_price', 'pe_ratio', 'roe', 'debt_to_equity']
        for field in numeric_fields:
            if field in data:
                try:
                    float(data[field])
                except (ValueError, TypeError):
                    logger.warning(f"Campo {field} contém valor inválido: {data[field]}")
        
        return True
    
    @staticmethod
    def clean_financial_data(data: Dict) -> Dict:
        """Limpa e normaliza dados financeiros"""
        cleaned_data = data.copy()
        
        # Campos numéricos que devem ser tratados
        numeric_fields = [
            'current_price', 'pe_ratio', 'pb_ratio', 'roe', 'debt_to_equity',
            'profit_margin', 'revenue_growth', 'dividend_yield', 'market_cap',
            'drawdown', 'volatility'
        ]
        
        for field in numeric_fields:
            if field in cleaned_data:
                try:
                    value = cleaned_data[field]
                    if value is None or pd.isna(value) or np.isinf(value):
                        cleaned_data[field] = 0
                    else:
                        cleaned_data[field] = float(value)
                        
                        # Limitar valores extremos
                        if field == 'pe_ratio' and cleaned_data[field] > 1000:
                            cleaned_data[field] = 0
                        elif field in ['roe', 'profit_margin'] and abs(cleaned_data[field]) > 5:
                            cleaned_data[field] = min(max(cleaned_data[field], -5), 5)
                        
                except (ValueError, TypeError):
                    cleaned_data[field] = 0
        
        return cleaned_data

class MetricsCalculator:
    """Calculadora de métricas financeiras avançadas"""
    
    @staticmethod
    def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calcula o Sharpe Ratio"""
        try:
            if not returns or len(returns) < 2:
                return 0
            
            returns_array = np.array(returns)
            excess_returns = returns_array - risk_free_rate / 252  # Daily risk-free rate
            
            if np.std(excess_returns) == 0:
                return 0
            
            return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
        except:
            return 0
    
    @staticmethod
    def calculate_max_drawdown(prices: List[float]) -> Dict[str, float]:
        """Calcula o máximo drawdown e duração"""
        try:
            if not prices or len(prices) < 2:
                return {'max_drawdown': 0, 'drawdown_duration': 0}
            
            prices_array = np.array(prices)
            peak = np.maximum.accumulate(prices_array)
            drawdown = (prices_array - peak) / peak
            
            max_dd = np.min(drawdown) * 100  # Converter para porcentagem
            
            # Calcular duração do drawdown
            is_drawdown = drawdown < -0.01  # 1% threshold
            dd_periods = 0
            max_dd_periods = 0
            
            for is_dd in is_drawdown:
                if is_dd:
                    dd_periods += 1
                    max_dd_periods = max(max_dd_periods, dd_periods)
                else:
                    dd_periods = 0
            
            return {
                'max_drawdown': abs(max_dd),
                'drawdown_duration': max_dd_periods
            }
        except:
            return {'max_drawdown': 0, 'drawdown_duration': 0}
    
    @staticmethod
    def calculate_volatility_metrics(prices: List[float]) -> Dict[str, float]:
        """Calcula métricas de volatilidade"""
        try:
            if not prices or len(prices) < 2:
                return {'volatility': 0, 'downside_volatility': 0}
            
            returns = np.diff(np.log(prices))
            
            # Volatilidade anualizada
            volatility = np.std(returns) * np.sqrt(252) * 100
            
            # Volatilidade downside (apenas retornos negativos)
            negative_returns = returns[returns < 0]
            downside_vol = np.std(negative_returns) * np.sqrt(252) * 100 if len(negative_returns) > 0 else 0
            
            return {
                'volatility': volatility,
                'downside_volatility': downside_vol
            }
        except:
            return {'volatility': 0, 'downside_volatility': 0}
    
    @staticmethod
    def calculate_momentum_score(prices: List[float], periods: List[int] = [20, 60, 120]) -> float:
        """Calcula score de momentum baseado em múltiplos períodos"""
        try:
            if not prices or len(prices) < max(periods):
                return 0
            
            momentum_scores = []
            
            for period in periods:
                if len(prices) >= period:
                    current_price = prices[-1]
                    past_price = prices[-period]
                    momentum = (current_price - past_price) / past_price
                    momentum_scores.append(momentum)
            
            if not momentum_scores:
                return 0
            
            # Média ponderada (períodos mais recentes têm maior peso)
            weights = [1, 2, 3][:len(momentum_scores)]
            weighted_momentum = np.average(momentum_scores, weights=weights)
            
            return weighted_momentum * 100  # Converter para porcentagem
        
        except:
            return 0

class RiskAnalyzer:
    """Analisador de riscos"""
    
    @staticmethod
    def assess_fundamental_risk(data: Dict) -> Dict[str, Any]:
        """Avalia riscos fundamentalistas"""
        risk_score = 0
        risk_factors = []
        
        # Análise de liquidez (Debt-to-Equity)
        debt_ratio = data.get('debt_to_equity', 0)
        if debt_ratio > 2.0:
            risk_score += 30
            risk_factors.append("Alto endividamento")
        elif debt_ratio > 1.0:
            risk_score += 15
            risk_factors.append("Endividamento moderado")
        
        # Análise de rentabilidade
        roe = data.get('roe', 0)
        if roe < 0:
            risk_score += 25
            risk_factors.append("ROE negativo")
        elif roe < 0.05:
            risk_score += 10
            risk_factors.append("ROE baixo")
        
        # Análise de valorização
        pe_ratio = data.get('pe_ratio', 0)
        if pe_ratio > 50:
            risk_score += 20
            risk_factors.append("P/L muito alto")
        elif pe_ratio > 30:
            risk_score += 10
            risk_factors.append("P/L elevado")
        
        # Análise de margem
        profit_margin = data.get('profit_margin', 0)
        if profit_margin < 0:
            risk_score += 25
            risk_factors.append("Margem negativa")
        elif profit_margin < 0.05:
            risk_score += 10
            risk_factors.append("Margem baixa")
        
        # Classificação do risco
        if risk_score >= 60:
            risk_level = "ALTO"
        elif risk_score >= 30:
            risk_level = "MÉDIO"
        else:
            risk_level = "BAIXO"
        
        return {
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level,
            'risk_factors': risk_factors
        }
    
    @staticmethod
    def assess_market_risk(data: Dict, market_data: Dict = None) -> Dict[str, Any]:
        """Avalia riscos de mercado"""
        risk_factors = []
        market_risk_score = 0
        
        # Volatilidade
        volatility = data.get('volatility', 0)
        if volatility > 50:
            market_risk_score += 25
            risk_factors.append("Alta volatilidade")
        elif volatility > 30:
            market_risk_score += 15
            risk_factors.append("Volatilidade moderada")
        
        # Drawdown atual
        drawdown = abs(data.get('drawdown', 0))
        if drawdown > 60:
            market_risk_score += 30
            risk_factors.append("Drawdown severo")
        elif drawdown > 40:
            market_risk_score += 20
            risk_factors.append("Drawdown significativo")
        
        # Setor de risco
        high_risk_sectors = ['Energy', 'Materials', 'Real Estate']
        if data.get('sector') in high_risk_sectors:
            market_risk_score += 10
            risk_factors.append("Setor de alta volatilidade")
        
        return {
            'market_risk_score': min(market_risk_score, 100),
            'risk_factors': risk_factors
        }

class PortfolioOptimizer:
    """Otimizador de portfólio"""
    
    @staticmethod
    def calculate_correlation_matrix(stocks_data: List[Dict]) -> pd.DataFrame:
        """Calcula matriz de correlação entre ativos"""
        try:
            price_data = {}
            
            for stock in stocks_data:
                ticker = stock['ticker']
                hist_data = stock.get('hist_data', [])
                
                if hist_data:
                    prices = [day['Close'] for day in hist_data]
                    if len(prices) > 20:  # Mínimo de dados
                        price_data[ticker] = prices
            
            if len(price_data) < 2:
                return pd.DataFrame()
            
            # Criar DataFrame com preços
            min_length = min(len(prices) for prices in price_data.values())
            aligned_data = {ticker: prices[-min_length:] for ticker, prices in price_data.items()}
            
            df = pd.DataFrame(aligned_data)
            
            # Calcular retornos
            returns = df.pct_change().dropna()
            
            # Matriz de correlação
            correlation_matrix = returns.corr()
            
            return correlation_matrix
        
        except Exception as e:
            logger.error(f"Erro ao calcular matriz de correlação: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def suggest_portfolio_weights(opportunities: List[Dict], max_positions: int = 10) -> Dict[str, float]:
        """Sugere pesos para portfólio baseado em scores"""
        try:
            if not opportunities:
                return {}
            
            # Selecionar melhores oportunidades
            top_opportunities = sorted(opportunities, key=lambda x: x.get('score', 0), reverse=True)[:max_positions]
            
            # Calcular pesos baseados em score e risco
            weights = {}
            total_adjusted_score = 0
            
            for opp in top_opportunities:
                score = opp.get('score', 0)
                # Ajustar score baseado em risco (penalizar alto P/L e baixo ROE)
                pe_ratio = opp.get('pe_ratio', 0)
                roe = opp.get('roe', 0)
                
                risk_adjustment = 1.0
                if pe_ratio > 25:
                    risk_adjustment *= 0.8
                if roe < 0.10:
                    risk_adjustment *= 0.9
                
                adjusted_score = score * risk_adjustment
                total_adjusted_score += adjusted_score
                weights[opp['ticker']] = adjusted_score
            
            # Normalizar pesos
            if total_adjusted_score > 0:
                for ticker in weights:
                    weights[ticker] = weights[ticker] / total_adjusted_score
            
            return weights
        
        except Exception as e:
            logger.error(f"Erro ao calcular pesos do portfólio: {e}")
            return {}

class ReportGenerator:
    """Gerador de relatórios"""
    
    @staticmethod
    def generate_stock_report(analysis: Dict) -> str:
        """Gera relatório detalhado de uma ação"""
        if not analysis:
            return "Dados insuficientes para gerar relatório."
        
        data = analysis.get('data', {})
        ticker = data.get('ticker', 'N/A')
        recommendation = analysis.get('recommendation', 'N/A')
        score = analysis.get('score', 0)
        
        report = f"""
=== RELATÓRIO DE ANÁLISE: {ticker} ===

RECOMENDAÇÃO: {recommendation}
SCORE DE OPORTUNIDADE: {score:.0f}/100

DADOS FUNDAMENTAIS:
• Preço Atual: ${data.get('current_price', 0):.2f}
• Drawdown: {data.get('drawdown', 0):.1f}%
• P/L: {data.get('pe_ratio', 0):.1f}
• ROE: {data.get('roe', 0)*100:.1f}%
• Dívida/Patrimônio: {data.get('debt_to_equity', 0):.1f}
• Margem de Lucro: {data.get('profit_margin', 0)*100:.1f}%
• Dividend Yield: {data.get('dividend_yield', 0)*100:.1f}%

SETOR: {data.get('sector', 'N/A')}
INDÚSTRIA: {data.get('industry', 'N/A')}

SENTIMENTO DAS NOTÍCIAS: {analysis.get('news', {}).get('sentiment_trend', 'Neutro')}
"""
        
        return report
    
    @staticmethod
    def generate_screening_report(opportunities: List[Dict]) -> str:
        """Gera relatório de varredura global"""
        if not opportunities:
            return "Nenhuma oportunidade encontrada nos critérios especificados."
        
        report = f"""
=== RELATÓRIO DE VARREDURA GLOBAL ===

TOTAL DE OPORTUNIDADES ENCONTRADAS: {len(opportunities)}

TOP 10 OPORTUNIDADES:
"""
        
        for i, opp in enumerate(opportunities[:10], 1):
            report += f"""
{i}. {opp['ticker']} ({opp['region']})
   Score: {opp['score']:.0f} | {opp['recommendation']}
   Drawdown: {opp['drawdown']:.1f}% | P/L: {opp['pe_ratio']:.1f} | ROE: {opp['roe']:.1f}%
   Setor: {opp['sector']}
"""
        
        # Estatísticas por região
        regions = {}
        for opp in opportunities:
            region = opp['region']
            regions[region] = regions.get(region, 0) + 1
        
        report += "\nDISTRIBUIÇÃO POR REGIÃO:\n"
        for region, count in regions.items():
            report += f"• {region}: {count} oportunidades\n"
        
        return report

def format_currency(value: float, currency: str = "USD") -> str:
    """Formata valores monetários"""
    if currency == "USD":
        return f"${value:,.2f}"
    elif currency == "BRL":
        return f"R$ {value:,.2f}"
    else:
        return f"{value:,.2f}"

def format_percentage(value: float) -> str:
    """Formata porcentagens"""
    return f"{value:.1f}%"

def calculate_business_days(start_date: datetime, end_date: datetime) -> int:
    """Calcula dias úteis entre duas datas"""
    business_days = 0
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.weekday() < 5:  # 0-4 são seg-sex
            business_days += 1
        current_date += timedelta(days=1)
    
    return business_days