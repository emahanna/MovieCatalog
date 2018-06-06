# Simple Movie Catalog Application
This project is a simple catalog for movies sorted by genre which allows users to login and complete CRUD operations.
The project consists of:


## Software Requirements
* Python 2.7 or above
* SQLite 3
* Flask
* sqlalchemy
* Terminal or command prompt

## Download
Download all files within this repository.

## How to Run Application

1. enter the file directory location with all downloaded files. 

2. run `database_setup.py` to create the database

3. run `lotsofmenus.py` to populate the database

4. run `project.py` and navigate to localhost:5000 in your browser


## How to Access API Endpoints

To access genres data: /genre/JSON

To access movies in a genre data: /genre/<int:genre_id>/movies/JSON

To access a single movie's data: /genre/<int:genre_id>/movies/<int:movie_id>/JSON
