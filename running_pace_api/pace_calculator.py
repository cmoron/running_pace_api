"""
The Running Pace Table API is a FastAPI application designed to calculate running paces for
various distances.  This API  takes input  parameters  like minimum pace, maximum pace, and
increment step, and returns a table of  estimated running times for official race distances.
"""

from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Official race distances in meters
OFFICIAL_DISTANCES = [100, 200, 300, 400, 500, 600, 800, 1000, 1500, 1609.34, 3000, 5000, 10000, 20000, 21097, 42195]

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

app = FastAPI()

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_table")
async def generate_table(params: TableParameters):
    """
    Endpoint to generate a table of paces for various official race distances.

    Args:
    params (TableParameters): The pace parameters for generating the table.

    Raises:
    HTTPException: If the minimum pace is not less than the maximum pace.

    Returns:
    List[Dict]: A table of calculated times for each distance at each pace.
    """
    if params.max_pace >= params.min_pace:
        raise HTTPException(status_code=400, detail="Minimum pace must be more than maximum pace.")

    return calculate_pace_table(params.min_pace, params.max_pace, params.increment)

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
        row = {"pace": pace}
        speed_km_h = 3600 / pace  # Convert pace to speed in km/h
        row["speed"] = round(speed_km_h, 2)  # Optional: round to 2 decimal places
        for distance in OFFICIAL_DISTANCES:
            time_in_sec = (distance / 1000) * pace  # Convert pace to time for each distance
            row[f"{distance}"] = round(time_in_sec, 2)
        results.append(row)

    return results
