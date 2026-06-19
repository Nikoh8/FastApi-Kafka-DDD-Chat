from fastapi import FastAPI

from application.api.messages.handlers import router as messages_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Kafka Chat",
        docs_url="/api/docs",
        description="Simple kafka + DDD exmaple chat",
        debug=True,
    )
    app.include_router(messages_router, prefix="/chat")
    return app
