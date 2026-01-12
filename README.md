# 💰 GiveHub - Donation Platform

GiveHub is a modern, full-stack crowdfunding and donation platform designed to connect donors with causes. It features secure authentication, real-time donation processing via PayPal, and a transparent dashboard for tracking contributions.

![GiveHub Banner](https://via.placeholder.com/1200x400?text=GiveHub+Donation+Platform)

## ✨ Features

*   **Secure Authentication:** User registration, login, and email verification using JWT and OTP.
*   **PayPal Integration:** Seamless donation processing with PayPal Sandbox/Live integration.
*   **Real-time Dashboard:** Track total donations, view history, and manage your profile.
*   **Responsive Design:** Fully responsive UI built with React and Tailwind CSS.
*   **Secure Backend:** FastAPI backend with rate limiting, input validation, and SQL injection protection.
*   **RESTful API:** Well-documented API with Swagger UI integration.

## 🛠️ Tech Stack

### **Backend**
*   **Framework:** Python 3.8+ with [FastAPI](https://fastapi.tiangolo.com/)
*   **Database:** PostgreSQL with SQLAlchemy ORM
*   **Authentication:** JWT (JSON Web Tokens) & Passlib (Argon2 hashing)
*   **Payment Gateway:** PayPal REST SDK
*   **Other Tools:** Pydantic (Validation), SlowAPI (Rate Limiting)

### **Frontend**
*   **Framework:** React 19 (via Vite)
*   **Styling:** Tailwind CSS
*   **State Management:** React Context API
*   **Routing:** React Router v7
*   **HTTP Client:** Axios

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites
*   Python 3.8 or higher
*   Node.js 18 or higher
*   PostgreSQL installed and running
*   A PayPal Developer account (for Sandbox credentials)

---

### 1. Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yshhh17/Donation-App.git
    cd Donation-App/backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the `backend/` directory:
    ```env
    # Database
    DATABASE_URL=postgresql://user:password@localhost:5432/donation_db

    # Security
    SECRET_KEY=your_super_secret_key_change_this
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_TIME=30

    # PayPal (Sandbox)
    PAYPAL_MODE=sandbox
    PAYPAL_CLIENT_ID=your_paypal_client_id
    PAYPAL_CLIENT_SECRET=your_paypal_client_secret
    PAYPAL_API_BASE=https://api-m.sandbox.paypal.com

    # Email (For OTP)
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_app_password
    MAIL_FROM=your_email@gmail.com
    MAIL_PORT=587
    MAIL_SERVER=smtp.gmail.com
    ```

5.  **Run the Backend Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.
    API Docs (Swagger UI): `http://localhost:8000/docs`

---

### 2. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd ../frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the `frontend/` directory:
    ```env
    VITE_API_BASE_URL=http://localhost:8000
    VITE_PAYPAL_CLIENT_ID=your_paypal_client_id
    ```

4.  **Run the Frontend Development Server:**
    ```bash
    npm run dev
    ```
    The app will typically run at `http://localhost:5173`.

---

## 📂 Project Structure

```
Donation-App/
├── backend/
│   ├── app/
│   │   ├── core/           # Config, Security, Rate Limiting
│   │   ├── db/             # Database connection & Models
│   │   ├── routers/        # API Endpoints (Users, Donations)
│   │   ├── schemas/        # Pydantic Models
│   │   ├── services/       # PayPal, Email, OTP services
│   │   └── main.py         # Entry point
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/     # Reusable UI components
    │   ├── context/        # Auth Context Provider
    │   ├── hooks/          # Custom Hooks (useAuth, useDonations)
    │   ├── pages/          # Application Pages
    │   ├── services/       # API integration
    │   └── utils/          # Helpers & Constants
    └── tailwind.config.js
```

## 🔒 Security Best Practices implemented
*   **Password Hashing:** Uses Argon2, the winner of the Password Hashing Competition.
*   **Rate Limiting:** Protects API endpoints against brute-force attacks.
*   **Input Validation:** Pydantic ensures all incoming data meets strict schema requirements.
*   **CORS:** Configured to allow requests only from trusted origins (customizable).
*   **Environment Variables:** Sensitive keys are never hardcoded.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
