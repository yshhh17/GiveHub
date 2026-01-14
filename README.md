# 💰 GiveHub - Donation Platform

GiveHub is a modern, full-stack crowdfunding and donation platform designed to connect donors with causes. It features secure authentication, real-time donation processing via PayPal, and a transparent dashboard for tracking contributions.

![GiveHub Banner](https://via.placeholder.com/1200x400?text=GiveHub+Donation+Platform)

## ✨ Features

*   **Secure Authentication:** User registration, login, and email verification using JWT and OTP.
*   **PayPal Integration:** Seamless donation processing with PayPal Sandbox/Live integration and Webhook support.
*   **Real-time Dashboard:** Track total donations, view history, and manage your profile.
*   **Responsive Design:** Fully responsive UI built with React, Tailwind CSS, and Material Design principles.
*   **Secure Backend:** FastAPI backend with rate limiting, input validation, and SQL injection protection.
*   **API Documentation:** Interactive Swagger UI documentation.
*   **Containerized:** Fully Dockerized setup for easy deployment.

## 🛠️ Tech Stack

### **Backend**
*   **Framework:** Python 3.9+ with [FastAPI](https://fastapi.tiangolo.com/)
*   **Database:** PostgreSQL with SQLAlchemy ORM
*   **Caching/Rate Limiting:** Redis
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

### Prerequisites
*   [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) (Recommended)
*   **OR**
*   Python 3.9+, Node.js 18+, and PostgreSQL/Redis installed locally.

---

### 🐳 Quick Start with Docker (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yshhh17/Donation-App.git
    cd Donation-App
    ```

2.  **Configure Environment Variables:**
    Copy the example env file:
    ```bash
    cp .env.example .env
    ```
    *Edit `.env` and provide your PayPal and SMTP credentials.*

3.  **Launch the application:**
    ```bash
    docker-compose up --build
    ```

4.  **Access the apps:**
    *   **Frontend:** `http://localhost:3000`
    *   **Backend API:** `http://localhost:8000`
    *   **API Docs:** `http://localhost:8000/docs`

---

### 🔧 Manual Local Setup

#### 1. Backend Setup
1.  Navigate to the backend directory: `cd backend`
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # Windows: venv\Scripts\activate
    ```
3.  Install dependencies: `pip install -r requirements.txt`
4.  Configure `.env` in the `backend/` folder (use `../.env.example` as a template).
5.  Run the server: `uvicorn app.main:app --reload`

#### 2. Frontend Setup
1.  Navigate to the frontend directory: `cd frontend`
2.  Install dependencies: `npm install`
3.  Configure `.env` in the `frontend/` folder:
    ```env
    VITE_API_BASE_URL=http://localhost:8000
    VITE_PAYPAL_CLIENT_ID=your_paypal_client_id
    ```
4.  Run the development server: `npm run dev`

---

## 📂 Project Structure

```text
Donation-App/
├── backend/
│   ├── app/
│   │   ├── core/           # Config, Security, Rate Limiting
│   │   ├── db/             # Database connection & Models
│   │   ├── routers/        # API Endpoints (Users, Donations, Webhooks)
│   │   ├── schemas/        # Pydantic Models (Validation)
│   │   ├── services/       # PayPal, Email, OTP services
│   │   └── main.py         # FastAPI Entry point
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── context/        # Auth & State Context
│   │   ├── hooks/          # Custom Hooks
│   │   ├── pages/          # Route components
│   │   ├── services/       # API/Axios configuration
│   │   └── utils/          # Helpers & Constants
│   └── Dockerfile
│
├── docker-compose.yml      # Orchestration for DB, Redis, Backend, Frontend
└── .env.example            # Template for environment variables
```

## 🔒 Security & Best Practices
*   **Argon2 Password Hashing:** State-of-the-art hashing for user passwords.
*   **JWT Authentication:** Stateless secure authentication.
*   **Rate Limiting:** IP-based and User-based rate limiting to prevent abuse.
*   **Input Sanitization:** Automated validation using Pydantic.
*   **Environment Isolation:** Strict use of environment variables for sensitive data.

## 🤝 Contributing



Contributions are welcome! Please feel free to submit a Pull Request.



1.  Fork the Project

2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)

3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)

4.  Push to the Branch (`git push origin feature/AmazingFeature`)

5.  Open a Pull Request
