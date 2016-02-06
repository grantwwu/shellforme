from flask import Flask, request
import simplejson as json

app = Flask(__name__)

@app.route('/')
# TODO: Render template
def hello_world():
    return 'Hello World!'

@app.route('/compile', methods=['POST'])
def compile():
    ir = request.get_json()
    # Do the thing!
    return json.dumps({result : 'success', output : compiled})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
