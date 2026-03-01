from typing import cast

import streamlit as st

from asembler import Asembler, Box
from components.command_edit_dialog import CommandEditDialog


class CommandContainer:

    def __init__(self, asembler: Asembler):

        self.asembler = asembler
        self.edit_dialog: CommandEditDialog = CommandEditDialog(asembler)

        st.button("Wypisz pudełko", icon="📤", on_click=self.edit_dialog.write_box)
        st.button("Wypisz napis", icon="✒️", on_click=self.edit_dialog.write_text)
        st.button("Przejdź do nowej linii", icon="⤵️", on_click=self.edit_dialog.new_line)
        st.button("Wczytaj do pudełka", icon="⌨️", on_click=self.edit_dialog.read_to_box)
        st.button("Ustaw pudełko na", icon="📥", on_click=self.edit_dialog.set_box)
        st.button("Zwiększ pudełko o", icon="⬆️", on_click=self.edit_dialog.increase)
        st.button("Zmniejsz pudełko o", icon="⬇️", on_click=self.edit_dialog.decrease)
        st.button("Jeżeli", icon="🔀", on_click=self.edit_dialog.if_)
        st.button("Skocz do", icon="⏩", on_click=self.edit_dialog.go_to)
