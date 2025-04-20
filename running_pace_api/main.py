"""
The Running Pace Table API is a FastAPI application designed to calculate running paces for
various distances.  This API  takes input  parameters  like minimum pace, maximum pace, and
increment step, and returns a table of  estimated running times for official race distances.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from running_pace_api.models import TableParameters
from running_pace_api.services import wr_service
from running_pace_api.services import athletes_service
from running_pace_api.services import pace_table_service
from running_pace_api.services import database_service

app = FastAPI()

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://allures.moron.at",
    "https://allures.moron.at",
    "http://mypacer.fr",
    "https://mypacer.fr",
    "http://www.mypacer.fr",
    "https://www.mypacer.fr",
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
    return wr_service.get_world_records()

@app.post("/generate_table")
async def generate_table(params: TableParameters):
    """
    Endpoint to generate a table of paces for various official race distances.

    Args:
    params (TableParameters): The pace parameters for generating the table.

    Raises:
    HTTPException: If the minimum pace is greater than the maximum pace.

    Returns:
    List[Dict]: A table of calculated times for each distance at each pace.
    """
    return pace_table_service.get_pace_table(params.min_pace, params.max_pace, params.increment, params.distances)

@app.get("/get_athletes")
async def get_athletes(name: str):
    """
    Retrieves athlete information from the 'le pistard' database based on the provided athlete name.

    Args:
    name (str): The name of the athlete to search for.

    Returns:
    JSON response containing the data of the athletes matched by the search. The data format
    includes a list of athlete entries with details specific to the 'le pistard' database structure.

    Examples:
    Response format example (success):
    [
    {
    "birth_date": "1983-04-22",
    "id": "123",
    "name": "John Doe",
    "url": "https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=453"
    }
    ]
    """
    return athletes_service.get_athlete(name)

@app.get("/get_athletes_from_db")
async def get_athletes_from_db(name: str):
    """
    Retrieves athlete information from the locale database based on the provided athlete name.

    Args:
    name (str): The name of the athlete to search for.

    Returns:
    dict: A dictionary containing the athlete's information.
    """
    return athletes_service.get_athletes_from_db(name)

@app.get("/get_athlete_records")
async def get_athlete_records(ident) -> dict:
    """
    Retrieves athlete records from the 'bases.athle.fr' website based on the provided athlete ID.

    Args:
    ident (str): The ID of the athlete to search for.

    Returns:
    dict: A dictionary containing the athlete's records for various disciplines and distances.
    """
    return athletes_service.get_athlete_records(ident)

@app.get("/database_status")
async def database_status():
    """
    Endpoint to retrieve information about the database state, including
    the number of clubs, the number of athletes, and the date of the last update.

    Returns:
        dict: A dictionary containing the number of clubs, number of athletes,
              and the date of the last update.
    """
    return database_service.get_database_status()
