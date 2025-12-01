@echo off
REM GitHub Push Helper Script for AI Coding Coach

echo =====================================
echo  AI Coding Coach - GitHub Uploader
echo =====================================
echo.

REM Stage all changes
echo [1/5] Staging files...
git add .
if %errorlevel% neq 0 (
    echo ERROR: Failed to stage files
    pause
    exit /b 1
)
echo ✓ Files staged successfully
echo.

REM Commit changes
echo [2/5] Committing changes...
git commit -m "feat: Add AI Coding Coach - Multi-Agent System with comprehensive documentation"
if %errorlevel% neq 0 (
    echo NOTE: No changes to commit or commit failed
    echo.
)
echo.

REM Check if remote exists
echo [3/5] Checking remote configuration...
git remote -v | findstr origin >nul
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  No remote 'origin' found!
    echo.
    echo Please enter your GitHub repository URL:
    echo Example: https://github.com/YOUR_USERNAME/ai-coding-coach.git
    echo.
    set /p REPO_URL="Repository URL: "

    echo.
    echo Adding remote origin...
    git remote add origin !REPO_URL!
    if %errorlevel% neq 0 (
        echo ERROR: Failed to add remote
        pause
        exit /b 1
    )
    echo ✓ Remote added successfully
) else (
    echo ✓ Remote 'origin' already configured
    git remote -v
)
echo.

REM Check current branch
echo [4/5] Checking branch...
for /f "tokens=2" %%i in ('git branch --show-current') do set BRANCH=%%i
git branch --show-current >nul 2>&1
if %errorlevel% neq 0 (
    REM Try alternative method
    for /f "tokens=*" %%i in ('git rev-parse --abbrev-ref HEAD') do set BRANCH=%%i
)
echo Current branch: %BRANCH%
echo.

REM Push to GitHub
echo [5/5] Pushing to GitHub...
echo.
echo ⚠️  You may be prompted for GitHub credentials:
echo - Username: your GitHub username
echo - Password: Personal Access Token (NOT your GitHub password)
echo.
echo To create a Personal Access Token:
echo   1. Go to GitHub Settings ^> Developer settings ^> Personal access tokens
echo   2. Generate new token with 'repo' scope
echo   3. Use that token as password
echo.
pause

git push -u origin %BRANCH%
if %errorlevel% neq 0 (
    echo.
    echo ❌ Push failed!
    echo.
    echo Common solutions:
    echo 1. Check your internet connection
    echo 2. Verify repository URL: git remote -v
    echo 3. Ensure you have correct permissions
    echo 4. Try: git pull origin %BRANCH% --rebase
    echo    Then run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ SUCCESS! Your project is now on GitHub!
echo.
echo View your repository at:
git remote get-url origin
echo.
echo Next steps:
echo - Add topics to your repository
echo - Update README with badges
echo - Share with the community!
echo.
pause
