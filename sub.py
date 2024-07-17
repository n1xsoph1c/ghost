import requests
from bs4 import BeautifulSoup
import tldextract
import re

# Function to extract all links from an HTML file
def extract_links_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()

    soup = BeautifulSoup(contents, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    
    return links

# Function to create a hashmap of domains to links
def create_domain_link_map(links):
    domain_link_map = {}
    for link in links:
        if link.__contains__(".gov"):
            ext = tldextract.extract(link)
            domain = f"{ext.domain}.{ext.suffix}"
            if domain:
                domain_link_map[domain] = link
    return domain_link_map


# Specify the path to your HTML file
html_file_path = 'test.html'

# Extract links from the HTML file
links = extract_links_from_html(html_file_path)

# Create a hashmap of domains to links
domain_link_map = create_domain_link_map(links)

# Print the results
print("{")
for domain, link in domain_link_map.items():
    print(f"'{domain}': '{link}',")
print("}")
# print("\nSubdomains Map:")
# for domain, subdomains in subdomains_map.items():
#     print(f"{domain}: {subdomains}")
