import mysql.connector
# Allow exec commands in terminal, for create tables to database
import click
# current_app keep the application
# g variable present in the app, assign and use
from flask import current_app, g
# For create the database, accesing variables of app
from flask.cli import with_appcontext
# Scripts for create database
from .schema import instructions


def get_db():
    """Obtain DB and cusor"""
    if 'db' not in g:
        g.db = mysql.connector.connect(user=current_app.config['TODOER_DATABASE_USER'],
                                       password=current_app.config['TODOER_DATABASE_PASSWORD'],
                                       host=current_app.config['TODOER_DATABASE_HOST'],
                                       database=current_app.config['TODOER_DATABASE'])

        # Use cursor to exec queries
        g.c = g.db.cursor(dictionary=True)

    return g.db, g.c


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    """Close DB after finish request"""
    # Registers a function to be called when the application context ends
    app.teardown_appcontext(close_db)
