@echo off
echo.
echo  =============================================
echo     FRAUDGUARD - CAMEROON FRAUD DETECTION
echo  =============================================
echo.

:: Check if .venv exists
if not exist ".venv" (
    echo [1/5] Creating virtual environment...
    python -m venv .venv
)

:: Activate venv
call .venv\Scripts\activate

:: Upgrade pip
echo.
echo [2/5] Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo.
echo [3/5] Installing requirements...
pip install -r requirements.txt

:: Apply migrations
echo.
echo [4/5] Running database migrations...
python manage.py migrate

:: Collect static
echo.
echo [5/5] Collecting static files...
python manage.py collectstatic --noinput

:: Start server
echo.
echo  Server starting at http://localhost:8000
echo  Press CTRL+C to stop.
echo.
daphne -b 0.0.0.0 -p 8000 fraudguard.asgi:application