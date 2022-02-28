Python Web Backend Sample Stack
=====================================
This project aims to speed up the development of a web backend written in [Python](https://www.python.org/) using [Flask](https://flask.palletsprojects.com/en/2.0.x/) + [SQLAlchemy](https://www.sqlalchemy.org/), with the more common needs addressed. Both the Web Framework and ORM chosen are the most popular at the time of this implementation.

Notes
-----
1. This sample code uses SQLite as database backend however SQLAlchemy also supports Postgresql, MySQL, Oracle, MS-SQL, Firebird, Sybase and others;
2. Using this project as starting point *absolutely not* exempt you of reading [all](https://www.python.org/) of the material that you can before start coding using Python;
3. VSCode is the suggested code editor. You just need to install the extension from the Marketplace.

Setup
-----
1. Assuming that Python 3 is available in your terminal, run (just once):
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install --upgrade Flask requests sqlalchemy
    ```
2. Define an environment variable DATABASE_URL pointing to a file to be created (our SQLite database);
3. Call `FLASK_APP=src/app.py FLASK_ENV=development flask run` and open in your browser the URL shown at the console.
