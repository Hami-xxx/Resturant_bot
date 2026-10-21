from db.models.user import User

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings

async def create_user(db: AsyncSession,telegram_id: int, username: str):

    user = await db.scalar(
        select(User)
        .where(
        User.telegram_id == telegram_id
        )
    )

    if user:
        return user

    new_user = User(
        telegram_id=telegram_id,
        username=username if username else None,
        role="admin" if telegram_id == settings.ADMIN_ID else "user" 
    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user

async def get_user_by_tel_id(db: AsyncSession, telegram_id: int):
    user = await db.scalar(
        select(User)
        .options(selectinload(User.orders))
        .where(
            User.telegram_id == telegram_id
        )
    )

    return user