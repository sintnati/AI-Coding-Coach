// API Configuration
const API_BASE_URL = 'http://localhost:8080';

// DOM Elements
const analyzeForm = document.getElementById('analyzeForm');
const analyzeBtn = document.getElementById('analyzeBtn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const metricsGrid = document.getElementById('metricsGrid');
const platformStats = document.getElementById('platformStats');
const analysisContent = document.getElementById('analysisContent');
const tasksList = document.getElementById('tasksList');
const errorMessage = document.getElementById('errorMessage');

// Form Submit Handler
analyzeForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const userId = document.getElementById('userId').value.trim();
    const codeforcesHandle = document.getElementById('codeforcesHandle').value.trim();
    const leetcodeHandle = document.getElementById('leetcodeHandle').value.trim();


    if (!userId) {
        showError('Please enter a User ID');
        return;
    }

    // Check if at least one platform is provided
    if (!codeforcesHandle && !leetcodeHandle) {
        showError('Please enter at least one platform handle');
        return;
    }

    // Prepare request data
    const requestData = {
        user_id: userId,
        handles: {}
    };

    if (codeforcesHandle) requestData.handles.codeforces = codeforcesHandle;
    if (leetcodeHandle) requestData.handles.leetcode = leetcodeHandle;


    // Show loading state
    setLoading(true);
    hideError();
    hideResults();

    try {
        // Add timeout to fetch
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout

        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server error: ${response.status}`);
        }

        const data = await response.json();

        if (data.status === 'failed') {
            throw new Error(data.error || 'Analysis failed');
        }

        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        if (error.name === 'AbortError') {
            showError('Analysis timed out. The server is taking too long to respond.');
        } else {
            showError(error.message || 'Failed to analyze. Please check if the server is running.');
        }
    } finally {
        setLoading(false);
    }
});

// Set Loading State
function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Display Results
function displayResults(data) {
    const analysis = data.analysis || {};
    const growthMetrics = data.growth_metrics || analysis.growth_metrics || {};

    // Display growth metrics
    displayGrowthMetrics(growthMetrics);

    // Display platform stats
    displayPlatformStats(growthMetrics.platform_stats || {});

    // Display AI analysis - handle nested structure from AnalyzerAgent
    let analysisData = analysis;
    if (analysis.analysis) {
        analysisData = analysis.analysis;
    }

    if (analysisData) {
        let analysisHtml = '';

        // Try to parse if it's a JSON string
        if (typeof analysisData === 'string') {
            try {
                const parsed = JSON.parse(analysisData);
                analysisData = parsed;
            } catch (e) {
                // If not JSON, treat as plain text
                analysisHtml = `<p>${escapeHtml(analysisData)}</p>`;
            }
        }

        // Handle structured object
        if (typeof analysisData === 'object' && analysisData !== null) {
            if (analysisData.skill_level) {
                analysisHtml += `
                    <div class="analysis-item">
                        <strong><i class="fas fa-star"></i> Skill Level:</strong>
                        <span class="skill-badge skill-${analysisData.skill_level.toLowerCase()}">${escapeHtml(analysisData.skill_level)}</span>
                    </div>
                `;
            }
            if (analysisData.languages && Array.isArray(analysisData.languages)) {
                analysisHtml += `
                    <div class="analysis-item">
                        <strong><i class="fas fa-code"></i> Primary Languages:</strong>
                        <div class="tag-list">
                            ${analysisData.languages.map(lang => `<span class="tag">${escapeHtml(lang)}</span>`).join('')}
                        </div>
                    </div>
                `;
            }
            if (analysisData.patterns) {
                const patterns = Array.isArray(analysisData.patterns) ? analysisData.patterns : [analysisData.patterns];
                analysisHtml += `
                    <div class="analysis-item">
                        <strong><i class="fas fa-chart-line"></i> Coding Patterns:</strong>
                        <ul class="pattern-list">
                            ${patterns.map(p => `<li>${escapeHtml(p)}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            if (analysisData.platform_preference) {
                analysisHtml += `
                    <div class="analysis-item">
                        <strong><i class="fas fa-heart"></i> Platform Preference:</strong>
                        <span>${escapeHtml(analysisData.platform_preference)}</span>
                    </div>
                `;
            }
            // If it's just a string in the object
            if (analysisData.summary || analysisData.analysis) {
                analysisHtml += `<div class="analysis-item"><p>${escapeHtml(analysisData.summary || analysisData.analysis)}</p></div>`;
            }
        }

        // Fallback if empty
        if (!analysisHtml && Object.keys(analysisData).length > 0) {
            analysisHtml = `<pre class="json-preview">${escapeHtml(JSON.stringify(analysisData, null, 2))}</pre>`;
        }

        analysisContent.innerHTML = analysisHtml || '<p class="no-data">No analysis available</p>';
    } else {
        analysisContent.innerHTML = '<p class="no-data">No analysis available</p>';
    }

    // Display Weaknesses - handle nested structure from WeaknessDetectorAgent
    const weaknessesData = data.weaknesses || {};
    const weaknessContent = document.getElementById('weaknessContent');
    const weaknessSection = document.getElementById('weaknessSection');

    if (weaknessContent && weaknessSection) {
        // Extract weaknesses from nested structure
        let weaknesses = weaknessesData.weaknesses || weaknessesData;

        // Try to parse if it's a JSON string
        if (typeof weaknesses === 'string') {
            try {
                weaknesses = JSON.parse(weaknesses);
            } catch (e) {
                // If not JSON, show as raw
                weaknessContent.innerHTML = `<p>${escapeHtml(weaknesses)}</p>`;
                weaknessSection.style.display = 'block';
                return;
            }
        }

        let weaknessHtml = '';

        if (weaknesses.weak_topics && Array.isArray(weaknesses.weak_topics) && weaknesses.weak_topics.length > 0) {
            weaknessHtml += `
                <div class="weakness-item">
                    <strong><i class="fas fa-exclamation-circle"></i> Weak Topics:</strong>
                    <div class="tag-list weakness-tags">
                        ${weaknesses.weak_topics.map(topic => `<span class="tag tag-weak">${escapeHtml(topic)}</span>`).join('')}
                    </div>
                </div>
            `;
        }

        if (weaknesses.missing_fundamentals && Array.isArray(weaknesses.missing_fundamentals) && weaknesses.missing_fundamentals.length > 0) {
            weaknessHtml += `
                <div class="weakness-item">
                    <strong><i class="fas fa-book"></i> Missing Fundamentals:</strong>
                    <ul class="pattern-list">
                        ${weaknesses.missing_fundamentals.map(f => `<li>${escapeHtml(f)}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        if (weaknesses.improvement_priority && Array.isArray(weaknesses.improvement_priority) && weaknesses.improvement_priority.length > 0) {
            weaknessHtml += `
                <div class="weakness-item">
                    <strong><i class="fas fa-arrow-up"></i> Improvement Priorities:</strong>
                    <ul class="pattern-list">
                        ${weaknesses.improvement_priority.map(p => `<li>${escapeHtml(p)}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        // Handle raw response
        if (weaknesses.raw) {
            weaknessHtml += `<div class="weakness-item"><p>${escapeHtml(weaknesses.raw)}</p></div>`;
        }

        weaknessContent.innerHTML = weaknessHtml || '<p class="no-data">No specific weaknesses detected. Great job!</p>';
        weaknessSection.style.display = 'block';
    }

    // Display Agent Insights
    const agentExecution = data.agent_execution || {};
    const agentInsights = document.getElementById('agentInsights');
    if (agentInsights) {
        agentInsights.innerHTML = `
            <div style="display: grid; gap: 0.5rem; font-size: 0.9rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: var(--text-secondary);">Orchestrator:</span>
                    <span style="color: var(--primary);">${escapeHtml(agentExecution.orchestrator || 'Unknown')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: var(--text-secondary);">Execution Mode:</span>
                    <span style="color: var(--text-primary);">${escapeHtml(agentExecution.execution_mode || 'Sequential')}</span>
                </div>
                <div style="margin-top: 0.5rem;">
                    <span style="color: var(--text-secondary);">Active Agents:</span>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.25rem;">
                        ${(agentExecution.agents_used || []).map(agent => `<span style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc; padding: 0.1rem 0.5rem; border-radius: 0.5rem; font-size: 0.8rem;">${escapeHtml(agent)}</span>`).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    // Display tasks
    const tasks = data.tasks || [];
    if (tasks.length > 0) {
        tasksList.innerHTML = tasks.map(task => `
            <div class="task-item">
                <div class="task-info">
                    <div class="task-title">${escapeHtml(task.title || 'Untitled Task')}</div>
                    <div class="task-meta">
                        ${task.topic ? `<span style="margin-right: 10px;"><i class="fas fa-tag"></i> ${escapeHtml(task.topic)}</span>` : ''}
                        ${task.difficulty ? `<span><i class="fas fa-layer-group"></i> ${escapeHtml(task.difficulty)}</span>` : ''}
                    </div>
                    ${task.reason || task.reasoning ? `<div class="task-reason">"${escapeHtml(task.reason || task.reasoning)}"</div>` : ''}
                </div>
                <div class="task-status">
                    ${task.due_days ? `${task.due_days} days` : 'Flexible'}
                </div>
            </div>
        `).join('');
    } else {
        tasksList.innerHTML = '<p style="color: var(--text-secondary);">No specific tasks recommended at this time.</p>';
    }

    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display Growth Metrics
function displayGrowthMetrics(metrics) {
    const metricsHTML = `
        <div class="metric-card">
            <div class="metric-value">${metrics.total_platforms || 0}</div>
            <div class="metric-label">Platforms</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${metrics.days_active || 0}</div>
            <div class="metric-label">Days Active</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${metrics.avg_problems_per_day || 0}</div>
            <div class="metric-label">Avg/Day</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${metrics.streak?.current || 0}</div>
            <div class="metric-label">Current Streak</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${metrics.streak?.longest || 0}</div>
            <div class="metric-label">Longest Streak</div>
        </div>
    `;

    metricsGrid.innerHTML = metricsHTML;
}

// Display Platform Stats
function displayPlatformStats(stats) {
    const platformHTML = Object.entries(stats).map(([platform, data]) => `
        <div class="platform-card">
            <div class="platform-name">
                <i class="fas fa-code"></i> ${platform.toUpperCase()}
            </div>
            <div class="platform-data">
                <div class="stat-row">
                    <span class="stat-label">Total Solved</span>
                    <span class="stat-val">${data.solved || 0}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Total Submissions</span>
                    <span class="stat-val">${data.total || 0}</span>
                </div>
                ${data.languages && data.languages.length > 0 ? `
                <div class="stat-row" style="margin-top: 0.5rem; display: block;">
                    <span class="stat-label" style="display: block; margin-bottom: 0.25rem; font-size: 0.8rem;">Languages</span>
                    <span class="stat-val" style="font-size: 0.9rem;">${data.languages.join(', ')}</span>
                </div>
                ` : ''}
            </div>
        </div>
    `).join('');

    platformStats.innerHTML = platformHTML || '<p style="color: var(--text-secondary);">No platform data available</p>';
}

// Show Error
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Hide Error
function hideError() {
    errorSection.style.display = 'none';
}

// Hide Results
function hideResults() {
    resultsSection.style.display = 'none';
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    if (typeof text !== 'string') return text;
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Check server status on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            console.warn('Server might not be running');
        }
    } catch (error) {
        console.warn('Could not connect to server. Make sure it is running on', API_BASE_URL);
    }
});
