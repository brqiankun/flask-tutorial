import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# 蓝图blueprint是一种组织相关试图及代码的方式，把相关试图注册到蓝图，然后在工厂函数中把蓝图注册到应用
bp = Blueprint('auth', __name__, url_prefix='/auth')

# 关联了URL /register 和register函数, 当Flask收到指向/auth/register的请求时就会调用register试图，并将其返回值作为响应
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':              # 如果用户提交了表单则为POST
        username = request.form['username']   # request.form映射了用户提交的键和值
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)  #使用了带有?占位符的SQL查询语句
        ).fetchone() is not None:  # 根据查询返回一个记录行。如果查询无结果，则返回None
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))    #不会把密码明文存储在数据库
            )
            db.commit() #报存修改
            return redirect(url_for('auth.login'))   #根据登录视图的名称生成URL，并跳转到登录页
        
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()    
            session['user_id'] = user['id']
            # session 是一个dict用于存储横跨请求的值。验证成功后，用户id被存储在一个新会话中。会话数据被存储在向浏览器发送的cookie中
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
