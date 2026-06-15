from datetime import datetime

import pytest
from domain.entities.messages import Chat, Message
from domain.exceptions.messages import TitleTooLongException
from domain.values.messages import Text, Title


def test_create_message_success():
    text = Text("Hello")
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success():
    title = Title("Title")
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_too_long():
    with pytest.raises(TitleTooLongException):
        Title("a" * 256)


def test_add_message_to_chat():
    message = Message(text=Text("Hello"))
    chat = Chat(title=Title("Title"))
    chat.add_message(message)

    assert message in chat.messages
