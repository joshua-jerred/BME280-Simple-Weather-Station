#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, parse_qsl

PORT = 8080
ADDRESS = "localhost"
CORS_POLICY = "localhost:8080"


class RequestHandler(BaseHTTPRequestHandler):
    def responseNotFound(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes('Not found', "utf-8"))

    def responseMalformed(self, message: str = "Malformed request"):
        self.send_response(400)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))
