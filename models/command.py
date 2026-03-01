from abc import abstractmethod
from typing import Callable, TypeVar, Generic

T = TypeVar('T', bound = int|str)


class Command(Generic[T]):

    @property
    @abstractmethod
    def label(self) -> str:...

    @property
    @abstractmethod
    def value(self) -> T:...

    @value.setter
    @abstractmethod
    def value(self, value: T) -> None:...

    @property
    @abstractmethod
    def function(self) -> Callable:...

    @property
    def contains_step(self) -> bool:
        return False
    

