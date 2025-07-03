import streamlit as st
from datos_carga import data_load
from datos_captura import view_capture
from analisis import view_analysis

st.set_page_config(page_title='My DENSO Spirit', page_icon='Denmaru.png', layout='wide', initial_sidebar_state='auto')

def main():
    data_load()
    st.sidebar.title('Menu')
    option = st.sidebar.selectbox('Go to:', ['Capture actions', 'Data analysis'])
    if option == 'Capture actions':
        view_capture()
    elif option == 'Data analysis':
        view_analysis()

if __name__ == "__main__":
    main()