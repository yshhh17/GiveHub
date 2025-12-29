# 💰 Donation App

A FastAPI-based backend application for handling donations through PayPal integration. This project provides a complete REST API for user authentication, donation management, and PayPal sandbox payment processing.

## ✨ Features

- 🔐 **User Authentication** - Register and login with JWT token-based authentication
- 💳 **PayPal Integration** - Complete PayPal sandbox payment flow
- 📝 **Donation Management** - Create, track, and verify donations
- 💾 **Database Tracking** - Store and retrieve donation history
- 📊 **User Analytics** - Track total donations per user
- 🔍 **Payment Verification** - Verify order status with PayPal API

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database with SQLAlchemy ORM
- **PayPal REST API** - Payment processing (Sandbox mode)
- **JWT** - JSON Web Token authentication
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── core/
│   │   ├── config.py              # Configuration and environment variables
│   │   └── security.py            # Authentication and JWT handling
│   ├── db/
│   │   ├── database.py            # Database connection and session
│   │   └── models. py              # SQLAlchemy models (User, Donation)
│   ├── routers/
│   │   ├── users.py               # User registration and login endpoints
│   │   └── donations.py           # Donation and PayPal endpoints
│   ├── schemas/
│   │   ├── user.py                # Pydantic schemas for users
│   │   └── donation.py            # Pydantic schemas for donations
│   └── services/
│       └── paypal_service.py      # PayPal API integration
├── .env                            # Environment variables (not in repo)
├── .gitignore
└── requirements.txt                # Python dependencies
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- PayPal Developer account (for sandbox credentials)

### 1. Clone the Repository

```bash
git clone https://github.com/yshhh17/Donation-App. git
cd Donation-App/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements. txt
```

### 4. Setup Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost: 5432/donation_db

# JWT Configuration
SECRET_KEY=your_super_secret_key_here_change_this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_TIME=30

# PayPal Sandbox Configuration
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=your_paypal_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_paypal_sandbox_client_secret
PAYPAL_API_BASE=https://api-m.sandbox.paypal.com
```

### 5. Setup Database

```bash
# Create database in PostgreSQL
createdb donation_db

# Tables will be created automatically when you run the app
```

## 🔑 PayPal Sandbox Setup

### Get Your Sandbox Credentials

1. Go to [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)
2. Login with your PayPal account
3. Navigate to **"Apps & Credentials"**
4. Make sure you're in **"Sandbox"** mode (toggle at top)
5. Click **"Create App"** or use the default app
6. Copy your **Client ID** and **Secret**
7. Paste them into your `.env` file

### Create Test Accounts

1. Go to **"Testing Tools"** → **"Sandbox accounts"**
2. You'll see auto-generated test accounts (Personal and Business)
3. Click on an account to view credentials
4. Use **PERSONAL** accounts to test payments (they act as donors)
5. Note:  Default balance is usually $5,000 USD

## 🏃‍♂️ Running the Application

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at: 
- **API Base**:  http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication

#### Register User
```http
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example. com",
  "password": "securepassword123"
}
```

#### Login
```http
POST /login
Content-Type:  application/x-www-form-urlencoded

username=john@example.com&password=securepassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.. .",
  "token_type":  "bearer"
}
```

### Donations

#### Create Donation Order
```http
POST /donations/create-order
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "amount": 10
}
```

**Response:**
```json
{
  "order_id": "5O190127TN364715T",
  "status": "CREATED",
  "approval_url": "https://www.sandbox.paypal.com/checkoutnow?token=5O190127TN364715T"
}
```

#### Capture Payment
```http
POST /donations/capture-order
Authorization:  Bearer <your_token>
Content-Type: application/json

{
  "order_id": "5O190127TN364715T"
}
```

#### Get My Donations
```http
GET /donations/my-donations
Authorization: Bearer <your_token>
```

#### Get Specific Donation
```http
GET /donations/{donation_id}
Authorization: Bearer <your_token>
```

#### Verify Order Status
```http
GET /donations/verify/{order_id}
Authorization: Bearer <your_token>
```

## 🔄 Complete Payment Flow

### Step 1: Register & Login
```bash
# Register
POST /users
Body: {"name": "John", "email": "john@example. com", "password": "pass123"}

# Login
POST /login
Body: username=john@example.com&password=pass123
# Save the access_token
```

### Step 2: Create Donation Order
```bash
POST /donations/create-order
Authorization: Bearer <token>
Body: {"amount": 10}
# Copy the approval_url from response
```

### Step 3: Approve Payment
1. Open the `approval_url` in your browser
2. Login with PayPal sandbox **PERSONAL** account (from Developer Dashboard)
3. Click **"Pay Now"** to approve
4. (Page may show loading - this is normal, just close the tab)

### Step 4: Capture Payment
```bash
POST /donations/capture-order
Authorization: Bearer <token>
Body: {"order_id": "5O190127TN364715T"}
```

### Step 5: Verify
```bash
GET /donations/my-donations
Authorization: Bearer <token>
# You should see your completed donation with status:  true
```

## 🧪 Testing

### Using FastAPI Swagger UI (Easiest)
1. Navigate to http://localhost:8000/docs
2. Click **"Authorize"** and enter:  `Bearer <your_token>`
3. Try out each endpoint interactively

### Using Postman
1. Import the endpoints
2. Set Authorization header: `Bearer <your_token>`
3. Test each endpoint

### Using cURL
```bash
# Login
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=pass123"

# Create Order
curl -X POST "http://localhost:8000/donations/create-order" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10}'
```

## 🌐 Production Deployment

### Switch to PayPal Live Mode

Update your `.env`:
```env
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=<your_live_client_id>
PAYPAL_CLIENT_SECRET=<your_live_client_secret>
PAYPAL_API_BASE=https://api-m.paypal.com
```

### Security Checklist
- ✅ Use HTTPS (SSL certificate)
- ✅ Keep `.env` secure (never commit to git)
- ✅ Use strong SECRET_KEY
- ✅ Enable CORS properly
- ✅ Add rate limiting
- ✅ Implement logging and monitoring
- ✅ Validate all inputs
- ✅ Add webhook signature verification

### Deployment Options
- **Heroku**: Easy deployment with PostgreSQL addon
- **AWS EC2/ECS**: Full control
- **DigitalOcean**: App Platform or Droplets
- **Railway**: Modern deployment platform
- **Render**: Free tier available

## 🔮 Future Enhancements

- [ ] PayPal Webhooks for automatic payment confirmation
- [ ] Refund functionality
- [ ] Multiple payment gateways (Stripe, Razorpay)
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Recurring donations
- [ ] Frontend application (React/Vue/Next.js)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👤 Author

**yshhh17**
- GitHub: [@yshhh17](https://github.com/yshhh17)
- Repository: [Donation-App](https://github.com/yshhh17/Donation-App)

## 📞 Support

If you have any questions or run into issues: 
- Open an issue on GitHub
- Check PayPal's [Developer Documentation](https://developer.paypal.com/docs/api/overview/)
- Review FastAPI [Documentation](https://fastapi.tiangolo.com/)

---

⭐ If you found this project helpful, please give it a star! 
