#!/usr/bin/env python3

"""
Module pour extraire les données de la base de données SQLite et les écrire dans des fichiers CSV.
"""
import sqlite3
import csv

def extract_data(db_path, output_dir):
    """
    Extrait les données de la base de données SQLite et les écrit dans des fichiers CSV.

    Args:
        db_path (str): Chemin vers la base de données SQLite.
        output_dir (str): Répertoire où écrire les fichiers CSV.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Pour chaque table à exporter
    for table_name in ['clubs', 'athletes']:
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        # Remove extra space at the begining of the data
        headers = [header.strip() for header in headers]
        data = [[str(cell).strip() for cell in row] for row in data]

        # Écrire les données dans un fichier CSV
        with open(f"{output_dir}/{table_name}.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)

    conn.close()

if __name__ == '__main__':
    extract_data('bases_athle.db', '.')
