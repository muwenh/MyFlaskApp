import os
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__, template_folder=".")
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.db"
app.secret_key = "supersecret"
db = SQLAlchemy(app)


migrate = Migrate(app, db)


class orders(db.Model):
    orderId = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.String(30), unique=False, nullable=False)
    customerId = db.Column(db.Integer, unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    priceEach = db.Column(db.Float, unique=False, nullable=False)
    orderDate = db.Column(db.String(30), unique=False, nullable=False)
    orderStatus = db.Column(db.String(25), unique=False, nullable=False)

    def __repr__(self):
        return f"Order Id : {self.orderId}, Customer Id : {self.customerId}, Order Date : {self.orderDate}"

    def __init__(
        self,
        orderId,
        productId,
        customerId,
        quantity,
        priceEach,
        orderDate,
        orderStatus,
    ):
        self.orderId = orderId
        self.productId = productId
        self.customerId = customerId
        self.quantity = quantity
        self.priceEach = priceEach
        self.orderDate = orderDate
        self.orderStatus = orderStatus


@app.route("/")
def display():
    return render_template("display.html", orders=orders.query.all())


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        if (
            not request.form["orderId"]
            or not request.form["productId"]
            or not request.form["customerId"]
            or not request.form["quantity"]
            or not request.form["priceEach"]
            or not request.form["orderDate"]
            or not request.form["orderStatus"]
        ):
            flash("Please enter all the fields", "error")
        else:
            order = orders(
                request.form["orderId"],
                request.form["productId"],
                request.form["customerId"],
                request.form["quantity"],
                request.form["priceEach"],
                request.form["orderDate"],
                request.form["orderStatus"],
            )

            db.session.add(order)
            db.session.commit()

            flash("Record was successfully added")
            return redirect(url_for("display"))
    return render_template("new.html")


if __name__ == "__main__":
    app.run()
