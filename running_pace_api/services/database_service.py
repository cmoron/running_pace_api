"""
This module contains functions that interact with the database.
"""
import os
from dotenv import load_dotenv
import psycopg2

def get_database_status():
    """
    Retrieves information about the database, including the number of clubs,
    the number of athletes, and the date of the last update.

    Returns:
        dict: A dictionary containing the number of clubs, number of athletes,
              and the date of the last update.
    """
    load_dotenv()
    db_connection = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432')
    }

    conn = psycopg2.connect(**db_connection)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM clubs;")
        num_clubs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM athletes;")
        num_athletes = cursor.fetchone()[0]

        cursor.execute("""
        SELECT GREATEST(
            MAX(last_vacuum),
            MAX(last_autovacuum),
            MAX(last_analyze),
            MAX(last_autoanalyze)
        ) AS last_update
        FROM pg_stat_all_tables
        WHERE relname = 'athletes';
        """)
        last_update = cursor.fetchone()[0]

        return {
            "num_clubs": num_clubs,
            "num_athletes": num_athletes,
            "last_update": last_update
        }
    except psycopg2.Error as exc:
        raise exc
    finally:
        cursor.close()
        conn.close()
