from typing import Callable, Literal, TYPE_CHECKING

from models.box import Box
from models.command import Command
from models.condition import Condition
from models.box_or_value import BoxOrValue
from helpers.fix_step import step_to_int

if TYPE_CHECKING:
    from asembler import Asembler


class If[BoxOrValue](Command):

    def __init__(
            self,
            box: Box,
            condition: Condition,
            box_or_value:
            BoxOrValue,
            to_if_true: int|str,
            to_if_false: int|str
        ):
        self._class: str = self.__class__.__name__
        self._box: Box = box
        self._condition: Condition = condition
        self._box_or_value: BoxOrValue = box_or_value
        self._to_if_true: int = step_to_int(to_if_true)
        self._to_if_false: int = step_to_int(to_if_false)

    @property
    def label(self) -> str:
        s1: str = str(self._to_if_true) if self._to_if_true > -1 else "koniec"
        s2: str = str(self._to_if_false) if self._to_if_false > -1 else "koniec"

        return (
            f"Jeżeli {self.box} {self.condition} {self.value}"
            f", skocz do {s1}"
            f", w przeciwnym razie skocz do {s2}"
        )
    
    @property
    def go_to_if_true(self) -> int:
        return self._to_if_true
    
    @go_to_if_true.setter
    def go_to_if_true(self, step: int|str) -> None:
        self._to_if_true = step_to_int(step)

    @property
    def go_to_if_false(self) -> int:
        return self._to_if_false
    
    @go_to_if_false.setter
    def go_to_if_false(self, step: int|str) -> None:
        self._to_if_false = step_to_int(step)
    
    @property
    def box(self) -> Box:
        return self._box

    @box.setter
    def box(self, box: Box) -> None:
        self._box = box
    
    @property
    def value(self) -> BoxOrValue:
        return self._box_or_value
    
    @value.setter
    def value(self, box_or_value: BoxOrValue) -> None:
        self._box_or_value = box_or_value

    @property
    def condition(self) -> Condition:
        return self._condition
    
    @condition.setter
    def condition(self, condition: Condition) -> None:
        self._condition = condition
    
    @property
    def function(self) -> Callable:
        return self._foo
    
    @property
    def contains_step(self) -> bool:
        return True
    
    def _foo(self, asembler: "Asembler") -> None:
        
        val1: int = asembler.boxes[self.box]
        val2: int = (
            int(self.value)
            if isinstance(self.value, int)
            else asembler.boxes[str(self.value)]
        )
        foo: Callable

        match self.condition:
            case "﹤":
                foo = lambda a, b: a<b
            case "=":
                foo = lambda a, b: a==b
            case "﹥":
                foo = lambda a, b: a>b
            case "≠":
                foo = lambda a, b: a!=b
            case "≤":
                foo = lambda a, b: a<=b
            case "≥":
                foo = lambda a, b: a>=b
            case _:
                raise ValueError(f"Condition {self.condition} cannot be used!")
            
        if foo(val1, val2):
            asembler.current_step = self.go_to_if_true
        else:
            asembler.current_step = self.go_to_if_false