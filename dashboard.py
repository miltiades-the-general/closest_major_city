import streamlit as st
import holoviews as hv
from utils import *
from pathlib import Path
import json

f = open('./cities.json')
data_to_json = json.load(f)

# In your conda env, you will need to run 'pip install --force-reinstall --no-deps bokeh==2.4.3' to support bokeh extension
hv.extension('bokeh', logo=False)

# To run .py script in Streamlit, a requirements.txt file is needed to tell Streamlit how to set up your Python env, what libraries are needed, etc.
# In your shell run 'pip install -r requirements.txt'

# Set the streamlit page layout to wide (reduces padding on the sides, makes page responsive)
st.set_page_config(layout="wide")

st.markdown("# What is your closest major city?")

a1, a2 = st.columns(2)
with a1:
    city_name = st.text_input("Input a City")

state_codes = ["AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MO", "MN", "MS", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "ND", "NC", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WV", "WA", "WI", "WY"]
with a2:
    state_code = st.selectbox("Select the State", options=state_codes)

def run_function(data_to_json, city_name, state_code):
    try:
        function = FindClosestCity.find_two_closest_cities_to_point(data_to_json, city_name, state_code)
    except: 
        "No Search Results"
    return function

if city_name:
    try:
        # st.button("Search", on_click=st.write(run_function(data_to_json, city_name, state_code)))
        st.write(run_function(data_to_json, city_name, state_code))
    except:
        "Invalid Search"

with st.expander("How to use this App"):
    st.write("""
        This app takes geolocation data from the top 150 cities in America by population. 
        Simply type in a city in the United States, select the state and press enter.
        The algorithm will find the closest city in the top 150 and return it to you.
        If you do not receive a result, check to make sure that the state is input correctly.
        If you enter a city in the top 150 it will return the closest city outside of itself in the top 150.
    """)