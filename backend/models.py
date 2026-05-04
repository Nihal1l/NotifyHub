from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Association table for notification recipients (by user)
notification_user = Table(
    'notification_user', Base.metadata,
    Column('notification_id', Integer, ForeignKey('notifications.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    users = relationship('User', back_populates='role')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('Role', back_populates='users')
    notifications = relationship('Notification', secondary=notification_user, back_populates='recipients')

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    audience = Column(String)  # 'all' or comma-separated role names
    recipients = relationship('User', secondary=notification_user, back_populates='notifications')

class NotificationRead(Base):
    __tablename__ = 'notification_reads'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    notification_id = Column(Integer, ForeignKey('notifications.id'))
    is_read = Column(Boolean, default=False)
    user = relationship('User')
    notification = relationship('Notification')
