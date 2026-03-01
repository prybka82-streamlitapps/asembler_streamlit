import streamlit as st

from views.start_view import Start
from views.edit_view import Edit
from asembler import Asembler


st.set_page_config("Asembler", page_icon="💻", layout="wide")

if "view" not in st.session_state:
    st.session_state.view = "main"

if "asembler" not in st.session_state:
    st.session_state.asembler = Asembler()


match st.session_state.view:

    case "main":
        Start()

    case "edit":

        Edit()
