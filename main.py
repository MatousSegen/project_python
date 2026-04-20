import sys
import csv

import click
import requests
from bs4 import BeautifulSoup
 
def get_soup(url: str):
    """
    Downloads HTML content from given URL and returns a beautifulsoup objets.
    If download fails, function prints an error message according to error type.
    """
    try:
        page_response = requests.get(url, timeout=15)
        page_response.raise_for_status()
        return BeautifulSoup(page_response.text, features="html.parser")
    except requests.exceptions.Timeout:
        sys.exit("Error: Server didn't responded in 15 seconds, try again later.")
    except requests.exceptions.HTTPError:
        sys.exit("Error: Page not found, check your URL.")
    except requests.exceptions.RequestException as error:
        sys.exit(f"Error: Bad request, see below: \n{error}")

def get_table_matrix(soup) -> list:
    """
    Parses a beautifulsoup object and returns a list of dictionaries
    containing text and urls from all HTML tables in the beautilsoup object.
    """
    matrix = []
    for row in soup.find_all("tr"):
        row_data = []
        for td in row.find_all("td"):
            text = td.get_text(strip=True).replace('\xa0', '')
            url_tag = td.find("a")
            url = url_tag["href"] if url_tag else None
            row_data.append({"text" : text, "url": url})
        if any(cell["text"] for cell in row_data):
            matrix.append(row_data)
    return matrix

def get_cities(region_url: str) -> list:
    """
    Scrapes a list of municipalities from region page.
    Extracts a city code, name and URL leading to election results in the city.
    """
    click.secho("INITIALIZING SCRAPER", fg="cyan", bold=True)
    soup = get_soup(region_url)
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    matrix = get_table_matrix(soup)
    data = []
    for row in matrix:
        if len(row) >= 3:
            code_cell = row[0]
            location_cell = row[1]
            if code_cell["text"].isdigit() and code_cell["url"]:
                data.append({"code": code_cell["text"], "location": location_cell["text"], "url": base_url + code_cell["url"]})
    if not data:
        sys.exit("Error: No data found, make sure you are entering the right URL.")
    return data

def get_cities_results(data: list) -> list:
    """
    Iterates through all cities and scrapes election details.
    Data collected: registered voters, number of envelopes, valid votes and parties.
    """
    results = []
    with click.progressbar(data, label="Downloading election results",
                           fill_char=click.style("#", fg="green"), empty_char="·") as bar:
        for city in bar:
            soup = get_soup(city["url"])
            matrix = get_table_matrix(soup)
            city_data = city.copy() #creates a 
            city_data.pop("url")
            city_data["registered"] = soup.find("td", headers="sa2").get_text(strip=True).replace('\xa0', '')
            city_data["envelopes"] = soup.find("td", headers="sa3").get_text(strip=True).replace('\xa0', '')
            city_data["valid"] = soup.find("td", headers="sa6").get_text(strip=True).replace('\xa0', '')
            for row in matrix:
                if len(row) >= 3:
                    code_cell = row[0]
                    location_cell = row[1]
                    votes_cell = row[2]
                    if code_cell["text"].isdigit():
                        party_name = location_cell["text"]
                        party_votes = votes_cell["text"]
                        if party_votes != "100,00":
                            city_data[party_name] = party_votes
            results.append(city_data)
    click.secho("Data successfully obtained.", fg="green", bold=True)
    return results
    
def export_to_csv(results: list, output_filename: str):
    """
    Exctracts party names from results and appends them into header.
    Saves results with complete header in a CSV file.
    If the party wasn't running in the city, function saves value 0.
    """
    click.secho(f"Exporting data to {output_filename}", fg="yellow", bold=True)
    header = ["code", "location", "registered", "envelopes", "valid"]
    for city_data in results:
        for key in city_data.keys():
            if key not in header:
                header.append(key)
    try:
        with open(output_filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header, restval="0")
            writer.writeheader()
            writer.writerows(results)
        click.secho(f"File {output_filename} successfully created", fg="green", bold=True)
    except Exception as e:
        sys.exit(f"Error: Cannot write to file, see below \n{e} ")
    
@click.command()
@click.argument("url", metavar="<url>")
@click.argument("file_name", metavar="<output_file>")
def main(url: str, file_name:str):
    """
    Election scraper of 2017 elections.
    
    This program scrapes data from specific region from volby.cz and saves them into a CSV file.

    
    \b
    <url>   The URL of the website in quotes.
    <output_file>  The path to the output CSV file
    """
    if "volby.cz" not in url:
        sys.exit("Error: This scraper only works with volby.cz URLs.")
    cities_info = (get_cities(url))
    results = get_cities_results(cities_info)
    export_to_csv(results, file_name)

if __name__ == "__main__":
    main()