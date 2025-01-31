CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    duration INTEGER NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    audio_link VARCHAR NOT NULL,
    is_bookmark BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TYPE episode_time AS ENUM ('MORNING', 'MIDDAY', 'ENDOFDAY');

ALTER TABLE episodes
ADD COLUMN time_of_day episode_time;

CREATE INDEX idx_is_bookmark ON episodes(is_bookmark);
CREATE INDEX idx_time_of_day ON episodes(time_of_day);
