import streamlit as st
import pandas as pd
import time

#----------------------------------
# Load Questions Information
#----------------------------------

def load_questions_info(id_screen: int):

    path = f"data/screen{id_screen}_questions.csv"
    df = pd.read_csv(path, header = None, sep = ";")

    return df

#--------------------------------------------------
# Helper Functions
#--------------------------------------------------

def all_responded(responses_dict):
    """Verifica que todas las preguntas hayan sido contestadas."""
    for _, value in responses_dict.items():
        if value == "" or value is None:
            return False
    return True

#--------------------------------------------------
# Question Widgets Generation
#--------------------------------------------------

def generate_question_widget(question_col_list, key_widget: str):
    """Genera el widget correspondiente según el tipo de pregunta."""
    
    question_type = question_col_list[0] #Selectbox o Number Input
    question_key = question_col_list[1] #Clave para almacenar la respuesta
    question_label = question_col_list[2] #Etiqueta de la pregunta

    if question_type == "title":
        st.title(question_label)
        return {}
    
    elif question_type == "selectbox":
        options = [opt for opt in question_col_list[3:] if pd.notna(opt)]
        response = selectbox_question(
            label=question_label,
            options=options,
            key= key_widget
        )
        
    elif question_type == "number_input":
        min_value = int(question_col_list[3])
        max_value = int(question_col_list[4])
        response = number_input_question(
            label=question_label,
            min_value=min_value,
            max_value=max_value,
            key= key_widget
        )

    return {question_key: response}

def selectbox_question(label: str, options: list, key: str):
    st.subheader(label)
    selectbox = st.selectbox(
        label="",
        options=[""] + options,
        key=key
    )
    return selectbox

def number_input_question(label: str, min_value: int, max_value: int, key: str):
    st.subheader(label)
    number_input = st.number_input(
        value = None,
        label="",
        key=key,
        min_value=min_value,
        max_value=max_value,
        step=1
    )
    return number_input

#--------------------------------------------------
# Button for Next Screen
#--------------------------------------------------

def screen_button(id_screen: int):

    def set_true_state_variable(id_screen: int):
        st.session_state[f"screen{id_screen}_completed"] = True
        st.session_state[f"time_list"].append(time.time())

    st.button(
        label="Siguiente",
        key=f"screen{id_screen}_button",
        use_container_width= True,
        on_click=set_true_state_variable,
        args=(id_screen,)
    )


#--------------------------------------------------
# Main Function for Screen
#--------------------------------------------------

def generate_general_screen(id_screen: int):

    # Information Questions DataFrame
    questions_df = load_questions_info(id_screen)
    n_questions = len(questions_df.columns) - 1 # Number of questions

    # Screen Responses Dictionary
    responses_dict = {}

    # Questions
    for i in range(1, n_questions + 1):

        question_col_list = questions_df.iloc[:, i].tolist() # Question Information List
        key_widget = f"s{id_screen}_q{i}" # Key for the widget
        question_widget = generate_question_widget(question_col_list, key_widget) # Generate Question Widget
        
        responses_dict.update(question_widget) # Update Responses Dictionary

    # Store answers in the state variable 'responses'
    st.session_state["responses"][f"screen{id_screen}"] = responses_dict

    if all_responded(responses_dict):
        screen_button(id_screen)

