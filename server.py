#!/usr/bin/env python3
"""
DSA Simulator - Localhost Server / Application Dispatcher
By default, launches the native interactive Python Desktop GUI.
If executed with --server, starts the headless REST API server.
"""

import sys
import os

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
if DIRECTORY not in sys.path:
    sys.path.insert(0, DIRECTORY)

if "--server" not in sys.argv and "--api" not in sys.argv:
    # Default behavior: Launch native interactive Python Capstone GUI
    from main import main
    if __name__ == "__main__":
        main()
else:
    # Headless REST API mode (if requested)
    import http.server
    import json
    import time
    import urllib.parse
    import backend.linked_list as ll_backend
    import backend.stack as stack_backend
    import backend.queue as queue_backend

    PORT = int(os.environ.get("PORT", 8080))
    active_lists = {
        "singly": ll_backend.SinglyLinkedList(),
        "doubly": ll_backend.DoublyLinkedList(),
        "circular-singly": ll_backend.CircularSinglyLinkedList(),
        "circular-doubly": ll_backend.CircularDoublyLinkedList()
    }
    for l_obj in active_lists.values():
        for val in [10, 20, 30, 40]:
            l_obj.insert_end(val)

    active_stack = stack_backend.Stack(capacity=10)
    active_queue = queue_backend.Queue(capacity=10)

    class LabServerHandler(http.server.SimpleHTTPRequestHandler):
        def _send_json(self, data, status_code=200):
            body = json.dumps(data, indent=2).encode('utf-8')
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path in ('/api/health', '/api/status'):
                self._send_json({
                    "status": "connected",
                    "backend": "Python 3 Standard Library",
                    "port": PORT,
                    "message": "DSA Simulator Python Backend Running Offline",
                    "activeLists": {k: {"length": len(v), "items": v.to_list()} for k, v in active_lists.items()}
                })
            else:
                self._send_json({"status": "ok", "app": "DSA Simulator Capstone"})

    if __name__ == "__main__":
        print(f"Starting Python DSA REST API Server on http://localhost:{PORT}")
        with http.server.HTTPServer(("", PORT), LabServerHandler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")
