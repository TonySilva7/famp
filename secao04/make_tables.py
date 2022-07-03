# function to create and delete all tables in the database
from core.configs import settings
from core.db import engine


async def create_tables() -> None:
    import models.__all_models

    print("Creating tables...")

    async with engine.begin() as conn:
        print("deleteing all tables...")
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        print("creating all tables...")
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)

    print("Tables created.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
    print("Done.")
    import sys

    sys.exit(0)
