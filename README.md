# CPE Viewer & API

A Flask-based web application and RESTful API that parses [CPE Dictionary XML]([https://nvd.nist.gov/products/cpe](https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz)) data, stores it in a SQLite database, and exposes both HTML and JSON views with pagination.

---

## 📁 Project Structure

```bash
.
├── app.py              # Flask app with HTML and JSON endpoints
├── load.py             # Script to parse and load XML data into SQLite
├── cpe_dictionary.xml  # (download this this) MITRE CPE Dictionary XML
├── cpe_data.db         # SQLite DB file (generated)
├── templates/
│   └── index.html      # HTML page to view paginated entries
└── README.md           # You're looking at it!
```

#Setup Instructions

##1. Clone the Repo
```
git clone https://github.com/your-username/cpe-dictionary-viewer.git
cd cpe-dictionary-viewer
```
## 2. Install Dependencies
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install flask lxml sqlite3 json math
```
## 3. Add XML File
Download Link : https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz
```
cpe_dictionary.xml (rename)
```

## 4. Load Data into SQLite
```
python load.py
```
```
Found 134567 cpe-item entries
Inserted 0 entries...
Inserted 5000 entries...
...
```
## 5. Run the Web App
```
python app.py
```
## 🌐 API Endpoints

### 📄 HTML View

**GET** `/api/cpes?page=1&limit=10`

- Renders a paginated HTML table of entries.

---

### 📦 JSON API

**GET** `/api/cpes/json?page=1&limit=10`

Returns:

```json
{
  "page": 1,
  "limit": 10,
  "total": 134567,
  "data": [
    {
      "id": 1,
      "cpe_title": "Example Software",
      "cpe_22_uri": "cpe:/a:vendor:product:version",
      "cpe_23_uri": "cpe:2.3:a:vendor:product:version:*:*:*:*:*:*:*:*",
      "reference_links": ["https://example.com"],
      "cpe_22_deprecation_date": null,
      "cpe_23_deprecation_date": "2023-05-16T20:06:08.790Z"
    }
  ]
}
```
## 🗃️ Database Schema  
The `load.py` script will automatically create the following schema:

```sql
CREATE TABLE IF NOT EXISTS cpe_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpe_title TEXT,
    cpe_22_uri TEXT,
    cpe_23_uri TEXT,
    reference_links TEXT,
    cpe_22_deprecation_date TEXT,
    cpe_23_deprecation_date TEXT
);

```
# output

![image](https://github.com/user-attachments/assets/ce4fa732-c9f2-4b8f-9558-5e85a2222ce6)

![image](https://github.com/user-attachments/assets/cd5a06db-3bd6-4c7a-8a2f-1912a299722c)


# Author
**Vijis Durai R** – BTech IT Student @ Saveetha Engineering College
