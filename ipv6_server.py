import http.server
import socket
import socketserver
import os


# ============================================================
# 配置
# ============================================================

# 服务器端口
PORT = 8080

# 网站目录
WEB_ROOT = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# 公网 IPv6 探测
# ============================================================

def get_public_ipv6():

    # 通过 UDP 连接公网 IPv6 DNS 探测本机出口 IPv6
    # （UDP connect 不会真正发包，只让系统选路）
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    try:

        s.connect(("2400:3200::1", 53))

        return s.getsockname()[0]

    except OSError:

        return ""

    finally:

        s.close()


# ============================================================
# HTTP Handler
# ============================================================

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        # 获取访问者 IP
        if self.path == "/ip":

            client_ip = self.client_address[0]

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/plain; charset=utf-8"
            )

            self.send_header(
                "Access-Control-Allow-Origin",
                "*"
            )

            self.end_headers()

            self.wfile.write(
                client_ip.encode("utf-8")
            )

            return

        # 其他请求交给普通网页服务器处理
        super().do_GET()


# ============================================================
# IPv6 Server
# ============================================================

class IPv6Server(socketserver.ThreadingTCPServer):

    address_family = socket.AF_INET6

    allow_reuse_address = True


# ============================================================
# 启动
# ============================================================

def main():

    os.chdir(WEB_ROOT)

    ipv6 = get_public_ipv6()

    index_file = os.path.join(
        WEB_ROOT,
        "index.html"
    )

    if not os.path.isfile(index_file):

        print("错误：没有找到 index.html")

        print(
            "网站目录：",
            WEB_ROOT
        )

        return

    try:

        with IPv6Server(
            ("::", PORT),
            MyHTTPRequestHandler
        ) as server:

            print("=" * 60)
            print("IPv6 公网服务器已启动")
            print("=" * 60)

            print()

            print("网站目录：")
            print(WEB_ROOT)

            print()

            print("公网 IPv6：")
            print(ipv6 or "（自动探测失败，请用 ipconfig 查看本机公网 IPv6）")

            print()

            print("访问地址：")
            if ipv6:
                print(f"http://[{ipv6}]:{PORT}/")

            print()

            print("按 Ctrl+C 停止服务器")

            print("=" * 60)

            server.serve_forever()

    except OSError as e:

        print("服务器启动失败：")
        print(e)


if __name__ == "__main__":

    main()