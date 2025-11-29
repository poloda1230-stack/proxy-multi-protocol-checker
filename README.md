项目简介
多协议代理检测器（HTTP / HTTPS / SOCKS5），支持从文本文件批量读取代理，使用多线程方式测试可用性，并分别输出可用代理列表。项目为原创实现，不依赖或引用其他仓库的代码或资料。​

功能特性
支持协议：HTTP、HTTPS、SOCKS5 三种代理。​

批量检测：从文件中读取代理列表（每行一个 ip:port）。​

多线程：使用线程池并行检测，加快检测速度。​

结果输出：自动将可用代理写入 good_http.txt / good_https.txt / good_socks5.txt。

文件结构
main.py：命令行入口，菜单和交互。

checker.py：核心检测逻辑和多线程实现。

requirements.txt：Python 依赖列表（requests + SOCKS 支持）。​

proxies.txt：待检测代理列表（需自行填写）。​

代理列表格式
编辑仓库根目录下的 proxies.txt，每行一个代理，格式为：

ip:port

示例：

127.0.0.1:8080

127.0.0.1:1080

可以使用 # 开头的行作为注释，这些行会被自动忽略。

环境要求
Python 3.8+（推荐 3.10 或更高）。​

pip（Python 包管理工具）。​

项目已在以下系统上验证可安装运行：

Debian 系列（如 Debian 11/12）​

Ubuntu 系列（如 Ubuntu 20.04/22.04/24.04）​

Alpine Linux（3.x）​

在 Debian / Ubuntu 上安装运行
安装系统依赖：

sudo apt update

sudo apt install -y git python3 python3-pip

克隆仓库：

cd ~

git clone https://github.com/你的用户名/你的仓库名.git

cd 你的仓库名

安装 Python 依赖：

pip3 install -r requirements.txt
或

python3 -m pip install -r requirements.txt

运行程序：

python3 main.py

按提示操作即可完成检测。

在 Alpine Linux 上安装运行
安装系统依赖：

apk update

apk add --no-cache git python3 py3-pip

如需要，可创建 python 软链接（部分环境方便使用 python 命令）：

ln -sf python3 /usr/bin/python

克隆仓库：

cd /root

git clone https://github.com/你的用户名/你的仓库名.git

cd 你的仓库名

安装 Python 依赖：

pip3 install -r requirements.txt
或

python3 -m pip install -r requirements.txt

运行程序：

python3 main.py

使用说明
启动程序后，终端会显示菜单：

检测 HTTP

检测 HTTPS

检测 SOCKS5

依次检测全部（HTTP, HTTPS, SOCKS5）

接着程序会依次询问：

代理列表文件名（默认 proxies.txt，直接回车即可）。

线程数（默认 100，越大速度越快，但对机器压力也更大）。

自定义测试 URL（留空则使用内置的 httpbin /ip 作为测试目标）。​

检测过程中，终端会实时打印每个代理的检测结果，包含：

[OK] / [BAD] 标记

响应耗时（秒）

HTTP 状态码或错误原因

检测完成后会统计总数、可用数量和总耗时，并在当前目录生成对应的输出文件：

good_http.txt

good_https.txt

good_socks5.txt

文件内每行一个可用代理，格式与输入文件相同。

常见问题
Q: 如何在不同 VPS 上快速部署？
A: 只需安装 git + python3 + pip，然后 git clone 仓库、pip 安装依赖、python3 main.py 即可，Debian/Ubuntu 用 apt，Alpine 用 apk。

Q: 如何更新代码？
A: 在仓库目录执行：git pull，然后重新运行 python3 main.py 即可。
