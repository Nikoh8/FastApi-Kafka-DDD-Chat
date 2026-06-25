from dataclasses import dataclass, field

from domain.entities.messages import Chat

from infra.repositories.messages.base import BaseChatsRepository


@dataclass
class MemoryChatRepository(BaseChatsRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return any(chat.title.as_generic_type() == title for chat in self._saved_chats)

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        return next((chat for chat in self._saved_chats if chat.oid == oid), None)

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)
