CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL
);

INSERT INTO messages (id, message) VALUES (1, 'Hello from PostgreSQL!')
ON CONFLICT (id) DO NOTHING;