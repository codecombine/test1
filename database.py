import aiosqlite

from config import settings

DATABASE_PATH = settings.DATABASE_URL


async def get_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                location_city TEXT NOT NULL,
                location_district TEXT,
                address TEXT,
                latitude REAL,
                longitude REAL,
                min_age INTEGER DEFAULT 0,
                max_age INTEGER DEFAULT 18,
                is_indoor INTEGER DEFAULT 1,
                is_free INTEGER DEFAULT 0,
                price_range TEXT,
                website_url TEXT,
                phone TEXT,
                tags TEXT,
                season TEXT DEFAULT 'all',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_location TEXT,
                child_ages TEXT,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            );

            CREATE INDEX IF NOT EXISTS idx_activities_location
                ON activities(location_city, location_district);
            CREATE INDEX IF NOT EXISTS idx_activities_age
                ON activities(min_age, max_age);
            CREATE INDEX IF NOT EXISTS idx_activities_category
                ON activities(category);
            CREATE INDEX IF NOT EXISTS idx_messages_session
                ON messages(session_id, created_at);
        """)
        await db.commit()
