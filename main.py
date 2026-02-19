import socket
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

# -----------------------------
# Default Configuration
# -----------------------------
DEFAULT_TIMEOUT = 1
DEFAULT_THREADS = 100

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}


# -----------------------------
# Resolve target
# -----------------------------
def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print("[!] Failed to resolve target")
        return None


# -----------------------------
# TCP Ping with multiple tries
# -----------------------------
def tcp_ping(ip, port, count, timeout):
    results = []

    for _ in range(count):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        start = time.time()
        result = sock.connect_ex((ip, port))
        end = time.time()

        sock.close()

        if result == 0:
            latency = (end - start) * 1000
            results.append(latency)

    if results:
        avg = sum(results) / len(results)
        return round(avg, 2)
    else:
        return None


# -----------------------------
# Banner grabbing
# -----------------------------
def grab_banner(ip, port, timeout):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, port))

        try:
            banner = sock.recv(1024).decode().strip()
        except:
            banner = ""

        sock.close()
        return banner
    except:
        return None


# -----------------------------
# Scan single port
# -----------------------------
def scan_port(ip, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    result = sock.connect_ex((ip, port))
    sock.close()

    if result == 0:
        service = COMMON_PORTS.get(port, "Unknown")
        banner = grab_banner(ip, port, timeout)
        return (port, service, banner)
    return None


# -----------------------------
# Parse ports
# -----------------------------
def parse_ports(port_str):
    ports = set()

    parts = port_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            for p in range(start, end + 1):
                ports.add(p)
        else:
            ports.add(int(part))

    return sorted(ports)


# -----------------------------
# Port scanning
# -----------------------------
def scan_ports(ip, ports, timeout, threads):
    results = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, ip, p, timeout) for p in ports]

        for future in futures:
            result = future.result()
            if result:
                results.append(result)

    return results


# -----------------------------
# Save results
# -----------------------------
def save_results(filename, ip, results):
    with open(filename, "w") as f:
        f.write(f"Scan results for {ip}\n\n")
        for port, service, banner in results:
            f.write(f"{port} ({service})\n")
            if banner:
                f.write(f"  Banner: {banner}\n")


# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Advanced TCP Scanner")

    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("-p", "--ports", default="80",
                        help="Ports (e.g. 80,443 or 1-1000)")
    parser.add_argument("-t", "--threads", type=int,
                        default=DEFAULT_THREADS)
    parser.add_argument("--timeout", type=float,
                        default=DEFAULT_TIMEOUT)
    parser.add_argument("--ping", type=int, default=0,
                        help="Number of TCP ping attempts")
    parser.add_argument("-o", "--output", help="Save results to file")

    args = parser.parse_args()

    ip = resolve_target(args.target)
    if not ip:
        return

    print(f"[+] Target: {args.target} ({ip})")

    # TCP Ping
    if args.ping > 0:
        latency = tcp_ping(ip, 80, args.ping, args.timeout)
        if latency:
            print(f"[+] TCP Ping: {latency} ms")
        else:
            print("[!] Ping failed")

    ports = parse_ports(args.ports)

    print(f"[+] Scanning {len(ports)} ports...")

    results = scan_ports(ip, ports, args.timeout, args.threads)

    print("\n[+] Open Ports:")
    for port, service, banner in results:
        print(f"{port} ({service})")
        if banner:
            print(f"   Banner: {banner}")

    if args.output:
        save_results(args.output, ip, results)
        print(f"\n[+] Results saved to {args.output}")


if __name__ == "__main__":
    main()