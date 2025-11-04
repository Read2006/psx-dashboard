from flask import Flask, render_template, request
from database import SessionLocal, StockSnapshot

app = Flask(__name__)

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
    app.run(debug=True)
