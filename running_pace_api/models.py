"""
Module containing data models for the Running Pace Table API.
"""

from pydantic import BaseModel

# Official race distances in meters
OFFICIAL_DISTANCES = [100, 200, 300, 400, 500, 600, 800, 1000, 1500,
                      1609.34, 3000, 5000, 10000, 20000, 21097, 42195]

class TableParameters(BaseModel):
    """
    Parameters for generating the pace table.

    Attributes:
    min_pace: The minimum pace in seconds per kilometer.
    max_pace: The maximum pace in seconds per kilometer.
    increment: The increment in seconds per kilometer for each row in the table.
    """
    min_pace: int
    max_pace: int
    increment: int
