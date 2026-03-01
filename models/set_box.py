from typing import Callable, TYPE_CHECKING

from models.command import Command
from models.box import Box
from models.box_or_value import BoxOrValue

if TYPE_CHECKING:
    from asembler import Asembler


class SetBox[BoxOrValue](Command):

    def __init__(self, box: Box, box_or_value: BoxOrValue):
        self._class: str = self.__class__.__name__
        self._box: Box = box
        self._box_or_value: BoxOrValue = box_or_value

    @property
    def label(self) -> str:
        return f"Ustaw wartość pudełka: {self._box} na {self._box_or_value}"
    
    @property
    def value(self) -> BoxOrValue:
        return self._box_or_value
    
    @value.setter
    def value(self, box_or_value: BoxOrValue) -> None:
        self._box_or_value = box_or_value
    
    @property
    def function(self) -> Callable:
        return self._foo
    
    @property
    def box(self) -> Box:
        return self._box
    
    @box.setter
    def box(self, box: Box) -> None:
        self._box = box

    def _foo(self, asembler: "Asembler") -> None:

        if isinstance(self.value, int):
            asembler.boxes[self.box] = self.value
        elif isinstance(self.value, str):
            asembler.boxes[self.box] = asembler.boxes[self.value]
        else:
            raise ValueError("Cannot set box value!")

        asembler.current_step += 1