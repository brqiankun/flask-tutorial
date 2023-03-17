from flask import Flask
print(__name__)
app = Flask(__name__)   #一个flask应用是一个Flask实例，所有配置和这个实例一起注册

@app.route('/')
def hello_world():
    return "hello"