"""
Analisador de Small Caps com Potencial Explosivo - Versão Robusta
Sistema otimizado para identificar ações de baixo valor com fundamentos sólidos
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import re

# Configuração de logging sem emojis para evitar erros de encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('smallcap_analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

@dataclass
class StockData:
    """Classe simplificada para dados de ações"""
    ticker: str
    preco: float = 0.0
    pl: Optional[float] = None
    pvp: Optional[float] = None
    roe: Optional[float] = None
    margem_liquida: Optional[float] = None
    liquidez_corrente: Optional[float] = None
    divida_liquida_ebitda: Optional[float] = None
    valor_mercado: Optional[float] = None
    setor: str = "N/A"

class FundamentusCollector:
    """Coletor otimizado de dados do Fundamentus"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        self.base_url = "https://www.fundamentus.com.br"
    
    def test_connection(self) -> bool:
        """Testa conexão com o Fundamentus"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            logging.info(f"Teste de conexão: Status {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Erro na conexão: {e}")
            return False
    
    def get_stocks_from_resultado(self) -> List[Dict]:
        """Obtém dados diretamente da página de resultados"""
        try:
            url = f"{self.base_url}/resultado.php"
            logging.info(f"Coletando dados de: {url}")
            
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                logging.error(f"Erro HTTP: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id': 'resultado'})
            
            if not table:
                logging.error("Tabela de resultados não encontrada")
                return []
            
            stocks_data = []
            rows = table.find_all('tr')[1:]  # Skip header
            
            logging.info(f"Processando {len(rows)} ações...")
            
            for i, row in enumerate(rows):
                try:
                    cells = row.find_all('td')
                    if len(cells) < 20:  # Garantir que tem dados suficientes
                        continue
                    
                    # Extrair dados das colunas (baseado na estrutura do Fundamentus)
                    ticker = cells[0].text.strip()
                    cotacao = self._parse_number(cells[1].text)
                    pl = self._parse_number(cells[2].text)
                    pvp = self._parse_number(cells[3].text)
                    psr = self._parse_number(cells[4].text)
                    div_yield = self._parse_number(cells[5].text)
                    pa = self._parse_number(cells[6].text)
                    pcg = self._parse_number(cells[7].text)
                    pebit = self._parse_number(cells[8].text)
                    pacl = self._parse_number(cells[9].text)
                    evebit = self._parse_number(cells[10].text)
                    evebitda = self._parse_number(cells[11].text)
                    mrgebit = self._parse_number(cells[12].text)
                    mrgliq = self._parse_number(cells[13].text)
                    roic = self._parse_number(cells[14].text)
                    roe = self._parse_number(cells[15].text)
                    liqcorr = self._parse_number(cells[16].text)
                    divbr_patrim = self._parse_number(cells[17].text)
                    cresc_rec = self._parse_number(cells[18].text)
                    
                    # Filtrar apenas ações com preço baixo inicialmente
                    if cotacao and 0.01 <= cotacao <= 5.0:
                        stock = StockData(
                            ticker=ticker,
                            preco=cotacao,
                            pl=pl,
                            pvp=pvp,
                            roe=roe,
                            margem_liquida=mrgliq,
                            liquidez_corrente=liqcorr,
                            divida_liquida_ebitda=evebitda
                        )
                        stocks_data.append(stock)
                        
                        if len(stocks_data) <= 10:  # Log primeiras 10
                            logging.info(f"Coletado {ticker}: R$ {cotacao:.2f}")
                
                except Exception as e:
                    logging.warning(f"Erro ao processar linha {i}: {e}")
                    continue
            
            logging.info(f"COLETADAS {len(stocks_data)} ACOES NA FAIXA DE PRECO DESEJADA")
            return stocks_data
            
        except Exception as e:
            logging.error(f"Erro ao coletar dados: {e}")
            return []
    
    def _parse_number(self, text: str) -> Optional[float]:
        """Parse robusto e otimizado de números"""
        if not text or text.strip() in ['-', 'N/A', '', '0', '0,00']:
            return None
        
        try:
            # Remove espaços e caracteres especiais
            clean_text = text.strip().replace('.', '').replace(',', '.')
            
            # Remove caracteres não numéricos exceto ponto, vírgula e sinal negativo
            clean_text = re.sub(r'[^\d.,-]', '', clean_text)
            
            # Trata porcentagem
            if text.strip().endswith('%'):
                clean_text = clean_text.replace('%', '')
                result = float(clean_text) if clean_text else None
                return result
            
            # Converte para float
            result = float(clean_text) if clean_text else None
            
            # Filtros de sanidade
            if result is not None:
                # Remove valores absurdos
                if abs(result) > 1000000:  # 1 milhão
                    return None
                # Remove valores muito próximos de zero
                if abs(result) < 0.001 and result != 0:
                    return None
            
            return result
            
        except (ValueError, TypeError):
            return None

class SmallCapAnalyzer:
    """Analisador principal otimizado"""
    
    def __init__(self):
        self.collector = FundamentusCollector()
    
    def calculate_potential_score(self, stock: StockData) -> float:
        """Calcula score de potencial (0-100)"""
        score = 0
        
        # Preço baixo (0-25 pontos)
        if stock.preco <= 0.5:
            score += 25
        elif stock.preco <= 1.0:
            score += 20
        elif stock.preco <= 2.0:
            score += 15
        elif stock.preco <= 5.0:
            score += 10
        
        # P/L (0-20 pontos)
        if stock.pl:
            if 0 < stock.pl <= 8:
                score += 20
            elif 8 < stock.pl <= 15:
                score += 15
            elif 15 < stock.pl <= 25:
                score += 10
            elif stock.pl > 0:
                score += 5
        else:
            score += 8  # Sem P/L pode ser oportunidade
        
        # P/VP (0-20 pontos)
        if stock.pvp:
            if stock.pvp <= 0.8:
                score += 20
            elif stock.pvp <= 1.2:
                score += 15
            elif stock.pvp <= 2.0:
                score += 10
            elif stock.pvp <= 3.0:
                score += 5
        else:
            score += 5
        
        # ROE (0-15 pontos)
        if stock.roe:
            if stock.roe >= 15:
                score += 15
            elif stock.roe >= 8:
                score += 12
            elif stock.roe >= 3:
                score += 8
            elif stock.roe >= 0:
                score += 5
        else:
            score += 3
        
        # Margem Líquida (0-10 pontos)
        if stock.margem_liquida:
            if stock.margem_liquida >= 10:
                score += 10
            elif stock.margem_liquida >= 5:
                score += 7
            elif stock.margem_liquida >= 0:
                score += 5
        else:
            score += 2
        
        # Liquidez (0-10 pontos)
        if stock.liquidez_corrente:
            if stock.liquidez_corrente >= 1.5:
                score += 10
            elif stock.liquidez_corrente >= 1.0:
                score += 7
            elif stock.liquidez_corrente >= 0.8:
                score += 5
        else:
            score += 2
        
        return min(score, 100)
    
    def is_potential_candidate(self, stock: StockData) -> bool:
        """Critérios otimizados para ser candidato"""
        # Preço na faixa
        if not (0.01 <= stock.preco <= 5.0):
            return False
        
        # Filtros de qualidade básicos
        if stock.pl and stock.pl < 0:  # P/L negativo muito ruim
            return False
        
        if stock.roe and stock.roe < -50:  # ROE muito negativo
            return False
        
        if stock.pvp and stock.pvp < 0:  # P/VP negativo suspeito
            return False
        
        # Pelo menos alguns dados disponíveis
        data_count = sum([
            stock.pl is not None,
            stock.pvp is not None,
            stock.roe is not None,
            stock.margem_liquida is not None,
            stock.liquidez_corrente is not None
        ])
        
        # Score mínimo
        score = self.calculate_potential_score(stock)
        
        return data_count >= 2 and score >= 35  # Critérios otimizados
    
    def run_analysis(self) -> pd.DataFrame:
        """Executa análise completa"""
        logging.info("INICIANDO ANALISE DE SMALL CAPS...")
        
        # Testar conexão
        if not self.collector.test_connection():
            logging.error("FALHA NA CONEXAO COM FUNDAMENTUS")
            return pd.DataFrame()
        
        # Coletar dados
        stocks_data = self.collector.get_stocks_from_resultado()
        
        if not stocks_data:
            logging.error("NENHUM DADO COLETADO")
            return pd.DataFrame()
        
        # Analisar candidatos
        candidates = []
        
        for stock in stocks_data:
            try:
                if self.is_potential_candidate(stock):
                    score = self.calculate_potential_score(stock)
                    
                    candidates.append({
                        'Ticker': stock.ticker,
                        'Preço': stock.preco,
                        'Score': score,
                        'P/L': stock.pl,
                        'P/VP': stock.pvp,
                        'ROE': stock.roe,
                        'Margem_Líq': stock.margem_liquida,
                        'Liquidez': stock.liquidez_corrente,
                        'Div/EBITDA': stock.divida_liquida_ebitda
                    })
            except Exception as e:
                logging.warning(f"Erro ao analisar {stock.ticker}: {e}")
        
        # Criar DataFrame
        df = pd.DataFrame(candidates)
        
        if not df.empty:
            df = df.sort_values('Score', ascending=False).reset_index(drop=True)
            logging.info(f"ENCONTRADOS {len(df)} CANDIDATOS!")
        else:
            logging.warning("NENHUM CANDIDATO ENCONTRADO COM OS CRITERIOS ATUAIS")
        
        return df
    
    def export_results(self, df: pd.DataFrame):
        """Exporta resultados"""
        if df.empty:
            return
        
        filename = f"small_caps_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Small_Caps', index=False)
            
            # Top 20
            if len(df) >= 20:
                df.head(20).to_excel(writer, sheet_name='Top_20', index=False)
        
        logging.info(f"RESULTADOS SALVOS EM: {filename}")

def main():
    """Função principal otimizada"""
    print("ANALISADOR DE SMALL CAPS - POTENCIAL EXPLOSIVO")
    print("=" * 55)
    
    analyzer = SmallCapAnalyzer()
    results = analyzer.run_analysis()
    
    if not results.empty:
        print(f"\nTOP 15 SMALL CAPS ENCONTRADAS:")
        print("-" * 50)
        
        for i, row in results.head(15).iterrows():
            print(f"{i+1:2d}. {row['Ticker']:6s} | R$ {row['Preço']:6.2f} | Score: {row['Score']:5.1f}")
            
            # Formatação segura para valores que podem ser float ou string
            pl_str = f"{row['P/L']:.1f}" if pd.notna(row['P/L']) else 'N/A'
            pvp_str = f"{row['P/VP']:.2f}" if pd.notna(row['P/VP']) else 'N/A'
            roe_str = f"{row['ROE']:.1f}" if pd.notna(row['ROE']) else 'N/A'
            
            print(f"    P/L: {pl_str:>6s} | P/VP: {pvp_str:>6s} | ROE: {roe_str:>6s}%")
            print()
        
        analyzer.export_results(results)
        print(f"TOTAL DE OPORTUNIDADES: {len(results)}")
        print("ARQUIVO EXCEL GERADO COM SUCESSO!")
        
        # Estatísticas adicionais
        print(f"\nESTATISTICAS:")
        print(f"- Preco medio: R$ {results['Preço'].mean():.2f}")
        print(f"- Score medio: {results['Score'].mean():.1f}")
        print(f"- Acoes abaixo de R$ 1,00: {len(results[results['Preço'] <= 1.0])}")
        print(f"- Acoes com Score > 80: {len(results[results['Score'] > 80])}")
        
    else:
        print("NENHUMA OPORTUNIDADE ENCONTRADA.")
        print("\nSUGESTOES:")
        print("1. Verifique sua conexao com a internet")
        print("2. O Fundamentus pode estar fora do ar")
        print("3. Tente executar novamente em alguns minutos")

if __name__ == "__main__":
    main()