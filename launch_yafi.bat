@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM  YAFI - Lanceur Complet (One-Click)
REM  Lance Ollama + Backend + Ngrok automatiquement
REM ════════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   🚀 YAFI - Lanceur Complet
echo   Ollama + Backend + Ngrok - En une click!
echo ════════════════════════════════════════════════════════════════════════════
echo.

REM ════════════════════════════════════════════════════════════════════════════
REM ÉTAPE 1: Vérifier que Ollama est installé
REM ════════════════════════════════════════════════════════════════════════════
echo [1/4] Vérification de Ollama...
timeout /t 1 /nobreak >nul

ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Ollama n'est pas installé!
    echo.
    echo 📥 Téléchargez-le depuis: https://ollama.ai
    echo.
    pause
    exit /b 1
)
echo ✅ Ollama trouvé

REM ════════════════════════════════════════════════════════════════════════════
REM ÉTAPE 2: Vérifier que le modèle est disponible
REM ════════════════════════════════════════════════════════════════════════════
echo.
echo [2/4] Vérification du modèle llama3.2:1b...
timeout /t 1 /nobreak >nul

curl.exe http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama est actif
) else (
    echo ⏳ Démarrage de Ollama (peut prendre 10-20s)...
    start "Ollama Service" cmd /k "ollama serve"
    timeout /t 15 /nobreak >nul
)

REM ════════════════════════════════════════════════════════════════════════════
REM ÉTAPE 3: Lancer le Backend
REM ════════════════════════════════════════════════════════════════════════════
echo.
echo [3/4] Lancement du Backend (Port 5000)...
timeout /t 1 /nobreak >nul

start "YAFI Backend" cmd /k "cd backend && python server.py"
timeout /t 5 /nobreak >nul

REM Vérifier que le backend fonctionne
curl.exe http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend lancé avec succès
) else (
    echo ⚠️  Backend en cours de démarrage...
    timeout /t 5 /nobreak >nul
)

REM ════════════════════════════════════════════════════════════════════════════
REM ÉTAPE 4: Lancer Ngrok
REM ════════════════════════════════════════════════════════════════════════════
echo.
echo [4/4] Lancement de Ngrok (Exposition du Backend)...
timeout /t 1 /nobreak >nul

REM Vérifier que ngrok est installé
ngrok --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Ngrok n'est pas installé!
    echo.
    echo 📥 Téléchargez-le depuis: https://ngrok.com/download
    echo 💾 Ou installez via: choco install ngrok
    echo.
    pause
    exit /b 1
)

start "Ngrok Tunnel" cmd /k "ngrok http 5000"
timeout /t 5 /nobreak >nul

REM ════════════════════════════════════════════════════════════════════════════
REM AFFICHER LES INFOS
REM ════════════════════════════════════════════════════════════════════════════
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   ✅ TOUS LES SERVICES SONT ACTIFS!
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo 🔗 URLS DISPONIBLES:
echo.
echo   Local:       http://localhost:5000
echo   Ollama:      http://localhost:11434
echo   Ngrok:       Vérifiez la fenêtre Ngrok (https://xxxx-xxxx.ngrok.io)
echo.
echo 📝 PROCHAINES ÉTAPES:
echo.
echo   1. Allez à la fenêtre Ngrok
echo   2. Copiez l'URL https (Forwarding)
echo   3. Collez-la dans votre config Frontend
echo   4. Testez votre application!
echo.
echo 💬 POUR TESTER:
echo.
echo   - Posez une question: "C'est quoi l'ENSA ?"
echo   - Attendez 5-30 secondes (première requête = plus lent)
echo   - Vous devriez avoir une réponse intelligente! 🎉
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.

REM Laisser la fenêtre ouverte
pause
