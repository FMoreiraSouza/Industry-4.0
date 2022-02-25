@echo off
TITLE OPC COLLECTOR
CALL .\venv\Scripts\activate.bat
CALL python .\run_collector.py
ECHO Press Enter to exit...
pause >nul