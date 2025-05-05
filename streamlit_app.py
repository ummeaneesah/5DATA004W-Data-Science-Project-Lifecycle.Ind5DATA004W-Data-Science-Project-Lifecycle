#for building interactive web apps
import streamlit as st
#for loading CSV files
import pandas as pd
#for creating interactive maps
import pydeck as pdk
#for creating charts and graphs
import matplotlib.pyplot as plt
#for making interactive altair charts
import altair as alt
#for generating numbers and data
import numpy as np
#for reading uploaded files string content and treating them like file objects
import io

#setting the title of the app
st.title("FCO_Posts_list_August_2019")

#the file uploader for csv files
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

#only proceed if a file has been uploaded
if uploaded_file is not None:
    try:
        #getting the raw bytes from uploaded file
        file_bytes = uploaded_file.getvalue()

        #decoding the bytes manually using cp1252 encoding instead of UTF-8
        decoded_str = file_bytes.decode("cp1252")

        #making the decoded string into file-like object
        string_io = io.StringIO(decoded_str)

        #printing message out
        st.info("Reading CSV from uploaded and decoded content")

        #reading csv into a data frame
        df = pd.read_csv(string_io)

        #stripping whitespace from column names to avoid KeyError
        df.columns = df.columns.str.strip()

        #displaying and printing the data
        st.success("CSV loaded successfully!")
        st.write(df)
        st.write("Column names:", df.columns.tolist())

        #plotting histogram
        rand = np.random.normal(1, 2, size=20)
        fig, ax = plt.subplots()
        ax.hist(rand, bins=15)
        st.pyplot(fig)

        #plotting line chart
        df_line = pd.DataFrame(np.random.randn(10, 2), columns=['x', 'y'])
        st.line_chart(df_line)

        #plotting bar chart
        df_bar = pd.DataFrame(np.random.randn(10, 2), columns=['x', 'y'])
        st.bar_chart(df_bar)

        #plotting area chart
        df_area = pd.DataFrame(np.random.randn(10, 2), columns=['x', 'y'])
        st.area_chart(df_area)

        #plotting altair chart
        df_alt = pd.DataFrame(np.random.randn(500, 3), columns=['x', 'y', 'z'])
        c = alt.Chart(df_alt).mark_circle().encode(x='x', y='y', size='z', color='z', tooltip=['x', 'y', 'z'])
        st.altair_chart(c, use_container_width=True)

        #naming coordinate columns to lat/lon
        df_map = df.rename(columns={'y': 'lat', 'x': 'lon'})
        df_map = df_map.dropna(subset=['lat', 'lon'])

        #creating region filter dropdown
        regions = ['All'] + sorted(df_map['Region'].dropna().unique().tolist())
        selected_region = st.selectbox("Select a Region", regions)
        if selected_region != 'All':
            df_map = df_map[df_map['Region'] == selected_region]

        #creating type of post filter dropdown
        post_types = ['All'] + sorted(df_map['Type of Post'].dropna().unique().tolist())
        selected_type = st.selectbox("Select a Type of Post", post_types)
        if selected_type != 'All':
            df_map = df_map[df_map['Type of Post'] == selected_type]

        #printing subhead
        st.subheader("Filtered Map of FCO Posts")

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_map,
            get_position='[lon, lat]',
            get_radius=50000,
            get_fill_color='[0, 0, 200, 160]',
            pickable=True,)

        view_state = pdk.ViewState(
            latitude=df_map['lat'].mean(),
            longitude=df_map['lon'].mean(),
            zoom=1,
            pitch=0)

        #tooltip shown when hovering on map points
        tooltip = {"html": "<b>City:</b> {Location (City)}<br/><b>Country:</b> {Country/Territory}","style": {"backgroundColor": "steelblue", "color": "white"}}

        #rendering the interactive map
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip))

    except Exception as e:
        # Show any errors that occur
        st.error(f"Error loading CSV: {e}")