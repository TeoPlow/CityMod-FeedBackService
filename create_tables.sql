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
    images_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    files_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE other_content (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    info TEXT,
    images_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    files_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE maps (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    game_versions TEXT NOT NULL,
    mod_version TEXT NOT NULL,
    info TEXT,
    images_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    files_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE objects_in_mod (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT NOT NULL,
    mod_id TEXT NOT NULL,
    path TEXT NOT NULL,
    info TEXT NOT NULL,
    version_added TEXT,
    image_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    model_id BIGINT REFERENCES Files(id) ON DELETE SET NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для ускорения запросов
CREATE INDEX idx_reviews_user_id ON feedback(user_id);
