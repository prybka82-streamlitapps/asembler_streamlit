from typing import Generic, Literal, TypeVar
import json

from models.box import Box
from models.condition import Condition
from models.box_or_value import BoxOrValue
from models.command import Command
from models.write_box import WriteBox
from models.write_text import WriteText
from models.increase import Increase
from models.decrease import Decrease
from models.read_to_box import ReadToBox
from models.set_box import SetBox
from models.go_to import GoTo
from models.if_ import If
from models.new_line import NewLine
from enums.personas import Persona
from helpers.encoder import encode_asembler


class Asembler(Generic[BoxOrValue]):

    def __init__(self):

        self.boxes: dict[str, int] = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
        }

        self.program: list[Command] = []
        self.is_running: bool = False
        self.current_step: int = -1
        self.console_messages: list[tuple[Persona, str]] = []

    @property
    def command_count(self) -> int:
        return len(self.program)
    
    @property
    def last_msg(self) -> tuple[Persona, str]|None:
        if self.console_messages:
            return self.console_messages[-1]
        else:
            return None
        
    @last_msg.setter
    def last_msg(self, msg: tuple[Persona, str]) -> None:
        if not self.console_messages:
            self.console_messages.append(msg)
        else:
            self.console_messages[-1] = msg
    
    def start(self):
        self.is_running=True
        self.current_step=0
        self.console_messages = []
        self._clear_boxes()

    def stop(self):
        self.is_running=False
        self.current_step=-1

    def next(self):
        if self.current_step < self.command_count and self.current_step >= 0:
            self.program[self.current_step].function(self)
        else:
            self.stop()

    def add_user_msg(self, msg: str) -> None:
        self.console_messages.append(
            (Persona.USER, msg)
        )

    def add_bot_msg(self, msg: str) -> None:
        self.console_messages.append(
            (Persona.BOT, msg)
        )

    def append_to_last_msg(self, msg: str) -> None:
        if not self.console_messages:
            self.console_messages.append(
                (Persona.USER, msg)
            )
        else:
            self.console_messages[-1] = (
                (Persona.USER, self.console_messages[-1][1] + msg)
            )

    def move_cmd_up(self, id: int):

        self.program[id], self.program[id-1] = self.program[id-1], self.program[id]

    def move_cmd_down(self, id: int):

        self.program[id], self.program[id+1] = self.program[id+1], self.program[id]

    def delete_cmd(self, id: int):

        self.program.pop(id)

    def add_write_box(self, box: Box):

        self.program.append(WriteBox(box))

    def add_write_text(self, text: str):

        self.program.append(WriteText(text))

    def add_new_line(self):

        self.program.append(NewLine())

    def add_read_to_box(self, box: Box):

        self.program.append(ReadToBox(box))

    def add_set_box(self, box: Box, value: BoxOrValue):

        self.program.append(SetBox(box, value))

    def add_increase(self, box: Box, value: BoxOrValue):

        self.program.append(Increase(box, value))

    def add_decrease(self, box: Box, value: BoxOrValue):

        self.program.append(Decrease(box, value))

    def add_if(
            self,
            box_1: Box,
            condition: Condition,
            box_2: BoxOrValue,
            go_to_if_true: int|str,
            go_to_if_false: int|str):

        self.program.append(
            If(
                box_1,
                condition,
                box_2,
                go_to_if_true,
                go_to_if_false
            )
        )

    def add_go_to(self, step: int|str):

        self.program.append(GoTo(step))

    def _clear_boxes(self):
        for key in self.boxes:
            self.boxes[key] = 0

    def to_json(self) -> str:

        return json.dumps(self.program, default=encode_asembler)
    
    def from_json(self, data: str|bytes|bytearray) -> None:

        self.program = []

        for item in json.loads(data):
            
            match item["_class"]:
                case "WriteBox":
                    self.program.append(WriteBox(item["_box"]))

                case "WriteText":
                    self.program.append(WriteText(item["_text"]))

                case "NewLine":
                    self.program.append(NewLine())
                
                case "ReadToBox":
                    self.program.append(ReadToBox(item["_box"]))

                case "SetBox":
                    self.program.append(SetBox(item["_box"], item["_box_or_value"]))

                case "Increase":
                    self.program.append(Increase(item["_box"], item["_val_or_box"]))

                case "Decrease":
                    self.program.append(Decrease(item["_box"], item["_val_or_box"]))

                case "If":
                    self.program.append(If(
                        item["_box"],
                        item["_condition"],
                        item["_box_or_value"],
                        item["_to_if_true"],
                        item["_to_if_false"]
                    ))

                case "GoTo":
                    self.program.append(GoTo(item["_step"]))