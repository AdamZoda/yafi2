@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM  YAFI - Lanceur Principal Interactif
REM  Choisissez votre mode de lancement
REM ════════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion
cd /d "%~dp0"

:menu
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                            ║
echo ║                    🎓 YAFI - ChatBot d'Orientation                        ║
echo ║                  Avec Ollama LLM pour des réponses intelligentes           ║
echo ║                                                                            ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo Sélectionnez votre mode de lancement:
echo.
echo   1️⃣  Lancement Complet (Ollama + Backend + Ngrok)
echo   2️⃣  Backend Seul (Pour tests locaux)
echo   3️⃣  Test Rapide (Sans Ngrok)
echo   4️⃣  Voir le Statut du Système
echo   5️⃣  Configuration & Aide
echo   0️⃣  Quitter
echo.
set /p choice="Votre choix (0-5): "

if "%choice%"=="1" goto :full_launch
if "%choice%"=="2" goto :backend_only
if "%choice%"=="3" goto :quick_test
if "%choice%"=="4" goto :status_check
if "%choice%"=="5" goto :help
if "%choice%"=="0" exit /b 0

echo ❌ Choix invalide!
timeout /t 2 /nobreak >nul
goto :menu

REM ════════════════════════════════════════════════════════════════════════════
REM OPTION 1: LANCEMENT COMPLET
REM ════════════════════════════════════════════════════════════════════════════
:full_launch
cls
echo.
echo 🚀 Lancement Complet: Ollama + Backend + Ngrok
echo ════════════════════════════════════════════════════════════════════════════
echo.

REM Vérifier Ollama
echo [1/4] Vérification de Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama n'est pas installé! Téléchargez-le: https://ollama.ai
    pause
    goto :menu
)
echo ✅ Ollama trouvé

REM Vérifier Ngrok
echo [2/4] Vérification de Ngrok...
ngrok --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ngrok n'est pas installé! Téléchargez-le: https://ngrok.com
    pause
    goto :menu
)
echo ✅ Ngrok trouvé

REM Lancer les services
echo [3/4] Lancement des services...
start "Ollama Service" cmd /k "set OLLAMA_HOST=0.0.0.0:11435 && ollama serve"
timeout /t 8 /nobreak >nul
start "YAFI Backend" cmd /k "cd backend && python server.py"
timeout /t 5 /nobreak >nul

echo [4/4] Lancement de Ngrok...
start "Ngrok Tunnel" cmd /k "ngrok http 5000"
timeout /t 3 /nobreak >nul

cls
echo.
echo ✅ TOUS LES SERVICES SONT LANCÉS!
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo 🔗 Vérifier la fenêtre NGROK pour obtenir l'URL https
echo.
echo 📋 Procédure:
echo   1. Cherchez "Forwarding" dans la fenêtre Ngrok
echo   2. Copiez l'URL https://xxxx-xxxx.ngrok.io
echo   3. Collez-la dans votre frontend ou .env
echo   4. Testez!
echo.
timeout /t 5 /nobreak >nul
goto :menu

REM ════════════════════════════════════════════════════════════════════════════
REM OPTION 2: BACKEND SEUL
REM ════════════════════════════════════════════════════════════════════════════
:backend_only
cls
echo.
echo 🖥️  Lancement du Backend Seul
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo Prérequis:
echo   - Ollama doit être lancé: set OLLAMA_HOST=0.0.0.0:11435 && ollama serve
echo   - Python 3.8+ installé
echo.

echo Lancement du backend...
cd backend
python server.py

pause
goto :menu

REM ════════════════════════════════════════════════════════════════════════════
REM OPTION 3: TEST RAPIDE
REM ════════════════════════════════════════════════════════════════════════════
:quick_test
cls
echo.
echo ⚡ Test Rapide du Système
echo ════════════════════════════════════════════════════════════════════════════
echo.

