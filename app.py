import os
from flask import Flask, render_template, request
from database import SessionLocal, StockSnapshot

app = Flask(__name__, template_folder="__bycache__templates")


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").upper()  # search term
    db = SessionLocal()

    if query:
        data = db.query(StockSnapshot).filter(StockSnapshot.symbol.like(f"%{query}%")).all()
    else:
        data = db.query(StockSnapshot).all()

    db.close()
    return render_template("index.html", data=data, query=query)


if __name__ == "__main__":
    # Use Render's PORT or default to 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
