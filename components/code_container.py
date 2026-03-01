from typing import cast

import streamlit as st

from asembler import Asembler
from models.command import Command
from components.command_edit_dialog import CommandEditDialog
from models.go_to import GoTo
from models.if_ import If


class CodeContainer:

    def __init__(self, asembler: Asembler):

        self.asembler: Asembler = asembler
        self.dialog: CommandEditDialog = CommandEditDialog(asembler)

        with st.container(
            horizontal_alignment="left",
            horizontal=True):

            st.subheader("Krok", width=60)
            st.subheader("Polecenie", width="stretch")

        cmd_count: int = asembler.command_count-1

        for id, cmd in enumerate(asembler.program):

            cmd: Command = cmd
            edit_dialog = self.dialog.find_dialog(cmd)

            with st.container(
                horizontal_alignment="left",
                horizontal=True,
                key=f"{id}_program_line"):

                st.text(id, width=60)
                st.text(cmd.label, width="stretch")
                st.button(
                    "🔼",
                    key=f"{id}_up_line_btn",
                    disabled=(id==0),
                    on_click=self.move_cmd_up,
                    args=[id],
                    help="Przesuń polecenie w górę",
                )
                st.button(
                    "🔽",
                    key=f"{id}_down_line_btn",
                    disabled=(id==cmd_count),
                    on_click=self.move_cmd_down,
                    args=[id],
                    help="Przesuń polecenie w dół",
                )
                st.button(
                    "🪛",
                    key=f"{id}_edit_line_btn",
                    on_click=edit_dialog,
                    args=[cmd],
                    disabled="do nowej linii" in cmd.label,
                    help="Zmień polecenie",
                )
                st.button(
                    "❌",
                    key=f"{id}_delete_line_btn",
                    on_click=self.delete_cmd,
                    args=[id],
                    help="Usuń polecenie",
                )

    def move_cmd_up(self, id: int):

        self.asembler.move_cmd_up(id)

    def move_cmd_down(self, id: int):

        self.asembler.move_cmd_down(id)

    def delete_cmd(self, id: int):

        for cmd_id, cmd in enumerate(self.asembler.program):
            if not cmd.contains_step or cmd_id == id:
                continue

            if hasattr(cmd, "value"):
                setattr(cmd, "value", -1)

            elif hasattr(cmd, "go_to_if_true"):
                setattr(cmd, "go_to_if_true", -1)

            elif hasattr(cmd, "go_to_if_false"):
                setattr(cmd, "go_to_if_false", -1)

        self.asembler.delete_cmd(id)