from __future__ import annotations

import sqlite3


_T28_TABLES_IN_DROP_ORDER = (
    "dependent_adoption_fences",
    "adoption_dependencies",
    "effect_adoptions",
    "operation_origins",
    "legacy_descriptor_bindings",
    "effect_relationships",
    "effect_definitions",
    "synthetic_authority_lifecycle_facts",
    "synthetic_authority_uses",
    "synthetic_authority_grants",
    "synthetic_authority_source_state",
    "synthetic_authority_source_events",
)


def strip_t28_foundation_schema(connection: sqlite3.Connection) -> None:
    """Turn a current test database into an exact pre-T28 schema fixture."""
    connection.commit()
    connection.execute("PRAGMA foreign_keys = OFF")
    connection.execute("BEGIN IMMEDIATE")
    try:
        connection.execute(
            "CREATE TABLE outstanding_slot_v3 ("
            "singleton INTEGER PRIMARY KEY CHECK (singleton = 1), "
            "repository_id TEXT NOT NULL REFERENCES repositories(repository_id), "
            "run_id TEXT NOT NULL REFERENCES runs(run_id), "
            "logical_effect_id TEXT NOT NULL, attempt_id TEXT NOT NULL, "
            "generation INTEGER NOT NULL CHECK (generation > 0))"
        )
        connection.execute(
            "INSERT INTO outstanding_slot_v3 SELECT singleton, repository_id, "
            "run_id, logical_effect_id, attempt_id, generation "
            "FROM outstanding_slot"
        )
        connection.execute("DROP TABLE outstanding_slot")
        connection.execute(
            "ALTER TABLE outstanding_slot_v3 RENAME TO outstanding_slot"
        )
        for table_name in _T28_TABLES_IN_DROP_ORDER:
            connection.execute(f"DROP TABLE {table_name}")
    except BaseException:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.execute("PRAGMA foreign_keys = ON")
