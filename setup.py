"""
Script de instalação e configuração do Sistema de Análise de Ações
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

class SystemInstaller:
    """Instalador do sistema"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.requirements_file = self.project_dir / "requirements.txt"
        self.db_file = self.project_dir / "stock_analysis.db"
    
    def check_python_version(self):
        """Verifica versão do Python"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8+ é necessário. Versão atual:", f"{version.major}.{version.minor}")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} encontrado")
        return True
    
    def install_requirements(self):
        """Instala dependências"""
        print("📦 Instalando dependências...")
        
        if not self.requirements_file.exists():
            print("❌ Arquivo requirements.txt não encontrado")
            return False
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)
            ])
            print("✅ Dependências instaladas com sucesso")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            return False
    
    def setup_database(self):
        """Configura banco de dados inicial"""
        print("🗄️ Configurando banco de dados...")
        
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            # Tabela de cache de dados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_cache (
                    ticker TEXT PRIMARY KEY,
                    data TEXT,
                    last_updated TIMESTAMP,
                    data_type TEXT DEFAULT 'stock_data'
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
                    fundamentals TEXT,
                    news_sentiment TEXT,
                    risk_assessment TEXT
                )
            ''')
            
            # Tabela de histórico de varreduras
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS screening_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_date TIMESTAMP,
                    total_analyzed INTEGER,
                    opportunities_found INTEGER,
                    filters_used TEXT,
                    results TEXT
                )
            ''')
            
            # Tabela de configurações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_config (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP
                )
            ''')
            
            # Inserir configurações padrão
            default_configs = [
                ('cache_duration_hours', '2'),
                ('max_stocks_per_scan', '100'),
                ('default_min_drawdown', '20'),
                ('default_max_pe', '30'),
                ('default_min_roe', '0.10'),
                ('app_version', '1.0.0')
            ]
            
            for key, value in default_configs:
                cursor.execute('''
                    INSERT OR IGNORE INTO app_config (key, value, updated_at)
                    VALUES (?, ?, datetime('now'))
                ''', (key, value))
            
            conn.commit()
            conn.close()
            
            print("✅ Banco de dados configurado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao configurar banco de dados: {e}")
            return False
    
    def download_models(self):
        """Baixa modelos de ML necessários"""
        print("🤖 Baixando modelos de análise de sentimento...")
        
        try:
            from transformers import pipeline
            
            # Tentar carregar modelo leve
            print("  Carregando modelo de sentimento...")
            pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
            print("✅ Modelo de sentimento carregado")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Aviso: Não foi possível baixar modelos avançados: {e}")
            print("  O sistema funcionará com modelos básicos")
            return True
    
    def create_run_script(self):
        """Cria script de execução"""
        print("📝 Criando script de execução...")
        
        run_script_content = '''#!/usr/bin/env python3
"""
Script de execução do Analisador Global de Ações
"""

import streamlit as st
import subprocess
import sys
import os

# Adicionar diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Executar aplicação Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "main.py",
        "--server.port=8501",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false"
    ])
'''
        
        run_script_path = self.project_dir / "run.py"
        with open(run_script_path, 'w', encoding='utf-8') as f:
            f.write(run_script_content)
        
        # Tornar executável no Unix
        if os.name != 'nt':
            os.chmod(run_script_path, 0o755)
        
        print("✅ Script de execução criado")
        return True
    
    def create_batch_files(self):
        """Cria arquivos batch para Windows"""
        if os.name == 'nt':  # Windows
            print("📝 Criando arquivos batch para Windows...")
            
            # Arquivo de instalação
            install_bat = '''@echo off
echo Instalando Analisador Global de Acoes...
python setup.py install
pause
'''
            
            # Arquivo de execução
            run_bat = '''@echo off
echo Iniciando Analisador Global de Acoes...
python -m streamlit run main.py --server.port=8501 --browser.gatherUsageStats=false
pause
'''
            
            with open(self.project_dir / "install.bat", 'w') as f:
                f.write(install_bat)
            
            with open(self.project_dir / "run.bat", 'w') as f:
                f.write(run_bat)
            
            print("✅ Arquivos batch criados")
    
    def run_installation(self):
        """Executa instalação completa"""
        print("🚀 Iniciando instalação do Analisador Global de Ações")
        print("=" * 60)
        
        steps = [
            ("Verificando versão do Python", self.check_python_version),
            ("Instalando dependências", self.install_requirements),
            ("Configurando banco de dados", self.setup_database),
            ("Baixando modelos de IA", self.download_models),
            ("Criando scripts de execução", self.create_run_script),
            ("Criando arquivos auxiliares", self.create_batch_files)
        ]
        
        failed_steps = []
        
        for step_name, step_function in steps:
            print(f"\n🔄 {step_name}...")
            if not step_function():
                failed_steps.append(step_name)
        
        print("\n" + "=" * 60)
        
        if not failed_steps:
            print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
            print("\nPara executar o sistema:")
            print("  python run.py")
            print("  ou")
            print("  streamlit run main.py")
            print("\nO sistema estará disponível em: http://localhost:8501")
        else:
            print("⚠️ INSTALAÇÃO CONCLUÍDA COM AVISOS")
            print(f"Passos com problemas: {', '.join(failed_steps)}")
            print("O sistema pode funcionar com funcionalidade limitada")
        
        return len(failed_steps) == 0

def main():
    """Função principal de instalação"""
    installer = SystemInstaller()
    
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        installer.run_installation()
    else:
        print("Sistema de Análise Global de Ações")
        print("=" * 40)
        print("Opções:")
        print("  python setup.py install  - Instalar sistema")
        print("  python run.py           - Executar aplicação")

if __name__ == "__main__":
    main()
        