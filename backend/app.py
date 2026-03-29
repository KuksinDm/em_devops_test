import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path != "/":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from Effective Mobile!")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", int(os.getenv("PORT"))), MyHandler)
    print(f"Server started on port {os.getenv('PORT')}")
    server.serve_forever()
