from datetime import datetime
from time import sleep
from io import StringIO

import streamlit as st

from asembler import Asembler, MAX_STEP


class Start:

    def __init__(self):

        self.asembler: Asembler = st.session_state.asembler

        with st.container(horizontal=True, horizontal_alignment="left"):
            st.button(
                "Uruchom",
                icon="⏯️",
                disabled=self.asembler.is_running or self.asembler.command_count==0,
                on_click=self.asembler.start,
            )
            st.button(
                "Zrób krok",
                icon="⏭️",
                disabled=not self.asembler.is_running,
                on_click=self.asembler.next_step,
            )
            st.button(
                "Idź do końca",
                icon="⏩",
                disabled=not self.asembler.is_running,
                on_click=self.asembler.fast_forward,
            )
            st.button(
                "Stop",
                icon="🛑",
                type="primary",
                disabled=not self.asembler.is_running,
                on_click=self.asembler.stop,
            )

            st.button(
                "Nowy",
                icon="🆕",
                type="secondary",
                on_click=self.new_program,
                disabled=self.asembler.is_running
            )
            st.button(
                "Edytuj",
                icon="🛠️",
                type="primary",
                on_click=self.go_to_edit,
                disabled=self.asembler.is_running
            )

            st.download_button(
                "Pobierz do pliku",
                icon="⤵️",
                mime="text/txt",
                data=self.get_file_content(),
                file_name=self.get_file_name(),
            )

            st.button(
                "Załaduj z pliku",
                icon="⤴️",
                on_click=self.upload_program,
                disabled=self.asembler.is_running
            )

        if self.asembler.is_max_step_exceeded:
            st.error(f"Wykonano ponad {MAX_STEP} kroków. Sprawdź program: może zawierać pętlę nieskończoną.")

        boxes, code, console = st.columns([1, 3, 2])

        with boxes.container(border=True):
            st.header("Pudełka")

            for key, val in self.asembler.boxes.items():

                st.metric(label=f"Pudełko {key}", value=val)

        with code.container(border=True):
            st.header("Program")

            if self.asembler.step_counter:
                st.text(f"Wykonano {self.asembler.step_counter} kroków.")

            with st.container(
                horizontal_alignment="left",
                horizontal=True):

                st.subheader("Krok", width=90)
                st.subheader("Polecenie", width="stretch")

            for id, cmd in enumerate(self.asembler.program):

                with st.container(
                    horizontal_alignment="left",
                    horizontal=True,
                    key=f"{id}_program_line"
                ):
                    st.text("➡️" if self.asembler.current_step == id else "", width=20)
                    st.text(id, width=60)
                    st.text(cmd.label, width="stretch")

        with console.container(border=True):
            st.header("Konsola")

            for persona, msg in self.asembler.console_messages:
                with st.chat_message(persona):
                    st.text(msg)

    def go_to_edit(self):
        st.session_state.view = "edit"

    @st.dialog("Załaduj program z pliku")
    def upload_program(self):
        
        file = st.file_uploader("Wybierz plik")
        
        if file is not None:
            data: str = StringIO(file.getvalue().decode("utf-8")).read()
            self.asembler.from_json(data)
            st.rerun()

    def get_file_content(self):

        data: bytes = self.asembler.to_json().encode("utf-8")
        
        return data
    
    def get_file_name(self):

        sufix: str = datetime.now().strftime(r"%Y%m%d%H%M%S")
        file_name: str = f"program_{sufix}.txt"

        return file_name
    
    def new_program(self):

        if self.asembler.program:
            self.new_confirmation()

    @st.dialog("Potwierdź skasowanie programu")
    def new_confirmation(self):
        
        if st.button("Tak, skasuj", type="primary"):
            self.asembler.new()
            st.rerun()

