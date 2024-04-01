from typing import List

def upgrade() -> List[str]:
    create_migrations_table_query = """
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """

    create_tasks_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            date DATETIME NOT NULL
        );
    """

    return [create_tasks_table_query, create_migrations_table_query]

def downgrade() -> List[str]:
    drop_tasks_table_query = """
        DROP TABLE IF EXISTS tasks;
    """

    drop_migrations_table_query = """
        DROP TABLE IF EXISTS migrations;
    """

    return [drop_tasks_table_query, drop_migrations_table_query]
