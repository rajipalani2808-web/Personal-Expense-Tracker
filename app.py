import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("web_expenses.db")


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                kind TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "Other").strip()
        kind = request.form.get("kind", "Expense")
        date = request.form.get("date", "")
        amount_text = request.form.get("amount", "")

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return "Please enter a valid amount greater than zero.", 400

        if not title or not date or kind not in ("Income", "Expense"):
            return "Please fill in all fields correctly.", 400

        with get_db() as connection:
            connection.execute(
                """INSERT INTO transactions
                   (title, amount, kind, category, date)
                   VALUES (?, ?, ?, ?, ?)""",
                (title, amount, kind, category, date)
            )

        return redirect(url_for("index"))

    with get_db() as connection:
        transactions = connection.execute(
            "SELECT * FROM transactions ORDER BY date DESC, id DESC"
        ).fetchall()

    income = sum(t["amount"] for t in transactions if t["kind"] == "Income")
    expenses = sum(t["amount"] for t in transactions if t["kind"] == "Expense")

    return render_template(
        "index.html",
        transactions=transactions,
        income=income,
        expenses=expenses,
        balance=income - expenses
    )
setup_database()

if __name__ == "__main__":
    port=int(os.environ.get(PORT,5000))
    app.run(host='0.0.0.0',port=port)









setup_database()

if __name__ == "__main__":
    app.run(debug=True)
