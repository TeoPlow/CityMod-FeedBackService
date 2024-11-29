CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL
);

CREATE TABLE feedback (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    type TEXT NOT NULL,
    message TEXT,
    files_id BIGINT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE files (
    id BIGSERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_info TEXT,
    file_path TEXT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mods (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    release_channel TEXT NOT NULL,
    version TEXT NOT NULL,
    game_versions TEXT NOT NULL,
    changelog TEXT,
    files_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE other_content (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    info TEXT,
    files_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE maps (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    changelog TEXT,
    files_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для ускорения запросов
CREATE INDEX idx_reviews_user_id ON feedback(user_id);
