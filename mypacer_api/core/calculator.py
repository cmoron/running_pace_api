"""
Module containing functions for calculating running paces and times.
"""

from typing import Dict, List


def calculate_pace_table(
    min_pace: int, max_pace: int, increment: int, distances: list
) -> List[Dict]:
    """
    Calculate the pace table for given pace parameters.

    Args:
    min_pace (int): The minimum pace in seconds per kilometer.
    max_pace (int): The maximum pace in seconds per kilometer.
    increment (int): The increment in seconds per kilometer for each row.
    distances (list): A list of distances in meters.

    Returns:
    List[Dict]: A list of dictionaries where each dictionary represents a row in the pace table,
    with keys being the distances and values being the calculated times.
    """
    # Validate input parameters
    if min_pace <= 0:
        raise ValueError("Minimum pace must be positive and greater than zero.")
    if max_pace > min_pace:
        raise ValueError("Minimum pace must be greater than maximum pace.")
    if increment <= 0:
        raise ValueError(
            "Increment must be positive and less than the difference between maximum\
                and minimum pace."
        )

    # Pre-compute distance conversions and keys to avoid repeated calculations
    distance_data = [(str(d), d / 1000) for d in distances]

    # Use list comprehension for better performance
    results = [
        {
            "pace": pace,
            "speed": round(3600 / pace, 2),
            **{key: round(dist_km * pace, 2) for key, dist_km in distance_data},
        }
        for pace in range(min_pace, max_pace - 1, -increment)
    ]

    return results
