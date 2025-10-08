-- migrate:up
CREATE TABLE IF NOT EXISTS team_registrations (
    id              SERIAL            PRIMARY KEY,
    team_name       VARCHAR(255)      NOT NULL,
    selected_case   VARCHAR(255)      NOT NULL,
    captain_name    VARCHAR(255)      NOT NULL,
    captain_email   VARCHAR(255)      NOT NULL,
    team_members    TEXT              NOT NULL,
    registration_date VARCHAR(255)    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event           VARCHAR(255)      NOT NULL,
    status          VARCHAR(50)       NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMPTZ       NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ       NOT NULL DEFAULT NOW()
);

-- migrate:down
DROP TABLE IF EXISTS team_registrations;