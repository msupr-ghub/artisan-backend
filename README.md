# artisan-backend

## Running the application 

Create a virtual environment and install the dependencies (This project was tested with Python 3.12.5):

```bash
python -m venv venv
source .venv/bin/activate
pip install -r requirements.txt
```

Before running, you'll need to setup database, database URL can be configured
in the .env file.

To create table you can use added migration, we use alembic to manage database migrations. 

Run following commands to set up tables in database, code has been tested with postgres and SQLite:
```bash
alembic upgrade head
```

##### Please also add OPEN_AI key in .env file to use OpenAI API. Without this APP will not work. Existing key is already expired.

To run the application, you can use the following command from root directory:

```bash
fastapi dev app/main.py
```

To run the tests, you can use the following command from root directory:

You must pass ENV as test to run the tests, as we are using SQLite database for testing.

```bash
ENV=test pytest app/tests/api_tests.py
```


