from functools import lru_cache

from infra.repositories.messages.base import BaseChatRepository
from infra.repositories.messages.mongo import MongoDBChatRepository
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope
from settings.config import Config

from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(CreateChatCommandHandler)
    container.register(Config, instance=Config(), scope=Scope.singleton)

    def init_mediator():
        mediator = Mediator()

        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )
        return mediator

    def init_chat_mongo_db_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(config.mongodb_uri, serverSelectionTimeoutMS=3000)
        return MongoDBChatRepository(
            mongodb_client=client,
            mongodb_db_name=config.mongodb_chat_database,
            mongodb_collection_name=config.mongodb_chat_collection,
        )

    container.register(Mediator, factory=init_mediator)
    container.register(
        BaseChatRepository, factory=init_chat_mongo_db_repository, scope=Scope.singleton
    )

    return container
