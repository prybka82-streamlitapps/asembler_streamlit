from typing import Callable, TYPE_CHECKING

import streamlit as st

from models.command import Command
from models.box import Box
from enums.personas import Persona

if TYPE_CHECKING:
    from asembler import Asembler


class ReadToBox(Command):

    def __init__(self, box: Box):
        self._class: str = self.__class__.__name__
        self._box: Box = box

    @property
    def label(self) -> str:
        return f"Wczytaj do pudełka: {self._box}."
    
    @property
    def value(self) -> Box:
        return self._box
    
    @value.setter
    def value(self, value: Box) -> None:
        self._box = value
    
    @property
    def function(self) -> Callable:
        return self._foo
    
    def _foo(self, asembler: "Asembler") -> None:

        if asembler.is_fast_forwarding == "yes":
            asembler.is_fast_forwarding = "paused"
        
        answer: bool = self._dialog(asembler, self._box)

        if asembler.is_fast_forwarding == "paused" and answer:
            asembler.is_fast_forwarding = "yes"

    @st.dialog("Podaj liczbę")
    def _dialog(self, asembler: "Asembler", box: str) -> bool:
        number: int|None = st.number_input(
            "Liczba",
            format="%d",
            step=1,
        )

        if st.button("OK"):
            asembler.boxes[box] = number
            asembler.console_messages.append(
                (Persona.BOT, str(number))
            )
            asembler.current_step += 1
            st.rerun()

            return True
        else:
            return False

