import requests
import json
import act

#Every request begins with the server's URL
server = 'http://data.neonscience.org/api/v0/'

site_code = 'BARR'

#Make request, using the sites/ endpoint
#site_request = requests.get(server + 'sites/' + site_code)

#Convert to Python JSON object
#site_json = site_request.json()

#View product code and name for every available data product
#for product in site_json['data']['dataProducts']:
#    print(product['dataProductCode'],product['dataProductTitle'])

products = act.discovery.get_neon.get_site_products(site_code, print_to_screen=True)

product_id = 'DP1.00002.001'


date = '2022-01'
end_date = '2022-10'
act.discovery.get_neon.download_neon_data(site_code, product_id, date, end_date)

