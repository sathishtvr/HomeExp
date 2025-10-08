# 🚀 Personal Finance Tracker - Complete Setup Guide

This guide will help you set up and test the complete Personal Finance Tracker application.

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- **Git** (optional, for version control)

## 🔧 Step-by-Step Setup

### 1. Backend Setup (Flask API)

#### 1.1 Navigate to Backend Directory
```bash
cd backend
```

#### 1.2 Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 1.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 1.4 Set Up Environment Variables
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env file with your settings (optional for development)
```

#### 1.5 Test Backend Installation
```bash
# Run the Flask application
python app.py
```

**Expected Output:**
```
🚀 Starting Personal Finance Tracker Backend...
📍 Backend URL: http://localhost:5000
✅ Database tables created/verified
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[::1]:5000
```

### 2. Frontend Setup (React App)

#### 2.1 Open New Terminal and Navigate to Frontend
```bash
cd frontend
```

#### 2.2 Install Node.js Dependencies
```bash
npm install
```

#### 2.3 Set Up Environment Variables (Optional)
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env file if needed (default settings should work)
```

#### 2.4 Start Frontend Development Server
```bash
npm run dev
```

**Expected Output:**
```
  VITE v4.4.5  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

## 🧪 Testing the Application

### 3. Backend API Testing

#### 3.1 Test Health Check
Open your browser or use curl:
```bash
curl http://localhost:5000/api/auth/register
```

#### 3.2 Test User Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

#### 3.3 Test User Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 4. Frontend Testing

#### 4.1 Open Application
Navigate to: `http://localhost:3000`

#### 4.2 Test User Registration
1. Click "create a new account"
2. Fill in the registration form
3. Submit and verify you're redirected to dashboard

#### 4.3 Test Core Features
1. **Dashboard**: Check if charts and summary cards load
2. **Expenses**: Add, edit, delete expenses
3. **Assets**: Add, edit, delete assets
4. **Liabilities**: Add, edit, delete liabilities
5. **Templates**: Create and use templates

## 🐛 Troubleshooting

### Common Backend Issues

#### Issue: "ModuleNotFoundError"
**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: "Database connection error"
**Solution:**
- The app uses SQLite by default (no setup needed)
- Check if `finance_dev.db` is created in backend folder

#### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Common Frontend Issues

#### Issue: "npm install fails"
**Solution:**
```bash
# Clear npm cache
npm cache clean --force
# Delete node_modules and reinstall
rmdir /s node_modules
npm install
```

#### Issue: "Module not found errors"
**Solution:**
```bash
# Reinstall dependencies
npm install
# Or install specific missing packages
npm install react react-dom @types/react @types/react-dom
```

#### Issue: "API connection fails"
**Solution:**
- Ensure backend is running on port 5000
- Check CORS settings in backend
- Verify API base URL in frontend config

## 🎯 Quick Start Commands

### Start Both Servers (Recommended)
```bash
# From project root directory
python start_dev.py
```

### Start Backend Only
```bash
python run_backend.py
```

### Start Frontend Only
```bash
python run_frontend.py
```

## 📊 Testing Checklist

### ✅ Backend API Tests
- [ ] User registration works
- [ ] User login works
- [ ] JWT authentication works
- [ ] Expense CRUD operations work
- [ ] Asset CRUD operations work
- [ ] Liability CRUD operations work
- [ ] Net worth calculation works
- [ ] Monthly comparison works
- [ ] Templates work

### ✅ Frontend Tests
- [ ] Registration page loads and works
- [ ] Login page loads and works
- [ ] Dashboard displays correctly
- [ ] Charts render properly
- [ ] Expense tracker works
- [ ] Asset manager works
- [ ] Liability manager works
- [ ] Templates page works
- [ ] Navigation works
- [ ] Responsive design works

### ✅ Integration Tests
- [ ] Frontend can communicate with backend
- [ ] Authentication flow works end-to-end
- [ ] Data persistence works
- [ ] Real-time updates work
- [ ] Error handling works

## 🔐 Security Notes

### Development Environment
- Default JWT secret is for development only
- SQLite database is stored locally
- CORS is enabled for localhost

### Production Deployment
- Change JWT secret key
- Use PostgreSQL/MySQL database
- Configure proper CORS origins
- Use HTTPS
- Set up proper environment variables

## 📱 Features to Test

### Core Functionality
1. **User Management**
   - Registration with validation
   - Login with authentication
   - Session management

2. **Financial Tracking**
   - Add/edit/delete expenses
   - Categorize expenses
   - Track assets and liabilities
   - Calculate net worth

3. **Analytics**
   - Monthly comparisons
   - Category breakdowns
   - Interactive charts
   - Trend analysis

4. **Templates**
   - Create reusable templates
   - Use templates to add entries
   - Recurring template functionality

### UI/UX Features
1. **Responsive Design**
   - Mobile-friendly interface
   - Tablet compatibility
   - Desktop optimization

2. **Interactive Elements**
   - Modal forms
   - Data tables
   - Charts and graphs
   - Navigation

## 🚀 Next Steps

After successful setup and testing:

1. **Customize the Application**
   - Add your own categories
   - Modify the UI theme
   - Add new features

2. **Deploy to Production**
   - Set up a cloud database
   - Deploy backend to Heroku/AWS
   - Deploy frontend to Netlify/Vercel

3. **Enhance Security**
   - Add password strength requirements
   - Implement rate limiting
   - Add input validation

## 💡 Tips for Success

1. **Keep Both Servers Running**
   - Backend on port 5000
   - Frontend on port 3000

2. **Check Browser Console**
   - Look for JavaScript errors
   - Monitor network requests

3. **Monitor Backend Logs**
   - Check for Python errors
   - Verify API requests

4. **Use Browser DevTools**
   - Inspect network requests
   - Debug React components
   - Check local storage

---

**🎉 Congratulations!** You now have a fully functional Personal Finance Tracker application running locally. Start by creating an account and exploring all the features!
