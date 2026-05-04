from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from models import User, Role, Notification, NotificationRead
from pydantic import BaseModel
from sqlalchemy.orm import joinedload
from typing import List, Dict, Optional
import asyncio

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

# In-memory store for WebSocket connections
active_connections: Dict[int, WebSocket] = {}

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).options(joinedload(User.role)))
    users = result.scalars().all()
    return [{"id": u.id, "username": u.username, "role": u.role.name} for u in users]

@app.get("/roles")
async def get_roles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role))
    roles = result.scalars().all()
    return [r.name for r in roles]

@app.get("/notifications/{user_id}")
async def get_notifications(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id, options=[joinedload(User.role)])
    if not user:
        raise HTTPException(404, "User not found")
    # Get notifications for this user (by role or all)
    result = await db.execute(select(Notification).order_by(Notification.created_at.desc()))
    notifications = result.scalars().all()
    user_role = user.role.name
    filtered = [n for n in notifications if n.audience == "all" or user_role in n.audience.split(",")] 
    # Get read status
    read_result = await db.execute(select(NotificationRead).where(NotificationRead.user_id == user_id))
    read_map = {r.notification_id: r.is_read for r in read_result.scalars().all()}
    return [{
        "id": n.id,
        "title": n.title,
        "message": n.message,
        "created_at": n.created_at,
        "is_read": read_map.get(n.id, False)
    } for n in filtered]

@app.post("/notifications")
async def create_notification(data: dict, db: AsyncSession = Depends(get_db)):
    title = data.get("title")
    message = data.get("message")
    audience = data.get("audience")  # 'all' or comma-separated roles
    if not title or not message or not audience:
        raise HTTPException(400, "Missing fields")
    notif = Notification(title=title, message=message, audience=audience)
    db.add(notif)
    await db.commit()
    await db.refresh(notif)
    # Send to all relevant users via WebSocket
    for user_id, ws in active_connections.items():
        user = await db.get(User, user_id, options=[joinedload(User.role)])
        if user and (audience == "all" or user.role.name in audience.split(",")):
            await ws.send_json({
                "id": notif.id,
                "title": notif.title,
                "message": notif.message,
                "created_at": str(notif.created_at),
                "is_read": False
            })
    return {"status": "sent"}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        del active_connections[user_id]

class MarkReadRequest(BaseModel):
    user_id: int
    is_read: bool

@app.post("/notifications/{notif_id}/read")
async def mark_read(notif_id: int, req: MarkReadRequest, db: AsyncSession = Depends(get_db)):
    # Mark notification as read/unread for user
    result = await db.execute(select(NotificationRead).where(NotificationRead.user_id == req.user_id, NotificationRead.notification_id == notif_id))
    record = result.scalars().first()
    if record:
        record.is_read = req.is_read
    else:
        record = NotificationRead(user_id=req.user_id, notification_id=notif_id, is_read=req.is_read)
        db.add(record)
    await db.commit()
    return {"status": "updated"}
