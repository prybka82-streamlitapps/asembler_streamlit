from typing import Any, cast

from models.read_to_box import ReadToBox
from models.write_text import WriteText


def encode_asembler(obj: object) -> dict[str, Any]:

    if hasattr(obj, "__dict__"):
        return vars(obj)
    
    return {
        "class": obj.__class__,
        "attrs": obj.__str__(),
    }    