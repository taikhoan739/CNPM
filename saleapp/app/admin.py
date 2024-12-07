from flask_admin.contrib.sqla import ModelView
from flask import redirect
from flask_admin import Admin,expose ,BaseView
from flask_login import current_user
from config import app,db

from models import Category, Product
admin = Admin(app, name="Quan ly ban hang",
template_mode="bootstrap4")

class AuthenticatedView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated
class CategoryModelView(AuthenticatedView):
    column_display_pk = False
    can_create = False
    can_edit = True
    can_export = True
    can_delete = False
    column_list=['id','name','products']

class ProductModelView(AuthenticatedView):
    column_display_pk = False
    column_list=['id','name','price','image','category_id']
class AboutUsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/about-us.html')
from flask_login import logout_user

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose('/')
    def __index__(self):
        return self.render('admin/stats.html')
    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(ProductModelView(Product, db.session))
admin.add_view(AboutUsView(name="Giới thiệu"))
admin.add_view(LogoutView(name="Đăng Xuất"))
admin.add_view(StatsView(name="Thống Kê"))