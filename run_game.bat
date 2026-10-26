@echo off
title Cronicas de Brumavalle: La Llama Antigua
cd /d "%~dp0"
echo Iniciando Cronicas de Brumavalle: La Llama Antigua...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error al ejecutar el juego.
    echo Verifica que tengas instaladas las dependencias: pip install -r requirements.txt
    pause
)
