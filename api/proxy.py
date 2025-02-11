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

# Vercel requires this handler for serverless function
def handler(event, context):
    with app.test_request_context(event['path'], method=event['httpMethod'], data=event['body']):
        response = app.full_dispatch_request()
    return {
        'statusCode': response.status_code,
        'body': response.get_data(as_text=True),
        'headers': dict(response.headers)
    }
