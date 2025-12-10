from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import Annotated
from App.presentation.api.deps import get_rabbit_config
from App.presentation.api.deps import get_db_config
from App.infrastructure.log.logger import logger
from App.presentation.api.routers import users

@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    db_config = get_db_config()
    rabbit_config = get_rabbit_config()
    try:
        await db_config.connect()
        await rabbit_config.connect()
        yield
    except Exception as e:
        logger.exception(f"Asynccontextmanager error: {e}")
        raise
    finally:
        await db_config.disconnect()
        await rabbit_config.disconnect()

app = FastAPI(title="FastAPI DDD Template", lifespan=lifespan)
app.include_router(users.router)