from domain.exceptions.base import ApplicationException
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.init import init_container
from logic.mediator import Mediator
from punq import Container

from application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
)
from application.api.schemas import ErrorSchema

router = APIRouter(tags=["chat"])


@router.post(
    "/",
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создает новый чат, если чат с таким названием существует, то возвращается ошибка 400",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatRequestSchema, container: Container = Depends(init_container)
) -> CreateChatResponseSchema:
    """Создать новый чат"""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    "/{chat_oid}/messages",
    response_model=CreateMessageResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт добавляет новое сообщение в чат с переданным ObjectID",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageRequestSchema,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """Добавить новое сообщение в чат"""
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid)
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return CreateMessageResponseSchema.from_entity(message)
