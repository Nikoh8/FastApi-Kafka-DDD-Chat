from dataclasses import dataclass

from domain.entities.messages import Chat
from motor.motor_asyncio import AsyncIOMotorClient

from infra.repositories.messages.base import BaseChatRepository
from infra.repositories.messages.converters import convert_chat_entity_to_document


@dataclass
class MongoDBChatRepository(BaseChatRepository):
    mongodb_client: AsyncIOMotorClient
    mongodb_db_name: str
    mongodb_collection_name: str

    def _get_chat_collection(self):
        return self.mongodb_client[self.mongodb_db_name][self.mongodb_collection_name]

    async def check_chat_exists_by_title(self, title: str) -> bool:
        collection = self._get_chat_collection()
        result = await collection.find_one({"title": title})
        return result is not None

    async def add_chat(self, chat: Chat) -> None:
        collection = self._get_chat_collection()

        await collection.insert_one(convert_chat_entity_to_document(chat))
