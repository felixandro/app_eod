import streamlit as st

from src.time_utils import process_time_list, record_datetime
from src.database import send_to_database

import ui.general_screen as gs
import ui.od_screen as od
import ui.restart_screen as rs



# --------------------------------------------------
# Configuración general de la app
# --------------------------------------------------
st.set_page_config(
    page_title = "EOD",
    layout="centered",
    initial_sidebar_state="auto"
)

# --------------------------------------------------
# Variables de Estado
# --------------------------------------------------

# Variables de estado para controlar la navegación entre pantallas

# Screen1: Encuestador y Lugar de Encuesta
if "screen1_completed" not in st.session_state:
    st.session_state["screen1_completed"] = False

# Screen2: Características del Usuario
if "screen2_completed" not in st.session_state:
    st.session_state["screen2_completed"] = False

# Screen3: Características del Viaje
if "screen3_completed" not in st.session_state:
    st.session_state["screen3_completed"] = False

# OD Screen: Origen y Destino del Viaje
if "od_screen_completed" not in st.session_state:
    st.session_state["od_screen_completed"] = False

# Screen5: Categoría de Usuario
if "screen5_completed" not in st.session_state:
    st.session_state["screen5_completed"] = False

# Variable para almacenar las respuestas

if "responses" not in st.session_state:
    st.session_state["responses"] = {}

# Variable para almacenar la hora de inicio en cada pantalla
if "time_list" not in st.session_state:
    st.session_state["time_list"] = []

if "responses_sent" not in st.session_state:
    st.session_state["responses_sent"] = False

# --------------------------------------------------
# Pantalla 1 // Encuestador y Lugar de Encuesta
# --------------------------------------------------

if not st.session_state["screen1_completed"]:

    gs.generate_general_screen(id_screen=1)


if st.session_state["screen1_completed"] and not st.session_state["screen2_completed"]:

    record_datetime()

    gs.generate_general_screen(id_screen=2)

if st.session_state["screen2_completed"] and not st.session_state["screen3_completed"]:

    gs.generate_general_screen(id_screen=3)

if st.session_state["screen3_completed"] and not st.session_state["od_screen_completed"]:

    od.generate_od_screen()

if st.session_state["od_screen_completed"] and not st.session_state["screen5_completed"]:

    gs.generate_general_screen(id_screen=5)

if st.session_state["screen5_completed"]:

    process_time_list()

    #Enviar Respuestas a BBDD online
    if not st.session_state["responses_sent"]:
        send_to_database(st.session_state["responses"])

    rs.generate_restart_screen()


st.divider()
st.write(st.session_state["responses"])

