from BaseHTTPServer import (HTTPServer, BaseHTTPRequestHandler)
import contextlib

import daemon

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Just received a GET request")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write('Hello world')
        return

server = HTTPServer(('127.0.0.1', 8000), MyHandler)
#
daemon_context = daemon.DaemonContext()
daemon_context.files_preserve = [server.fileno()]

# Become a daemon process.
with daemon_context:
    server.serve_forever()

