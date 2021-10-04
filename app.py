import pandas as pd
import streamlit as st

from helper import *


def main():
    st.title('Flight Scanner')

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
        option = st.selectbox('Currency',('USD', 'EUR', 'GBP'))


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


if __name__=='__main__':
    main()