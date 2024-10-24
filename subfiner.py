#!/usr/bin/env python3
import concurrent.futures
import requests
import socket
from api.certsh import get_subdomain_from_crtsh
from api.censys_api import get_subdomain_from_censys
from api.virustotal_api import get_subdomain_from_virustotal
import argparse

# Perform DNS Lookup to check if subdomain exists
def check_subdomain_dns(subdomain):
    try:
        socket.gethostbyname(subdomain)
        return True

    except socket.gaierror:
        return False
    

# Perform a single single domain scan
def scan_subdomain(subdomain):
    url = f"https://{subdomain}"
    try:
        # Making HTTP request with timeout
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f'[+] {url} is reachable'
        else:
            return f'[-] {url} returned {response.status_code}'
    except requests.ConnectionError:
        return f'[-] {url} - Connection Failed'
    except Exception as e:
        return f'[-] {url} - Error: {str(e)}'
    

# Main function to handle scanning of subdomains
def subdomain_scanner(domain_name, sub_domains):
    print("--------- This tools is writting by Ephraim Norbert to aide security analyst... ---------")
    print("------------------------------------ Scanner started -------------------------------------")

    # Filter out only valid subdomains by checking DNS
    valid_subdomains = [sub for sub in sub_domains if check_subdomain_dns(sub)]

    print(f"Found {len(valid_subdomains)} valid subdomains with DNS.")

    # ThreadPoolExecutor to speed up the scanning process
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scan_subdomain, subdomain) for subdomain in valid_subdomains]

        for future in concurrent.futures.as_completed(futures):
            print(future.result())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Subdomain Enumeration tools")
    parser.add_argument('domain', help="Domain name to scan")
    args = parser.parse_args()

    dom_name = args.domain

    #Fetch subdomains from multiple api
    subdomain_crtsh = get_subdomain_from_crtsh(dom_name)
    subdomains_virustotal = get_subdomain_from_virustotal(dom_name)
    subdomains_censys = get_subdomain_from_censys(dom_name)

    # Combine all subdomains and remove duplicates
    all_subdomains = set(subdomain_crtsh + subdomains_virustotal + subdomains_censys)
     
    if all_subdomains:
        print(f"Found {len(all_subdomains)} unique subdomains.")
        subdomain_scanner(dom_name, list(all_subdomains))

    else:
        print("No subdomains found.")