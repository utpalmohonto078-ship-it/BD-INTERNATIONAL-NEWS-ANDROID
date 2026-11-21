ফাংশন সংবাদ_তৈরি(db, title, body, category, author, image_url, video_url)
যদি title == ""
ফেরত 0
শেষ
যদি body == ""
ফেরত 0
শেষ
যদি category == ""
ফেরত 0
শেষ
ডেটাবেস_চালাও(db, "INSERT INTO articles (title, body, category, author, status, image_url, video_url) VALUES (?, ?, ?, ?, 'draft', ?, ?)", [title, body, category, author, image_url, video_url])
ফেরত 1
শেষ

ফাংশন সংবাদ_দেখাও(db, article_id)
ফেরত ডেটাবেস_জিজ্ঞাসা(db, "SELECT * FROM articles WHERE id = ?", [article_id])
শেষ

ফাংশন সংবাদ_তালিকা(db, limit, offset)
ফেরত ডেটাবেস_জিজ্ঞাসা(db, "SELECT * FROM articles ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?", [limit, offset])
শেষ

ফাংশন সংবাদ_সম্পাদনা(db, article_id, title, body, category, author, image_url, video_url)
যদি title == ""
ফেরত 0
শেষ
যদি body == ""
ফেরত 0
শেষ
ডেটাবেস_চালাও(db, "UPDATE articles SET title = ?, body = ?, category = ?, author = ?, image_url = ?, video_url = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", [title, body, category, author, image_url, video_url, article_id])
ফেরত 1
শেষ

ফাংশন সংবাদ_অবস্থা_পরিবর্তন(db, article_id, new_status)
যদি new_status == "draft"
ডেটাবেস_চালাও(db, "UPDATE articles SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", [new_status, article_id])
ফেরত 1
শেষ
যদি new_status == "published"
ডেটাবেস_চালাও(db, "UPDATE articles SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", [new_status, article_id])
ফেরত 1
শেষ
যদি new_status == "archived"
ফেরত সংবাদ_আর্কাইভ(db, article_id)
শেষ
ফেরত 0
শেষ

ফাংশন সংবাদ_প্রকাশ(db, article_id)
ফেরত সংবাদ_অবস্থা_পরিবর্তন(db, article_id, "published")
শেষ

ফাংশন সংবাদ_আর্কাইভ(db, article_id)
let existing = ডেটাবেস_জিজ্ঞাসা(db, "SELECT id FROM article_archive WHERE article_id = ?", [article_id])
যদি দৈর্ঘ্য(existing) == 0
ডেটাবেস_চালাও(db, "INSERT INTO article_archive (article_id) VALUES (?)", [article_id])
শেষ
ডেটাবেস_চালাও(db, "UPDATE articles SET status = 'archived', updated_at = CURRENT_TIMESTAMP WHERE id = ?", [article_id])
ফেরত 1
শেষ

ফাংশন সংবাদ_অনুসন্ধান(db, keyword)
let pattern = "%" + keyword + "%"
ফেরত ডেটাবেস_জিজ্ঞাসা(db, "SELECT * FROM articles WHERE title LIKE ? OR body LIKE ? OR category LIKE ? ORDER BY created_at DESC LIMIT 100", [pattern, pattern, pattern])
শেষ

ফাংশন বিভাগ_যোগ(db, category_name)
যদি category_name == ""
ফেরত 0
শেষ
ডেটাবেস_চালাও(db, "INSERT OR IGNORE INTO categories (name) VALUES (?)", [category_name])
ফেরত 1
শেষ

ফাংশন বিভাগ_তালিকা(db)
ফেরত ডেটাবেস_জিজ্ঞাসা(db, "SELECT * FROM categories ORDER BY name", [])
শেষ

ফাংশন আর্কাইভ_তালিকা(db)
ফেরত ডেটাবেস_জিজ্ঞাসা(db, "SELECT articles.*, article_archive.archived_at FROM articles INNER JOIN article_archive ON articles.id = article_archive.article_id ORDER BY article_archive.archived_at DESC LIMIT 100", [])
শেষ

দেখাও "NEWS CORE COMMIT TEST START"

let db = ডেটাবেস_খোলো("local-data/news_core_test.db")

দেখাও "TEST CATEGORY"
দেখাও বিভাগ_যোগ(db, "পরীক্ষামূলক সংবাদ")

দেখাও "TEST ARTICLE CREATE"
দেখাও সংবাদ_তৈরি(db, "BBH Test Article", "News Core test body", "পরীক্ষামূলক সংবাদ", "BBH Test", "", "")

দেখাও "TEST ARTICLE SEARCH"
let found = সংবাদ_অনুসন্ধান(db, "BBH Test Article")
দেখাও দৈর্ঘ্য(found)

দেখাও "TEST ARTICLE READ"
let article = সংবাদ_দেখাও(db, 1)
দেখাও দৈর্ঘ্য(article)

দেখাও "TEST ARTICLE UPDATE"
দেখাও সংবাদ_সম্পাদনা(db, 1, "BBH Test Article Updated", "Updated test body", "পরীক্ষামূলক সংবাদ", "BBH Test", "", "")

দেখাও "TEST PUBLISH"
দেখাও সংবাদ_প্রকাশ(db, 1)

দেখাও "TEST ARCHIVE"
দেখাও সংবাদ_আর্কাইভ(db, 1)

দেখাও "TEST ARCHIVE LIST"
let archived = আর্কাইভ_তালিকা(db)
দেখাও দৈর্ঘ্য(archived)

দেখাও "TEST ARTICLE LIST"
let articles = সংবাদ_তালিকা(db, 20, 0)
দেখাও দৈর্ঘ্য(articles)

দেখাও "TEST EMPTY ARTICLE"
দেখাও সংবাদ_তৈরি(db, "", "body", "category", "author", "", "")

দেখাও "COMMIT DATABASE"
ডেটাবেস_কমিট(db)

ডেটাবেস_বন্ধ(db)

দেখাও "NEWS CORE COMMIT TEST FINISHED"
