@echo off
chcp 65001
echo ============================================
echo    锌锭库管理系统 - 启动脚本
echo ============================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo [信息] 首次运行，正在创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo [信息] 正在检查并安装依赖...
pip install -r requirements.txt -q

echo.
echo [信息] 正在启动服务器...
echo ============================================
echo.

REM 启动Flask服务
python app.py

pause

