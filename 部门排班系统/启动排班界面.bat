@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在启动部门排班系统...
python run_gui.py
if errorlevel 1 pause
