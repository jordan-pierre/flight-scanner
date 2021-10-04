import pandas as pd
import streamlit as st

from helper import *
from scanner import generate_quotes_csv

@st.cache
def load_data(file, nrows):
    data = pd.read_csv(file, nrows=nrows)
    data = data.drop(['Unnamed: 0'], axis=1, errors='ignore')
    return data


def main():
    st.title('Flight Scanner')
    data = None

    # Form for generating search
    with st.form(key='search_form'):
        # Origin location
        origin = st.text_input("Enter your origin (airport code or city)", "Airport", help='e.g. "CMH", "Columbus, OH", "Ohio"')
        # TODO: add validation for valid originplace (airport, city, state, country, but not continent or other region)

        # Destination location
        destination = st.text_input("Enter your destination or 'anywhere'", "Anywhere", help='e.g. "CMH", "Columbus, OH", "Ohio"')
        # TODO: validate using the same as origin

        # Outbound date
        #outbound_date = st.date_input('Outbound Date')

        outbound_months_dict = get_next_x_months(datetime.today(), 5)
        outbound_date = st.selectbox('Departure Date', outbound_months_dict.values())


        # # Inbound date
        # inbound_date = st.selectbox('Return Date', [])
        # if st.session_state.outbound_date == 'Anytime':
        #     inbound_months_dict = get_next_x_months(datetime.today(), 7)
        #     inbound_date = st.selectbox('Return Date', outbound_months_dict.values())
        # else:
        #     inbound_months_dict = get_next_x_months(str_date_to_datetime(st.session_state.outbound_date, outbound_months_dict), 5, inbound_mode=True)
        #     inbound_date = st.selectbox('Return Date', outbound_months_dict.values())
        
        #inbound_date_flexible = st.checkbox("Inbound Date is Flexible")
        
        # Toggle One-way
        one_way = st.checkbox('One-way only', value=False)
        inbound_date = '' if one_way else 'Anytime'


        # Currency dropdown
        # TODO:
        currency = st.selectbox('Currency',('USD', 'EUR', 'GBP'))

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        data_load_state = st.text('Loading data...')

        results_file = 'site_results.csv'
        generate_quotes_csv(output_file=results_file, currency=currency, originplace=origin, destinationplace=destination, inboundpartialdate=inbound_date, outboundpartialdate=outbound_date)
        
        data = load_data(results_file, 10000)
        data_load_state.text("Done! (using st.cache)")

        # Price
        max_price = min(data['MinPrice'].max(), 2000)
        price_filter = st.slider('Select a range of values', 0, max_price, (0, 250))
        print(price_filter)

        filtered_data = data[data['MinPrice'] < price_filter[1]]
        st.write(filtered_data)
        # df[df['MinPrice'] < 250]

    # Direct
    # TODO: add toggle button and filter for 'Direct' column



    st.write(f"""  """)


if __name__=='__main__':
    main()