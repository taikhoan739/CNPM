from flask import render_template,request,jsonify,redirect,flash
from config import app, db
import dao
from flask_login import login_user,login_required
from models import User
from werkzeug.security import check_password_hash
import admin


@app.route("/")
def index():
    cates = dao.load_categories()
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    prods = dao.load_products(cate_id=cate_id,kw=kw)
    return render_template('index.html', categories=cates, products=prods)
@app.route("/api/products/add", methods=['POST'])
def add_product():
    data = request.get_json()
    if isinstance(data, dict):
        new_product = dao.add_product(data)
        return jsonify(new_product.json()), 201
    else:
        return jsonify({"error": "Invalid input data"}), 400
@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(username == username).first()
        if user and user.is_admin and check_password_hash(user.password, password):
            login_user(user=user)
            return redirect("/admin")
        else:
            flash("Invalid credentials or not an admin", "error")
            return redirect("/login-admin")
@app.route("/payment")
@login_required
def pay():
    return "Payment page"
if __name__ == '__main__':
    app.run(debug=True)
