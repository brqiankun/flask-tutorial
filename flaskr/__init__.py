import os

from flask import Flask

def create_app(test_config=None):
    #create and configure the app  创建Flask实例，应用配置文件相对于实例文件夹的相对位置
    print(__name__)
    app = Flask(__name__, instance_relative_config=True)
    print(app.instance_path)
    app.config.from_mapping(    #应用的缺省配置
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),   # 位于实例文件夹内 app.instance_path
    )

    if test_config is None:
        #load the instance config, if it exists, when no testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that says hello
    @app.route('/hello')   #创建了URL/hello和函数之间的关联
    def hello():
        return 'hello world'
    
    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app


