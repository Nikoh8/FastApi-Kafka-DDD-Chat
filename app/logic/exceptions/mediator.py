from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(LogicException):
    event_type: str

    @property
    def message(self) -> str:
        return f"Event handlers not registered for event type: {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: str

    @property
    def message(self) -> str:
        return f"Command handlers not registered for command type: {self.command_type}"
