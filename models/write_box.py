from typing import Callable, TYPE_CHECKING

from enums.personas import Persona
from models.command import Command
from models.box import Box

if TYPE_CHECKING:
    from asembler import Asembler


class WriteBox(Command):

    def __init__(self, box: Box):
        self._class: str = self.__class__.__name__
        self._box: Box = box

    @property
    def label(self) -> str:
        return f"Wypisz pudełko: {self._box}"
    
    @property
    def value(self) -> Box:
        return self._box
    
    @value.setter
    def value(self, box: Box) -> None:
        self._box = box
    
    @property
    def function(self) -> Callable:
        return self._foo
    
    def _foo(self, asembler: "Asembler") -> None:

        box_value: str = str(asembler.boxes[self.value])
        
        if not asembler.last_msg:
            asembler.add_user_msg(box_value)
        elif asembler.last_msg[0] == Persona.USER:
            asembler.append_to_last_msg(box_value)
        else:
            asembler.add_user_msg(box_value)

        asembler.current_step += 1