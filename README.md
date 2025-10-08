# Personal Finance Tracker

A full-stack personal finance management application built with Flask (Python) backend and React (TypeScript) frontend. Track expenses, assets, liabilities, and calculate net worth by month with beautiful charts and analytics.

## Features

### 🎯 Core Features
- **Expense Tracking**: Add, edit, delete expenses with category breakdown
- **Asset Management**: Track various assets (cash, investments, real estate)
- **Liability Management**: Monitor debts, loans, and other liabilities
- **Net Worth Calculation**: Automatic calculation and monthly comparison
- **Templates**: Create reusable templates for recurring entries
- **Analytics Dashboard**: Interactive charts and financial insights

### 📊 Analytics & Reporting
- Monthly net worth trends
- Category-wise expense breakdown
- Asset vs liability comparison
- Interactive charts using Recharts
- Monthly comparison views

### 🔐 Security
- JWT-based authentication
- Password hashing with Werkzeug
- Activity logging for all user actions
- CORS protection

## Tech Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-JWT-Extended**: JWT authentication
- **MySQL/SQLite**: Database (configurable)
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **React Query**: Server state management
- **Tailwind CSS**: Styling
- **Recharts**: Data visualization
- **React Hook Form**: Form handling
- **React Router**: Client-side routing

## Project Structure

```
personal-finance-tracker/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── models.py           # SQLAlchemy models
│   ├── routes.py           # API routes
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts (Auth)
│   │   ├── lib/            # API client and utilities
│   │   ├── types/          # TypeScript type definitions
│   │   └── main.tsx        # React entry point
│   ├── package.json        # Node.js dependencies
│   ├── vite.config.ts      # Vite configuration
│   └── tailwind.config.js  # Tailwind CSS configuration
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL (optional, SQLite used by default in development)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Expenses
- `GET /api/expenses/month/{month}` - Get expenses by month
- `POST /api/expenses` - Create expense
- `PUT /api/expenses/{id}` - Update expense
- `DELETE /api/expenses/{id}` - Delete expense
- `GET /api/expenses/total/{month}` - Get total expenses by month
- `GET /api/expenses/category/{month}` - Get expenses by category

### Assets
- `GET /api/assets/month/{month}` - Get assets by month
- `POST /api/assets` - Create asset
- `PUT /api/assets/{id}` - Update asset
- `DELETE /api/assets/{id}` - Delete asset
- `GET /api/assets/total/{month}` - Get total assets by month

### Liabilities
- `GET /api/liabilities/month/{month}` - Get liabilities by month
- `POST /api/liabilities` - Create liability
- `PUT /api/liabilities/{id}` - Update liability
- `DELETE /api/liabilities/{id}` - Delete liability
- `GET /api/liabilities/total/{month}` - Get total liabilities by month

### Analytics
- `GET /api/networth/{month}` - Get net worth for specific month
- `GET /api/monthly-comparison` - Get monthly comparison data
- `GET /api/available-months` - Get months with data
- `GET /api/month-has-data/{month}` - Check if month has data

### Templates
- `GET /api/templates/expenses` - Get expense templates
- `POST /api/templates/expenses` - Create expense template
- `GET /api/templates/assets` - Get asset templates
- `POST /api/templates/assets` - Create asset template
- `GET /api/templates/liabilities` - Get liability templates
- `POST /api/templates/liabilities` - Create liability template

## Database Schema

### Users
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `created_at`, `updated_at`

### Expenses
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `category`, `description`
- `amount`, `date`, `month`
- `created_at`, `updated_at`

### Assets
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `name`, `category`
- `value`, `month`
- `created_at`, `updated_at`

### Liabilities
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `name`, `category`
- `amount`, `month`
- `created_at`, `updated_at`

### Templates (Expenses, Assets, Liabilities)
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `name`, `category`
- `amount/value`
- `is_recurring`
- `created_at`, `updated_at`

### Activity Log
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `action`, `entity_type`, `entity_id`
- `details`, `timestamp`

## Configuration

### Environment Variables

**Backend (.env)**
```
DATABASE_URL=mysql://username:password@localhost/finance_db
JWT_SECRET_KEY=your-super-secret-jwt-key
FLASK_ENV=development
```

**Frontend**
```
VITE_API_BASE_URL=http://localhost:5000
```

### Database Configuration

The application supports both SQLite (development) and MySQL (production):

- **Development**: Uses SQLite by default (`finance_dev.db`)
- **Production**: Requires MySQL connection string in `DATABASE_URL`

## Development

### Backend Development
- Models are defined in `models.py` using SQLAlchemy
- API routes are in `routes.py` with proper error handling
- All user actions are logged in `activity_log` table
- JWT authentication protects all endpoints except auth routes

### Frontend Development
- TypeScript for type safety
- React Query for server state management
- Tailwind CSS for consistent styling
- Responsive design for mobile and desktop
- Form validation with React Hook Form

### Adding New Features
1. **Backend**: Add model → Add routes → Update API client
2. **Frontend**: Add types → Create components → Add pages

## Deployment

### Backend Deployment
1. Set environment variables for production
2. Configure MySQL database
3. Set `FLASK_ENV=production`
4. Use a WSGI server like Gunicorn

### Frontend Deployment
1. Build the application: `npm run build`
2. Serve the `dist` folder with a web server
3. Configure API base URL for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Built with ❤️ using Flask + React**
