from sqlalchemy import select
from app.database.database import Session
from app.database.models import Texts

async def save_text(name, new_text):
    async with Session() as session:
        stmt = select(Texts).where(Texts.name == name)
        result = await session.execute(stmt)
        old_text = result.scalar_one_or_none()

        if old_text:
            old_text.text = new_text
            await session.commit()
            await session.refresh(old_text)
        else:
            new_text_obj = Texts(name=name, text=new_text)
            session.add(new_text_obj)
            await session.commit()
            await session.refresh(new_text_obj)


async def get_text(name):
    async with Session() as session:
        tmp = select(Texts).where(Texts.name == name)
        result = await session.execute(tmp)
        return result.scalar_one_or_none()
