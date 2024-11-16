from config import db, app
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,
    autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)  # Increase length to 512
    is_admin = db.Column(db.Boolean, default=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    products = relationship('Product', backref='category', lazy=True)
    def __str__(self):
        return self.name

class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    image = Column(String(100), nullable=True)
    price = Column(Float, default=0, nullable=True)
    active = Column(Boolean, default=1, nullable=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "price": self.price,
            "active": self.active,
            "category_id": self.category_id
        }
def create_admin_user():
    with app.app_context():
        username = "user"
        password = "user"
        name = "user"  # Add a name for the admin user
        if not User.query.filter_by(username=username).first():
            admin_user = User(username=username, name=name)  # Include the name field
            admin_user.set_password(password)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
if __name__ == '__main__':
    create_admin_user()
    # with app.app_context():
    #     db.create_all()  # This will create the tables in the database
        # Uncomment the following lines to add initial data
        # c1 = Category(name='Mobile')
        # c2 = Category(name='Tablet')
        # c3 = Category(name='Laptop')
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        # products = [{'name': 'Iphone 15', 'description': 'New Iphone 15', 'image': 'iphone15.jpg', 'price': 10000, 'category_id': 1},
        #             {'name': 'Samsung Galaxy S21', 'description': 'New Samsung Galaxy S21', 'image': 's21.jpg', 'price': 900, 'category_id': 2}]
        # for p in products:
        #     prod = Product(**p)
        #     db.session.add(prod)
        # db.session.commit()