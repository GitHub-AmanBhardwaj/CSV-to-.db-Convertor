from flask import Flask, render_template, request, send_file
import pandas as pd
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
DATABASE_FILE = "database.db"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def home():
    table_data = None
    columns = []
    if request.method == "POST":
        file = request.files["file"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        df = pd.read_csv(file_path)
        conn = sqlite3.connect(DATABASE_FILE)
        df.to_sql("my_table", conn, if_exists="replace", index=False)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM my_table")
        table_data = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()

        return render_template("home.html", success=True, table_data=table_data, columns=columns)

    return render_template("home.html", success=False, table_data=table_data, columns=columns)

@app.route("/download")
def download():
    return send_file(DATABASE_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
