import pandas as pd
import streamlit as st
import os

from helper import *
from scanner import generate_quotes_csv

default_csv = 'default.csv'

@st.cache
def load_data(file, nrows):
    data = pd.read_csv(file, nrows=nrows)
    data = data.drop(['Unnamed: 0'], axis=1, errors='ignore')
    return data


def main():
    print("FROM THE TOP")

    st.title('Flight Scanner')
    results_file = 'site_results.csv' if os.path.exists('site_results.csv') else 'default.csv'

    # Form for generating search
    with st.form(key='search_form'):
        # Origin location
        origin = st.text_input("Enter your origin airport code", "Airport", help='e.g. "CMH", "JFK", "LAX"')

        # Destination location
        destination = st.text_input("Enter your destination or 'anywhere'", "Anywhere", help='e.g. "CMH", "JFK", "LAX"')

        # Outbound date
        outbound_months_dict = get_next_x_months(datetime.today(), 5)
        outbound_date = st.selectbox('Departure Date', outbound_months_dict.values())
        
        # Toggle One-way
        one_way = st.checkbox('One-way only', value=False)
        inbound_date = '' if one_way else 'Anytime'

        # Currency dropdown
        currency = st.selectbox('Currency',('USD', 'EUR', 'GBP'))
        # TODO: Test other currencies

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        results_file = 'site_results.csv'

        # Validate destination place is appropriate
        try:
            valid_origin = validate_place(origin)
        except InvalidPlaceError:
            valid_origin = False
            results_file = default_csv
            st.markdown('**ERROR: Invalid origin code.**')
        
        # Validate departure place is appropriate
        try:
            valid_destination = validate_place(destination)
        except InvalidPlaceError:
            valid_destination = False
            results_file = default_csv
            st.markdown('**ERROR: Invalid destination code.**')
        
        if valid_origin and valid_destination:
            try:
                generate_quotes_csv(output_file=results_file, currency=currency, originplace=origin, destinationplace=destination, inboundpartialdate=inbound_date, outboundpartialdate=outbound_date)
                first_run = False
            except KeyError as e:
                results_file = default_csv
                st.markdown('**ERROR: Place not found.  Please use a valid airport code.**')

    data = load_data(results_file, 10000)
    

    # Filter on Price
    try:
        max_price = min(int(data['MinPrice'].max()), 2000)
    except ValueError as e:
        max_price = 2000
    
    price_filter = st.slider('Select a range of values', 0, max_price, (0, 250))
    print(price_filter)

    filtered_data = data[data['MinPrice'] < price_filter[1]]
    
    direct_filter = st.checkbox('Direct', value=False)
    if direct_filter:
        filtered_data = data[data['Direct']]

    st.table(filtered_data)
    st.write(filtered_data)
    print(f"results_file = {results_file}")


if __name__=='__main__':
    main()