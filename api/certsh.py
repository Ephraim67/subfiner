import requests
import json

#API call from crt.sh for subdomain enum
def get_subdomain_from_crtsh(domain_name):
    url = f"https://crt.sh/?q=%25.{domain_name}&output=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            subdomains = set()
            for entry in json_data:
                common_name = entry['name_value']
                subdomains.update(common_name.split('\n'))
            return list(subdomains)
        else:
            print(f"Failed to get subdomains from crt.sh (status code: {response.status_code})")
            return []

    except Exception as e:
        print(f"Error occured while fetching subdomains: {e}")
        return []

