# URL Shortener API (Python Flask)

This is a simple URL Shortener service built with Python and Flask. It lets you create short codes for long URLs, and then redirect, update, delete, or get info about them.

---

## 🛠️ Features

- Shorten long URLs
- Redirect using short code
- View short URL info
- Update the long URL
- Delete the short URL

---

## 📦 Tech Used

- Python
- Flask
- SQLite
- SQLAlchemy

---

## 🚀 How to Run This Project

### Step 1: Clone or Download

Download this project or copy the files to your computer.

### Step 2: Open Folder in VS Code

Navigate to this folder in VS Code.

### Step 3: Create and Activate Virtual Environment


python -m venv venv
venv\Scripts\activate  # On Windows

### Step 4: Install Flask

pip install Flask


### Step 5: Run the App

```
python app.py
```

- You’ll see the message: `Database is set up and running!`
- The server will be live at: `http://127.0.0.1:5000`

---

## 📬 API Endpoints

### 🔹 POST `/shorten`

Create a short URL.

- **Method:** POST  
- **URL:** `/shorten`  
- **Body (JSON):**
  ```json
  {
    "original_url": "https://example.com"
  }
  ```

---

### 🔹 GET `/<short_code>`

Redirect to the original URL.

- **Method:** GET  
- **Example:** `/abc123`  
- **Result:** Redirects to `https://example.com`

---

### 🔹 GET `/info/<short_code>`

View information about a short code.

- **Method:** GET  
- **Example:** `/info/abc123`  
- **Response:**
  ```json
  {
    "original_url": "https://example.com",
    "short_code": "abc123",
    "access_count": 1,
    "created_at": "2025-05-04 11:37:29",
    "updated_at": "2025-05-04 11:42:22"
  }
  ```

---

### 🔹 PUT `/update/<short_code>`

Update the long URL for a short code.

- **Method:** PUT  
- **URL:** `/update/abc123`  
- **Body (JSON):**
  ```json
  {
    "original_url": "https://new-url.com"
  }
  ```

---

### 🔹 DELETE `/delete/<short_code>`

Delete a short code.

- **Method:** DELETE  
- **URL:** `/delete/abc123`

---

## 📂 Database

- SQLite database is saved in `instance/urls.db`

### Columns:

- `id`: Unique ID
- `original_url`: Full destination URL
- `short_code`: Unique short identifier
- `created_at`: Time it was created
- `updated_at`: Last update time
- `access_count`: Number of times visited

---

## ✅ Status

Project completed and working successfully.
