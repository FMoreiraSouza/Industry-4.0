@echo off
setlocal ENABLEDELAYEDEXPANSION
title "DB-CONFIGURING EXECUTION"
echo Running DB configuration script...
echo ------------------------------------------------------
call .\venv\Scripts\activate.bat
call python .\run_migrations.py
call .\venv\Scripts\deactivate.bat
echo Job finished...
echo Press a key to exit...
pause >nul