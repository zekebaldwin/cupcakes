from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route("/")
def root():
    return render_template("index.html")

@app.route('/api/cupcakes')
def info():
    cupcakes_info = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes_info)

@app.route("/api/cupcakes", methods=["POST"])
def create():
    cupcake = Cupcake(
        flavor = request.json["flavor"],
        rating = request.json["rating"],
        size = request.json["size"],
        image = request.json["image"]
    )
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route("/api/cupcakes/<int:id>")
def cupcake_info(id):
    specific_cake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=specific_cake.to_dict())

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update(id):
    specific_cake = Cupcake.query.get_or_404(id)
    db.session.query(specific_cake).filter_by(id=id).update(request.json)
    db.session.commit()
    return jsonify(cake=specific_cake.to_dict())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="delted")



