@echo off
echo Iniciando Analisador Global de Acoes...
python -m streamlit run main.py --server.port=8501 --browser.gatherUsageStats=false
pause
