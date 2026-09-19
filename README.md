# 📱 Social Media Content Planner

A simple terminal (console) based social media content planner. It offers features like adding posts, updating statuses, recording engagement metrics, viewing a content calendar, and generating performance reports. All data is stored in plain text (`.txt`) files — no database required.

---

## ✨ Features

- **Post Management**
  - Add posts (ID, platform, caption, date)
  - Update post status (`Draft → Scheduled → Posted`)
  - Display posts
  - Delete posts
- **Platform Management**
  - Auto-assign IDs when adding new platforms (`PL1`, `PL2`, ...)
  - Canonical name check to prevent the same platform being stored with different capitalisation
- **Engagement Metrics**
  - Record likes, comments, shares, and views only for posts with `Posted` status
- **Content Calendar**
  - Displays posts sorted by date (bubble sort)
  - Skips posts with invalid dates
- **Performance Report**
  - Total post count per platform
  - Best performing post (Total Engagement = likes + comments + shares)
  - Most interactive platform
- **Export Report**
  - Writes the report to `report.txt`

---

## 🗂️ File Structure

The program automatically creates the following files in its own directory:

| File | Description | Format |
|------|-------------|--------|
| `posts.txt` | Post records | `id\|platform\|caption\|date\|status` |
| `platforms.txt` | Platform records | `id\|name\|followers` |
| `engagement.txt` | Engagement metrics | `post_id,likes,comments,shares,views` |
| `report.txt` | Exported performance report | Free text |

> ⚠️ `|` is the field delimiter in `posts.txt`. The `|` character is not allowed in Post ID, platform, or caption fields (the program blocks it).

---

## 🚀 Installation and Running

No external libraries are required. Python 3 is enough.

```bash
python from_datetime_import_datetime.py
```

The main menu opens when the program starts.

---

## 🖥️ Usage

Main menu:

```
=====================================
SOCIAL MEDIA CONTENT PLANNER
=====================================
1. Post Management (Add/Update/Display/Delete Posts)
2. Record Engagement Metrics
3. Display Content Calendar
4. Generate Performance Report
5. Export Report to File
6. Exit
```

### 1. Post Management
Through the submenu, you can add, update, display, or delete posts.

- **When adding a post:** If a new platform is entered, the program asks for its follower count and registers it automatically.
- **Status update:** Only forward transitions are allowed:
  - `Draft → Scheduled`
  - `Scheduled → Posted`
  - Once a post is `Posted`, its status can no longer be changed.

### 2. Record Engagement
Metrics can only be entered for posts with `Posted` status. All values must be numbers.

### 3. Content Calendar
Posts are listed in date order. Captions longer than 30 characters are truncated.

### 4. Performance Report
Printed to the screen:
- Post count per platform
- Best performing post
- Most interactive platform

### 5. Export Report to File
Writes the same report to `report.txt`.

---

## 🧮 Calculations

- **Total Engagement** = `likes + comments + shares` (views excluded)
- **Best Post:** The post with the highest Total Engagement
- **Most Interactive Platform:** The platform with the highest total Total Engagement

---

## ✅ Validations and Error Handling

- Empty ID / platform / caption / date is not accepted
- Post ID must be unique
- Date must be in `YYYY-MM-DD` format
- The `|` character is not allowed in fields
- Engagement values must be positive integers
- Follower count must be numeric

---

## 🐛 Known Fixes / Design Notes

Some important fixes marked with comments in the code:

- **Canonical platform name:** The `register_platform()` function returns the original spelling of an already-registered platform. This prevents different spellings like `"Instagram"` and `"instagram"` from fragmenting the report.
- **`|` character check:** The delimiter character is blocked from entering fields; otherwise the record would silently disappear.
- **Platform registration timing:** The platform is saved only after all validations pass, so a failed post creation does not leave an orphan platform record in `platforms.txt`.
- **Status transition:** Only forward transitions are allowed.

---

## 📌 Notes

- The program is fully synchronous and single-user; it is not designed for concurrent access.
- Data is stored in plain text files; manual editing is possible, but if the format is broken, the affected line will not load.
- A simple bubble sort is used for sorting (suitable for small datasets).

---

## 📄 License

This project is for educational/learning purposes. You are free to use, modify, and distribute it as you wish.
