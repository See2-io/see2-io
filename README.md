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
From within your python virtual environment, switch to the project root directory.

`cd <PROJECT_ROOT>`

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

## Django Fixtures
There are currently no Django fixtures in the project, but it makes sense to create one after running `make_enron_communities`    as this process takes a few minutes and requires a clean database to run.

```
python manage.py dumpdata > sense/fixtures/enron_communities.json
```

When needed, this dump can be reloaded with:

```
python manage.py loaddata < sense/fixtures/enron_communities.json
