from sqlalchemy import select
from app.database.database import Session
from app.database.models import Orders


async def save_todb(new_order):
    async with Session() as session:
        order = Orders(
            name=new_order.get("name", ""),
            user_id=new_order.get("user_id", ""),
            contact=new_order.get("contact", ""),
            description=new_order.get("description", ""),
        )
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order.id


async def get_orders(id):
    async with Session() as session:
        tmp = select(Orders).where(Orders.user_id == id)
        result = await session.execute(tmp)
        return result.scalars().all()


async def remove_order(id, user_id):
    async with Session() as session:
        tmp = select(Orders).where(Orders.id == id, Orders.user_id == user_id)
        result = await session.execute(tmp)
        order = result.scalar_one_or_none()
        if order:
            await session.delete(order)
            await session.commit()
            return True
        else:
            return False


async def remove_admin_order(id):
    async with Session() as session:
        tmp = select(Orders).where(Orders.id == id)
        result = await session.execute(tmp)
        order = result.scalar_one_or_none()
        if order:
            await session.delete(order)
            await session.commit()
            return True
        else:
            return False


async def get_admin_orders():
    async with Session() as session:
        tmp = select(Orders).where()
        result = await session.execute(tmp)
        return result.scalars().all()


async def get_old_order():
    async with Session() as session:
        tmp = select(Orders).order_by(Orders.created_at.asc()).limit(1)
        result = await session.execute(tmp)
        return result.scalar_one_or_none()


async def get_last_order():
    async with Session() as session:
        tmp = select(Orders).order_by(Orders.created_at.desc()).limit(1)
        result = await session.execute(tmp)
        return result.scalar_one_or_none()
