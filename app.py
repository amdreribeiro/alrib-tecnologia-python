from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello from Simple Python App! 🚀</h1><p>This app is deployed via GitHub Actions + Docker.</p>"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)