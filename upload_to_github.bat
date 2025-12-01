@echo off
cd /d "c:\Users\kashy\OneDrive\Desktop\ai agent"

echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/sintnati/AI-Coding-Coach.git

echo.
echo Staging all files...
git add .

echo.
echo Committing changes...
git commit -m "feat: AI Coding Coach - Multi-Agent System with Gemini 2.0 Flash"

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main --force

echo.
echo Done!
pause
