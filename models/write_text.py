from typing import Callable, TYPE_CHECKING

from models.command import Command
from enums.personas import Persona

if TYPE_CHECKING:
    from asembler import Asembler


class WriteText(Command):
    
    def __init__(self, text: str):
        self._class: str = self.__class__.__name__
        self._text: str = text

    @property
    def label(self) -> str:
        return f"Wypisz tekst: ''{self._text}''"
    
    @property
    def value(self) -> str:
        return self._text
    
    @value.setter
    def value(self, text: str) -> None:
        self._text = text
    
    @property
    def function(self) -> Callable:
        return self._foo
    
    def _foo(self, asembler: "Asembler") -> None:

        if not asembler.last_msg:
            asembler.console_messages.append(
                (Persona.USER, self.value)
            )
        elif asembler.last_msg[0] == Persona.USER:
            asembler.last_msg = (
                Persona.USER,
                asembler.last_msg[1] + self.value
            )
        else:
            asembler.console_messages.append(
                (Persona.USER, self.value)
            )

        asembler.current_step += 1

    def __str__(self) -> str:

        return str(self.__dict__)