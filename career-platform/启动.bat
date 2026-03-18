@echo off
chcp 65001 >nul
echo ================================================
echo          大学生职业规划与实习对接平台
echo                  职引未来
echo ================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.x
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [检查] Python 已安装
echo.

REM 检查依赖是否安装
echo [检查] 正在检查依赖...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装 Flask 依赖...
    pip install flask flask-cors
    echo [完成] 依赖安装完成
) else (
    echo [检查] 依赖已安装
)
echo.

echo ================================================
echo 正在启动服务器...
echo.
echo 访问地址：http://127.0.0.1:5000
echo 后台管理：http://127.0.0.1:5000/admin
echo.
echo 测试账号:
echo   学生：student1 / 123456
echo   企业：hr1 / 123456
echo   管理：admin / 123456
echo ================================================
echo.

REM 启动应用
python app.py

pause
