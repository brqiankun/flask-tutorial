import sqlite3

import flask
import click
from flask import current_app, g   
from flask.cli import with_appcontext

# g是一个特殊的对象，独立于每个请求，可以用于存储每个函数都会用到的数据，把连接存储与其中，
# 可以多次使用，而不需要在同一个请求中多次调用get_db时都创建一个新连接
# current_app对象指向处理请求的Flask应用
def get_db():  
    if 'db' not in g:
        g.db = sqlite3.connect(     #建立一个数据库连接，连接指向配置中的DATABASE指定的文件
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row   #告诉连接返回类似于dict的行

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


#用于运行SQL命令的函数
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:    #打开一个文件，文件名相对于flaskr包
        db.executescript(f.read().decode('utf8'))
    
@click.command('init-db')   #定义一个init-db命令行，调用init_db()函数
@with_appcontext
def init_db_command():
    """Clear the existing adta and create new tables."""
    init_db()
    click.echo('initialized the database.')

# 在应用实例中注册
def init_app(app: flask.Flask):
    app.teardown_appcontext(close_db)      #在返回响应后进行清理时调用
    app.cli.add_command(init_db_command)   #添可以于flask一起执行的命令

    