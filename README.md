# IPV6服务器 | IPv6 Web Server

> 仅用 Python 标准库搭建的公网 IPv6 网站：启动时自动探测本机公网 IPv6 并打印访问地址，内置 `/ip` 接口向访客显示"你的 IP 是多少"。
> A public-IPv6 website built with nothing but the Python standard library: it auto-detects the machine's public IPv6 at startup, prints the access URL, and serves a `/ip` endpoint that shows visitors their own IP.

## 功能特性 | Features

- **零依赖**：仅用 `http.server` / `socketserver` / `socket`，多线程处理请求。
  **Zero dependencies**: built on `http.server` / `socketserver` / `socket`, multi-threaded.
- **自动探测公网 IPv6**：启动时通过 UDP 路由探测（对公共 DNS `2400:3200::1` 的 connect，不实际发包）取得本机出口 IPv6，直接打印 `http://[IPv6]:8080/`。
  **Automatic public-IPv6 detection**: on startup it probes the routing table via a UDP connect to public DNS `2400:3200::1` (no actual packet sent) and prints `http://[IPv6]:8080/`.
- **`/ip` 接口**：返回访问者的 IP（纯文本，带 CORS 头），配套 `index.html` 展示页。
  **`/ip` endpoint**: returns the visitor's IP as plain text with CORS headers; `index.html` displays it.
- 其余请求按静态文件服务处理，网站根目录即脚本所在目录。
  Everything else is served as static files from the script's directory.

## 快速开始 | Quick Start

```bash
python ipv6_server.py
```

按控制台打印的地址访问即可。`index.html` 依赖后端的 `/ip` 接口，**不能**直接双击打开。
Visit the URL printed in the console. `index.html` relies on the backend's `/ip` endpoint — it **cannot** be opened by double-click.

## 配置 | Configuration

| 项 | Item | 位置 | Location |
|---|---|---|---|
| 端口 | Port | `PORT`（脚本顶部，默认 8080） | `PORT` (top of the script, default 8080) |
| 网站目录 | Web root | 脚本所在目录 | The script's own directory |

## 说明 | Notes

- 需要你的网络环境**支持公网 IPv6**（家宽一般可向运营商开启）；防火墙需放行对应端口。
  Your network must have **public IPv6 connectivity** (home broadband can usually enable it via the ISP); open the port in your firewall.
- 探测地址 `2400:3200::1` 是阿里公共 DNS，仅用于路由选路，不发送任何数据。
  The probe address `2400:3200::1` is Alibaba Public DNS, used only for route selection — no data is sent.
