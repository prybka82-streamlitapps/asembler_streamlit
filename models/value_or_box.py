from typing import TypeVar

from models.box import Box


ValueOrBox = TypeVar("ValueOrBox", bound = int|Box)