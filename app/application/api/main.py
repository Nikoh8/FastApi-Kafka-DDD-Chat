from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI(
        title="FastAPI Kafka Chat",
        docs_url="/api/docs",
        description="Simple kafka + DDD exmaple chat",
        debug=True,
    )
