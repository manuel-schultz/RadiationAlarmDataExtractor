CREATE TABLE IF NOT EXISTS schema_histories (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    migration_version INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(migration_version)
    ON CONFLICT IGNORE
);

INSERT INTO schema_histories (migration_version) VALUES (0);