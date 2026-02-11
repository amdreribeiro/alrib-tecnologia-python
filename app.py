from flask import Flask, Response
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "site.html"   # vai ser o teu HTML do portal

@app.route("/")
def home():
    if not HTML_FILE.exists():
        return Response(
            "<h1>Arquivo site.html não encontrado</h1><p>Coloque o HTML na raiz do repo com o nome <b>site.html</b>.</p>",
            mimetype="text/html; charset=utf-8",
            status=404,
        )

    html = HTML_FILE.read_text(encoding="utf-8", errors="replace")
    return Response(html, mimetype="text/html; charset=utf-8")

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
