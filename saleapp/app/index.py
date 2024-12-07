import math

from flask import render_template,request,jsonify,redirect,flash,session
from config import app, db
import dao
from flask_login import login_user,login_required
from models import User,UserRole
from werkzeug.security import check_password_hash

import utils


@app.route("/")
def index():
    cates = dao.load_categories()
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = request.args.get('page',1)
    total_page = dao.count_products()
    page_size = app.config['PAGE_SIZE']
    prods = dao.load_products(cate_id=cate_id,kw=kw,page=int(page))
    return render_template('index.html', categories=cates, products=prods,pages = math.ceil(total_page/page_size))

@app.route("/login",methods=['get','post'])
def login_process():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username,password)
        if user:
            login_user(user)
            redirect('/')
    return render_template('login.html')
@app.route("/api/products/add", methods=['POST'])
def add_product():
    data = request.get_json()
    if isinstance(data, dict):
        new_product = dao.add_product(data)
        return jsonify(new_product.json()), 201
    else:
        return jsonify({"error": "Invalid input data"}), 400


@app.context_processor
def common_context_params():
    return {
        'categories':dao.load_categories(),
        'cart_stats':utils.count_cart(session.get('cart'))
    }

@app.route('/cart')
def cart():
    return  render_template('cart.html')

@app.route('/api/carts',methods=['post'])
def add_to_cart():
    cart = session.get('cart',{})
    if not cart:
        cart ={}
    id = str(request.json.get('id'))
    name = request.json.get('name')
    price = request.json.get('price')
    if id in cart:
        cart[id]["quantity"]+=1
    else:
        cart[id]={
            "id":id,
            "name":name,
            "price":price,
            "quantity":1
        }
    session['cart'] = cart
    return jsonify(utils.count_cart(cart))
@app.route("/admin_login", methods=['POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.auth_user(username,password,role=UserRole.ADMIN)
        if user:
            login_user(user=user)
        return redirect("/admin")
@app.route("/payment")
@login_required
def pay():
    return "Payment page"
if __name__ == '__main__':
    import admin
    app.run(debug=True)
