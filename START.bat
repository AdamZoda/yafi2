@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM  🚀 YAFI - The Ultimate One-Click Launcher
REM  Double-click and the entire system starts automatically!
REM ════════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion
cd /d "%~dp0"

cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                            ║
echo ║                    🚀 YAFI - Ultimate One-Click Start                     ║
echo ║                                                                            ║
echo ║                     Ollama + Backend + Ngrok Launcher                     ║
echo ║                                                                            ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo ⏳ Initialisation du système YAFI...
echo.

REM ════════════════════════════════════════════════════════════════════════════
REM CHECK REQUIREMENTS
REM ════════════════════════════════════════════════════════════════════════════

echo [Vérification des prérequis]
echo.

REM Check Ollama
echo   Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama n'est pas installé!
    echo.
    echo 📥 Téléchargez depuis: https://ollama.ai
    echo.
    pause
    exit /b 1
)
echo   ✅ Ollama OK

REM Check Ngrok
echo   Checking Ngrok...
ngrok --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ngrok n'est pas installé!
    echo.
    echo 📥 Téléchargez depuis: https://ngrok.com/download
    echo 💾 Ou: choco install ngrok
    echo.
    pause
    exit /b 1
)
echo   ✅ Ngrok OK

REM Check Python
echo   Checking Python...
<<<<<<< HEAD
=======
set "PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python312;%PATH%"
>>>>>>> 3257fc1 (final)
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé!
    echo.
    echo 📥 Téléchargez depuis: https://python.org
    echo.
    pause
    exit /b 1
)
echo   ✅ Python OK

echo.
echo ════════════════════════════════════════════════════════════════════════════

REM ════════════════════════════════════════════════════════════════════════════
REM LAUNCH SERVICES
REM ════════════════════════════════════════════════════════════════════════════

echo.
echo [Démarrage des services]
echo.

REM Start Ollama (only if not already running)
echo   🤖 Vérification d'Ollama...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Ollama est déjà en cours d'exécution!
) else (
    echo   🤖 Démarrage d'Ollama sur port 11434...
    start "YAFI - Ollama Service" cmd /k "ollama serve"
    timeout /t 12 /nobreak >nul
)

REM Start Backend
echo   🖥️  Démarrage du Backend (Expert System)...
start "YAFI - Backend" cmd /k "cd backend && python server_optimized.py"
REM Start Frontend
echo   🚀 Démarrage du Frontend (Vite)...
start "YAFI - Frontend" cmd /k "npm run dev"
timeout /t 5 /nobreak >nul

REM Start Ngrok
echo   🌐 Démarrage de Ngrok (Tunnel)...
start "YAFI - Ngrok Tunnel" cmd /k "ngrok http 5000"
timeout /t 5 /nobreak >nul

REM ════════════════════════════════════════════════════════════════════════════
REM SUCCESS INFO
REM ════════════════════════════════════════════════════════════════════════════

cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                            ║
echo ║                  ✅ YAFI est maintenant EN LIGNE!                         ║
echo ║                                                                            ║
echo ║                   🎉 Tous les services sont actifs! 🎉                    ║
echo ║                                                                            ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo 🔗 SERVICES ACTIFS:
echo.
echo   Local Backend:        http://localhost:5000
echo   Local Frontend:       http://localhost:5173
echo   Ollama LLM:           http://localhost:11434
echo   Ngrok Tunnel:         Fenêtre "YAFI - Ngrok Tunnel"
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo 📋 PROCHAINES ÉTAPES:
echo.
echo   1️⃣  Allez à la fenêtre "YAFI - Ngrok Tunnel"
echo.
echo   2️⃣  Cherchez la ligne "Forwarding" (elle ressemble à):
echo        Forwarding    https://abcd-1234-efgh-5678.ngrok.io -> localhost:5000
echo.
echo   3️⃣  Copiez l'URL https (https://abcd-1234-efgh-5678.ngrok.io)
echo.
echo   4️⃣  Collez-la dans:.env ou config du frontend Vercel
echo        VITE_PYTHON_API_URL=https://abcd-1234-efgh-5678.ngrok.io
echo.
echo   5️⃣  Rechargez votre application frontend (Ctrl+F5)
echo.
echo   6️⃣  Testez! Posez une question: "C'est quoi l'ENSA ?"
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo 💡 INFOS:
echo.
echo   • Première réponse: 30-60 secondes (normal, le modèle charge)
echo   • Messages suivants: 5-15 secondes
echo   • Les réponses sont générées par Ollama (IA naturelle)
echo   • Les données viennent de votre base de connaissances Prolog + RAG
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo ⏳ IMPORTANT: Laissez toutes les fenêtres ouvertes!
echo.
echo Les fenêtres ne doivent PAS être fermées:
echo   • YAFI - Ollama Service
echo   • YAFI - Backend
echo   • YAFI - Frontend
echo   • YAFI - Ngrok Tunnel
echo.
echo 🛑 Pour arrêter complètement:
echo   1. Fermez les 3 fenêtres
echo   2. Les services s'arrêteront automatiquement
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo ✨ Votre système YAFI avec Ollama est PRÊT! ✨
echo.
echo 🎓 Happy Orienting! (Bonne orientation!)
echo.

timeout /t 10 /nobreak >nul
echo.
echo ℹ️  Cette fenêtre va se fermer automatiquement...
echo.
timeout /t 5 /nobreak >nul
