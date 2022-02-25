@echo off
setlocal ENABLEDELAYEDEXPANSION
title "OPC-COLLECTOR INSTALLER"
echo Setup a virtual environment...
echo ------------------------------------------------------
echo Checking if need python version is installed...

:: Store python versions
set /a count=1
for /F "tokens=* USEBACKQ" %%F in (`py --list`) do (
  set version!count!=%%F
  set /a count=!count!+1
)
:: Find if requested python is installed
set /a count=!count!-1
set /a found=0
for /L %%G in (1,1,!count!) do (
  echo !version%%G! | findstr "^-3.8-3" >nul
  if !errorlevel!==0 (
    set /a found=1
    set py_version=!version%%G!
  )
)

:: Kill the installation if python not found
if !found!==0 (
  echo Python 3.8.3 not found
  echo ------------------------------------------------------
  exit /b 1
) else (
  echo Python 3.8.3 found
)
echo ------------------------------------------------------
echo Creating the virtual environment...
call py !py_version! -m pip install --no-index --find-links=dependencies virtualenv
call py !py_version! -m virtualenv venv
echo ------------------------------------------------------
echo Activating the virtual environment...
call .\venv\Scripts\activate.bat
echo Installing dependencies...
call pip install --no-index --find-links=dependencies -r .\requirements.txt
call .\venv\Scripts\deactivate.bat
echo ------------------------------------------------------
echo Job finished...
echo Press a key to exit...
pause >nul