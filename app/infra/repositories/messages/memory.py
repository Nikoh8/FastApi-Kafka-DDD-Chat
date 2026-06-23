from dataclasses import dataclass, field

from domain.entities.messages import Chat

from infra.repositories.messages.base import BaseChatRepository


@dataclass
class MemoryChatRepository(BaseChatRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return any(chat.title.as_generic_type() == title for chat in self._saved_chats)

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)
