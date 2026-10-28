@echo off
title DSA Simulator - Capstone Interactive Laboratory
echo ==============================================================
echo    DSA Simulator - Interactive Data Structures Laboratory
echo    100%% Python Capstone Edition • Zero Dependencies
echo ==============================================================
echo.
cd /d "%~dp0"
echo Launching native Python Desktop Visualizer...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo An error occurred while launching. Press any key to exit.
    pause >nul
)
