CREATE SCHEMA IF NOT EXISTS todo;

SET search_path TO todo;

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    priority VARCHAR(10) NOT NULL CHECK (priority IN ('низкий', 'средний', 'высокий')),
    is_done BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
