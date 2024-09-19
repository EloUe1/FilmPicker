# Telegram bot for selecting movies [@FilmPickerTgBot](https://t.me/FilmPickerTgBot)
## Introduction
Every weekend people have difficulty choosing a movie for the evening. This bot is designed to solve this problem.
Movies are shown in the form of descriptions so that you don't miss a good movie because of the negativity of a boring title or poster.
## Features
* Selecting a film based on an intriguing description
* View information about the film (director, actors, year of production, genre, poster)
## Structure
PostgreSQL:
* Storing information about films, with the ability to add new ones.
* Storing anonymized information about the number of unique users with the last date of use of the bot.

pgAdmin 4 web:
* Database interaction and control.

.py app:
* Provides processing of data received from users, interaction with the database and Telegram.

Docker Compose:
* Provides convenient and quick deployment and configuration of interaction of application services on the server.

## Launch
1. Install [Docker](https://www.docker.com/)
2. Install [Docker Compose](https://docs.docker.com/compose/install/)
3. Create empty directory: "images" for storing posters from volumes.
4. Create and fill .env file like below:

```
PG_USER="..."
PG_PASSWORD="..."
PG_DB="..."
PG_ADMIN_PORTS="..."
DB_PORTS="..."
PGADMIN_DEFAULT_EMAIL="..."
PGADMIN_DEFAULT_PASSWORD="..."

BOT_TOKEN="..."
SECRET_MESSAGE="..."
SECRET_NUMBER="..."
SECRET_NAME="..."
```
5. Build, create, start, and attaches to containers for a service:
```
docker compose up
```
6. Create tables in the database (use "your server IP":5000" in browser), fill the films2 table with data about your films.
```
CREATE TABLE "users_table" (
    "tg_id"	VARCHAR,
    "datetime"	VARCHAR
);

CREATE TABLE position (
    "tg_id" VARCHAR,
    "place" INT
);

CREATE TABLE "films2" (
    "place"	INT,
    "name"	VARCHAR,
    "year"	VARCHAR,
    "filmmaker"	VARCHAR,
    "ganre"	VARCHAR,
    "actors"	VARCHAR,
    "description"	VARCHAR,
    "authority"	VARCHAR
);
```
7. Upload the posters to the folder following the path: /root/project/images
