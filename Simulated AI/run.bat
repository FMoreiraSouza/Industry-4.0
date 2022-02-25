@echo off
:: Activating the virtual environment
CALL .\venv\Scripts\activate.bat
:: Starting the script
start "IA_FALSA" python .\main.py
:: Deactivating the virtual environment
CALL .\venv\Scripts\deactivate.bat