"""
Module containing functions for scraping running records from the World Athletics website.
"""

from typing import Dict
from bs4 import BeautifulSoup as bs, Tag
import requests

WA_URL = "https://worldathletics.org/records/by-category/world-records"

def convert_time_to_seconds(time_str: str) -> float:
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
    seconds = convert_time_to_seconds(time_str_stripped)
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

def scrap_records_page() -> Dict[str, Dict[int, float]]:
    """
    Function to scrape record data from the World Athletics website.

    Returns:
    dict: A dictionary containing record data for men and women, 
    with discipline distances as keys and record times in seconds as values.
    """
    # Send a HTTP GET request to the URL and get the HTML content
    html = requests.get(WA_URL, timeout=10)

    # Initialize an empty dictionary to store record data
    records = {}

    # Parse the HTML page with BeautifulSoup
    soup = bs(html.text, "lxml")

    # Find the div with the ID 'women'
    women_div = soup.find("div", {"id": "women"})

    # Find the div with the ID 'men'
    men_div = soup.find("div", {"id": "men"})

    # Call the parse_records_table function to extract record data from each div
    records["women"] = parse_records_table(women_div)
    records["men"] = parse_records_table(men_div)

    return records
