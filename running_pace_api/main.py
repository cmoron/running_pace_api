"""
The Running Pace Table API is a FastAPI application designed to calculate running paces for
various distances.  This API  takes input  parameters  like minimum pace, maximum pace, and
increment step, and returns a table of  estimated running times for official race distances.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from running_pace_api.models import TableParameters
from running_pace_api.core import calculator, scrapper

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

@app.get("/get_world_records")
async def get_world_records():
    """
    Endpoint to retrieve world records from the World Athletics website.

    Returns:
    dict: A dictionary containing world records for various distances and events.
    """
    return scrapper.scrap_records_page()

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
    return calculator.calculate_pace_table(params.min_pace, params.max_pace, params.increment)
