const API_BASE = 'http://localhost:5000';
let charts = {};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setCurrentDate();
    loadDashboard();
});

function initializeApp() {
    // Set current date for all date inputs
    const now = new Date();
    const currentDate = now.toISOString().split('T')[0];
    const currentMonth = now.toISOString().slice(0, 7);
    
    document.querySelectorAll('input[type="date"]').forEach(input => {
        input.value = currentDate;
    });
    
    document.querySelectorAll('input[type="month"]').forEach(input => {
        input.value = currentMonth;
    });
}

function setCurrentDate() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('currentDate').textContent = now.toLocaleDateString('en-US', options);
}

// Navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Add active class to clicked nav item
    event.target.closest('.nav-item').classList.add('active');
    
    // Update page title
    const titles = {
        'dashboard': 'Dashboard',
        'expenses': 'Expenses',
        'assets': 'Assets',
        'liabilities': 'Liabilities',
        'loan-calculator': 'Loan Calculator',
        'reports': 'Reports'
    };
    document.getElementById('pageTitle').textContent = titles[sectionId];
    
    // Load section data
    if (sectionId === 'dashboard') loadDashboard();
    if (sectionId === 'expenses') loadExpenses();
    if (sectionId === 'assets') loadAssets();
    if (sectionId === 'liabilities') loadLiabilities();
    if (sectionId === 'reports') loadReports();
}

