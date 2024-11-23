from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

BACKEND_API_URL = os.environ.get('BACKEND_API_URL', 'http://localhost:5000/api/data')

@app.route('/')
def index():
    try:
        response = requests.get(BACKEND_API_URL)
        data = response.json()
    except Exception as e:
        data = []
    return render_template('index.html', items=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
