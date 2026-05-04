# NotifyHub 🔔

NotifyHub is a real-time, role-based notification system designed to deliver targeted messages to users based on their organizational roles. Built with a modern full-stack architecture, it demonstrates real-time communication using WebSockets and a robust asynchronous backend.

## 🚀 Features

- **Role-Based Targeting**: Send notifications to specific user groups (Admin, Manager, Editor, etc.) or "All Users".
- **Real-Time Delivery**: Instant message broadcasting using WebSockets.
- **Unread Tracking**: Persistent unread/read status tracking per user.
- **Admin Dashboard**: A centralized interface for creating and managing notifications.
- **Modern UI**: A clean, responsive interface built with Material UI.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18
- **UI Library**: Material UI (MUI)
- **State/API**: Axios
- **Real-time**: Native WebSocket API

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy (Asynchronous)
- **Database**: PostgreSQL
- **Driver**: `asyncpg` (Async PostgreSQL driver)
- **Web Server**: Uvicorn

---

## ⚙️ Local Setup Instructions

### 1. Prerequisites
- **Python 3.9+**
- **Node.js 16+**
- **PostgreSQL** (running locally)

### 2. Database Setup
1. Ensure PostgreSQL is running.
2. Create the database:
   ```bash
   # Using psql (Password may be required)
   psql -U postgres -c "CREATE DATABASE notifyhub"
   ```
   *(Alternatively, run `python backend/create_db.py` if your postgres credentials match `postgres:postgres`)*

### 3. Backend Configuration
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/notifyhub
   ```
5. **Initialize and Seed Database**:
   ```bash
   python seed.py
   ```
6. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   *Backend runs at: `http://localhost:8000`*

### 4. Frontend Configuration
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the application:
   ```bash
   npm start
   ```
   *Frontend runs at: `http://localhost:3000`*

---

## 🏗️ Design Decisions & Assumptions

1. **In-Memory WebSocket Management**: WebSocket connections are stored in an in-memory dictionary. This is optimized for low latency in a single-server deployment. For horizontal scaling, a pub/sub system like Redis would be required.
2. **Asynchronous Architecture**: The entire backend (FastAPI + SQLAlchemy + asyncpg) is built using `async/await` to handle high-concurrency WebSocket connections efficiently.
3. **Role-Based Logic**: Notifications are filtered twice—once when fetching history from the DB and once during live broadcast—ensuring users only see messages intended for their role.
4. **Read Status Persistence**: A dedicated `notification_reads` table tracks the status for every user-notification pair, allowing for granular "Mark as Read" functionality.
5. **Pre-defined Roles**: The system assumes five core roles: `Admin`, `Manager`, `Editor`, `Viewer`, and `Support`.
6. **Simplified Auth**: For demonstration purposes, the system uses a simple user selection/ID mechanism rather than a full OAuth2/JWT flow.

---

## 👥 Test Users (Pre-seeded)

| Username | Role |
| :--- | :--- |
| `alice` | Admin |
| `bob` | Manager |
| `carol` | Editor |
| `dave` | Viewer |
| `eve` | Support |
| `frank` | Viewer |

