# NotifyHub - Role-Based Notification System

A real-time, role-based notification system built with FastAPI (Backend), React (Frontend), and PostgreSQL (Database).

## Features
- **Role-Based Notifications**: Send notifications to all users or specific roles (Admin, Manager, Editor, Viewer, Support).
- **Real-Time Updates**: Notifications are delivered instantly via WebSockets.
- **Admin Panel**: Dedicated panel for admins to create and dispatch notifications.
- **Unread Badges**: Real-time unread count indicators.
- **Mark Read/Unread**: Users can manage their notification status.
- **Search & Filter**: Quickly find notifications by content.

---

## Local Setup Instructions

### 1. Database Setup (PostgreSQL)
1. Ensure PostgreSQL is installed and running on your machine.
2. Create a database named `notifyhub`:
   ```bash
   psql -U postgres -c "CREATE DATABASE notifyhub"
   ```
3. Create a `.env` file in the `backend/` directory and add your database URL:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/notifyhub
   ```

### 2. Backend Setup (FastAPI)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Seed the database with initial users and roles:
   ```bash
   python seed.py
   ```
5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

### 3. Frontend Setup (React)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000`.

---

## Default Users (Pre-seeded)
- **alice**: Admin
- **bob**: Manager
- **carol**: Editor
- **dave**: Viewer
- **eve**: Support
- **frank**: Viewer

---

## Technologies Used
- **Backend**: FastAPI, SQLAlchemy (Async), PostgreSQL
- **Frontend**: React, Material UI, Axios
- **Real-time**: WebSockets
