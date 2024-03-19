# Running Pace Table API

## Overview

The Running Pace Table API is a FastAPI application designed to calculate running paces for various distances. This API takes input parameters like minimum pace, maximum pace, and increment step, and returns a table of estimated running times for official race distances.

## Installation

To set up the Running Pace Table API on your local machine, follow these steps:
1. Clone the Repository

```bash
git clone https://your-repository-url/running_pace_table.git
cd running_pace_table
```

2. Create and Activate a Virtual Environment (Optional)

For Linux/MacOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```
python -m venv venv
venv\Scripts\activate
```

3. Install Requirements

```
pip install -r requirements.txt
```

## Running the API

To start the API server, run the following command:

```
uvicorn running_pace_api.main:app --reload
```

The API will be available at http://localhost:8000.

## API Endpoints

The API provides the following endpoints:

- POST /generate\_table: Generates a pace table based on the provided minimum pace, maximum pace, and increment values.

## Generating Documentation

To generate the API documentation using Sphinx:

1. Navigate to the docs directory:

``` bash
cd docs
```

2. Run the following command to generate the documentation:

``` bash
make html
```

3. The generated HTML documentation will be available in the _build/html directory.

## Testing

To run the test suite, execute the following:

```bash
pytest
```

Ensure that all tests pass successfully to confirm that the API is functioning as expected.
Contribution

Feel free to contribute to the Running Pace Table API. If you encounter any issues or have suggestions, please open an issue or a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
