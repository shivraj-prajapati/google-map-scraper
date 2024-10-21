import os
import json
import requests
from bs4 import BeautifulSoup

# Fetch URL content with retries
def fetch_url_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    attempt = 0
    while attempt < 5:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return response, True
        except requests.RequestException as error:
            print(f"Attempt {attempt+1} failed for {url}: {error}")
            attempt += 1
    print(f"All attempts failed for {url}")
    return None, False

# Parse and extract details from soup
def scrape_details(html_content):
    results = []
    for entry in html_content.find_all('div', class_='rllt__details'):
        data = {
            "name": "", "contact": "", "address": "", "status": "",
            "extra_info": "", "site_link": "", "map_link": ""
        }
        try:
            data["name"] = entry.find('span', class_='OSrXXb').text.strip()
            all_details = entry.find_all('div')
            
            # Check if contact and address are combined
            if len(all_details) >= 3:
                addr_contact = all_details[2].text.strip()
                if '·' in addr_contact:
                    data["address"], data["contact"] = map(str.strip, addr_contact.split('·'))
                    data["contact"] = data["contact"].replace(" ", "").lstrip('0')
                else:
                    data["address"] = addr_contact
            if len(all_details) > 3:
                data["status"] = all_details[3].text.strip()
            extra_info = entry.find('div', class_='pJ3Ci')
            if extra_info:
                data["extra_info"] = extra_info.text.strip()
            results.append(data)
        except Exception as err:
            print(f"Error extracting data: {err}")
    return results

# Extract links (website and directions) from soup
def gather_links(html_content, result_list):
    for idx, link_div in enumerate(html_content.find_all('div', {'jsname': 'jXK9ad'})):
        try:
            if idx < len(result_list):
                website = link_div.find('a', class_='yYlJEf Q7PwXb L48Cpd brKmxb')
                if website:
                    result_list[idx]["site_link"] = website['href']
                directions = link_div.find('a', href=lambda href: href and '/maps/dir/' in href)
                if directions:
                    result_list[idx]["map_link"] = directions['href']
        except Exception as link_error:
            print(f"Error extracting links: {link_error}")
    return result_list

# Generate a unique ID for each entry based on name and address
def create_unique_identifier(data):
    return f"{data['name']}_{data['address']}"

# Main logic for fetching and processing results
def run_scraper(total_pages, location, category):
    unique_items = set()
    for offset in range(10, total_pages+1, 10):
        search_url = f"https://www.google.com/search?sca_esv=76f4423ea649153a&tbs=lf:1,lf_ui:3&tbm=lcl&q={category}+in={location}&start={offset}"
        print(f"Fetching: {search_url}")
        response, successful = fetch_url_content(search_url)
        
        if successful:
            soup = BeautifulSoup(response.text, 'html.parser')
            extracted_data = scrape_details(soup)
            data_with_links = gather_links(soup, extracted_data)
            unique_results = []
            
            for item in data_with_links:
                unique_id = create_unique_identifier(item)
                if unique_id not in unique_items:
                    unique_results.append(item)
                    unique_items.add(unique_id)
            
            save_to_file(unique_results, category, location)

# Save the results to a JSON file
def save_to_file(data, category, location):
    filename = f"{category}_{location}.json"
    existing_data = []
    
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                pass
    
    existing_data.extend(data)
    
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
    
    print(f"Data saved in {filename}")

# Run the script
if __name__ == "__main__":
    total_pages = 60
    category = "cafe"
    location = "jamnagar"
    run_scraper(total_pages, location, category)
