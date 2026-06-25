from abc import ABC
from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from motor.motor_asyncio import AsyncIOMotorClient

from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from infra.repositories.messages.converters import (
    convert_chat_document_to_entity,
    convert_chat_entity_to_document,
    convert_message_entity_to_document,
)


@dataclass
class BaseMongoDBRepository(ABC):
    mongodb_client: AsyncIOMotorClient
    mongodb_db_name: str
    mongodb_collection_name: str

    @property
    def _collection(self):
        return self.mongodb_client[self.mongodb_db_name][self.mongodb_collection_name]


@dataclass
class MongoDBChatsRepository(BaseMongoDBRepository, BaseChatsRepository):
    async def check_chat_exists_by_title(self, title: str) -> bool:
        result = await self._collection.find_one({"title": title})
        return result is not None

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one({"oid": oid})
        return convert_chat_document_to_entity(chat_document) if chat_document else None

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_chat_entity_to_document(chat))


@dataclass
class MongoDBMessagesRepository(BaseMongoDBRepository, BaseMessagesRepository):
    async def add_message(self, chat_oid: str, message: Message) -> None:
        await self._collection.update_one(
            filter={"oid": chat_oid},
            update={"$push": {"messages": convert_message_entity_to_document(message)}},
        )
