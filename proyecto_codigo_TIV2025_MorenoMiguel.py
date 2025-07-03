import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='My DENSO Spirit', page_icon='Denmaru.png', layout='wide', initial_sidebar_state='auto')

class associate:
    def __init__(self):
        path = os.path.join(os.getcwd(), 'competencies.csv') # "os.path.join" une la ruta "os.getcwd" (la ruta absoluta de este código) y la ruta relativa del csv

        try:
            df = pd.read_csv(path) # Carga info de csv a un DataFrame llamado "df"
            st.session_state.df = df # Asegura persistencia de "df"
            if 'competencies' not in st.session_state: # Evita que la información ingresada por el usuario (en caso de haber) se sobreescriba con la info del csv
                st.session_state.competencies = df.to_dict(orient='records')
        except FileNotFoundError:
            st.session_state.competencies = [] #Inicializa el DataFrame
            st.session_state.df = pd.DataFrame(columns=['Competency', 'Level', 'Action', 'Date'])
            st.session_state.df.to_csv(path, index=False)  # Crear archivo .csv vacío
    
    def view_capture(self):
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
                    st.session_state.df = pd.DataFrame(st.session_state.competencies) # Actualizar DataFrame y asegurar que las gráficas muestre la última información
                    path = os.path.join(os.getcwd(), 'competencies.csv')
                    st.session_state.df.to_csv(path, index=False) # Guardar en csv sin índice
                else:
                    st.error("Submit a valid action description")
            
    def view_analysis(self):
        df = st.session_state.df
        if not df.empty:
            st.subheader('Competencies data')

            st.dataframe(st.session_state.df, height=200) # Mostrar un DataFrame como tabla en streamlit

            df['date_df-format'] = pd.to_datetime(df['Date']) # Transformar "Date" a formato Pandas
            df['fiscal_year'] = df['date_df-format'].apply(lambda x: x.year if x.month >= 4 else x.year - 1) # Transformar años calendario a años fiscales estableciendo el corte en abril
            df_years = sorted(df['fiscal_year'].dropna().unique()) # Crear DataFrame con valores únicos de años
            year_selection = st.number_input('Fiscal year', min_value=min(df_years), max_value=max(df_years), value=max(df_years), step=1, format='%d')
            filtered_df = df[df['fiscal_year'].isin([year_selection])] # Filtrar DataFrame por año seleccionado
            
            level_counts = filtered_df.groupby(['Competency', 'Level']).size().reset_index(name='Count')
            fig1 = px.bar(
                level_counts,
                x='Competency',
                y='Count',
                color='Level',
                title='Actions per competency',
                barmode='stack'
            )
            fig1.update_layout(yaxis=dict(tickformat=',d', dtick=1)) # Formatear eje y para mostrar sólo valores enteros y evitar valores repetidos como mostrar 0.5 como 1
            st.plotly_chart(fig1)

            level_avg = filtered_df.groupby('Competency')['Level'].mean().reset_index()
            fig2 = px.bar(
                level_avg,
                x='Competency',
                y='Level',
                title='Average level per competency',
                labels={'Level': 'Average level'},
                color='Competency'
            )
            fig2.update_layout(yaxis=dict(tickformat='.2f'))  # Mostrar dos decimales de los promedios
            st.plotly_chart(fig2)

            filtered_df['Month'] = filtered_df['date_df-format'].dt.to_period('M').astype(str) # Crear una columna con los meses
            monthly_counts = filtered_df.groupby(['Month', 'Competency']).size().reset_index(name='Count') # Agrupar por mes y competencias
            monthly_counts['Month'] = pd.to_datetime(monthly_counts['Month']) # Transformar "Month" a formato Pandas
            monthly_counts = monthly_counts.sort_values('Month') # Ordenar cronológicamente
            monthly_counts['Month'] = monthly_counts['Month'].dt.strftime('%B') # Formatear fechas para mostrar año y mes
            fig3 = px.bar(
                monthly_counts,
                x='Month',
                y='Count',
                color='Competency',
                title='Monthly actions per competency',
                barmode='stack'
            )
            st.plotly_chart(fig3)

            csv = df.to_csv(index=False).encode('utf-8') # Guarda la información en la variable csv
            st.download_button('Download csv', csv, file_name='competencies.csv', mime='text/csv') # Permite descargar el csv con la información filtrada. mime='text/csv' asegura que el explorador reconozca el formato del archivo
        else:
            st.info('No data available')
    
    def run(self):
        st.sidebar.title('Menu')
        option = st.sidebar.selectbox('Go to:', ['Capture actions', 'Data analysis'])
        if option == 'Capture actions':
            self.view_capture()
        elif option == 'Data analysis':
            self.view_analysis()
    
app = associate()
app.run()