import streamlit as st
import altair as alt
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS

data = pd.read_csv("Suicides in India 2001-2012.csv")
st.set_page_config(layout="wide")

st.markdown("# Visualization of Suicides data in India 2001-2012")
columns=data.columns

st.sidebar.header("Suicides data of India")
state_names=list(data['State'].unique())
# st.write(state_names)
words_to_remove = ["Causes known", "Causes", "means (please specify)","known","(Please Specity)", "Others","means"," (Please Specify) ","(Please Specity)","Please"]  # Add your own words to remove

stop_words = set(STOPWORDS)
data['Type'] = data['Type'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
data['Type'] = data['Type'].apply(lambda x: ' '.join([word for word in x.split() if word not in words_to_remove]))

selected_state = st.sidebar.multiselect('Select a State', data['State'].unique(),default=['Total (All India)'])
filtered_data = data[data['State'].isin(selected_state)]
grouped_data = data.groupby(['State','Age_group'])['Total'].sum().reset_index()
filtered_grouped_data = grouped_data[grouped_data['State'].isin(selected_state)]

grouped_data2 = data.groupby(['State','Gender'])['Total'].sum().reset_index()
filtered_grouped_data2 = grouped_data2[grouped_data2['State'].isin(selected_state)]


tab1, tab2, tab3 = st.tabs(["State Wide Suicide Count By Age_Group", "Type of Suicide By State", "Suicide Statistics Analysis by Gender"])
with tab1:
    st.header("States Wide Suicide Count")
    st.markdown(f"#### Suicide count for {', '.join(selected_state)}")
    chart = alt.Chart(filtered_grouped_data).mark_bar().encode(
    x='State',
    y=alt.Y('Total:Q', title='Sum of Total Suicides'),  
    color='Age_group:N',
    tooltip=['State', 'Total']
    )

    # Display the bar chart
    st.altair_chart(chart, use_container_width=True)
    st.write(filtered_grouped_data)
with tab2:
    st.header("Suicide Type Wordcloud")
    text = ' '.join(filtered_data['Type'])

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Plot the word cloud
    st.markdown(f"#### Suicide Types for {', '.join(selected_state)}")

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Display the filtered data
    st.write(f'Suicide Data for {selected_state}:')
    st.write(filtered_data)

with tab3:
    st.markdown(f"#### Count of Each Gender Suicides for {', '.join(selected_state)}")
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