import json
from models import Category, Product,User
from config import login,db,app


def load_categories():
    return Category.query.order_by("id").all()
def load_products(cate_id=None,kw=None,page=1):
    query = Product.query
    if cate_id:
        query = Product.query.filter_by(category_id=cate_id)
    if kw:
        query = query.filter(Product.name.contains(kw))

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)
    return query.all()

def count_products():
    return Product.query.count()
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
def add_product(data):
    name = data.get("name")
    price = data.get("price")
    category_id = data.get("category_id")

    new_product = Product(
        name=name,
        price=price,
        category_id=category_id
    )
    print(new_product)
    db.session.add(new_product)
    db.session.commit()
    return new_product
