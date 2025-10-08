# 🚀 Quick Start Guide - Personal Finance Tracker

## ⚡ TL;DR - Get Started in 3 Commands

```bash
# 1. Test everything works
python run_tests.py

# 2. Start both servers
python start_dev.py

# 3. Open your browser
# Go to: http://localhost:3000
```

## 📋 What You Get

✅ **Complete Full-Stack Application**
- 🐍 Flask backend with REST API
- ⚛️ React frontend with TypeScript
- 🎨 Beautiful UI with Tailwind CSS
- 📊 Interactive charts with Recharts
- 🔐 JWT authentication
- 💾 SQLite database (auto-created)

✅ **Core Features**
- 💰 Expense tracking with categories
- 🏦 Asset management
- 💳 Liability tracking
- 📈 Net worth calculation
- 📊 Monthly comparisons
- 📝 Reusable templates
- 📱 Responsive design

## 🎯 Step-by-Step Setup

### Prerequisites
- Python 3.8+ 
- Node.js 16+ and npm

### Option 1: Automated Setup (Recommended)
```bash
# Run comprehensive tests and setup
python run_tests.py

# If all tests pass, start the application
python start_dev.py
```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python app.py
```

#### Frontend Setup (New Terminal)
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Docs**: Check the routes in `backend/routes.py`

## 🧪 Testing

### Test Everything
```bash
python run_tests.py
```

### Test Backend Only
```bash
python test_backend.py
```

### Test Frontend Only
```bash
python test_frontend.py
```

## 🎮 Using the Application

### 1. Create Account
- Go to http://localhost:3000
- Click "create a new account"
- Fill in username, email, password
- Click "Create account"

### 2. Add Your First Expense
- Navigate to "Expenses" page
- Click "Add Expense"
- Fill in category, description, amount, date
- Click "Add Expense"

### 3. Add Assets & Liabilities
- Go to "Assets" page to add savings, investments, etc.
- Go to "Liabilities" page to add debts, loans, etc.
- View your net worth on the Dashboard

### 4. Create Templates
- Go to "Templates" page
- Create reusable templates for recurring entries
- Use templates to quickly add common expenses/assets/liabilities

### 5. View Analytics
- Dashboard shows net worth trends
- Monthly comparisons
- Category breakdowns
- Interactive charts

## 🔧 Configuration

### Environment Variables

**Backend** (`.env` in backend folder):
```
DATABASE_URL=sqlite:///finance_dev.db
JWT_SECRET_KEY=your-secret-key
FLASK_ENV=development
```

**Frontend** (`.env` in frontend folder):
```
VITE_API_BASE_URL=http://localhost:5000
```

## 📁 Project Structure

```
personal-finance-tracker/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── routes.py           # API endpoints
│   ├── extensions.py       # Flask extensions
│   ├── config.py           # Configuration
│   └── requirements.txt    # Python dependencies
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   ├── lib/            # API client
│   │   └── types/          # TypeScript types
│   ├── package.json        # Node dependencies
│   └── vite.config.ts      # Vite configuration
├── start_dev.py           # Start both servers
├── run_tests.py           # Run all tests
├── test_backend.py        # Backend tests
├── test_frontend.py       # Frontend tests
├── SETUP_GUIDE.md         # Detailed setup guide
└── README.md              # Full documentation
```

## 🚨 Troubleshooting

### Backend Issues
- **Import errors**: Activate virtual environment and install requirements
- **Port 5000 in use**: Kill existing process or change port in config
- **Database errors**: Delete `finance_dev.db` and restart

### Frontend Issues
- **npm errors**: Delete `node_modules`, run `npm install`
- **Build errors**: Check Node.js version (16+ required)
- **API connection**: Ensure backend is running on port 5000

### Common Solutions
```bash
# Reset backend
cd backend
rm finance_dev.db
python app.py

# Reset frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev

# Check ports
netstat -ano | findstr :3000
netstat -ano | findstr :5000
```

## 🎉 Success Indicators

✅ **Backend Working**:
- Console shows "Backend server starting..."
- Can access http://localhost:5000/api/auth/login
- Database file `finance_dev.db` is created

✅ **Frontend Working**:
- Console shows "Local: http://localhost:3000/"
- Browser shows login/register page
- No console errors in browser DevTools

✅ **Integration Working**:
- Can register new user
- Can login successfully
- Dashboard loads with charts
- Can add expenses/assets/liabilities

## 📞 Need Help?

1. **Read the detailed guide**: `SETUP_GUIDE.md`
2. **Check test results**: `python run_tests.py`
3. **Verify setup**: Follow troubleshooting steps above
4. **Check logs**: Look at console output for errors

---

**🎊 Enjoy tracking your finances with style!** 

Your personal finance tracker is now ready to help you manage your money, track your net worth, and achieve your financial goals!
