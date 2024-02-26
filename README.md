# Casting Agency API
Final project for the full stack web dev course.
This API is intended to be used by a casting agency with data models for actors and movies.

The API is hosted at https://udacity-fsnd-final-project.onrender.com

## Motivation

This project is the final project for the Udacity Full Stack Nanodegree. It combines the skills taught regarding databases, APIs, and authentication into a single project.

## Setting Up the Backend

### Install Dependancies

1. **Python 3.12** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Postman** - Postman is an API platform for building and using APIs. In this application, postman is used to test the API endpoints. Install the latest version of postman for your platform [here](https://www.postman.com/)

3. **PostgresSQL 15** - PostgreSQL is a relational database system which is an extension of SQL. Download PostgreSQL version 15 [here](https://www.postgresql.org/download/). The installation includes the psql tool which will be used to set up and interact with the database outside of the app.

3. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

4. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the root directory and running:

```bash
pip install -r requirements.txt
```
#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Set Up the Database

With postgres running, create a `casting` and `casting_test` database:

**Windows (psql tool)**
```powershell
CREATE DATABASE casting;
CREATE DATABASE casting_test;
```

**Linux**
```bash
createdb trivia
createdb casting_test
```

Populate the two databases using the `casting.psql` file provided. From the root folder in terminal run:

**Windows (psql tool)**
```powershell
\c casting
\i casting.psql
\c casting_test
\i casting.psql
```

**Linux**
```bash
psql casting < casting.psql
psql casting_test < casting.psql
```

### Set Up Environment Variables

Create a .env file in the `./src` directory. A template for the file is below, fill in variables as applicable.

```bash
DB_NAME=""
TEST_DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_PATH_HOSTED=""
AUTH0_DOMAIN=""
API_AUDIENCE=""
```

### Authentication with Auth0

This app makes use of the Auth0 service to generate jwt access tokens, used for RBAC. Auth0 will need to be set up with the appropriate application, API, and roles (described in the RBAC section) to make the application work. 

### Run the Server Locally

from within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

**Windows**
```powershell
$env:FLASK_APP='flaskr'
$env:FLASK_DEBUG='true'
```

**Linux**
```bash
export FLASK_APP=api.py;
export FLASK_DEBUG=true;
```

To run the server, execute:

```bash
flask run
```

the `FLASK_DEBUG` variable will detect file changes and restart the server automatically.

## Local Development

### Running the Postman Collection

1. **Import the Postman Collection** - Use the Postman tool to import Casting-Service.postman_collection.json.

2. **Verify Variables** - Navigate to the main collection folder (Casting-Service) and verify that `base_url, casting_assistant_token, casting_director_token, and executive_prod_token are correct.

3. **Verify Endpoints** - Verify that PATCH and DELETE URIs are referencing objects that exist in the database. ie {{base_url}}/movies/ **1**

4. **Run the collection** - The collection can be run by right-clicking the selection (Casting-Service) and selecting run. Note that some of the PATCH and DELETE tests may fail as the database is updated during certain tests and objects may no longer exist. Therefore, it is recommended that the tests for each role be run indivdually.

## Deployment to Render

### Setting Up the Hosted Database

1. **Create a Hosted Database** - Create a new PostgreSQL database with PostgreSQL Version 15.

2. **Copy Internal Database URL** - Once the database is created, copy the internal database URL. This is required later.

3. **Set Up the Database** - Copy the database's PSQL command (under connections). This is used to connect to the database with the psql tool. Then follow the instructions in the "Set Up the Database" section to populate the database with the casting.psql file.

### Create the Web Service

4. **Create a Web Service** - Create a new web service, configured to build and deploy from a GitHub repository. Setup the following parameters as follows:
    - Root directory: src
    - Build Command: `pip install -r ../requirements.txt`
    - Start Command: `guinicorn wsgi:app`

5. **Set Environment Variables** - Set up the environment variables unique to the application
    - API_AUDIANCE: As applicable to the app
    - AUTH0_DOMAIN: As applicable to the app
    - DB_PATH_HOSTED: Copied from step two

Now, the web service can be created and it will automatically start the build using the latest commit on the `main` branch in the specified GitHub repository. Verify the build is successful in the logs. Postman can also be used to test the endpoints, just change the `base_url` variable to match the hosted URL.

## Role Based Access Controls

There are three roles in this application. Casting Assistant, Casting Director, and Excutive Producer. Their permissions are listed below.

- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

## API Endpoints

### `GET '/actors'`

Gets a list of all actors.
Sample response:
```json
{
    "actors": [
        {
            "age": 30,
            "gender": "Female",
            "id": 1,
            "movies": 1,
            "name": "Jennifer Lawrence"
        },
        {
            "age": 30,
            "gender": "Male",
            "id": 2,
            "movies": 1,
            "name": "Josh Hutcherson"
        }
    ],
    "success": true
}
```

### `GET '/movies'`

Gets a list of all movies.
Sample response:
```json
{
    "movies": [
        {
            "actors": [
                {
                    "age": 30,
                    "gender": "Female",
                    "id": 1,
                    "movies": 1,
                    "name": "Jennifer Lawrence"
                },
                {
                    "age": 30,
                    "gender": "Male",
                    "id": 2,
                    "movies": 1,
                    "name": "Josh Hutcherson"
                }
            ],
            "id": 1,
            "release_date": "Thu, 01 Mar 2012 00:00:00 GMT",
            "title": "The Hunger Games"
        }
    ],
    "success": true
}
```

### `POST '/actors'`

Create a new actor.
Sample response:
```json
{
    "actors": [
        {
            "age": 30,
            "gender": "Female",
            "id": 1,
            "movies": 1,
            "name": "Jennifer Lawrence"
        },
        {
            "age": 30,
            "gender": "Male",
            "id": 2,
            "movies": 1,
            "name": "Josh Hutcherson"
        },
        {
            "age": 20,
            "gender": "test",
            "id": 3,
            "movies": null,
            "name": "test actor"
        }
    ],
    "created": 3,
    "success": true
}
```

### `POST '/movies'`

Create a new movie.
Sample response:
```json
{
    "created": 2,
    "movies": [
        {
            "actors": [],
            "id": 2,
            "release_date": "Wed, 01 Jan 2020 00:00:00 GMT",
            "title": "test movie"
        },
        {
            "actors": [
                {
                    "age": 30,
                    "gender": "Female",
                    "id": 1,
                    "movies": 1,
                    "name": "Jennifer Lawrence"
                },
                {
                    "age": 30,
                    "gender": "Male",
                    "id": 2,
                    "movies": 1,
                    "name": "Josh Hutcherson"
                }
            ],
            "id": 1,
            "release_date": "Thu, 01 Mar 2012 00:00:00 GMT",
            "title": "The Hunger Games"
        }
    ],
    "success": true
}
```

### `PATCH '/actors/actor_id'`

Edit an actor.
Sample response:
```json
{
    "actor_id": 3,
    "success": true
}
```

### `PATCH '/movies/movie_id'`

Edit a movie.
Sample response:
```json
{
    "movie_id": 2,
    "success": true
}
```

### `DELETE '/actors/actor_id'`

Delete an actor.
Sample response:
```json
{
    "actors": [
        {
            "age": 30,
            "gender": "Female",
            "id": 1,
            "movies": 1,
            "name": "Jennifer Lawrence"
        },
        {
            "age": 30,
            "gender": "Male",
            "id": 2,
            "movies": 1,
            "name": "Josh Hutcherson"
        }
    ],
    "deleted": 3,
    "success": true
}
```

### `DELETE '/movies/movie_id'`

Delete a movie.
Sample response:
```json
{
    "deleted": 2,
    "movies": [
        {
            "actors": [
                {
                    "age": 30,
                    "gender": "Female",
                    "id": 1,
                    "movies": 1,
                    "name": "Jennifer Lawrence"
                },
                {
                    "age": 30,
                    "gender": "Male",
                    "id": 2,
                    "movies": 1,
                    "name": "Josh Hutcherson"
                }
            ],
            "id": 1,
            "release_date": "Thu, 01 Mar 2012 00:00:00 GMT",
            "title": "The Hunger Games"
        }
    ],
    "success": true
}
```
