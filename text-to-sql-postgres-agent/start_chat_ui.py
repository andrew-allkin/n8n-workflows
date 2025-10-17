#!/usr/bin/env python3
"""
Simple HTTP server for the Chat UI
Serves the chat interface on http://localhost:PORT
"""

import http.server
import socketserver
import webbrowser
import os
import socket

# Try these ports in order
PORTS = [8000, 8001, 8080, 8888, 3000, 5000]

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging for cleaner output
        pass

def find_available_port(ports):
    """Find the first available port from the list"""
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

def start_server():
    # Change to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Find available port
    port = find_available_port(PORTS)
    
    if port is None:
        print("❌ Error: All common ports are in use!")
        print("")
        print("Tried ports:", ", ".join(map(str, PORTS)))
        print("")
        print("💡 Try killing existing servers or specify a custom port:")
        print("   python3 start_chat_ui.py 9000")
        return
    
    Handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            url = f"http://localhost:{port}/chat_ui.html"
            print("🚀 Chat UI Server Started!")
            print("")
            print(f"📍 Server URL: {url}")
            print(f"📡 Port: {port}")
            print("")
            print("Opening browser...")
            print("")
            print("Press Ctrl+C to stop the server")
            print("-" * 50)
            
            # Open browser automatically
            webbrowser.open(url)
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n\n✋ Server stopped.")
                print("Goodbye! 👋")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("")
        print("💡 Try a different port or check if another server is running.")

if __name__ == "__main__":
    start_server()

