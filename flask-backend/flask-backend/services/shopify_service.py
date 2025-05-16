import requests
from flask import current_app

def get_shopify_products():
    api_key = current_app.config['SHOPIFY_API_KEY'] # add shopify store api key
    store_domain = current_app.config['SHOPIFY_STORE_DOMAIN'] # add shopify store domain
    
    url = f"https://{store_domain}/admin/api/2023-01/products.json"
    headers = {
        "X-Shopify-Access-Token": api_key
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('products', [])
    return []
