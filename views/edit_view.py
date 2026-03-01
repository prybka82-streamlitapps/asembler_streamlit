from typing import cast

import streamlit as st

from asembler import Asembler
from components.code_container import CodeContainer
from components.command_container import CommandContainer


class Edit:

    def __init__(self):

        self.asembler: Asembler = st.session_state.asembler

        with st.container(horizontal_alignment="left", horizontal=True):
            st.button("◀️ Wróć", on_click=self.go_to_main)

        code, commands = st.columns([7, 3])
        
        with code.container(border=True, key="code_container"):
            st.header("Program")

            CodeContainer(self.asembler)

        with commands.container(border=True, key="commands_container"):
            st.header("Polecenia")

            CommandContainer(self.asembler)

    def go_to_main(self):
        st.session_state.view = "main"
