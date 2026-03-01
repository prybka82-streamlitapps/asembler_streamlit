from typing import Callable, TYPE_CHECKING

from models.command import Command
from helpers.fix_step import step_to_int

if TYPE_CHECKING:
    from asembler import Asembler


class GoTo(Command):

    def __init__(self, step: int|str):
        self._class: str = self.__class__.__name__
        self._step: int = step_to_int(step)

    @property
    def label(self) -> str:
        step: str = (
            str(self._step)
            if self._step != -1
            else "koniec"
        )
        return f"Skocz do: {step}"
    
    @property
    def value(self) -> int:
        return self._step
    
    @value.setter
    def value(self, step: int|str) -> None:
        self._step = step_to_int(step)
    
    @property
    def function(self) -> Callable:
        return self._foo

    @property
    def contains_step(self) -> bool:
        return True
    
    def _foo(self, asembler: "Asembler") -> None:

        asembler.current_step = self.value