// Dashboard Functions
async function loadDashboard() {
    try {
        const now = new Date();
        const currentMonth = now.toISOString().slice(0, 7);
        
        // Load net worth
        const netWorthResponse = await fetch(`${API_BASE}/api/networth/${currentMonth}`);
        const netWorthData = await netWorthResponse.json();
        
        // Load expenses
        const expensesResponse = await fetch(`${API_BASE}/api/expenses/total/${currentMonth}`);
        const expensesData = await expensesResponse.json();
        
        // Update stats
        document.getElementById('netWorth').textContent = `$${netWorthData.net_worth.toFixed(2)}`;
        document.getElementById('totalAssets').textContent = `$${netWorthData.total_assets.toFixed(2)}`;
        document.getElementById('totalLiabilities').textContent = `$${netWorthData.total_liabilities.toFixed(2)}`;
        document.getElementById('monthlyExpenses').textContent = `$${expensesData.total.toFixed(2)}`;
        
        // Load charts
        await loadCharts();
        
        // Load financial health
        await loadFinancialHealth();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

async function loadCharts() {
    try {
        // Get data for multiple months
        const months = [];
        const now = new Date();
        for (let i = 5; i >= 0; i--) {
            const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
            months.push(date.toISOString().slice(0, 7));
        }
        
        const monthlyData = [];
        for (const month of months) {
            try {
                const netWorthResponse = await fetch(`${API_BASE}/api/networth/${month}`);
                const netWorthData = await netWorthResponse.json();
                monthlyData.push({
                    month: month,
                    netWorth: netWorthData.net_worth
                });
            } catch (e) {
                monthlyData.push({ month: month, netWorth: 0 });
            }
        }
        
        // Net Worth Chart
        const netWorthCtx = document.getElementById('netWorthChart').getContext('2d');
        if (charts.netWorth) charts.netWorth.destroy();
        
        charts.netWorth = new Chart(netWorthCtx, {
            type: 'line',
            data: {
                labels: monthlyData.map(d => d.month),
                datasets: [{
                    label: 'Net Worth',
                    data: monthlyData.map(d => d.netWorth),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
        
        // Expense Chart
        const currentMonth = new Date().toISOString().slice(0, 7);
        const expensesResponse = await fetch(`${API_BASE}/api/expenses/category/${currentMonth}`);
        const expensesData = await expensesResponse.json();
        
        const expenseCtx = document.getElementById('expenseChart').getContext('2d');
        if (charts.expense) charts.expense.destroy();
        
        charts.expense = new Chart(expenseCtx, {
            type: 'doughnut',
            data: {
                labels: expensesData.map(e => e.category),
                datasets: [{
                    data: expensesData.map(e => e.total),
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#f093fb',
                        '#4facfe',
                        '#43e97b',
                        '#fa709a'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

async function loadFinancialHealth() {
    try {
        const response = await fetch(`${API_BASE}/api/financial-health`);
        const data = await response.json();
        
        const scoreElement = document.querySelector('.score-value');
        const labelElement = document.querySelector('.score-label');
        
        scoreElement.textContent = data.score;
        
        if (data.score >= 80) {
            labelElement.textContent = 'Excellent';
        } else if (data.score >= 60) {
            labelElement.textContent = 'Good';
        } else if (data.score >= 40) {
            labelElement.textContent = 'Fair';
        } else {
            labelElement.textContent = 'Needs Work';
        }
        
        // Display recommendations
        const recommendationsHtml = data.recommendations.map(rec => `
            <div style="padding: 10px; margin: 5px 0; background: #f8fafc; border-left: 3px solid #667eea; border-radius: 5px;">
                ${rec}
            </div>
        `).join('');
        
        document.getElementById('recommendations').innerHTML = recommendationsHtml || '<p>Great job! Keep up the good work!</p>';
        
    } catch (error) {
        console.error('Error loading financial health:', error);
    }
}

// Expenses Functions
async function loadExpenses() {
    try {
        const response = await fetch(`${API_BASE}/api/expenses`);
        const expenses = await response.json();
        
        const tbody = document.getElementById('expensesTableBody');
        tbody.innerHTML = expenses.map(expense => `
            <tr>
                <td>${expense.date}</td>
                <td>${expense.category}</td>
                <td>${expense.description}</td>
                <td style="color: #ef4444; font-weight: bold;">$${expense.amount}</td>
                <td>
                    <button onclick="deleteExpense(${expense.id})" style="background: #ef4444; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Delete</button>
                </td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error loading expenses:', error);
    }
}

async function addExpense(event) {
    event.preventDefault();
    
    const data = {
        category: document.getElementById('expenseCategory').value,
        description: document.getElementById('expenseDescription').value,
        amount: parseFloat(document.getElementById('expenseAmount').value),
        date: document.getElementById('expenseDate').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/expenses`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            closeModal('addExpenseModal');
            loadExpenses();
            loadDashboard();
            alert('✅ Expense added successfully!');
        }
    } catch (error) {
        alert('❌ Error adding expense');
    }
}

async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/admin/delete/expenses/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadExpenses();
            loadDashboard();
        }
    } catch (error) {
        alert('❌ Error deleting expense');
    }
}

// Assets Functions
async function loadAssets() {
    try {
        const response = await fetch(`${API_BASE}/api/assets`);
        const assets = await response.json();
        
        const tbody = document.getElementById('assetsTableBody');
        tbody.innerHTML = assets.map(asset => `
            <tr>
                <td>${asset.name}</td>
                <td>${asset.category}</td>
                <td style="color: #10b981; font-weight: bold;">$${asset.value}</td>
                <td>${asset.month}</td>
                <td>
                    <button onclick="deleteAsset(${asset.id})" style="background: #ef4444; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Delete</button>
                </td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error loading assets:', error);
    }
}

async function addAsset(event) {
    event.preventDefault();
    
    const data = {
        name: document.getElementById('assetName').value,
        category: document.getElementById('assetCategory').value,
        value: parseFloat(document.getElementById('assetValue').value),
        month: document.getElementById('assetMonth').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/assets`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            closeModal('addAssetModal');
            loadAssets();
            loadDashboard();
            alert('✅ Asset added successfully!');
        }
    } catch (error) {
        alert('❌ Error adding asset');
    }
}

async function deleteAsset(id) {
    if (!confirm('Are you sure you want to delete this asset?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/admin/delete/assets/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadAssets();
            loadDashboard();
        }
    } catch (error) {
        alert('❌ Error deleting asset');
    }
}

// Liabilities Functions
async function loadLiabilities() {
    try {
        const response = await fetch(`${API_BASE}/api/liabilities`);
        const liabilities = await response.json();
        
        const tbody = document.getElementById('liabilitiesTableBody');
        tbody.innerHTML = liabilities.map(liability => `
            <tr>
                <td>${liability.name}</td>
                <td>${liability.category}</td>
                <td style="color: #ef4444; font-weight: bold;">$${liability.amount}</td>
                <td>${liability.month}</td>
                <td>
                    <button onclick="deleteLiability(${liability.id})" style="background: #ef4444; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Delete</button>
                </td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error loading liabilities:', error);
    }
}

async function addLiability(event) {
    event.preventDefault();
    
    const data = {
        name: document.getElementById('liabilityName').value,
        category: document.getElementById('liabilityCategory').value,
        amount: parseFloat(document.getElementById('liabilityAmount').value),
        month: document.getElementById('liabilityMonth').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/liabilities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            closeModal('addLiabilityModal');
            loadLiabilities();
            loadDashboard();
            alert('✅ Liability added successfully!');
        }
    } catch (error) {
        alert('❌ Error adding liability');
    }
}

async function deleteLiability(id) {
    if (!confirm('Are you sure you want to delete this liability?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/admin/delete/liabilities/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadLiabilities();
            loadDashboard();
        }
    } catch (error) {
        alert('❌ Error deleting liability');
    }
}

// Loan Calculator
async function calculateLoan(event) {
    event.preventDefault();
    
    const principal = parseFloat(document.getElementById('loanAmount').value);
    const rate = parseFloat(document.getElementById('interestRate').value);
    const years = parseInt(document.getElementById('loanYears').value);
    
    try {
        const response = await fetch(`${API_BASE}/api/loan/calculate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                principal: principal,
                rate: rate,
                months: years * 12
            })
        });
        
        const data = await response.json();
        
        // Display loan details
        document.getElementById('loanDetails').innerHTML = `
            <div style="background: #f8fafc; padding: 20px; border-radius: 10px; margin: 15px 0;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                    <div>
                        <strong style="color: #6b7280;">Monthly Payment</strong><br>
                        <span style="font-size: 1.8rem; color: #3b82f6; font-weight: bold;">$${data.monthly_payment}</span>
                    </div>
                    <div>
                        <strong style="color: #6b7280;">Total Payment</strong><br>
                        <span style="font-size: 1.8rem; color: #ef4444; font-weight: bold;">$${data.total_payment}</span>
                    </div>
                    <div>
                        <strong style="color: #6b7280;">Total Interest</strong><br>
                        <span style="font-size: 1.8rem; color: #f59e0b; font-weight: bold;">$${data.total_interest}</span>
                    </div>
                </div>
            </div>
        `;
        
        // Display smart tips
        const tipsHtml = data.tips.map(tip => `
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; margin: 15px 0; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h4 style="margin-bottom: 10px; font-size: 1.2rem;">${tip.title}</h4>
                <p style="margin-bottom: 10px; opacity: 0.95;">${tip.description}</p>
                ${tip.savings ? `<div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 8px; font-weight: bold;">💰 Potential Savings: $${tip.savings}</div>` : ''}
                ${tip.potential_savings ? `<div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 8px; font-weight: bold;">💰 Potential Savings: $${tip.potential_savings}</div>` : ''}
                ${tip.impact ? `<div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 8px; margin-top: 5px; font-weight: bold;">⚡ Impact: ${tip.impact}</div>` : ''}
            </div>
        `).join('');
        
        document.getElementById('loanTips').innerHTML = tipsHtml;
        
    } catch (error) {
        alert('Error calculating loan. Please check your inputs.');
    }
}

// Reports
async function loadReports() {
    // Implementation for reports
    console.log('Loading reports...');
}

// Modal Functions
function showAddExpenseModal() {
    document.getElementById('addExpenseModal').classList.add('active');
}

function showAddAssetModal() {
    document.getElementById('addAssetModal').classList.add('active');
}

function showAddLiabilityModal() {
    document.getElementById('addLiabilityModal').classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Refresh Data
function refreshData() {
    const activeSection = document.querySelector('.content-section.active').id;
    showSection(activeSection);
}
