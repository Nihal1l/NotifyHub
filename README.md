# NotifyHub - Role-Based Notification System

## Backend (FastAPI + PostgreSQL)

1. Create a PostgreSQL database named `notifyhub` locally.
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Seed the database:
   ```bash
   python seed.py
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## Frontend (React)

1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the React app:
   ```bash
   npm start
   ```

## Features
- 6 pre-seeded users, each with one of 5 roles
- Admin panel for sending notifications to all or by role
- User view for receiving and managing notifications
- Real-time updates via WebSocket
- Mark notifications as read/unread
- Search/filter notifications

## Notes
- No authentication; switch users via dropdown
- Local PostgreSQL only (no cloud DB)
