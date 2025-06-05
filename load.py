import sqlite3
import json
from lxml import etree

# Parse XML
parser = etree.XMLParser(recover=True)
tree = etree.parse("cpe_dictionary.xml", parser)
root = tree.getroot()

# Namespaces
ns = {
    "cpe": "http://cpe.mitre.org/dictionary/2.0",
    "cpe-23": "http://scap.nist.gov/schema/cpe-extension/2.3"
}

# Connect to DB
conn = sqlite3.connect("cpe_data.db")
cur = conn.cursor()

# Create Table
cur.execute('''
    CREATE TABLE IF NOT EXISTS cpe_entries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpe_title TEXT,
        cpe_22_uri TEXT,
        cpe_23_uri TEXT,
        reference_links TEXT,
        cpe_22_deprecation_date TEXT,
        cpe_23_deprecation_date TEXT
    )
''')
conn.commit()

# Parse Entries
items = root.findall(".//cpe:cpe-item", ns)
print(f"Found {len(items)} cpe-item entries")

for i, item in enumerate(items):
    try:
        # CPE 2.2 URI
        cpe_22_uri = None
        cpe_22_deprecation_date = None

        # Title
        title_elem = item.find("cpe:title", ns)
        cpe_title = title_elem.text if title_elem is not None else None

        # Reference links
        ref_links = []
        refs_elem = item.find("cpe:references", ns)
        if refs_elem is not None:
            for ref in refs_elem.findall("cpe:reference", ns):
                href = ref.attrib.get("href")
                if href:
                    ref_links.append(href)
        reference_links = json.dumps(ref_links)

        # CPE 2.3 URI and deprecation
        cpe23_elem = item.find("cpe-23:cpe23-item", ns)
        if cpe23_elem is not None:
            cpe_23_uri = cpe23_elem.attrib.get("name")

            # Method 1: Direct attribute
            cpe_23_deprecation_date = cpe23_elem.attrib.get("deprecation date")

            # Method 2: Nested <cpe-23:deprecation> child
            if cpe_23_deprecation_date is None:
                deprecation_elem = cpe23_elem.find("cpe-23:deprecation", ns)
                if deprecation_elem is not None:
                    cpe_23_deprecation_date = deprecation_elem.attrib.get("date")
        else:
            cpe_23_uri = None
            cpe_23_deprecation_date = None

        # Insert
        cur.execute('''
            INSERT INTO cpe_entries (
                cpe_title, cpe_22_uri, cpe_23_uri,
                reference_links, cpe_22_deprecation_date, cpe_23_deprecation_date
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            cpe_title, cpe_22_uri, cpe_23_uri,
            reference_links, cpe_22_deprecation_date, cpe_23_deprecation_date
        ))

        if i % 5000 == 0:
            print(f"Inserted {i} entries...")

    except Exception as e:
        print(f"Error on entry {i}: {e}")

conn.commit()
conn.close()
