"""
Module containing functions for calculating running paces and times.
"""
from typing import List, Dict
from running_pace_api.models import OFFICIAL_DISTANCES

def calculate_pace_table(min_pace: int, max_pace: int, increment: int) -> List[Dict]:
    """
    Calculate the pace table for given pace parameters.

    Args:
    min_pace (int): The minimum pace in seconds per kilometer.
    max_pace (int): The maximum pace in seconds per kilometer.
    increment (int): The increment in seconds per kilometer for each row.

    Returns:
    List[Dict]: A list of dictionaries where each dictionary represents a row in the pace table,
    with keys being the distances and values being the calculated times.
    """
    results = []
    for pace in range(min_pace, max_pace - 1, -increment):
        pace_row = {"pace": pace}
        speed_km_h = 3600 / pace  # Convert pace to speed in km/h
        pace_row["speed"] = round(speed_km_h, 2)  # Optional: round to 2 decimal places
        for distance in OFFICIAL_DISTANCES:
            time_in_sec = (distance / 1000) * pace  # Convert pace to time for each distance
            pace_row[f"{distance}"] = round(time_in_sec, 2)
        results.append(pace_row)

    return results
