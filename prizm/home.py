from flask import Blueprint,redirect,render_template,url_for,request

bp = Blueprint('home',__name__,url_prefix='/')


@bp.route('/')
def home():
    return render_template("home.html")
