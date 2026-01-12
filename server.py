from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import sqlite3
import os
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "contacto.db")

USER = "admin"
PASSWORD = "1234"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            email TEXT,
            mensaje TEXT
        )
    """)
    conn.commit()
    conn.close()

class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.send_html("index.html")

        elif self.path.startswith("/assets/") or self.path.startswith("/images/"):
            self.send_static()

        elif self.path in ["/mensajes", "/mensajes/"]:
            if not self.is_authenticated():
                self.request_auth()
                return
            self.show_messages()

        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/contacto":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length).decode()
            form = parse_qs(data)

            nombre = form.get("nombre", [""])[0]
            email = form.get("email", [""])[0]
            mensaje = form.get("mensaje", [""])[0]

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
                "INSERT INTO mensajes (nombre, email, mensaje) VALUES (?, ?, ?)",
                (nombre, email, mensaje)
            )
            conn.commit()
            conn.close()

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<h2>Mensaje enviado correctamente</h2><a href='/'>Volver</a>"
            )

    # ---------- AUTENTICACIÓN ----------
    def is_authenticated(self):
        auth = self.headers.get("Authorization")
        if not auth or not auth.startswith("Basic "):
            return False

        try:
            decoded = base64.b64decode(auth.split(" ")[1]).decode()
            user, pwd = decoded.split(":", 1)
            return user == USER and pwd == PASSWORD
        except:
            return False

    def request_auth(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Mensajes protegidos"')
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Acceso restringido")

    # ---------- ARCHIVOS ----------
    def send_html(self, filename):
        path = os.path.join(BASE_DIR, filename)
        if not os.path.isfile(path):
            self.send_error(404)
            return

        with open(path, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content)

    def send_static(self):
        path = self.path.lstrip("/")
        full_path = os.path.join(BASE_DIR, path)

        if not os.path.isfile(full_path):
            self.send_error(404)
            return

        self.send_response(200)
        self.end_headers()
        with open(full_path, "rb") as f:
            self.wfile.write(f.read())

    # ---------- MENSAJES ----------
    def show_messages(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT nombre, email, mensaje FROM mensajes")
        rows = c.fetchall()
        conn.close()

        html = "<h1>Mensajes recibidos</h1><ul>"
        for nombre, email, mensaje in rows:
            html += f"<li><b>{nombre}</b> ({email}): {mensaje}</li>"
        html += "</ul><a href='/'>Volver</a>"

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    init_db()
    print("Servidor corriendo en http://localhost:8000")
    HTTPServer(("localhost", 8000), Server).serve_forever()
