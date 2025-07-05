from flask import Flask, request, Response,render_template
import requests

app = Flask(__name__, static_folder='static', template_folder='static')

# Default ProPresenter API base URL
PROPRESENTER_IP = "0.0.0.0"
PROPRESENTER_PORT = 1025

FLASK_PORT = 80

def get_propresenter_base():
    return f'http://{PROPRESENTER_IP}:{PROPRESENTER_PORT}'

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/v1/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(path):
    # Build proxied URL
    propresenter_url = f"{get_propresenter_base()}/v1/{path}"
    req_args = {
        "params": request.args,
        "headers": {k: v for k, v in request.headers if k.lower() != "host"},
        "data": request.get_data(),
        "cookies": request.cookies,
        "allow_redirects": False
    }
    # Send appropriate HTTP method
    try:
        resp = requests.request(request.method, propresenter_url, **req_args)
    except requests.RequestException as e:
        return Response(str(e), status=502)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

@app.route('/api/update-propresenter', methods=['POST'])
def update_propresenter():
    global PROPRESENTER_IP, PROPRESENTER_PORT
    data = request.get_json()
    if not data or 'ip' not in data or 'port' not in data:
        return {"error": "IP and Port required"}, 400
    PROPRESENTER_IP = data['ip']
    PROPRESENTER_PORT = str(data['port'])
    if len(PROPRESENTER_PORT) not in [4,5]:
        PROPRESENTER_PORT = 1025
    return {"message": "Updated successfully"}

@app.route('/api/get-propresenter', methods=['GET'])
def get_propresenter():
    global PROPRESENTER_IP, PROPRESENTER_PORT
    return {"ip": PROPRESENTER_IP,"port":PROPRESENTER_PORT}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=FLASK_PORT,debug=False)
