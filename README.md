# artisan-backend

## Running the application 

Before running, you'll need to setup database, database URL can be configured
in the .env file.

To create table you can use added migration, we use alembic to manage database migrations. 

Run following commands to set up tables in database, code has been tested with postgres and SQLite:
```bash
alembic upgrade head
```

To run the application, you can use the following command from root directory:

```bash
fastapi dev app/main.py
```

To run the tests, you can use the following command from root directory:

You must pass ENV as test to run the tests, as we are using SQLite database for testing.

```bash
ENV=test pytest
```


