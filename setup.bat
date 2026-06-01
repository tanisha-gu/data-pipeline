@echo off
REM Data Pipeline Setup Script for Windows

echo.
echo 🚀 Data Pipeline Setup
echo =====================

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✓ Python found

REM Create virtual environment
echo.
echo 📦 Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo ✓ Virtual environment created and activated

REM Install requirements
echo.
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ✓ Dependencies installed

REM Copy .env file
echo.
echo 📝 Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo ✓ Created .env file (please edit with your MySQL credentials)
) else (
    echo ✓ .env file already exists
)

REM Create required directories
echo.
echo 📁 Creating directories...
if not exist data\raw mkdir data\raw
if not exist output\visualizations mkdir output\visualizations
if not exist logs mkdir logs

echo ✓ Directories created

echo.
echo =====================
echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo 1. Edit .env with your MySQL credentials
echo 2. Place CSV files in data\raw\
echo 3. Run: python main.py
echo.
echo 📚 For more help, see README.md
echo.
pause
