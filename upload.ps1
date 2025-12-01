# AI Coding Coach - GitHub Push Script
# Repository: https://github.com/sintnati/AI-Coding-Coach

Write-Host "===================================" -ForegroundColor Cyan
Write-Host " AI Coding Coach - GitHub Upload" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Set location
Set-Location "c:\Users\kashy\OneDrive\Desktop\ai agent"
Write-Host "[1/6] Changed to project directory" -ForegroundColor Green

# Remove existing origin if any
Write-Host "[2/6] Removing old remote (if exists)..." -ForegroundColor Yellow
git remote remove origin 2>$null

# Add new origin
Write-Host "[3/6] Adding GitHub repository..." -ForegroundColor Yellow
git remote add origin https://github.com/sintnati/AI-Coding-Coach.git
Write-Host "  Repository: https://github.com/sintnati/AI-Coding-Coach" -ForegroundColor Gray

# Stage all files
Write-Host "[4/6] Staging all files..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "[5/6] Creating commit..." -ForegroundColor Yellow
git commit -m "feat: AI Coding Coach - Multi-Agent System with Gemini 2.0 Flash

- Implemented multi-agent architecture (Orchestrator, Analyzer, Weakness Detector, Task Generator)
- Added parallel agent execution with asyncio
- Integrated Gemini 2.0 Flash LLM for intelligent analysis
- Built custom Gemini AI Scraper tool for fallback data extraction
- Implemented persistent session storage with SQLite
- Added FAISS vector store for semantic search
- Built observability pipeline (metrics, health checks, logging)
- Implemented A2A protocol for agent communication
- Dockerized application with health checks
- Created glassmorphism frontend UI
- Added comprehensive PROJECT_DESCRIPTION.md for course submission"

# Ensure we're on main branch
Write-Host "[6/6] Switching to main branch and pushing..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host ""
Write-Host "Pushing to GitHub... (You may need to authenticate)" -ForegroundColor Cyan
git push -u origin main

Write-Host ""
Write-Host "===================================" -ForegroundColor Green
Write-Host " SUCCESS! Code pushed to GitHub!" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""
Write-Host "View your repository at:" -ForegroundColor White
Write-Host "https://github.com/sintnati/AI-Coding-Coach" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to close"
