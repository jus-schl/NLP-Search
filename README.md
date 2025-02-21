README

The app uses a PostgreSQL database, so in order to run the app locally you need to install PostgreSQL and create the needed table to the database with the command psql < schema.sql. Also the .env file should have the database address of the form DATABASE_URL=postgresql://user:password@localhost:port/databasename

user, password, port and databasename should be changed according to your local info, but the port is by default 5432.

After the table is created, the data can be added to the database by running the create_db.py file.
