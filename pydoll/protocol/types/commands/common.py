from typing import TypedDict, NotRequired, TypeVar, Generic


T_CommandResponse = TypeVar('T_Response')


class CommandParams(TypedDict, total=False):
    """Base structure for command parameters. All fields are optional."""
    pass


class Command(TypedDict, Generic[T_CommandResponse]):
    """Base structure for all commands.
    
    Attributes:
        method: The command method name
        params: Optional dictionary of parameters for the command
    """
    method: str
    params: NotRequired[CommandParams]