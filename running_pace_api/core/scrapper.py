"""
Module containing functions for scraping running records from the World Athletics website.
"""

from typing import Dict
from bs4 import BeautifulSoup as bs, Tag
import requests
from fastapi import HTTPException

def wa_convert_time_to_seconds(time_str: str) -> float:
    """
    Convert a time string in the format HH:mm:ss, mm:ss, mm:ss.cc or ss.cc to seconds.

    Args:
    time_str (str): The time string to convert.

    Returns:
    float: The number of seconds represented by the time string.
    """
    if not time_str:
        return ""

    # If the time string is in the format HH:mm:ss
    if ":" in time_str and len(time_str.split(":")) == 3:
        hours, minutes, seconds = time_str.split(":")
        if "." in seconds:
            seconds = float(seconds)
        else:
            seconds = int(seconds)
        # Calculate the total seconds
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + seconds
    # If the time string is in the format mm:ss or mm:ss.cc
    elif ":" in time_str and len(time_str.split(":")) == 2:
        # Split the time string into minutes and seconds
        minutes, seconds = time_str.split(":")
        # If the seconds part has a decimal point, convert it to a float
        if "." in seconds:
            seconds = float(seconds)
        else:
            seconds = int(seconds)
        # Calculate the total seconds
        total_seconds = int(minutes) * 60 + seconds
    # If the time string is in the format ss.cc
    else:
        # Convert the time string to a float and multiply by 100 to get the number of centiseconds
        centiseconds = float(time_str) * 100
        # Calculate the total seconds
        total_seconds = int(centiseconds / 100) + (centiseconds % 100) / 100
    return float(total_seconds)

def extract_time_and_convert_to_seconds(time_str: str) -> float:
    """
    Extract the time from a record string and convert it to seconds.

    Args:
    time_str (str): The record string containing the time.

    Returns:
    float: The number of seconds represented by the time.
    """
    # Use a regular expression to extract the time from the record string
    time_str_stripped = time_str.split(" ")[0]
    # Convert the time string to seconds
    seconds = wa_convert_time_to_seconds(time_str_stripped)
    return seconds

def parse_records_table(table: Tag) -> Dict[int, float]:
    """
    Function to extract record data from a table using BeautifulSoup.

    Args:
    table (Tag): The table element containing record data.

    Returns:
    dict: A dictionary containing record data,
    with discipline distances as keys and record times in seconds as values.
    """
    # If table is not found, return an empty dictionary
    if not table:
        return {}

    # Initialize an empty dictionary to store record data
    distances = {
        "100 Metres": 100,
        "200 Metres": 200,
        "400 Metres": 400,
        "800 Metres": 800,
        "1000 Metres": 1000,
        "1500 Metres": 1500,
        "Mile": 1609.34,
        "2000 Metres": 2000,
        "3000 Metres": 3000,
        "5000 Metres": 5000,
        "10,000 Metres": 10000,
        "Half Marathon": 21097,
        "Marathon": 42195,
    }
    records = dict.fromkeys(distances.values(), "")

    # Find the table with the class 'records-table'
    record_table = table.find("table", {"class": "records-table"})
    if not record_table:
        return {}

    # Find all rows in the table
    rows = [row for row in record_table.find_all("tr") if "clickable" not in row.get("class", [])]

    # Iterate through the rows
    for row in rows:
        # Find all columns in the row without 'data-bind' attribute
        cols = row.find_all("td")

        for col in cols:
            # Check if the column contains a discipline
            if col.find("a") and col.find("a")[
                "href"
            ].startswith("/disciplines/"):
                discipline = col.text.strip()
            # Check if the column contains a record
            elif col.get("data-th") == "PERF" and discipline in distances:
                record = col.text.strip()
                if record:
                    # Add the discipline and record to the dictionary
                    records[distances[discipline]] = extract_time_and_convert_to_seconds(
                        record
                    )
    return records

