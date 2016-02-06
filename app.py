from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/compile', methods=['POST'])
def compile():
    ir = request.get_json()
    # Do the thing!
    return json.dumps({result : 'success', output : compiled})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
