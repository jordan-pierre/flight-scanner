import streamlit as st
import pandas as pd

st.title('Flight Scanner')

# Form for generating search
with st.form(key='search_form'):
    # Origin location
    origin = st.text_input("Enter your origin (airport code or city)")
    # TODO: add validation for valid originplace (airport, city, state, country, but not continent or other region)

    # Destination location
    destination = st.text_input("Enter your destination or 'anywhere'")
    # TODO: validate using the same as origin

    # Outbound date
    outbound_date = st.date_input('Outbound Date')
    # TODO: Calendar widget + 'Anytime' toggle button

    # Inbound date
    # TODO: Calendar widget + 'Anytime' toggle button

    # Currency dropdown
    # TODO:

    #  




    submit_button = st.form_submit_button(label='Submit')

# Toggle search results
quotes_df = pd.read_csv('output.csv')
print(quotes_df.columns)

# Price
max_price = min(quotes_df['MinPrice'].max(), 2000)
price_filter = st.slider('Select a range of values', 0, max_price, (0, 250))

# Direct
# TODO: add toggle button and filter for 'Direct' column



st.write(f"""  """)