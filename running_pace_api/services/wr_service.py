"""
This module contains functions to retrieve world records from the World Athletics website.
"""

from running_pace_api.core import scrapper

WA_URL = "https://worldathletics.org/records/by-category/world-records"

def get_world_records():
    """
    Retrieve world records from the World Athletics website.

    Returns:
    dict: A dictionary containing world records for various distances and events.
    """
    return scrapper.scrap_records_page(WA_URL)
