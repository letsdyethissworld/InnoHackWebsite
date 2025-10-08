from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.sql import text


class SQLModelAdapter:
    """Adapter to handle database connection pool using SQLAlchemy"""

    __engine: None | (
        AsyncEngine
    )  # async SQLAlchemy engine, which will handle database connection pool
    __database_url: str  # database url with asyncpg driver
    __application_name: str  # application name, use in connection string and used in postgres to track which application is using the database

    def __init__(
        self,
        database_host: str,
        database_port: int,
        database_user: str,
        database_password: str,
        database_name: str,
        application_name: str,
    ):
        # Build SQLModelAdapter database url using asyncpg driver
        self.__database_url = (
            f"postgresql+asyncpg://{database_user}:{database_password}@"
            f"{database_host}:{database_port}/{database_name}"
        )
        self.__application_name = application_name
        self.__engine = None

    async def create_engine(self) -> None:
        """Create async engine for database connection pool. This should be done on application start."""
        if not self.__engine:
            self.__engine = create_async_engine(
                self.__database_url,
                connect_args={
                    "server_settings": {"application_name": self.__application_name}
                },
            )
            # Connection check
            async with self.__engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

    async def dispose_engine(self) -> None:
        """Dispose (shut down) async engine with database connection pool. This should be done on application shutdown."""
        if self.__engine:
            await self.__engine.dispose()
            self.__engine = None

    async def get_session(self) -> AsyncSession:
        """Get a new AsyncSession for handling database operations during one unit of work or tests."""
        if not self.__engine:
            raise RuntimeError("Engine not initialized. Call create_engine() first")
        return AsyncSession(self.__engine)
