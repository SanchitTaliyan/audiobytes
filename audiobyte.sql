CREATE TABLE episodes
(
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

INSERT INTO episodes
    (title, description, duration, published_at, audio_link, is_bookmark, is_deleted, time_of_day)
VALUES
    ('Morning Talk', 'A relaxing morning conversation with a special guest.', 30, '2025-01-30 08:00:00+00', 'https://audiobyte.s3.amazonaws.com/audio/068a834c-2314-4079-85e1-83cf414bd3ed.mp3', TRUE, FALSE, 'MORNING');

INSERT INTO episodes
    (title, description, duration, published_at, audio_link, is_bookmark, is_deleted, time_of_day)
VALUES
    ('Midday News', 'The latest updates from around the world.', 45, '2025-01-30 12:00:00+00', 'https://audiobyte.s3.amazonaws.com/audio/e2fac1e3-066a-417f-a241-0ec70c2414f5.mp3', FALSE, FALSE, 'MIDDAY');

INSERT INTO episodes
    (title, description, duration, published_at, audio_link, is_bookmark, is_deleted, time_of_day)
VALUES
    ('End of Day Wrap-Up', 'Summary of the days most important events.', 60, '2025-01-30 18:00:00+00', 'https://audiobyte.s3.amazonaws.com/audio/4ac766fb-c4f4-4efa-ad37-9613ab4e6595.mp3', TRUE, FALSE, 'ENDOFDAY');