"""
This module contains the pace table service, which is responsible for generating a pace table.
"""

from fastapi import HTTPException
from running_pace_api.core import calculator

def get_pace_table(min_pace: int, max_pace: int, increment: int):
    """
    Get a pace table for a given range of paces and increment.

    Args:
    min_pace (int): The minimum pace in seconds per kilometer.
    max_pace (int): The maximum pace in seconds per kilometer.
    increment (int): The increment in seconds per kilometer.

    Returns:
    List[Dict]: A list of dictionaries where each dictionary represents a row in the pace table,
    with keys being the distances and values being the calculated times.
    """
    if max_pace > min_pace:
        raise HTTPException(status_code=400, detail="Minimum pace must be more than maximum pace.")
    return calculator.calculate_pace_table(min_pace, max_pace, increment)
