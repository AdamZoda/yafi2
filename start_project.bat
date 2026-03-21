@echo off
echo Démarrage de YAFI - Assistant d'Orientation...
echo.

echo [1/2] Lancement du Backend (Python + RAG)...
start "YAFI Backend" cmd /k "cd backend && python server.py"

echo [2/2] Lancement du Frontend (React)...
start "YAFI Frontend" cmd /k "npm run dev"

echo.
echo ✅ Le projet est en cours de démarrage !
echo - Backend sur http://localhost:5000 (attendre "Vector Knowledge Base initialized")
echo - Frontend sur http://localhost:5173
echo.
pause
