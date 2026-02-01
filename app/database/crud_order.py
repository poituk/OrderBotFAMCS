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
