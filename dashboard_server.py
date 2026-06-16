#!/usr/bin/env python3
"""
Local server for the canonical Sabin dashboard package.
"""

import argparse
import http.server
import logging
import os
from pathlib import Path
import socketserver
from urllib.parse import urlsplit, urlunsplit
import webbrowser

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

DASHBOARD_ROOT = Path(__file__).resolve().parent


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        return super().end_headers()

    def do_GET(self):
        parts = urlsplit(self.path)
        if parts.path in ('', '/', '/app'):
            self.path = urlunsplit(
                ('', '', '/DASHBOARD_PREVIEW.html', parts.query, parts.fragment)
            )
        return super().do_GET()


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


def start_server(port=8080, open_browser=True):
    os.chdir(DASHBOARD_ROOT)
    with ThreadingTCPServer(('', port), DashboardHandler) as httpd:
        url = f'http://localhost:{port}/DASHBOARD_PREVIEW.html'
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
