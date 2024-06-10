import argparse
import http.server
import socketserver
import sys


class ReuseAddressTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    REDIRECT_PATHS = ["/mp3/", "/other/", "/pdf/", "/wma/", "/zip/"]

    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", f"/html/")
            self.end_headers()
            return

        for path in self.REDIRECT_PATHS:
            if self.path.startswith(path):
                self.send_response(302)
                self.send_header("Location", f"http://analogion.com/site{self.path}")
                self.end_headers()
                return

        super().do_GET()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="Specify alternate port",
    )
    args = parser.parse_args()

    with ReuseAddressTCPServer(("", args.port), CustomHTTPRequestHandler) as httpd:
        host = httpd.socket.getsockname()[0]
        print(
            f"Serving HTTP on {host} port {args.port} "
            f"(http://{host}:{args.port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
