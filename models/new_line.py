from typing import Callable, TYPE_CHECKING

import streamlit as st

from models.command import Command
from enums.personas import Persona

if TYPE_CHECKING:
    from asembler import Asembler


class NewLine(Command):

    def __init__(self):
        self._class: str = self.__class__.__name__

    @property
    def label(self) -> str:
        return f"Przejdź do nowej linii."
    
    @property
    def value(self) -> str:
        return "\n"
    
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