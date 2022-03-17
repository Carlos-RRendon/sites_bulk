
def sites_parser(body):

    if 'sites' in body:


        sites = body['sites']

        for site in sites:
            latitude = site['latitude']
            longitude = site['longitude']
            address = site['address']

            if site['latitude'] and site['longitude']:
                print(f'latitude {latitude} longitude{longitude}')
                print(f'Con coordenadas: {find_by_coordinates(latitude,longitude)}')

            elif site['address']:
                print(f'address {address}')

            else:
                print('no tiene nada')

    else:
        print("There are no sites")


def find_by_coordinates(lat,lng):
    import googlemaps
    gmaps = googlemaps.Client(key='AIzaSyDB8BwnMN8b0T9polJEdiMilCpX7ty7bkc')

    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    return reverse_geocode_result

def find_by_address(address):
    import googlemaps
    gmaps = googlemaps.Client(key='AIzaSyDB8BwnMN8b0T9polJEdiMilCpX7ty7bkc')

    geocode_result = gmaps.geocode(address,components={'country': 'MX'})
    return geocode_result[0]['geometry']['location']

def find_by_place(address):
    import googlemaps
    gmaps = googlemaps.Client(key='AIzaSyDB8BwnMN8b0T9polJEdiMilCpX7ty7bkc')

    response = gmaps.places(address)
    results = response['results']['geometry']['location']
    return results

def get_factibility(lattitude,longitude):
    import requests


