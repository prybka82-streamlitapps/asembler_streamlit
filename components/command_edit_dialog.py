from typing import Callable, cast

import streamlit as st

from asembler import Asembler, Box, BoxOrValue
from models.command import Command
from models.condition import Condition
from models.increase import Increase
from models.decrease import Decrease
from models.set_box import SetBox
# from models.step import Step
from models.write_box import WriteBox
from models.go_to import GoTo
from models.if_ import If
from helpers.fix_step import step_to_selection_index
from models.write_text import WriteText

class CommandEditDialog:

    def __init__(self, asembler: Asembler):

        self.asembler: Asembler = asembler

    def find_dialog(self, command: Command):

        label: str = command.label.lower()

        if "pudełko" in label:
            return self.write_box
        
        if "tekst" in label:
            return self.write_text
        
        if "przejdź" in label:
            return self.new_line
        
        if "wczytaj" in label:
            return self.read_to_box
        
        if "ustaw" in label:
            return self.set_box
        
        if "zwiększ" in label:
            return self.increase
        
        if "zmniejsz" in label:
            return self.decrease
        
        if "jeżeli" in label:
            return self.if_
        
        if "skocz" in label:
            return self.go_to

    def _set_value_or_box(
            self,
            command: SetBox|Increase|Decrease|None,
            add_function: Callable[[Box, int|str|Box], None],
        ):
        
        box: str|None = st.pills(
            "Wybierz pudełko:", ["A", "B", "C", "D"],
            selection_mode="single",
            default=command.box if command else None,
            key="selected_box"
        )

        tab1, tab2 = st.tabs(
            ["Pudełka", "Liczba"],
            default="Pudełka" if command and isinstance(command.value, str) else "Liczba"
        )

        with tab1:
            selected_box: str|None = st.pills(
                "Wybierz pudełko:", ["A", "B", "C", "D"],
                selection_mode="single",
                default=command.value 
                    if command and isinstance(command.value, str) 
                    else None,
                key="selected_value"
            )

            if st.button("OK", key="box_selection_submit_btn"):
                if not box:
                    st.error("Wybierz pudełko!")
                elif not selected_box:
                    st.error("Wybierz pudełko!")
                elif command:
                    command.box = cast(Box, box)
                    command.value = selected_box
                    st.rerun()
                else:
                    add_function(cast(Box, box), selected_box)
                    st.rerun()

        with tab2:
            selected_value: int|None = st.number_input(
                "Ustaw wartość",
                step=1,
                format="%d",
                value=command.value 
                    if command and isinstance(command.value, int) 
                    else 0
            )

            if st.button("OK", key="value_selection_submit_btn"):
                if not box:
                    st.error("Wybierz pudełko!")
                elif command:
                    command.box = cast(Box, box)
                    command.value = selected_value
                    st.rerun()
                else:
                    add_function(cast(Box, box), selected_value)
                    st.rerun()

    @st.dialog("Wypisz pudełko")
    def write_box(self, command: Command|None = None):
        selection: str|None = st.pills(
            "Wybierz pudełko:", ["A", "B", "C", "D"],
            selection_mode="single",
            default=command.value if command else None
        )

        if st.button("OK"):
            if not selection:
                st.error("Wybierz pudełko!")
            elif command and selection:
                command.value = selection
                st.rerun()
            else:
                self.asembler.add_write_box(cast(Box, selection))
                st.rerun()

    @st.dialog("Wypisz napis")
    def write_text(self, command: Command|None = None):
        
        text: str|None = st.text_input(
            "Napis:",
            placeholder="Wpisz napis",
            value=command.value if command else None,
        )
        
        if st.button("OK"):
            if not text:
                st.error("Wpisz tekst!")
            else:
                if command:
                    command.value = text
                else:
                    self.asembler.add_write_text(text)
                st.rerun()

    def new_line(self):

        self.asembler.add_new_line()

    @st.dialog("Wczytaj do pudełka")
    def read_to_box(self, command: Command|None = None):
        selection: str|None = st.pills(
            "Wybierz pudełko:", ["A", "B", "C", "D"],
            selection_mode="single",
            default=command.value if command else None
        )

        if st.button("OK"):
            if not selection:
                st.error("Wybierz pudełko!")
            elif command and selection:
                command.value = selection
                st.rerun()
            else:
                self.asembler.add_read_to_box(cast(Box, selection))
                st.rerun()

    @st.dialog("Ustaw pudełko na")
    def set_box(self, command: Command|None = None):
        set_box_cmd: SetBox = cast(SetBox, command)

        self._set_value_or_box(
            set_box_cmd,
            lambda box, sel: self.asembler.add_set_box(box, sel)
        )

    @st.dialog("Zwiększ")
    def increase(self, command: Command|None = None):
        increase_cmd: Increase = cast(Increase, command)

        self._set_value_or_box(
            increase_cmd,
            lambda box, sel: self.asembler.add_increase(box, sel)
        )

    @st.dialog("Zmniejsz")
    def decrease(self, command: Command|None = None):
        decrease_cmd: Decrease = cast(Decrease, command)

        self._set_value_or_box(
            decrease_cmd,
            lambda box, sel: self.asembler.add_decrease(box, sel)
        )

    @st.dialog("Jeżeli")
    def if_(self, command: Command|None = None):
        if_cmd: If = cast(If, command)

        steps_count: int = self.asembler.command_count

        box: str|None = st.pills(
            "Wybierz pudełko:", 
            ["A", "B", "C", "D"],
            selection_mode="single",
            default=if_cmd.box if command else None,
            key="selected_box",
        )

        condition: str|None = st.pills(
            "Wybierz warunek:",
            ["=", "≠", "﹤", "≤", "﹥", "≥"],
            selection_mode="single",
            default=if_cmd.condition if command else "=",
            key="selected_condition",
        )
        
        tab1, tab2 = st.tabs(
            ["Pudełka", "Liczba"],
            default="Pudełka" if command and isinstance(command.value, str) else "Liczba"
        )

        with tab1:
            selected_box: str|None = st.pills(
                "Wybierz pudełko:", ["A", "B", "C", "D"],
                selection_mode="single",
                default=if_cmd.value 
                    if command and isinstance(command.value, str) 
                    else None,
                key="selected_value"
            )

            selected_step_if_true: int|str|None = st.selectbox(
                "Skocz do:",
                [k for k in range(steps_count)] + ["koniec"],
                key="selected_step_if_true_for_box",
                index=(
                    step_to_selection_index(if_cmd.go_to_if_true, steps_count)
                    if command
                    else 0
                ),
            )

            selected_step_if_false: int|str|None = st.selectbox(
                "W przeciwnym razie skocz do:",
                [k for k in range(steps_count)] + ["koniec"],
                key="selected_step_if_false_for_box",
                index=(
                    step_to_selection_index(if_cmd.go_to_if_false, steps_count)
                    if command
                    else 0
                ),
            )

            if st.button("OK", key="box_selection_submit_btn"):
                if not box:
                    st.error("Wybierz pudełko!")
                elif not selected_box:
                    st.error("Wybierz pudełko!")
                elif command:
                    if_cmd.box = cast(Box, box)
                    if_cmd.value = selected_box
                    if_cmd.condition = cast(Condition, condition)
                    if_cmd.go_to_if_true = selected_step_if_true
                    if_cmd.go_to_if_false = selected_step_if_false
                    st.rerun()
                else:
                    self.asembler.add_if(
                        cast(Box, box),
                        cast(Condition, condition.replace("\\", "") if condition else condition),
                        selected_box,
                        selected_step_if_true,
                        selected_step_if_false,
                    )
                    st.rerun()

        with tab2:
            selected_value: int|None = st.number_input(
                "Ustaw wartość",
                step=1,
                format="%d",
                value=if_cmd.value 
                    if command and isinstance(command.value, int) 
                    else 0
            )

            selected_step_if_true: int|str|None = st.selectbox(
                "Skocz do:",
                [k for k in range(steps_count)] + ["koniec"],
                key="selected_step_if_true_for_value",
                index=(
                    step_to_selection_index(if_cmd.go_to_if_true, steps_count)
                    if command
                    else 0
                ),
            )

            selected_step_if_false: int|str|None = st.selectbox(
                "W przeciwnym razie skocz do:",
                [k for k in range(steps_count)] + ["koniec"],
                key="selected_step_if_false_for_value",
                index=(
                    step_to_selection_index(if_cmd.go_to_if_false, steps_count)
                    if command
                    else 0
                ),
            )

            if st.button("OK", key="value_selection_submit_btn"):
                if not box:
                    st.error("Wybierz pudełko!")
                elif command:
                    if_cmd.box = cast(Box, box)
                    if_cmd.value = selected_value
                    if_cmd.condition = cast(Condition, condition)
                    if_cmd.go_to_if_true = selected_step_if_true
                    if_cmd.go_to_if_false = selected_step_if_false
                    st.rerun()
                else:
                    self.asembler.add_if(
                        cast(Box, box),
                        cast(Condition, condition.replace("\\", "") if condition else condition),
                        selected_value,
                        selected_step_if_true,
                        selected_step_if_true,
                    )
                    st.rerun()

    @st.dialog("Skocz do")
    def go_to(self, command: Command|None = None):         
        go_to_cmd: GoTo = cast(GoTo, command)

        steps_count: int = self.asembler.command_count
        
        selection: int|str|None = st.selectbox(
        "Wybierz krok",
        [k for k in range(steps_count)] + ["koniec"],
        index=step_to_selection_index(go_to_cmd.value, steps_count) if command else 0,
        )

        if st.button("OK") and selection is not None:
            if command:
                go_to_cmd.value = selection
                st.rerun()
            else:
                self.asembler.add_go_to(selection)
                st.rerun()
