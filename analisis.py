import streamlit as st
import pandas as pd
import plotly.express as px

def view_analysis():
    df = st.session_state.df
    if not df.empty:
        st.subheader('Competencies data')
        st.dataframe(df, height=200)

        df['date_df-format'] = pd.to_datetime(df['Date'])
        df['fiscal_year'] = df['date_df-format'].apply(lambda x: x.year if x.month >= 4 else x.year - 1)
        df_years = sorted(df['fiscal_year'].dropna().unique())
        year_selection = st.number_input('Fiscal year', min_value=min(df_years), max_value=max(df_years), value=max(df_years), step=1, format='%d')
        filtered_df = df[df['fiscal_year'].isin([year_selection])]

        level_counts = filtered_df.groupby(['Competency', 'Level']).size().reset_index(name='Count')
        fig1 = px.bar(level_counts, x='Competency', y='Count', color='Level', title='Actions per competency', barmode='stack')
        fig1.update_layout(yaxis=dict(tickformat=',d', dtick=1))
        st.plotly_chart(fig1)

        level_avg = filtered_df.groupby('Competency')['Level'].mean().reset_index()
        fig2 = px.bar(level_avg, x='Competency', y='Level', title='Average level per competency', labels={'Level': 'Average level'}, color='Competency')
        fig2.update_layout(yaxis=dict(tickformat='.2f'))
        st.plotly_chart(fig2)

        filtered_df['Month'] = filtered_df['date_df-format'].dt.to_period('M').astype(str)
        monthly_counts = filtered_df.groupby(['Month', 'Competency']).size().reset_index(name='Count')
        monthly_counts['Month'] = pd.to_datetime(monthly_counts['Month'])
        monthly_counts = monthly_counts.sort_values('Month')
        monthly_counts['Month'] = monthly_counts['Month'].dt.strftime('%B')
        fig3 = px.bar(monthly_counts, x='Month', y='Count', color='Competency', title='Monthly actions per competency', barmode='stack')
        st.plotly_chart(fig3)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download csv', csv, file_name='competencies.csv', mime='text/csv')
    else:
        st.info('No data available')