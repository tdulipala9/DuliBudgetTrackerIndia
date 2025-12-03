from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store entries as objects: {name, category, rupees, dollars}
items = []

EXCHANGE_RATE = 90.17  # ₹ → $


@app.route("/", methods=["GET", "POST"])
def index():

    total_rupees = sum(item["rupees"] for item in items)
    total_dollars = sum(item["dollars"] for item in items)

    categories = ["Food", "Travel", "Shopping", "Rent", "Fun", "Misc"]

    return render_template(
        "index.html",
        items=items,
        categories=categories,
        total_rupees=total_rupees,
        total_dollars=total_dollars,
        rate=EXCHANGE_RATE
    )


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    rupees = float(request.form.get("rupees"))
    category = request.form.get("category")

    dollars = round(rupees / EXCHANGE_RATE, 2)

    items.append({
        "name": name,
        "category": category,
        "rupees": rupees,
        "dollars": dollars
    })

    return redirect(url_for("index"))


@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    if 0 <= index < len(items):
        items.pop(index)
    return redirect(url_for("index"))


@app.route("/clear", methods=["POST"])
def clear():
    items.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
