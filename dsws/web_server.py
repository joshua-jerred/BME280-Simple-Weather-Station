#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from .config import ReadConfig
from .db import DB

WEB_SRC = "web_interface/"
ALLOWED_FILES = ["/", "/style.css", "/script.js", "/w3.css"]
API_PATHS = ["/api/temperature", "/api/humidity", "/api/pressure"]


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

    def handleGetFile(self):
        self.send_response(200)
        file = WEB_SRC
        if self.path == "/":
            self.send_header('Content-type', 'text/html')
            file += "index.html"
        elif self.path == "/style.css":
            self.send_header('Content-type', 'text/css')
            file += "style.css"
        elif self.path == "/w3.css":
            self.send_header('Content-type', 'text/css')
            file += "w3.css"
        elif self.path == "/script.js":
            self.send_header('Content-type', 'text/javascript')
            file += "script.js"
        self.end_headers()
        with open(file, "r") as f:
            self.wfile.write(bytes(f.read(), "utf-8"))

    def handleGetAPI(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        db = DB(ReadConfig("config.json"))
        json_data = ""
        if self.path == "/api/temperature":
            json_data = db.getMostRecent("air_temperature")
        elif self.path == "/api/humidity":
            json_data = db.getMostRecent("relative_humidity")
        elif self.path == "/api/pressure":
            json_data = db.getMostRecent("atmospheric_pressure")
        self.wfile.write(bytes(json.dumps(json_data), "utf-8"))

    def do_GET(self):
        if self.path in ALLOWED_FILES:
            self.handleGetFile()
            return
        elif self.path in API_PATHS:
            self.handleGetAPI()
            return
        else:
            self.responseNotFound()


def StartServer(config_location):
    config = ReadConfig(config_location)
    address = config["web_server"]["address"]
    port = config["web_server"]["port"]
    print(f'Starting web server at {address}, with port {port}')
    HTTPServer((address, port), RequestHandler).serve_forever()
    #db = DB(config)
    # print(db.countEntries('air_temperature'))
    # print(db.getMostRecent('air_temperature'))
