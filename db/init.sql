-- Création des tables
CREATE TABLE IF NOT EXISTS clubs (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    first_year INTEGER DEFAULT 0,
    last_year INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS athletes (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url TEXT,
    birth_date VARCHAR(255),
    license_id VARCHAR(255),
    sexe VARCHAR(10),
    nationality VARCHAR(50)
);

-- Importation des données
COPY clubs FROM '/var/lib/postgresql/db/clubs.csv' DELIMITER ',' CSV HEADER;
COPY athletes FROM '/var/lib/postgresql/db/athletes.csv' DELIMITER ',' CSV HEADER;
