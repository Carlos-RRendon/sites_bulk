__author__ = "Miguel Angel Valente Vargas"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Miguel Angel Valente Vargas"
__email__ = "miguel.valente@totalplay.com.mx"
__status__ = "Development"

import requests

def sites_bulk_load(body):
    quote_id = body['quoteId']
    account_id = body['accountId']
    sites = body['sites']

    sites_list = []

    for site in sites:
        site_name = site['name']
        latitude = site['latitude']
        longitude = site['longitude']
        address = site['address']

        if (latitude and longitude) or address:
            location = f"{latitude}, {longitude}" if latitude and longitude else address
            gmaps_info = get_gmaps_info(location)

            if gmaps_info is not None:
                address_components = gmaps_info['address_components']
                geometry = gmaps_info['geometry']
            else:
                continue

            # Create the site object
            site_to_send = {
                'cuenta': account_id,
                'consecutivo': '1',
                'idSitio': site_name,
                'latitud': latitude if latitude else geometry['location']['lat'],
                'longitud': longitude if longitude else geometry['location']['lng'],
                'calle': '[Pendiente]',
                'numExt': '[Pendiente]',
                'colonia': '[Pendiente]',
                'delegacionMunicipio': '[Pendiente]',
                'ciudad': '[Pendiente]',
                'estado': '[Pendiente]',
                'codigoPostal': '[Pendiente]'
            }

            keys_mapping = {
                'route': 'calle',
                'street_number': 'numExt',
                'neighborhood': 'colonia',
                'sublocality': 'delegacionMunicipio',
                'locality': 'ciudad',
                'postal_code': 'codigoPostal'
            }

            for element in address_components:
                types = element['types']
                value = element['long_name']

                for key in keys_mapping.keys():
                    if key in types:
                        site_to_send[keys_mapping[key]] = value if value else site_to_send[keys_mapping[key]]

                if 'administrative_area_level_1' in types:
                    site_to_send['estado'] = element['short_name'] if element['short_name'] else site_to_send['estado']

            feasibility = get_feasibility(site_to_send['latitud'], site_to_send['longitud'])

            if feasibility is not None:
                site_to_send.update(feasibility)
            else:
                continue
            sites_list.append(site_to_send)

    if len(sites_list) > 1 :
        send_salesforce_request(quote_id,sites_list)


def get_gmaps_info(location):

    API_MAPS_URL = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDB8BwnMN8b0T9polJEdiMilCpX7ty7bkc"
    API_MAPS_PARAMS = {
        'address': location
    }

    response = requests.get(url=API_MAPS_URL, params=API_MAPS_PARAMS)

    # extracting data in json format
    response = response.json()

    if response['status'] == 'ZERO RESULTS':
        return None
    else:
        return response['results'][0]

def get_feasibility(latitud, longitud):

    GSALITE_URL = "http://10.216.47.28/soa-infra/resources/SalesForce/FactibilidadMDL!2.3/RestFactibilidadMDL/RestFactibilidadMDL"
    # GSAlite request configuration
    GSALITE_HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    GSALITE_DATA = {
        'Login': {
            'User': '574011',
            'Password': 'SalesF0rc31557$',
            'Ip': '127.0.0.1'
        },
        "Coordenadas": {
            'TipoCliente': 'Enlace',
            'latitud': latitud,
            'longitud': longitud
        }
    }

    response_dict = {}

    try:
        # Send the GSAlite request
        response = requests.post(
            url=GSALITE_URL, headers=GSALITE_HEADERS, json=GSALITE_DATA)

        # extracting data in json format
        response = response.json()
        feasibility = response['CalculaFactibilidad']

        if feasibility['Detalle_Respuesta']['CodigoRespuesta'] == 'OK':
          response_dict['cluster'] = feasibility['nombre_cluster']
          response_dict['plaza'] = feasibility['Cuidad']
          response_dict['region'] = feasibility['Region']
          response_dict['regionId'] = feasibility['IdRegion']
          response_dict['cobertura'] = 'Cobertura'
          response_dict['zona'] = feasibility['zona']
          response_dict['factibilidad'] = feasibility['factibilidad']
          response_dict['distrito'] = feasibility['distrito']
          return response_dict
        else:
            return None
    except:
        return None

def send_salesforce_request(quote,sites):

    SALESFORCE_URL = 'https://totalplay--developsf.my.salesforce.com/services/apexrest/WS_CrearSitioMasivoEmpresarial'

    data = {
        'idCotizacion': quote,
        'accion': 'crearSitio',
        'datosSitio': sites
    }
    # Salesforce request configuration
    SALESFORCE_HEADERS = {
        'Authorization': 'Bearer 00D8A0000005h6O!ASAAQGBy9973iJAECpKklkqxL7yoHfxSz81cnPoRDv_OrkpsUMA3yFqTdW2wfRTvl_ztnUDcy23TzEXK.fjduSqmm82IAbgI',
        'Content-Type': 'application/json'
    }
    # Send the Salesforce request
    response = requests.post(
        url=SALESFORCE_URL, headers=SALESFORCE_HEADERS, json=data)
