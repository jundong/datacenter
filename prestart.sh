#! /usr/bin/env bash

# Let the DB start
python ./db/db_pre_start.py

# Run migrations
alembic revision --autogenerate -m "first commit"

alembic upgrade head

# Create initial data in DB
python ./app/initial_data.py
