import sys
from tcp_ping.core import tcp_ping


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <host> [port]")
        return

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 80

    latency = tcp_ping(host, port)

    if latency is not None:
        print(f"Latency to {host}:{port} = {latency:.2f} ms")
    else:
        print("Connection failed.")


if __name__ == "__main__":
    main()
