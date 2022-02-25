@echo off
setlocal ENABLEDELAYEDEXPANSION
title "FAKE-AI INSTALLER"
echo Setup a virtual environment...
echo ------------------------------------------------------
call py -m pip install virtualenv
call py -m virtualenv venv
echo ------------------------------------------------------
echo Activating the virtual environment...
call .\venv\Scripts\activate.bat
echo Installing dependencies...
call pip install -r .\requirements.txt
call .\venv\Scripts\deactivate.bat
echo ------------------------------------------------------
echo Job finished...
echo Press a key to exit...
pause >nul