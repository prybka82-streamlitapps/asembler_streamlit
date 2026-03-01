from typing import Callable, Generic, TypeVar, TYPE_CHECKING

from models.command import Command
from models.value_or_box import ValueOrBox, Box

if TYPE_CHECKING:
    from asembler import Asembler


class Decrease[ValueOrBox](Command):

    def __init__(self, box: Box, value_or_box: ValueOrBox):
        self._class: str = self.__class__.__name__
        self._box: Box = box
        self._val_or_box: ValueOrBox = value_or_box

    @property
    def label(self) -> str:
        return f"Zmniejsz pudełko {self._box} o {self._val_or_box}"
    
    @property
    def box(self) -> Box:
        return self._box
    
    @box.setter
    def box(self, box: Box) -> None:
        self._box = box
    
    @property
    def value(self) -> ValueOrBox:
        return self._val_or_box
    
    @value.setter
    def value(self, value_or_box: ValueOrBox) -> None:
        self._val_or_box = value_or_box
    
    @property
    def function(self) -> Callable:
        return self._foo
    
    def _foo(self, asembler: "Asembler") -> None:
        
        if isinstance(self.value, int):
            asembler.boxes[self.box] -= self.value
        elif isinstance(self.value, str):
            asembler.boxes[self.box] -= asembler.boxes[self.value]
        else:
            raise ValueError("Cannot decrease box value!")
        
        asembler.current_step += 1