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

# Screen21: Características del Usuario (Automóvil Particular)
if "screen21_completed" not in st.session_state:
    st.session_state["screen21_completed"] = False

# Screen22: Características del Usuario (Bus)
if "screen22_completed" not in st.session_state:
    st.session_state["screen22_completed"] = False

# Screen23: Características del Usuario (Tren)
if "screen23_completed" not in st.session_state:
    st.session_state["screen23_completed"] = False

# Screen3: Características del Viaje
if "screen3_completed" not in st.session_state:
    st.session_state["screen3_completed"] = False

# Screen31: Características del Viaje (Automóvil Particular)
if "screen31_completed" not in st.session_state:
    st.session_state["screen31_completed"] = False

# Screen32: Características del Viaje (Bus)
if "screen32_completed" not in st.session_state:
    st.session_state["screen32_completed"] = False

# Screen33: Características del Viaje (Tren)
if "screen33_completed" not in st.session_state:
    st.session_state["screen33_completed"] = False

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
# Screen 1 // Encuestador y Lugar de Encuesta
# --------------------------------------------------

if not st.session_state["screen1_completed"]:

    gs.generate_general_screen(id_screen=1)

# --------------------------------------------------
# Screen 2 // Características del Usuario
# --------------------------------------------------

screen_2x_completed = any([
    st.session_state["screen21_completed"],
    st.session_state["screen22_completed"],
    st.session_state["screen23_completed"]
])

if st.session_state["screen1_completed"] and not screen_2x_completed:

    record_datetime()

    tipo_veh = st.session_state["responses"]["screen1"]["pc"].split()[0]

    if tipo_veh == "Terminal":
        gs.generate_general_screen(id_screen=22)

    elif tipo_veh == "Estación":
        gs.generate_general_screen(id_screen=23)

    else:
        gs.generate_general_screen(id_screen=21)


# --------------------------------------------------
# Screen 3 // Características del Viaje
# --------------------------------------------------

screen_3x_completed = any([
    st.session_state["screen31_completed"],
    st.session_state["screen32_completed"],
    st.session_state["screen33_completed"]
])

if screen_2x_completed and not screen_3x_completed:

    tipo_veh = st.session_state["responses"]["screen1"]["pc"].split()[0]

    if tipo_veh == "Terminal":
        gs.generate_general_screen(id_screen=32)

    elif tipo_veh == "Estación":
        gs.generate_general_screen(id_screen=33)

    else:
        gs.generate_general_screen(id_screen=31)

# --------------------------------------------------
# OD Screen // Origen y Destino del Viaje
# --------------------------------------------------

if screen_3x_completed and not st.session_state["od_screen_completed"]:

    od.generate_od_screen()

# --------------------------------------------------
# Screen 5 // Categoría de Usuario
# --------------------------------------------------

if st.session_state["od_screen_completed"] and not st.session_state["screen5_completed"]:

    gs.generate_general_screen(id_screen=5)

# --------------------------------------------------
# Restart Screen // Nueva Encuesta
# --------------------------------------------------

if st.session_state["screen5_completed"]:

    process_time_list()

    #Enviar Respuestas a BBDD online
    if not st.session_state["responses_sent"]:
        send_to_database(st.session_state["responses"])

    rs.generate_restart_screen()


st.divider()
#st.write(st.session_state["responses"])

