import requests
import streamlit as st


def georreferenciar(direccion):
    print("Georreferenciando dirección:", direccion)

    # URL base para la API de geocodificación de Google Maps
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    # Parámetros de la solicitud
    params = {
        'address': direccion,
        'key': st.secrets["api_key"]
    }
    
    # Realizar la solicitud GET
    respuesta = requests.get(url, params=params)

    # Verificar si la solicitud fue exitosa
    if respuesta.status_code == 200:
        datos = respuesta.json()
        
        # Si la respuesta tiene resultados, obtener la latitud y longitud
        if datos['status'] == 'OK':
            latitud = datos['results'][0]['geometry']['location']['lat']
            longitud = datos['results'][0]['geometry']['location']['lng']
            return latitud, longitud
        else:
            return None
    else:
        return None