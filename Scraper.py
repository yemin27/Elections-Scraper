"""
Scraper.py: třetí projekt do Engeto Online Python Akademie
author: Yegor Gladush
email: ygladush@seznam.cz
discord: yegi95
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAIN_URL = "https://volby.cz/pls/ps2017nss/"

def is_valid_url(url):
    #Ověří, zda je URL platný.
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_html(url):
    #Získá HTML kód stránky.
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as e:
        logging.error(f"Chyba při stahování dat z {url}: {e}")
        return None

def extract_city_data(soup):
    #Extrahuje data o obcích z první stránky.
    cities = []
    tables = soup.find_all("div", {"class": "t3"})
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 3:
                code = cells[0].text
                name = cells[1].text
                link = cells[2].find("a")["href"] if cells[2].find("a") else None
                if link:
                    cities.append({"code": code, "name": name, "link": link})
    return cities

def extract_election_results(soup):
    #Extrahuje výsledky voleb z detailní stránky.
    results = {}
    tables = soup.find_all("div", {"class": "t2_470"})
    if tables:
        for table in tables:
            rows = table.find_all("tr")
            for row in rows[1:]:  #Přeskočíme hlavičku
                cells = row.find_all("td")
                if len(cells) >= 3:
                    party = cells[1].text
                    votes = cells[2].text.replace("\xa0", "")
                    results[party] = votes
    return results

def extract_header_data(soup):
    #Extrahuje data z hlavičky tabulky.
    header_data = {}
    table = soup.find("table", {"id": "ps311_t1"})
    if table:
        cells = table.find_all("td")
        if len(cells) >= 8:
            header_data["registered"] = cells[3].text.replace("\xa0", "")
            header_data["envelopes"] = cells[4].text.replace("\xa0", "")
            header_data["votes"] = cells[7].text.replace("\xa0", "")
    return header_data

def scrape_data(url):
    #Hlavní funkce pro scrapování dat.
    soup = get_html(url)
    if not soup:
        return None
    cities = extract_city_data(soup)
    all_data = []
    for city in cities:
        city_url = MAIN_URL + city["link"]
        city_soup = get_html(city_url)
        if not city_soup:
            continue
        results = extract_election_results(city_soup)
        header = extract_header_data(city_soup)
        all_data.append({
            "code": city["code"],
            "name": city["name"],
            "registered": header.get("registered", ""),
            "envelopes": header.get("envelopes", ""),
            "votes": header.get("votes", ""),
            **results
        })
    logging.info(f"Extrahováno {len(all_data)} záznamů.")
    return all_data

def save_to_csv(data, filename):
    #Uloží data do CSV souboru.
    if not data:
        logging.info("Žádná data k uložení.")
        return

    #Shromáždění všech názvů stran
    all_parties = set()
    for row in data:
        for key in row.keys():
            if key not in ["code", "name", "registered", "envelopes", "votes"]:
                all_parties.add(key)

    #Vytvoření hlavičky s názvy stran
    fieldnames = ["code", "name", "registered", "envelopes", "votes"] + sorted(list(all_parties))

    try:
        with open(filename, "w", newline="", encoding="utf-8-sig") as output_file: #Zajistí správné zobrazení diakritiky v Excelu
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Data uložena do {filename}.")
    except Exception as e:
        logging.error(f"Chyba při ukládání do CSV: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python script.py <URL> <output.csv>")
        sys.exit(1)
    url, output_file = sys.argv[1], sys.argv[2]

    if not is_valid_url(url):
        print("Chyba: Neplatný URL formát.")
        sys.exit(1)

    try:
        data = scrape_data(url)
        if data:
            save_to_csv(data, output_file)
        else:
            logging.info("Žádná data nebyla nalezena.")
    except Exception as e:
        logging.error(f"Došlo k chybě: {e}")
