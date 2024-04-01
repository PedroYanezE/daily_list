NEW_MIGRATION_TEMPLATE = """from typing import List

def upgrade() -> List[str]:
    create_query = \"\"\"
    \"\"\"

    return [create_query]

def downgrade() -> List[str]:
    drop_query = \"\"\"
    \"\"\"

    return [drop_query]
"""

INSERT_PERFORMED_MIGRATION = """
    INSERT INTO
        migrations (name)
    VALUES
        ('{0}');
"""
