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

selected_state = st.sidebar.multiselect('Select a State', data['State'].unique(),default=['Total (All India)'])
filtered_data = data[data['State'].isin(selected_state)]
grouped_data = data.groupby(['State','Age_group'])['Total'].sum().reset_index()
filtered_grouped_data = grouped_data[grouped_data['State'].isin(selected_state)]

tab1, tab2, tab3 = st.tabs(["Bar chart visualization of State Wide Suicide Count", "WordCloud visualization of Suicide Type", "Tab3"])
with tab1:
    st.header("Visualization of State Wide Suicide Count")
    chart = alt.Chart(filtered_grouped_data).mark_bar().encode(
    x='State',
    y=alt.Y('Total:Q', title='Sum of Total Suicides'),  
    color='Age_group:N',
    tooltip=['State', 'Total']
    ).properties(
    title=f'Total Suicide Records by {selected_state}'
    )

    # Display the bar chart
    st.altair_chart(chart, use_container_width=True)
    st.write(filtered_data)
with tab2:
    st.header("Visualization of Suicide Type")
    text = ' '.join(filtered_data['Type'])

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Plot the word cloud
    st.write(f'Suicide Types Word Cloud for {selected_state}')
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Display the filtered data
    st.write(f'Suicide Data for {selected_state}:')
    st.write(filtered_data)

with tab3:
   st.header("Visualization")
