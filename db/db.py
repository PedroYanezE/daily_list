import sqlite3
from sqlite3 import Error
from datetime import datetime
from templates import INSERT_PERFORMED_MIGRATION, NEW_MIGRATION_TEMPLATE
from os import listdir
from os.path import isfile, join
import importlib.util
from typing import List

def create_connection() -> sqlite3.Connection:
    connection = None
    try:
        connection = sqlite3.connect("db/daily_list.sqlite")
    except Error as e:
        print(f"Error '{e}' ocurred")
    
    return connection

def perform_create_query(connection: sqlite3.Connection, query: str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"Error performing query: {e}")

def perform_get_all_query(connection: sqlite3.Connection, table_name):
    select_table_query = f"""
        SELECT * FROM {table_name};
    """

    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(select_table_query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error reading table {table_name}: {e}")
        return []

def insert_task(connection: sqlite3.Connection, title,  date, description = "Sin descripción."):
    insert_task_query = f"""
        INSERT INTO
            tasks (title, description, date)
        VALUES
            ('{title}', '{description}', '{date}');
    """

    perform_create_query(connection, insert_task_query)


def create_migration(name: str):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    with open(f"db/migrations/{current_time}-{name}.py", "w") as outfile:
        outfile.write(NEW_MIGRATION_TEMPLATE)

def upgrade_migration(connection: sqlite3.Connection):
    first_pending_migration = get_first_pending_migration(connection)
    print(first_pending_migration)

    spec = importlib.util.spec_from_file_location("upgrade", f"db/migrations/{first_pending_migration}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    upgrade_function = getattr(module, "upgrade")
    query_list = upgrade_function()
    query_list.append(INSERT_PERFORMED_MIGRATION.format(first_pending_migration))

    for query in query_list:
        perform_create_query(connection, query.strip())

def get_first_pending_migration(connection: sqlite3.Connection) -> str:
    migration_files = [f[:-3] for f in listdir("db/migrations") if isfile(join("db/migrations", f))]
    performed_migrations = perform_get_all_query(connection, "migrations")

    if len(performed_migrations) == 0:
        return migration_files[0]

    for counter, migration_name in enumerate(migration_files):
        if(migration_files[counter] != performed_migrations[counter]):
            return migration_name
