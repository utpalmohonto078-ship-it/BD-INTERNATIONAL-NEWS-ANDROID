let db = ডেটাবেস_খোলো("local-data/news.db")

ডেটাবেস_চালাও(db, "CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, body TEXT NOT NULL, category TEXT NOT NULL, author TEXT NOT NULL DEFAULT '', status TEXT NOT NULL DEFAULT 'draft', image_url TEXT NOT NULL DEFAULT '', video_url TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)", [])

ডেটাবেস_চালাও(db, "CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)", [])

ডেটাবেস_চালাও(db, "CREATE TABLE IF NOT EXISTS article_archive (id INTEGER PRIMARY KEY AUTOINCREMENT, article_id INTEGER NOT NULL, archived_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)", [])

ডেটাবেস_কমিট(db)

let rows = ডেটাবেস_জিজ্ঞাসা(db, "SELECT name FROM sqlite_master WHERE type = ? AND name IN (?, ?, ?) ORDER BY name", ["table", "articles", "categories", "article_archive"])

দেখাও দৈর্ঘ্য(rows)

ডেটাবেস_বন্ধ(db)
