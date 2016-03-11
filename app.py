from flask import Flask, json, Response
import os

app = Flask(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return "ssh, i'm a secret!"

@app.route('/totals')
def totals():
    with open(os.path.join(base_path, 'totals.json')) as f:
        return Response(f.read(), mimetype='application/json')

@app.route('/state/<state>')
def state_results(state):
    with open(os.path.join(base_path, 'output.json')) as f:
        res = json.load(f)
        return Response(json.dumps(res.get(state, {})), mimetype='application/json')

@app.route('/party/<party>')
def party_results(party):
    with open(os.path.join(base_path, 'output.json')) as f:
        res = json.load(f)
        part = {}
        for state, r in res.iteritems():
            if r.get(party):
                part[state] = r.get(party)
        return Response(json.dumps(part), mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
