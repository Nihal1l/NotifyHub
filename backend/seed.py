import asyncio
from .database import engine, Base, SessionLocal
from .models import Role, User

ROLES = ["Admin", "Manager", "Editor", "Viewer", "Support"]
USERS = [
    {"username": "alice", "role": "Admin"},
    {"username": "bob", "role": "Manager"},
    {"username": "carol", "role": "Editor"},
    {"username": "dave", "role": "Viewer"},
    {"username": "eve", "role": "Support"},
    {"username": "frank", "role": "Viewer"},
]

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        # Create roles
        role_objs = {name: Role(name=name) for name in ROLES}
        session.add_all(role_objs.values())
        await session.flush()
        # Create users
        user_objs = [User(username=u["username"], role=role_objs[u["role"]]) for u in USERS]
        session.add_all(user_objs)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
