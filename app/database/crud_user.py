from sqlalchemy import select
from app.database.database import Session
from app.database.models import Users


async def new_admin(new_user):
    async with Session() as session:
        tmp = select(Users).where(Users.user_id == new_user["user_id"])
        result = await session.execute(tmp)
        user = result.scalar_one_or_none()
        if not user:
            user = Users(
                user_id=new_user["user_id"], name=new_user["name"], is_admin=True
            )
            session.add(user)
            await session.commit()
        elif user.is_admin == False:
            user.is_admin = True
            user.name = new_user["name"]
            await session.commit()
            await session.refresh(user)


async def remove_admin(old_used_id):
    async with Session() as session:
        tmp = select(Users).where(Users.is_admin == True, Users.user_id == old_used_id)
        result = await session.execute(tmp)
        user = result.scalar_one_or_none()
        if user:
            user.is_admin = False
            await session.commit()
            await session.refresh(user)
            return True
        else:
            return False

async def get_admins():
    async with Session() as session:
        tmp = select(Users).where(Users.is_admin == True)
        result = await session.execute(tmp)
        return result.scalars().all()

async def is_admin(id):
    async with Session() as session:
        tmp = select(Users).where(Users.user_id == id, Users.is_admin == True)
        result = await session.execute(tmp)
        if result.scalars().all():
            return True
        else:
            return False
