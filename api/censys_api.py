import requests

censys_api_id = 'eb4ed9e0-5916-473a-9071-9e8e7e5e7c28'
censys_secret_api = 'RyieCHq1CUUYsQE2wnHjXuSDOYeDmAdd'

def get_subdomain_from_censys(domain_name):
    url = f"https://censys.io/api/v1/search/certificates"
    params = {
        "query": f"{domain_name}",
        "fields": ["parsed.names"],
        "flatten": True
    }

    try:
        response = requests.post(url, json=params, auth=(censys_api_id, censys_secret_api))
        if response.status_code == 200:
            json_data = response.json()
            subdomains = set()
            for result in json_data.get('results', []):
                subdomains.update(result.get('parsed.names', []))
            return list
        else:
            print(f"Failed to get subdomains from censys (status code: {response.status_code})")
            return []
        
    except Exception as e:
        print(f"Error occured while fetching subdomains from censys: {e}")
        return []