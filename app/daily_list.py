import argparse
from db import (
    create_connection,
    create_migration as db_create_migration,
    perform_get_all_query as db_get,
    insert_task,
    upgrade_migration as db_upgrade_migration
)
import sqlite3
from datetime import datetime

def get_arguments():
    parser = argparse.ArgumentParser(
        prog="Daily list",
        description="Simple list program, meant for daily tasks."
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-st", "--show-tasks", action="store_true", dest="show_tasks")
    group.add_argument("-sm", "--show-migrations", action="store_true", dest="show_migrations")

    group.add_argument("-a", "--add")
    group.add_argument("-r", "--remove")

    group.add_argument("-mc", "--migration-create", dest="migration_create")
    group.add_argument("-mu", "--migration-upgrade", dest="migration_upgrade", action="store_true")
    group.add_argument("-md", "--migration-downgrade", dest="migration_downgrade", action="store_true")

    return parser.parse_args()

def daily_list():
    args = get_arguments()
    db_connection = create_connection()

    if(args.show_tasks):
        show_tasks(db_connection)
    elif(args.show_migrations):
        show_migrations(db_connection)
    elif(args.add):
        add(db_connection, args.add)
    elif(args.migration_create):
        create_migration(args.migration_create)
    elif(args.migration_upgrade):
        upgrade_migration(db_connection)

def show_tasks(db_connection: sqlite3.Connection):
    tasks = db_get(db_connection, "tasks")

    print("-"*64)

    for task in tasks:
        _, title, description, date = task
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').date()

        print("Título: ", title)
        print(date)
        print("Descripción:", description)

        print("-"*64)

def add(db_connection: sqlite3.Connection, object_string: str):
    name = ""
    description = None

    if len(object_string.split(";")) < 2:
        name = object_string
        insert_task(db_connection, name, datetime.now())
    else:
        name, description = object_string.split(";")
        insert_task(db_connection, name, datetime.now(), description=description)

def create_migration(name):
    db_create_migration(name)

def upgrade_migration(db_connection: sqlite3.Connection):
    db_upgrade_migration(db_connection)

def show_migrations(db_connection: sqlite3.Connection):
    migrations = db_get(db_connection, "migrations")

    print("-"*64)

    for migration in migrations:
        _, title = migration

        print("Título: ", title)

        print("-"*64)