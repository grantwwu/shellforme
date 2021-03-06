from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/favicon.png')
def favicon():
    return app.send_static_file('favicon.png')

@app.route('/resize.css')
def resize():
    return app.send_static_file('resize.css')

@app.route('/main.js')
def js():
    return app.send_static_file('main.js')

@app.route('/compile', methods=['POST'])
def compile():
    ir = request.get_json()
    try:
        ret = compile(json.loads(p))
    except compiler.Error as exception:
        ret = exception.as_dict()

    return json.dumps(ret)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
