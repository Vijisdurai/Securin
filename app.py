from flask import Flask, request, render_template, jsonify
import sqlite3
import math
import json

app = Flask(__name__)

def get_cpes(page=1, limit=10):
    offset = (page - 1) * limit
    conn = sqlite3.connect("cpe_data.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM cpe_entries")
    total_count = cur.fetchone()[0]

    cur.execute("""
        SELECT id, cpe_title, cpe_22_uri, cpe_23_uri, reference_links,
            cpe_22_deprecation_date, cpe_23_deprecation_date
        FROM cpe_entries
        ORDER BY id 
        LIMIT ? OFFSET ?
    """, (limit, offset))
    rows = cur.fetchall()
    conn.close()

    parsed_rows = []
    for row in rows:
        row = list(row)
        try:
            row[4] = json.loads(row[4]) if row[4] else []
        except:
            row[4] = []
        parsed_rows.append(row)

    total_pages = math.ceil(total_count / limit) if limit else 1
    return parsed_rows, total_pages, total_count

@app.route("/api/cpes")
def paginated_html():
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    try:
        limit = int(request.args.get("limit", 10))
    except ValueError:
        limit = 10

    if page < 1:
        page = 1
    if limit <= 0:
        limit = 10

    cpe_entries, total_pages, total_count = get_cpes(page, limit)

    return render_template("index.html",
                        cpe_entries=cpe_entries,
                        page=page,
                        total_pages=total_pages,
                        limit=limit,
                        total_count=total_count)


@app.route("/api/cpes/json")
def paginated_json():
    try:
        page = int(request.args.get("page",130000))
        limit = int(request.args.get("limit", 10))
    except:
        return jsonify({"error": "Invalid parameters"}), 400

    cpe_entries, total_pages, total_count = get_cpes(page, limit)

    data = [
        {
            "id": r[0],
            "cpe_title": r[1],
            "cpe_22_uri": r[2],
            "cpe_23_uri": r[3],
            "reference_links": r[4],
            "cpe_22_deprecation_date": r[5],
            "cpe_23_deprecation_date": r[6]
        } for r in cpe_entries
    ]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total_count,
        "data": data
    })
    

if __name__ == '__main__':
    app.run(debug=True,port=5001)
