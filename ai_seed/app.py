import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import seed

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the raw request body, hand it to the kernel, return JSON
        try:
            length = int(self.headers.get('Content-Length'))
            text = self.rfile.read(length).decode('utf-8')
            result = seed.process_request(text)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def do_GET(self):
        # Serve index.html at the root path
        if self.path == '/':
            self.path = '/index.html'
        try:
            with open(self.path[1:], 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content)
        except:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print("TianDao Seed v0.1 running on http://127.0.0.1:8000 (Ctrl+C to quit)")
    HTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
