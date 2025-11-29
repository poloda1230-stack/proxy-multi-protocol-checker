import concurrent.futures
import time
from typing import List, Tuple, Optional

import requests

DEFAULT_TEST_URL_HTTP = "http://httpbin.org/ip"
DEFAULT_TEST_URL_HTTPS = "https://httpbin.org/ip"
REQUEST_TIMEOUT = 8


def _build_proxy_dict(proxy: str, mode: str) -> dict:
    """
    mode: "http", "https", "socks5"
    proxy: "ip:port"
    """
    host_port = proxy.strip()
    if not host_port:
        return {}
    if mode == "http":
        url = f"http://{host_port}"
        return {"http": url, "https": url}
    elif mode == "https":
        # 对于 HTTPS，我们同样通过 HTTP 代理通道发起 CONNECT
        url = f"http://{host_port}"
        return {"http": url, "https": url}
    elif mode == "socks5":
        # socks5h 让 DNS 走代理端
        url = f"socks5h://{host_port}"
        return {"http": url, "https": url}
    else:
        return {}


def _test_single_proxy(
    proxy: str,
    mode: str,
    test_url: Optional[str],
) -> Tuple[str, bool, float, Optional[int], Optional[str]]:
    """
    返回: (proxy, 是否可用, 耗时秒, HTTP 状态码, 错误信息)
    """
    if mode in ("http", "https"):
        url = test_url or (DEFAULT_TEST_URL_HTTPS if mode == "https" else DEFAULT_TEST_URL_HTTP)
    else:
        url = test_url or DEFAULT_TEST_URL_HTTPS

    proxies = _build_proxy_dict(proxy, mode)
    if not proxies:
        return proxy, False, 0.0, None, "invalid_proxy_string"

    start = time.time()
    try:
        resp = requests.get(
            url,
            proxies=proxies,
            timeout=REQUEST_TIMEOUT,
        )
        cost = time.time() - start
        ok = 200 <= resp.status_code < 300
        return proxy, ok, cost, resp.status_code, None
    except Exception as exc:
        cost = time.time() - start
        return proxy, False, cost, None, str(exc)


def _load_proxies_from_file(path: str) -> List[str]:
    items: List[str] = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            items.append(line)
    return items


def _save_good_proxies(path: str, results: List[Tuple[str, bool, float, Optional[int], Optional[str]]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for proxy, ok, _cost, _status, _err in results:
            if ok:
                f.write(f"{proxy}\n")


def run_check(
    mode: str,
    source_file: str = "proxies.txt",
    output_file: str = "",
    threads: int = 100,
    test_url: Optional[str] = None,
) -> None:
    """
    mode: "http" / "https" / "socks5"
    """
    mode = mode.lower()
    if mode not in ("http", "https", "socks5"):
        raise ValueError("mode must be http / https / socks5")

    proxies = _load_proxies_from_file(source_file)
    if not proxies:
        print(f"[!] 代理列表为空: {source_file}")
        return

    if not output_file:
        output_file = f"good_{mode}.txt"

    print(f"[*] 模式: {mode}")
    print(f"[*] 待检测代理数量: {len(proxies)}")
    print(f"[*] 输出文件: {output_file}")
    if test_url:
        print(f"[*] 测试地址: {test_url}")

    start_all = time.time()
    results: List[Tuple[str, bool, float, Optional[int], Optional[str]]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_map = {
            executor.submit(_test_single_proxy, proxy, mode, test_url): proxy
            for proxy in proxies
        }
        for future in concurrent.futures.as_completed(future_map):
            proxy = future_map[future]
            try:
                proxy, ok, cost, status, err = future.result()
            except Exception as exc:
                print(f"[错误] {proxy} -> {exc}")
                continue

            if ok:
                print(f"[OK]   {proxy}  ({cost:.2f}s, status={status})")
            else:
                short_err = (err or "error").split("\n", 1)[0]
                print(f"[BAD]  {proxy}  ({cost:.2f}s, err={short_err})")

            results.append((proxy, ok, cost, status, err))

    duration = time.time() - start_all
    good_count = sum(1 for _proxy, ok, _c, _s, _e in results if ok)
    print("-" * 50)
    print(f"[统计] 总数: {len(results)}, 可用: {good_count}, 耗时: {duration:.2f} 秒")

    _save_good_proxies(output_file, results)
    print(f"[完成] 已保存可用代理到: {output_file}")
