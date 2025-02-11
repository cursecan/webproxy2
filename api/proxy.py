import requests
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/api/proxy', methods=['GET', 'POST'])
def proxy():
    target = request.args.get('target')  # Get the target URL from query parameters
    
    if not target:
        return Response("Target URL is required", status=400)

    # Forward the request to the target URL
    if request.method == 'GET':
        response = requests.get(target, params=request.args)
    else:
        response = requests.post(target, json=request.json)

    # Create a response object
    return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])

if __name__ == '__main__':
    app.run(debug=True)
