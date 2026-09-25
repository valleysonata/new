import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

class RewriteHandler(SimpleHTTPRequestHandler):
    """Serve extensionless URLs (/about -> about.html) like GitHub Pages."""
    def translate_path(self, path):
        path = super().translate_path(path)
        if os.path.isdir(path):
            idx = os.path.join(path, 'index.html')
            if os.path.exists(idx):
                return idx
        if not os.path.exists(path):
            p = path + '.html'
            if os.path.exists(p):
                return p
        return path

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--host', default='127.0.0.1')
    p.add_argument('--port', type=int, default=8765)
    args = p.parse_args()
    print(f"Serving {os.getcwd()} at http://{args.host}:{args.port} (extensionless URLs)")
    HTTPServer((args.host, args.port), RewriteHandler).serve_forever()
