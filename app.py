from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/favicon.png')
def index():
    return app.send_static_file('favicon.png')

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
