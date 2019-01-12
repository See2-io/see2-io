# See2.io
An early prototype for See2.io using the Enron Corporation emails.

## Requirements
- Python3.7
- Virtualenv
- All required libraries should be listed in setup.py file and requirements.txt

## Installation
```
virtualenv .venv
source .venv/bin/activate
pip install .
```

This will install all requirements into virtual environment, to use it you will need to activate it first:

`source .venv/bin/activate`

## How to Use
Create Django database (default SQLite)

```
python manage.py makemigrations
python manage.py migrate
```
If there are no reported errors, this should create the "db.sqlite3" database file in the project root directory.

Make the Enron Corporation Super Community and its sub-communities, run:

`python manage.py make_enron_communities`

This sets up the database to run the Enron simulation, which generates "user sign-up" and email events:

`python manage.py enron_sim`
