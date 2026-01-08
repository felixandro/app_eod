import streamlit as st
import pandas as pd
import time
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import st_folium

from src.geocoding import georreferenciar

def get_surveyor_location():

    st.subheader("Ubicación del Encuestador")

    location = streamlit_geolocation()

    st.divider()

    if location["latitude"] and location["longitude"]:
        surveyor_location = {"surveyor_lat": location["latitude"], 
                             "surveyor_lon": location["longitude"],
                             "surveyor_acc": location["accuracy"]}
        return surveyor_location
    
    else:
        empty_surveyor_location = {"surveyor_lat": "", 
                                   "surveyor_lon": "",
                                   "surveyor_acc": ""}
        return empty_surveyor_location

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
# Location Question Widgets Generation
#--------------------------------------------------

def selectbox_question(label: str, options: list, key: str):
    selectbox = st.selectbox(
        label=label,
        options=[""] + options,
        key=key
    )
    return selectbox

def generate_location_question_widget(od):

    st.subheader(f"{od} del viaje")

    location_type = selectbox_question(
        label="Tipo de ubicación",
        options=["Dirección","Intersección","Hito"],
        key=f"{od}_location_type_selectbox"
    )

    adress = ""
    responses_dict = {f"{od}_comuna": ""}

    if location_type == "Dirección":
        adress, responses_dict = direction_input_question(od)

    elif location_type == "Intersección":
        adress, responses_dict = intersection_input_question(od)

    elif location_type == "Hito":
        adress, responses_dict = landmark_input_question(od)

    if adress != "":
        location = generate_geocode_button(od, adress)

    st.divider()

    return responses_dict

def direction_input_question(od):
    
    calle = st.text_input(
        label="Nombre de la Calle",
        key=f"{od}_direction_input"
    )

    nro_calle = st.text_input(
        label="Número",
        key=f"{od}_nro_calle_input"
    )

    comuna = st.text_input(
        label="Comuna",
        key=f"{od}_comuna_input"
    )

    if calle != "" and nro_calle != "" and comuna != "":
        adress = f"{calle} #{nro_calle}, {comuna}, Chile"
        responses_dict = {}
        responses_dict[f"{od}_calle"] = calle
        responses_dict[f"{od}_nro_calle"] = nro_calle
        responses_dict[f"{od}_comuna"] = comuna
        return adress, responses_dict
    
    else:
        empty_adress = ""
        empty_responses_dict = {}
        empty_responses_dict[f"{od}_calle"] = ""
        empty_responses_dict[f"{od}_nro_calle"] = ""
        empty_responses_dict[f"{od}_comuna"] = ""
        return empty_adress, empty_responses_dict

def intersection_input_question(od):
    calle1 = st.text_input(
        label="Calle 1",
        key=f"{od}_intersection_calle1_input"
    )
    calle2 = st.text_input(
        label="Calle 2",
        key=f"{od}_intersection_calle2_input"
    )
    comuna = st.text_input(
        label="Comuna",
        key=f"{od}_comuna_input"
    )

    if calle1 != "" and calle2 != "" and comuna != "":
        adress = f"{calle1} & {calle2}, {comuna}, Chile"
        responses_dict = {}
        responses_dict[f"{od}_calle1"] = calle1
        responses_dict[f"{od}_calle2"] = calle2          
        responses_dict[f"{od}_comuna"] = comuna
        return adress, responses_dict   
    else:
        empty_adress = ""
        empty_responses_dict = {}
        empty_responses_dict[f"{od}_calle1"] = ""
        empty_responses_dict[f"{od}_calle2"] = ""
        empty_responses_dict[f"{od}_comuna"] = ""
        return empty_adress, empty_responses_dict

def landmark_input_question(od):
    landmark = st.text_input(
        label="Nombre del Hito",
        key=f"{od}_landmark_input"
    )

    comuna = st.text_input(
        label="Comuna",
        key=f"{od}_comuna_input"
    )

    if landmark != "" and comuna != "":        
        adress = f"{landmark}, {comuna}, Chile"
        responses_dict = {}
        responses_dict[f"{od}_hito"] = landmark
        responses_dict[f"{od}_comuna"] = comuna
        return adress, responses_dict  
    
    else:
        empty_adress = ""
        empty_responses_dict = {}
        empty_responses_dict[f"{od}_hito"] = ""
        empty_responses_dict[f"{od}_comuna"] = ""
        return empty_adress, empty_responses_dict

#--------------------------------------------------
# Geocoding  Button
#--------------------------------------------------

def generate_geocode_button(od, adress: str):

    geocode_button = st.button(
                            label=f"Georreferenciar {od}",
                            key=f"geocode_{od}_button")
    
    if geocode_button:

        location = georreferenciar(adress)
        if location:
            st.session_state.coords_origen = location
            st.session_state.center_map_origen = location
            st.session_state.zoom_map_origen = 13

            map = folium.Map(location = st.session_state["center_map_origen"], 
                         zoom_start= st.session_state["zoom_map_origen"])

            if st.session_state.coords_origen:
                folium.Marker(
                    location=st.session_state.coords_origen,
                    popup=od,
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(map)

            st_folium(map, width=300, height = 300 ,returned_objects=[], key=f"map_{od}")

        else:
            st.error("No se encontró la ubicación")

        



#--------------------------------------------------
# Button for Next Screen
#--------------------------------------------------

def od_screen_button():

    def set_true_state_variable():
        st.session_state["od_screen_completed"] = True
        st.session_state["time_list"].append(time.time())

    st.button(
        label="Siguiente",
        key="od_screen_button",
        use_container_width= True,
        on_click=set_true_state_variable
    )

#--------------------------------------------------
# Main Function for Screen
#--------------------------------------------------


def generate_od_screen():
    st.title("Origen y Destino del Viaje")


    # Screen Responses Dictionary
    responses_dict = {}

    # Surveyor Location
    surveyor_location = get_surveyor_location()
    responses_dict.update(surveyor_location)

    # Origin Question
    origin_responses_dict = generate_location_question_widget(od="Origen")
    responses_dict.update(origin_responses_dict)

    # Destination Question
    destination_responses_dict = generate_location_question_widget(od="Destino")
    responses_dict.update(destination_responses_dict)

    

    # Store answers in the state variable 'responses'
    st.session_state["responses"][f"od_screen"] = responses_dict

    if all_responded(responses_dict):
        od_screen_button()