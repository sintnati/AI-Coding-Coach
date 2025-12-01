# 🚀 Push to GitHub - Quick 3-Step Guide

## Step 1: Create GitHub Repository (2 minutes)

1. **Login to GitHub**: Go to https://github.com/login
2. **Create New Repo**: Click here → https://github.com/new
3. **Fill in**:
   - Repository name: `ai-coding-coach`
   - Description: `Multi-Agent AI System for Competitive Programming Analysis`
   - Visibility: **Public** (or Private)
   - **IMPORTANT**: Do NOT check "Add a README file"
4. Click **"Create repository"**
5. **Copy the repository URL** shown (looks like: `https://github.com/YOUR_USERNAME/ai-coding-coach.git`)

## Step 2: Run These Commands

Open PowerShell or Command Prompt in your project directory and run:

```bash
cd "c:\Users\kashy\OneDrive\Desktop\ai agent"

# Add all files
git add .

# Commit
git commit -m "feat: AI Coding Coach - Multi-Agent System"

# Add your GitHub repo (REPLACE with your actual URL from Step 1)
git remote add origin https://github.com/YOUR_USERNAME/ai-coding-coach.git

# Push to GitHub
git push -u origin main
```

If it says "branch 'main' does not exist", try:
```bash
git branch -M main
git push -u origin main
```

## Step 3: Enter GitHub Credentials When Prompted

- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (NOT your password!)

### How to Get Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "AI Coding Coach Upload"
4. Select scope: Check **"repo"**
5. Click "Generate token"
6. **COPY the token immediately** (you only see it once!)
7. Use this token as your password when git asks

---

## ✅ That's It!

Your project will be on GitHub. View it at:
`https://github.com/YOUR_USERNAME/ai-coding-coach`

---

## 🆘 Having Issues?

### Authentication Failed?
Use GitHub CLI instead:
```bash
# Install GitHub CLI from: https://cli.github.com/
gh auth login
gh repo create ai-coding-coach --public --source=. --push
```

### Already exists?
```bash
git remote remove origin
# Then add it again with the correct URL
```
