from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>André Ribeiro 🚀</h1><p> ALRIB TECNOLOGIA.</p>"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
