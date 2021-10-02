import requests
import pandas as pd
from datetime import datetime


def create_df_from_json(json):
    return pd.DataFrame(pd.json_normalize(json))


def create_carriers_dict(json):
    carriers_dict = dict()
    for item in json:
        carriers_dict[item['CarrierId']] = item['Name']

    return carriers_dict


def convert_carriers(id_list, carriers_dict):
    carrier_list = []
    for id in id_list:
        carrier_list.append(carriers_dict[id])
    return ', '.join(carrier_list)


def generate_quotes_csv(country='US', currency='USD', originplace='CMH', destinationplace='anywhere', inboundpartialdate='anytime', outboundpartialdate='anytime', locale='en-US', output_file=''):
    """Generate airline quotes from origin place to destination place between the outbound and inbound date.

    Args:
        country (str, optional): Country you're searching from. Defaults to 'US'.
        currency (str, optional): Currency of prices displayed. Defaults to 'USD'.
        originplace (str, optional): Origin place. Defaults to 'CMH'.
        destinationplace (str, optional): Flight destination. Defaults to 'anywhere'.
        inboundpartialdate (str, optional): The return date. Format “yyyy-mm-dd”, “yyyy-mm” or “anytime”. Use empty string for oneway trip. Defaults to 'anytime'.
        outboundpartialdate (str, optional): The outbound date. Format “yyyy-mm-dd”, “yyyy-mm” or “anytime”. Defaults to 'anytime'.
        locale (str, optional): Language locale for results. Defaults to 'en-US'.
        

    Returns:
        CSV
    """

    url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/{country}/{currency}/{locale}/{originplace}/{destinationplace}/{outboundpartialdate}/{inboundpartialdate}"

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': "2d32d04dd5msh5cb7c5e39103bebp1cd117jsn0f0dea8441dc"
        }

    response = requests.request("GET", url, headers=headers).json()

    places_df = create_df_from_json(response['Places'])
    places_df = places_df.drop(columns=['Type', 'SkyscannerCode', 'CityId'])

    carriers_dict = create_carriers_dict(response['Carriers'])

    quotes_df = create_df_from_json(response['Quotes'])

    quotes_df = quotes_df.merge(places_df, left_on='OutboundLeg.OriginId', right_on='PlaceId', suffixes=('', '_OutboundOrigin'))
    quotes_df = quotes_df.merge(places_df, left_on='OutboundLeg.DestinationId', right_on='PlaceId', suffixes=('', '_OutboundDestination'))
    quotes_df = quotes_df.merge(places_df, left_on='InboundLeg.OriginId', right_on='PlaceId', suffixes=('', '_InboundOrigin'))
    quotes_df = quotes_df.merge(places_df, left_on='InboundLeg.DestinationId', right_on='PlaceId', suffixes=('', '_InboundDestination'))

    quotes_df = quotes_df.rename(columns={'Name':'Name_OutboundOrigin', 'Type':'Type_OutboundOrigin',
        'SkyscannerCode':'SkyscannerCode_OutboundOrigin', 'IataCode':'IataCode_OutboundOrigin', 'CityName':'CityName_OutboundOrigin', 
        'CityId':'CityId_OutboundOrigin', 'CountryName':'CountryName_OutboundOrigin'})
    
    quotes_df['OutboundLeg.Carriers'] = quotes_df['OutboundLeg.CarrierIds'].apply(lambda x: convert_carriers(x, carriers_dict))
    quotes_df['InboundLeg.Carriers'] = quotes_df['InboundLeg.CarrierIds'].apply(lambda x: convert_carriers(x, carriers_dict))
    
    latest_scan_df = quotes_df[['QuoteId', 'MinPrice', 'Direct', 'QuoteDateTime', 'OutboundLeg.Carriers', 'InboundLeg.Carriers',
                                'OutboundLeg.DepartureDate', 'InboundLeg.DepartureDate', 'Name_OutboundOrigin', 'IataCode_OutboundOrigin',
                                'CityName_OutboundOrigin', 'CountryName_OutboundOrigin', 'Name_OutboundDestination', 
                                'IataCode_OutboundDestination', 'CityName_OutboundDestination', 'CountryName_OutboundDestination', 
                                'IataCode_InboundOrigin', 'IataCode_InboundDestination']]

    latest_scan_df['RunDate'] = datetime.now()

    output_file = 'output.csv' if output_file == '' else output_file
    latest_scan_df.to_csv(output_file) # to append, pass mode='a', header=False
    print(f"Wrote outputs to {output_file}")


if __name__=='__main__':
    generate_quotes_csv()