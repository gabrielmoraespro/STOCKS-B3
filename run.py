#!/usr/bin/env python3
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
