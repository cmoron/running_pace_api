"""
This module contains the service functions for the 'athletes' endpoint.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
from unidecode import unidecode
from fastapi import HTTPException
from running_pace_api.core import scrapper
from dotenv import load_dotenv

load_dotenv()

def convert_id_to_url(ident):
    """
    Converts base.athle.fr id to base.athle.fr records url

    Args:
    ident (str): The id retrieve from lepistard.run

    Returns:
    url (str) to the base.athle.fr records page
    """
    records_url = "https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq="
    complement = ''.join(f"{99 - ord(c)}{ord(c)}" for c in str(ident))

    return records_url + complement

def get_athlete(name: str) -> list:
    """
    Retrieves athlete information from the 'le pistard' database based on the provided athlete name.

    Args:
    name (str): The name of the athlete to search for.

    Returns:
    JSON response containing the data of the athletes matched by the search. The data format
    includes a list of athlete entries with details specific to the 'le pistard' database structure.

    Raises:
    HTTPException: If the external request fails or the response is not in JSON format.

    Note:
    This endpoint makes a POST request to 'https://lepistard.run/wp-admin/admin-ajax.php' using
    the 'get_listing_names' action to search within the 'athlete' table by 'nom' (name) column.
    The API relies on correct formatting of the request and appropriate handling of the response.
    """
    url = "https://lepistard.run/wp-admin/admin-ajax.php"
    data = {
            'action': 'get_listing_names',
            'name': name,
            'table': "athlete",
            'column': "nom"
            }
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

    response = requests.post(url, data=data, headers=headers, timeout=10)
    if response.status_code == 200:
        try:
            athletes = response.json()
            transformed_response = [
                    {
                        'id': athlete['code'],
                        'url': convert_id_to_url(athlete['code']),
                        'name': athlete['nom'],
                        'birth_date': athlete['date_naissance']
                        }
                    for athlete in athletes
                    ]
            return transformed_response
        except ValueError as exc:
            raise HTTPException(status_code=500,
                                detail="The response is not in JSON format.") from exc
    else:
        raise HTTPException(status_code=response.status_code,
                            detail="Failed to make an external request")

def get_athletes_from_db(name: str) -> list:
    """
    Retrieves athletes information from the PostgreSQL database based on the provided athlete name.

    Args:
        name (str): The name of the athlete to search for.

    Returns:
        List of dictionaries containing athlete data.
    """
    db_connection = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432')
    }

    try:
        conn = psycopg2.connect(**db_connection)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        normalized_query = ' '.join(unidecode(name).lower().strip().split())
        query_parts = normalized_query.split()
        where_clause = " AND ".join(["LOWER(name) LIKE %s" for _ in query_parts])
        query = f"""
        SELECT id, name, url, birth_date, license_id, sexe, nationality
        FROM athletes
        WHERE {where_clause}
        LIMIT 25
        """
        search_patterns = [f'%{part}%' for part in query_parts]

        cursor.execute(query, search_patterns)
        results = cursor.fetchall()

    except psycopg2.Error as exc:
        raise HTTPException(status_code=500, detail="Failed to connect to the database.") from exc
    finally:
        cursor.close()
        conn.close()

    return results

def get_athlete_records(ident) -> dict:
    """
    Retrieves athlete records from the 'bases.athle.fr' website based on the provided athlete ID.

    Args:
    ident (str): The ID of the athlete to search for.

    Returns:
    dict: A dictionary containing the athlete's records for various disciplines and distances.
    """
    url = convert_id_to_url(ident)
    return scrapper.scrap_athlete_records(url)
