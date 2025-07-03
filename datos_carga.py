import os
import pandas as pd
import streamlit as st

def data_load():
    path = os.path.join(os.getcwd(), 'competencies.csv')
    try:
        df = pd.read_csv(path)
        st.session_state.df = df
        if 'competencies' not in st.session_state:
            st.session_state.competencies = df.to_dict(orient='records')
    except FileNotFoundError:
        st.session_state.competencies = []
        st.session_state.df = pd.DataFrame(columns=['Competency', 'Level', 'Action', 'Date'])
        st.session_state.df.to_csv(path, index=False)

def data_save():
    path = os.path.join(os.getcwd(), 'competencies.csv')
    st.session_state.df.to_csv(path, index=False)