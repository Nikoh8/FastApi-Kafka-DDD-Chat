from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongodb_uri: str = Field(default="")
    mongodb_chat_database: str = Field(default="chat")
    mongodb_chat_collection: str = Field(default="chat")
