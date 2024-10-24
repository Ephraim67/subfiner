import requests

virus_total_api = "bbe407658a899a17667bd1114f4d14128279ea2eda68e0d481a056a81086d92c"


def get_subdomain_from_virustotal(domain_name):
    url = f"https://www.virustotal.com/vtapi/v2/domain/report?apikey={virus_total_api}&domain={domain_name}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            subdomains = json_data.get('subdomains', [])
            return subdomains
        else:
            print(f"Failed to get subdomains from virustotal (status code: {response.status_code})")
            return []
    except Exception as e:
        print(f"Error occured while fetching subdomains from virustotal: {e}")
        return []
    