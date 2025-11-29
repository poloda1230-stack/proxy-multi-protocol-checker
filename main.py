from checker import run_check


def ask_int(prompt: str, default: int) -> int:
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print("输入不是数字，使用默认值。")
        return default


def main():
    print("=== 多协议代理检测器 (HTTP / HTTPS / SOCKS5) ===")
    print("1) 检测 HTTP")
    print("2) 检测 HTTPS")
    print("3) 检测 SOCKS5")
    print("4) 依次检测全部 (HTTP, HTTPS, SOCKS5)")
    choice = input("请选择(1-4): ").strip()

    src = input("请输入代理列表文件名 [proxies.txt]: ").strip() or "proxies.txt"
    threads = ask_int("线程数", 100)

    custom_url = input("自定义测试 URL (留空使用默认): ").strip()
    test_url = custom_url or None

    if choice == "1":
        run_check("http", source_file=src, output_file="good_http.txt", threads=threads, test_url=test_url)
    elif choice == "2":
        run_check("https", source_file=src, output_file="good_https.txt", threads=threads, test_url=test_url)
    elif choice == "3":
        run_check("socks5", source_file=src, output_file="good_socks5.txt", threads=threads, test_url=test_url)
    elif choice == "4":
        run_check("http", source_file=src, output_file="good_http.txt", threads=threads, test_url=test_url)
        run_check("https", source_file=src, output_file="good_https.txt", threads=threads, test_url=test_url)
        run_check("socks5", source_file=src, output_file="good_socks5.txt", threads=threads, test_url=test_url)
    else:
        print("无效选择。")


if __name__ == "__main__":
    main()