echo [1/3] Vérification de Ollama...
curl.exe http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama est accessible
) else (
    echo ❌ Ollama n'est pas accessible!
    echo    Lancez: set OLLAMA_HOST=0.0.0.0:11435 && ollama serve
    pause
    goto :menu
)

echo [2/3] Vérification du Backend...
curl.exe http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend est accessible
) else (
    echo ❌ Backend n'est pas accessible!
    echo    Lancez: python backend/server.py (dans un autre terminal)
    pause
    goto :menu
)

echo [3/3] Test de requête...
echo.
echo 🧪 Envoi une requête test au backend...
echo.
cd backend
python -c "import requests; r = requests.post('http://localhost:5000/chat', json={'message': 'Bonjour'}); print('Réponse:', r.json().get('response', 'Pas de réponse'))" 2>nul

echo.
echo ✅ Test rapide terminé!
echo.
pause
goto :menu

REM ════════════════════════════════════════════════════════════════════════════
REM OPTION 4: VÉRIFIER LE STATUT
REM ════════════════════════════════════════════════════════════════════════════
:status_check
cls
echo.
echo 📊 Statut du Système
echo ════════════════════════════════════════════════════════════════════════════
echo.

echo [Ollama]
curl.exe http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama est actif sur http://localhost:11434
) else (
    echo ❌ Ollama n'est pas accessible
)

echo.
echo [Backend]
curl.exe http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend est actif sur http://localhost:5000
) else (
    echo ❌ Backend n'est pas accessible
)

echo.
echo [Ngrok]
ngrok --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ngrok est installé
) else (
    echo ❌ Ngrok n'est pas installé
)

echo.
echo [Python]
python --version
echo.
echo [Fichiers Clés]
if exist "backend/server.py" (
    echo ✅ server.py trouvé
) else (
    echo ❌ server.py manquant
)
if exist "backend/llm_engine.py" (
    echo ✅ llm_engine.py trouvé
) else (
    echo ❌ llm_engine.py manquant
)
if exist ".env" (
    echo ✅ .env trouvé
) else (
    echo ❌ .env manquant
)

echo.
pause
goto :menu

REM ════════════════════════════════════════════════════════════════════════════
REM OPTION 5: AIDE & CONFIGURATION
REM ════════════════════════════════════════════════════════════════════════════
:help
cls
echo.
echo 📚 Aide & Configuration
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo 🔧 INSTALLATION PRÉREQUISES:
echo.
echo   1. Ollama
echo      - Téléchargez: https://ollama.ai
echo      - Vérifiez: ollama --version
echo.
echo   2. Ngrok
echo      - Téléchargez: https://ngrok.com/download
echo      - Ou: choco install ngrok
echo      - Vérifiez: ngrok --version
echo.
echo   3. Python 3.8+
echo      - Téléchargez: https://python.org
echo      - Vérifiez: python --version
echo.
echo ⚙️  CONFIGURATION:
echo.
echo   .env file:
echo      USE_LLM=true
echo      LLM_PROVIDER=ollama
echo      LLM_MODEL=llama3.2:1b
echo      OLLAMA_HOST=http://localhost:11434
echo.
echo 📝 TROUBLESHOOTING:
echo.
echo   Si "Ollama not found":
echo      → Avez-vous suivi l'installation?
echo      → Relancez Ollama: set OLLAMA_HOST=0.0.0.0:11435 && ollama serve
echo.
echo   Si "Backend timeout":
echo      → Premier message est lent (30-60s)
echo      → Vérifiez que Ollama fonctionne
echo.
echo   Si "Ngrok failure":
echo      → Authentifiez: ngrok config add-authtoken TOKEN
echo.
echo ❓ PLUS D'AIDE:
echo.
echo   - Docs: OLLAMA_SETUP.md
echo   - Report: OLLAMA_INTEGRATION_REPORT.md
echo   - Quick: README_OLLAMA.md
echo.
pause
goto :menu
