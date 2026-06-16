from datetime import datetime

import pytest
from domain.entities.messages import Chat, Message
from domain.events.messages import NewMessageReceivedEvent
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


def test_new_message_events():
    message = Message(text=Text("Hello"))
    chat = Chat(title=Title("Title"))
    chat.add_message(message)

    events = chat.pull_events()
    pulled_events = chat.pull_events()
    assert not pulled_events
    assert len(events) == 1

    new_event = events[0]
    assert isinstance(new_event, NewMessageReceivedEvent), new_event
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.message_oid == message.oid
    assert new_event.chat_oid == chat.oid
