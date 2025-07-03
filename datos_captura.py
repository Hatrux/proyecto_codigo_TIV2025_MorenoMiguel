import streamlit as st
import pandas as pd
from datos_carga import data_save

def view_capture():
    st.title('Capture actions')
    with st.form('competencies_form'):
        col1, col2 = st.columns(2)
        with col1:
            competency = st.selectbox('Competency', ['Communication', 'Teamwork', 'Human development', 'Quality first', 'On-site verification', 'Kaizen', 'Vision', 'Creativity', 'Challenge'])
            level = st.slider('Level', min_value=1, max_value=6)
        with col2:
            action = st.text_input('Action description')
            date = st.date_input('Date: ')
        submitted = st.form_submit_button('Capture action')

        if submitted:
            if isinstance(action, str) and action.strip() != "":
                new = {
                    'Competency': competency,
                    'Level': level,
                    'Action description': action,
                    'Date': date,
                }
                st.session_state.competencies.append(new)
                st.success('Action captured')
                st.write(f"""
                Competency: {competency}  
                Level: {level}  
                Action description: {action}  
                Date: {date}
                """)
                st.session_state.df = pd.DataFrame(st.session_state.competencies)
                data_save()
            else:
                st.error("Submit a valid action description")