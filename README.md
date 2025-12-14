# MyPacer API

## Overview

The MyPacer API is a FastAPI application designed to calculate running paces for various distances. This API takes input parameters like minimum pace, maximum pace, and increment step, and returns a table of estimated running times for official race distances.

The application also provides athlete data integration with the French Athletics Federation (FFA) database, allowing users to search for athletes and retrieve their performance records.

## Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.12+ (for local development without Docker)
- PostgreSQL (included in Docker setup)

## Quick Start with Docker

### Production Deployment

1. Clone the repository:

```bash
git clone https://your-repository-url/mypacer_api.git
cd mypacer_api
```

2. Create a `.env` file with the required environment variables:

```bash
POSTGRES_CONTAINER=mypacer_pgsql
POSTGRES_DB=mypacer
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secure_password
```

3. Build and start the services:

```bash
docker-compose up -d
```

4. The API will be available at http://localhost:8000

5. To view logs:

```bash
docker-compose logs -f api
```

6. To stop the services:

```bash
docker-compose down
```

### Development Mode with Hot Reload

For development with automatic code reloading, use the dedicated development compose file.

**Note for Linux/MacOS users:** To avoid file permission issues between your host machine and the container, it's crucial to run the application with the same user ID (UID) and group ID (GID) as your current user. The `Dockerfile` is configured to accept these as build arguments.

Run the following command to start the development environment. It will build the image on first run, passing your user's UID/GID:

```bash
HOST_UID=$(id -u) HOST_GID=$(id -g) docker-compose -f docker-compose.dev.yml up --build
```

Once the container is built, you can start and stop it with:
```bash
# To start
HOST_UID=$(id -u) HOST_GID=$(id -g) docker-compose -f docker-compose.dev.yml up

# To run in detached mode
HOST_UID=$(id -u) HOST_GID=$(id -g) docker-compose -f docker-compose.dev.yml up -d
```

This configuration:
- Mounts your source code as a volume for live reloading.
- Runs uvicorn with the `--reload` flag.
- Ensures the container user has the correct permissions on the mounted source code.


## Local Installation (Without Docker)

If you prefer to run the application without Docker:

1. Clone the Repository:

```bash
git clone https://your-repository-url/mypacer_api.git
cd mypacer_api
```

2. Create and Activate a Virtual Environment:

For Linux/MacOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Requirements:

```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database and configure environment variables

5. Run the API:

```bash
uvicorn mypacer_api.main:app --reload
```

Or use the provided script:

```bash
./run.sh
```

The API will be available at http://localhost:8000.

## CI/CD & Docker Images

- `.github/workflows/ci.yml` exécute les tests avec PostgreSQL sur chaque push/PR.
- `.github/workflows/docker.yml` construit et pousse l'image multi-stage (cible `prod`) vers GHCR : `ghcr.io/cmoron/mypacer_api:latest-prod` (tags semver/sha aussi).
- Pour une construction locale :
  ```bash
  docker build -t mypacer_api:dev --target dev .
  docker build -t mypacer_api:latest-prod --target prod .
  ```

## API Documentation

Once the application is running, you can access:

- **Interactive API documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API documentation (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

The API provides the following endpoints:

### Pace Calculation

- **POST /generate_table**: Generates a pace table based on the provided minimum pace, maximum pace, and increment values.
  - Parameters: `min_pace`, `max_pace`, `increment`, `distances`
  - Returns: A table of calculated times for each distance at each pace

### Athletes Management

- **GET /get_athletes**: Retrieves athlete information from the FFA database
  - Query parameter: `name` (athlete name to search for)
  - Returns: List of athletes matching the search

- **GET /get_athletes_from_db**: Retrieves athlete information from the local database
  - Query parameter: `name` (athlete name to search for)
  - Returns: Athlete information from local database

- **GET /get_athlete_records**: Retrieves athlete records from bases.athle.fr
  - Query parameter: `ident` (athlete ID)
  - Returns: Dictionary containing the athlete's records for various disciplines

### Database Status

- **GET /database_status**: Get information about the database state
  - Returns: Number of clubs, number of athletes, and date of last update

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
POSTGRES_CONTAINER=mypacer-postgres
POSTGRES_DB=mypacer_db
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secure_password
```

### Database Initialization

The PostgreSQL database is automatically initialized with the `db/init.sql` script on first startup.

## Testing

To run the test suite:

With Docker:

```bash
docker-compose exec api pytest
```

Without Docker:

```bash
pytest
```

Ensure that all tests pass successfully to confirm that the API is functioning as expected.

## Generating Documentation

To generate the API documentation using Sphinx:

1. Navigate to the docs directory:

```bash
cd docs
```

2. Run the following command to generate the documentation:

```bash
make html
```

3. The generated HTML documentation will be available in the `docs/_build/html` directory.

## Project Structure

```
mypacer_api/
├── mypacer_api/           # Main application package
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # Data models
│   ├── dependencies.py    # Dependency injection
│   ├── core/              # Core modules (calculator, database, scrapper)
│   └── services/          # Business logic services
├── db/                    # Database files
│   └── init.sql           # Database initialization script
├── docs/                  # Documentation and optimization guides
├── tests/                 # Test files
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker services configuration (production)
├── docker-compose.dev.yml # Docker services configuration (development)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Troubleshooting

### Port Already in Use

If port 8000 or 5432 is already in use, modify the port mappings in `docker-compose.yml` or `docker-compose.dev.yml`:

```yaml
ports:
  - "8001:8000"  # Use port 8001 on host instead
```

### Database Connection Issues

Ensure the PostgreSQL container is running and healthy:

```bash
docker-compose ps
docker-compose logs postgres
```

### Rebuild After Code Changes

If you make changes to dependencies, rebuild the Docker image:

```bash
docker-compose build
docker-compose up -d
```

Or for development:

```bash
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d
```

## Contributing

Feel free to contribute to the MyPacer API. If you encounter any issues or have suggestions, please open an issue or a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
