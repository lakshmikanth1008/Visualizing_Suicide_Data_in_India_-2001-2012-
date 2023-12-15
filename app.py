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
st.sidebar.info("Customize your analysis:")
st.sidebar.write("1. Select one or more states from the 'Select State(s)' filter. By default it is Andhra pradesh, customize according to your analysis")

state_names=list(data['State'].unique())
# st.write(state_names)

selected_state = st.sidebar.multiselect('Select State(s):', data['State'].unique(),default=['Andhra Pradesh'])
st.sidebar.write("2. Select one or more groups from the 'Select Age_group(s)' filter.By default it is 0-100+, customize according to your analysis")
selected_age_group=st.sidebar.multiselect('Select Age_group(s):',data['Age_group'].unique(),default=['0-100+'])
if not selected_state or not selected_age_group:
    st.warning("Please select at least one option for State and Age_group.")

else:
    filtered_data = data[data['State'].isin(selected_state)]

    tab1, tab2, tab3,tab4,tab5 = st.tabs(["State Wide Suicide Count By Age_Group", "Type of Suicide By State", "Suicide Statistics Analysis by Gender","Suicides Statistics Analysis by Year and Age_group","Suicide Trends (2001-2012)"])
    with tab1:
        st.header("States Wide Suicide Count by Age_group")
        st.markdown(
        "Welcome to Tab1 - **State-Wide Suicide Count By Age_Group**. In this section, we delve into the comprehensive analysis of suicide counts "
        "across various states and age groups from 2001 to 2012. This interactive exploration empowers you to select specific states and age groups, "
        "revealing nuanced insights into the trends and patterns of suicides across different demographic categories. "
        )
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
        text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=0,
        dy=-5  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
        text='Total:Q'
        )   


        # Display the bar chart
        st.altair_chart(chart+text, use_container_width=True)
        st.write(filtered_grouped_data)
    with tab2:
        st.header("Type of Suicides based on State")
        st.markdown(
        "Welcome to **Suicide Explorer**, where we not only dissect the trends in suicide rates but also delve into the diverse landscape of suicide types. "
        "In this tab, we focus on understanding the nuanced prevalence of suicide types in different states across India. "
        "Select a specific state from the sidebar, and witness the power of visualization through our Word Cloud representation. "
        "Each word in the cloud signifies a different suicide type, with size reflecting its frequency. "
        "Embark on this insightful journey to gain a comprehensive understanding of the distribution of suicide types, "
        "unraveling a crucial layer in the complex tapestry of suicide data.")
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
        st.markdown(
        "Welcome to the **Suicide Statistics Analysis by Gender** tab. This section is dedicated to unraveling the intricate dynamics of "
        "suicides, focusing on the lens of gender. Explore how different demographic combinations shape gender-specific patterns and "
        "gain a comprehensive overview of suicide statistics for the years 2001 to 2012. Interact with the filters to analyze the count of "
        "suicides for each gender, considering the selected age group and state. Your journey into understanding gender-related suicide "
        "trends starts here."
        )
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
        st.markdown(
        "Welcome to the insightful world of **Suicides Statistics Analysis by Year and Age_group**. In this tab, we present a heatmap visualization "
        "that offers a unique perspective on the distribution of suicides for the selected years and age groups. Dive into the data, explore the intricate "
        "patterns, and witness how the number of suicides unfolds across different age groups and years. The heatmap provides an interactive canvas, "
        "enabling you to unravel trends, identify correlations, and gain a comprehensive understanding of the complex landscape of suicide statistics. "
        "Use the intuitive interface to interact with the heatmap, allowing it to unveil the stories hidden within the numbers."
        )

        selected_year = st.multiselect('Select Year:(By default it is 2001, customize according to your analysis)', data['Year'].unique(),default=[2001])
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
        st.markdown(
        "Welcome to the **Trend of Suicides from 2001 to 2012** tab. In this section, we delve into the dynamic landscape of suicides "
        "in India over the twelve-year period from 2001 to 2012. The interactive line chart below serves as your window into the evolving trends. "
        "Each point on the line carries the weight of a specific year, allowing you to visually trace the highs and lows, discern patterns, "
        "and gain valuable insights into the overarching narrative of this critical timeframe. Hover over the chart to unveil detailed information, "
        "and explore suicide count trends over the years. Let's embark on this journey of exploration and understanding."
        )
        grouped_data4['Year'] = grouped_data4['Year'].astype(str).str.replace(',', '')
        st.title("Trend of suicides from 2001 to 2012.")
        line_chart=alt.Chart(grouped_data4).mark_line(point=True).encode(
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






