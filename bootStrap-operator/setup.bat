@echo off
setlocal enabledelayedexpansion

:: Set MySQL credentials
set "DB_NAME=bootstrap_db"
set "DB_USER=root"
set "DB_PASSWORD=NewSecurePassword123"
set "DB_HOST=127.0.0.1"

:: Check if MySQL is installed
where mysql >nul 2>nul
if %errorlevel% neq 0 (
    echo MySQL is not installed. Please install MySQL and try again.
    exit /b
)

:: Step 1: Create MySQL Database
echo Setting up MySQL database...
mysql -u %DB_USER% -p %DB_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS %DB_NAME%;"

:: Step 2: Create Virtual Environment
echo Creating virtual environment...
python -m venv venv

:: Step 3: Activate Virtual Environment and Install Dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

:: Step 4: Run the FastAPI Application
echo Starting the FastAPI Bootstrap Operator...
uvicorn app.main:app --reload
