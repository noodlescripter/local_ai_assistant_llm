@echo off
echo Starting voice assistant...

:: Check if virtual environment exists
if not exist "%~dp0.venv" (
    echo Creating virtual environment...
    python -m venv "%~dp0.venv"
)

:: Activate virtual environment
call "%~dp0.venv\Scripts\activate"

:: Check if requirements are installed
echo Installing/Updating requirements...
pip install -r "%~dp0requirements.txt"

:: Run the assistant
echo Starting the assistant...
python "%~dp0assistant.py"
