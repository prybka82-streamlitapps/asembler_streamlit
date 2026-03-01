from typing import TypeVar

from models.box import Box


BoxOrValue = TypeVar("BoxOrValue", bound=Box|int)