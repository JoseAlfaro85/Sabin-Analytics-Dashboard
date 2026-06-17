#!/usr/bin/env python3
"""
Local server for the canonical Sabin dashboard web app.
"""

import argparse
import http.server
import logging
import mimetypes
import os
from pathlib import Path
import socketserver
from urllib.parse import unquote, urlparse
import webbrowser

logging.basicConfig(level='INFO', format='%(message)s')
logger = logging.getLogger(__name__)

DASHBOARD_ROOT = Path(__file__).resolve().parent
DEFAULT_DASHBOARD = 'DASHBOARD_PREVIEW.html'
APP_ROUTES = {'', '/', '/app', '/app/'}


def content_type_for(path):
    suffix = path.suffix.lower()
    if suffix == '.html':
        return 'text/html; charset=utf-8'
    if suffix == '.json':
        return 'application/json; charset=utf-8'
    if suffix == '.csv':
        return 'text/csv; charset=utf-8'
    if suffix == '.css':
        return 'text/css; charset=utf-8'
    if suffix == '.js':
        return 'text/javascript; charset=utf-8'
    if suffix == '.webmanifest':
        return 'application/manifest+json; charset=utf-8'
    if suffix == '.svg':
        return 'image/svg+xml'
    return mimetypes.guess_type(str(path))[0] or 'application/octet-stream'


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    server_version = 'SabinDashboardHTTP/1.1'

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        return super().end_headers()

    def do_HEAD(self):
        self.serve_dashboard_file(send_body=False)

    def do_GET(self):
        self.serve_dashboard_file(send_body=True)

    def serve_dashboard_file(self, send_body):
        url_path = unquote(urlparse(self.path).path or '/')
        if url_path in APP_ROUTES:
            url_path = f'/{DEFAULT_DASHBOARD}'

        requested = (DASHBOARD_ROOT / url_path.lstrip('/')).resolve()
        try:
            requested.relative_to(DASHBOARD_ROOT)
        except ValueError:
            self.send_error(404, 'File not found')
            return

        if requested.is_dir():
            requested = (requested / DEFAULT_DASHBOARD).resolve()
            try:
                requested.relative_to(DASHBOARD_ROOT)
            except ValueError:
                self.send_error(404, 'File not found')
                return

        if not requested.is_file():
            self.send_error(404, 'File not found')
            return

        try:
            body = requested.read_bytes() if send_body else b''
            length = len(body) if send_body else requested.stat().st_size
            self.send_response(200)
            self.send_header('Content-Type', content_type_for(requested))
            self.send_header('Content-Length', str(length))
            self.end_headers()
            if send_body:
                self.wfile.write(body)
        except BrokenPipeError:
            logger.info('Client disconnected while serving %s', url_path)
        except OSError:
            logger.exception('Unable to serve %s', requested)
            self.send_error(500, 'Unable to read dashboard file')


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


def start_server(port=8080, open_browser=True):
    os.chdir(DASHBOARD_ROOT)
    with ThreadingTCPServer(('', port), DashboardHandler) as httpd:
        url = f'http://localhost:{port}/app'
        print(f'Serving dashboard from: {DASHBOARD_ROOT}')
        print(f'Open dashboard at: {url}')
        print('Press Ctrl+C to stop the server.')
        if open_browser:
            try:
                webbrowser.open(url)
            except Exception:
                logger.info('Browser did not open automatically; open the URL above manually.')

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Serve the Sabin dashboard locally')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    start_server(port=args.port, open_browser=not args.no_browser)
