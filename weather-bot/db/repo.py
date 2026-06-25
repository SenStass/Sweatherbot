from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ForecastRecord, User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self._session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_or_create(self, telegram_id: int) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user is not None:
            return user

        user = User(telegram_id=telegram_id)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def update_location(
        self,
        telegram_id: int,
        city: str,
        latitude: float,
        longitude: float,
    ) -> User:
        user = await self.get_or_create(telegram_id)
        user.city = city
        user.latitude = latitude
        user.longitude = longitude
        await self._session.commit()
        await self._session.refresh(user)
        return user


class ForecastRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_record(
        self,
        user_id: int,
        source: str,
        temperature: float,
    ) -> ForecastRecord:
        record = ForecastRecord(
            user_id=user_id,
            source=source,
            temperature=temperature,
        )
        self._session.add(record)
        await self._session.commit()
        await self._session.refresh(record)
        return record
