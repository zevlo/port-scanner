import argparse
from queue import Queue
from socket import AF_INET, gethostbyname, socket, SOCK_STREAM
import threading


def tcp_test(port: int, target_ip: str) -> None:
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"Opened Port: {port}")


def worker(target_ip: str, queue: Queue) -> None:
    while not queue.empty():
        port = queue.get()
        tcp_test(port, target_ip)
        queue.task_done()


def main(host: str, start_port: int, end_port: int) -> None:
    target_ip = gethostbyname(host)
    queue = Queue()
    for port in range(start_port, end_port + 1):
        queue.put(port)
    for _ in range(100):  # Adjust the number of threads if necessary
        t = threading.Thread(
            target=worker,
            args=(
                target_ip,
                queue,
            ),
        )
        t.daemon = True
        t.start()
    queue.join()
    print("Scanning completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Port Scanner")
    parser.add_argument("host", help="Host to scan")
    parser.add_argument("ports", help="Port range to scan, formatted as start-end")
    args = parser.parse_args()

    start_port, end_port = map(int, args.ports.split("-"))
    main(args.host, start_port, end_port)
