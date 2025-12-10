import http.server
import socketserver
import json
import os
from columnar_cipher import ColumnarTranspositionCipher

PORT = 8000

class CipherRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    HANDLING FILES (GET Requests):
    When you go to 'http://localhost:8000', the browser sends a GET request.
    We need to tell Python to look inside the 'templates' folder for index.html.
    """
    def do_GET(self):
        if self.path == '/':
            # If the user asks for the root homepage...
            try:
                # Open the file inside the templates folder
                with open('templates/index.html', 'rb') as f:
                    content = f.read()
                
                # Send standard HTTP headers
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                # Send the HTML content
                self.wfile.write(content)
                return
            except FileNotFoundError:
                self.send_error(404, "index.html not found in templates folder")
                return
        
        # For all other files (like /static/style.css), let the built-in parent class handle it.
        # It automatically looks for folders in the current directory, so it will find 'static/' correctly.
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    """
    HANDLING DATA (POST Requests):
    This is where we handle /encrypt and /decrypt.
    """
    def do_POST(self):
        # 1. READ DATA: Get the length of the message, then read those bytes
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 2. PARSE DATA: Decode bytes -> String -> JSON Dictionary
        data = json.loads(post_data.decode('utf-8'))
        
        key = data.get('key').upper().replace(" ", "")
        msg = data.get('message').upper()
        
        cipher = ColumnarTranspositionCipher(key)
        response_data = {}
        
        # 3. ROUTING: Check the URL path (The "Envelope Address")
        if self.path == '/encrypt':
            result_text, grid = cipher.encrypt(msg)
            response_data = {'result': result_text, 'grid': grid}
            
        elif self.path == '/decrypt':
            result_text, grid = cipher.decrypt(msg)
            response_data = {'result': result_text, 'grid': grid}
            
        else:
            self.send_error(404, "Route not found")
            return

        # 4. SEND RESPONSE
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

if __name__ == "__main__":
    print(f"Server started at http://localhost:{PORT}")
    print("Files served from: templates/ and static/")
    print("Press Ctrl+C to stop.")
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CipherRequestHandler) as httpd:
        httpd.serve_forever()