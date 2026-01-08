import streamlit as st
import pandas as pd

#--------------------------------------------------
# Questions for Screen 1
#--------------------------------------------------



def id_encuestador_selectbox():

    #Cargar lista de encuestadores
    encuestadores_csv_path = "data/encuestadores.csv"
    encuestadores_df = pd.read_csv(encuestadores_csv_path)
    encuestadores_list = [""] + encuestadores_df["Encuestador"].tolist()

    selectbox = st.selectbox(
        label="Encuestador",
        options=encuestadores_list,
        key="id_encuestador_selectbox")

    return selectbox


#--------------------------------------------------
# Helper Functions
#--------------------------------------------------

def all_responded(responses_dict):
    """Verifica que todas las preguntas hayan sido contestadas."""
    for _, value in responses_dict.items():
        if value == "":
            return False
    return True


#--------------------------------------------------
# Button for Next Screen
#--------------------------------------------------

def screen1_button():

    def set_true_state_variable(var_name: str):
        st.session_state[var_name] = True

    button = st.button(
        label="Siguiente",
        key="boton_id_encuestador",
        use_container_width= True,
        on_click=set_true_state_variable,
        args=("id_encuestador",)
    )
    return button


#--------------------------------------------------
# Main Function for Screen 1
#--------------------------------------------------

def screen1_main():

    # Título de la pantalla
    st.title("Encuestador y Lugar de Encuesta")

    # Diccionario de respuestas
    responses_dict = {}

    # Preguntas
    responses_dict["id_encuestador"] = id_encuestador_selectbox()

    # Almacenar respuestas en la variable de estado 'responses'
    st.session_state["responses"]["screen1"] = responses_dict

    if all_responded(responses_dict):
        screen1_button()

