import streamlit as st
import altair as alt
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

data = pd.read_csv("Suicides in India 2001-2012.csv")
st.set_page_config(layout="wide")

st.markdown("# Visualization of Suicides data in India 2001-2012")
columns=data.columns

st.sidebar.header("Suicides data of India")
state_names=list(data['State'].unique())
# st.write(state_names)

selected_state = st.sidebar.multiselect('Select a State:', data['State'].unique(),default=['Andhra Pradesh'])
selected_age_group=st.sidebar.multiselect('Select a Age_group:',data['Age_group'].unique(),default=['0-100+'])
if not selected_state or not selected_age_group:
    st.warning("Please select at least one option for State.")

else:
    filtered_data = data[data['State'].isin(selected_state)]

    tab1, tab2, tab3,tab4,tab5 = st.tabs(["State Wide Suicide Count By Age_Group", "Type of Suicide By State", "Suicide Statistics Analysis by Gender","Suicides Statistics Analysis by Year and Age_group","Suicide Trends (2001-2012)"])
    with tab1:
        st.header("States Wide Suicide Count by Age_group")
        grouped_data = data.groupby(['State','Age_group'])['Total'].sum().reset_index()
        filtered_grouped_data = grouped_data[grouped_data['State'].isin(selected_state) & grouped_data['Age_group'].isin(selected_age_group)]
        filtered_data['Year'] = filtered_data['Year'].astype(str).str.replace(',', '')

        st.markdown(f"###### Suicide count for {', '.join(selected_state)} and {', '.join(selected_age_group)}")
        chart = alt.Chart(filtered_grouped_data).mark_bar().encode(
        x='State',
        y=alt.Y('Total:Q', title='Sum of Total Suicides'),  
        color='Age_group:N',
        tooltip=['State', 'Total','Age_group']
        )

        # Display the bar chart
        st.altair_chart(chart, use_container_width=True)
        st.write(filtered_grouped_data)
    with tab2:
        st.header("Type of Suicides based on State")
        text = ' '.join(filtered_data['Type'])

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        # Plot the word cloud
        st.markdown(f"###### Suicide Types for {', '.join(selected_state)}")

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # Display the filtered data
        st.write(filtered_data)

    with tab3:
        st.header("Suicide Data Analysis By Gender")
        grouped_data2 = data.groupby(['State','Gender'])['Total'].sum().reset_index()
        filtered_grouped_data2 = grouped_data2[grouped_data2['State'].isin(selected_state)] 
        st.markdown(f"###### Count of Each Gender Suicides for {', '.join(selected_state)}")
        chart2 = alt.Chart(filtered_grouped_data2).mark_bar().encode(
        x='State:N',
        y=alt.Y('Total:Q', title='Sum of Total Suicides'),
        color='Gender:N'
        ).properties(
        width=600,
        height=400
        )
        st.altair_chart(chart2, use_container_width=True)
        st.write(filtered_grouped_data2)

    with tab4:
        st.header("Statistics of Suicides by Year and Age_group")
        selected_year = st.multiselect('Select a Year', data['Year'].unique())
        filtered_data_year=data[data['Year'].isin(selected_year)]
        grouped_data3= data.groupby(['Age_group','Year'])['Total'].sum().reset_index()
        filtered_grouped_data3 = grouped_data3[grouped_data3['Year'].isin(selected_year) & grouped_data3['Age_group'].isin(selected_age_group)]
        filtered_grouped_data3['Year'] = filtered_grouped_data3['Year'].astype(str).str.replace(',', '')

        heat_map = alt.Chart(filtered_grouped_data3).mark_rect().encode(
        x='Year:O',
        y='Age_group:O',
        color='Total:Q',
        tooltip=['Year:O', 'Age_group:N', 'Total:Q']
        ).properties(
        title='Suicide Statistics by Year using Heat Map',
        width=600,
        height=400
        )
        st.altair_chart(heat_map, use_container_width=True)
        st.write(filtered_grouped_data3)
    
    with tab5:
        grouped_data4= data.groupby(['Year'])['Total'].sum().reset_index()
        grouped_data4['Year'] = grouped_data4['Year'].astype(str).str.replace(',', '')
        st.title("Trend of suicides from 2001 to 2012.")
        line_chart=alt.Chart(grouped_data4).mark_line().encode(
        x='Year:N',
        y='Total:Q',
        tooltip=['Year:N', 'Total:Q']
        ).properties(
        width=600,
        height=400
        )

        # Display the line chart
        st.altair_chart(line_chart, use_container_width=True)
        st.write(grouped_data4)






