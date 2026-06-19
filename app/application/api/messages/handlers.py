from domain.exceptions.base import ApplicationException
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from logic.commands.messages import CreateChatCommand
from logic.init import init_container
from logic.mediator import Mediator

from application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
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
    schema: CreateChatRequestSchema, container=Depends(init_container)
):
    """Создать новый чат"""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return CreateChatResponseSchema.from_entity(chat)