def scrap_records_page(url) -> Dict[str, Dict[int, float]]:
    """
    Function to scrape record data from the World Athletics website.

    Args:
    url (str): The URL of the page containing the record data.

    Returns:
    dict: A dictionary containing record data for men and women,
    with discipline distances as keys and record times in seconds as values.
    """
    # Send a HTTP GET request to the URL and get the HTML content
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        # Parse the HTML page with BeautifulSoup
        soup = bs(response.text, "lxml")
    else:
        raise HTTPException(status_code=response.status_code,
                        detail="Failed to make an external request")

    # Initialize an empty dictionary to store record data
    records = {}

    # Find the div with the ID 'women'
    women_div = soup.find("div", {"id": "women"})

    # Find the div with the ID 'men'
    men_div = soup.find("div", {"id": "men"})

    # Call the parse_records_table function to extract record data from each div
    records["women"] = parse_records_table(women_div)
    records["men"] = parse_records_table(men_div)

    return records

def ba_convert_time_to_seconds(time_str: str) -> float:
    """
    Convert a time string in the format HHhmm'ss, mm'ss, mm'ss"cc or ss"cc to seconds.

    Args:
    time_str (str): The time string to convert.

    Returns:
    float: The number of seconds represented by the time string.
    """
    time_str = time_str.replace("''", "\"")
    time_str = time_str.split(" ")[0] # Remove any additional information after the time
    if not time_str:
        return ""

    # If the time string is in the format HHhmm'ss
    if "h" in time_str and "'" in time_str and "\"" in time_str:
        hours, rest = time_str.split("h")
        minutes, seconds = rest.split("'")
        seconds = seconds.replace("\"", "")
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    # If the time string is in the format mm'ss or mm'ss"cc
    elif "'" in time_str and "\"" in time_str:
        # Split the time string into minutes and seconds
        minutes, seconds = time_str.split("'")
        seconds, centiseconds = seconds.split("\"")
        if centiseconds:
            seconds = f"{seconds}.{centiseconds}"

        # Calculate the total seconds
        total_seconds = int(minutes) * 60 + float(seconds)
    elif "\"" in time_str:
        # Convert the time string to a float and multiply by 100 to get the number of centiseconds
        seconds, centiseconds = time_str.split("\"")
        # Calculate the total seconds
        total_seconds = int(seconds) + int(centiseconds) / 100
    else:
        total_seconds = -1
    return float(total_seconds)

def parse_bases_athle_record_page(soup: bs) -> Dict[str, str]:
    """
    Function to extract athlete data from a record page using BeautifulSoup.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the record page.

    Returns:
    dict: A dictionary containing athlete data, including the athlete's name,
    """
    distances = {
        "100m": 100,
        "100m - Salle": 100,
        "200m": 200,
        "200m - Salle": 200,
        "400m": 400,
        "400m - Salle": 400,
        "800m": 800,
        "800m - Salle": 800,
        "1 000m": 1000,
        "1000m - Salle": 1000,
        "1 500m": 1500,
        "1 500m - Salle": 1500,
        "Mile": 1609.34,
        "Mile - Salle": 1609.34,
        "3 000m": 3000,
        "3 000m - Salle": 3000,
        "5 000m": 5000,
        "5 Km Route": 5000,
        "10 Km Route": 10000,
        "20 Km Route": 20000,
        "1/2 Marathon": 21097,
        "Marathon": 42195,
    }

    # Chercher la table des records personnels
    table = soup.find('table', class_='linedRed')

    # Dictionnaire pour stocker les résultats
    athlete_records = {}

    # Traiter chaque ligne de données dans la table (sauf l'en-tête)
    if table:
        for row in table.find_all('tr')[1:]:  # sauter l'en-tête
            cols = row.find_all('td')
            if not cols:  # éviter les lignes sans données
                continue
            event = cols[0].get_text(strip=True)
            performance = cols[1].get_text(strip=True)

            # Convertir les noms d'épreuve pour correspondre au dictionnaire `distances`
            event_key = distances.get(event, None)
            if event_key:
                # Ajouter le record à la liste des records
                if event_key in athlete_records:
                    perf_seconds = ba_convert_time_to_seconds(performance)
                    if perf_seconds > 0:
                        athlete_records[event_key] = min(athlete_records[event_key], perf_seconds)
                else:
                    athlete_records[event_key] = ba_convert_time_to_seconds(performance)
    return athlete_records


def scrap_athlete_records(url: str) -> Dict[str, str]:
    """
    Function to scrape athlete data from the 'bases.athle.fr' website.

    Args:
    html (str): The HTML content of the athlete record page.

    Returns:
    dict: A dictionary containing athlete data, including the athlete's name,
    """
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        return parse_bases_athle_record_page(soup)
    raise HTTPException(status_code=response.status_code,
                        detail="Failed to make an external request")
