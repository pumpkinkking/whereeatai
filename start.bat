@echo off
REM WhereEatAI 启动脚本 (Windows)

echo ======================================
echo   WhereEatAI 智能旅游推荐系统
echo ======================================
echo.

REM 检查Python版本
echo 检查Python版本...
python --version
echo.

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo.
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo.
echo 检查并安装依赖...
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

REM 检查.env文件
if not exist ".env" (
    echo.
    echo 警告: .env文件不存在
    echo 正在复制.env.example到.env...
    copy .env.example .env
    echo.
    echo 请编辑.env文件并填入你的API_KEY
    echo 编辑完成后重新运行此脚本
    pause
    exit /b 1
)

REM 检查API_KEY
findstr /C:"your_siliconflow_api_key" .env >nul
if %errorlevel% equ 0 (
    echo.
    echo 警告: 请在.env文件中配置API_KEY
    echo 编辑.env文件并将your_siliconflow_api_key替换为实际的API密钥
    pause
    exit /b 1
) else (
    echo.
    echo ✓ API配置已完成
)

REM 创建日志目录
if not exist "logs" mkdir logs

echo.
echo ======================================
echo   启动服务...
echo ======================================
echo.

REM 启动应用
python main.py

pause
