import socket
import threading

class SSHPortScanner:
    def __init__(self, input_file, output_file, start_port=22, end_port=65355):
        self.input_file = input_file
        self.output_file = output_file
        self.start_port = start_port
        self.end_port = end_port
        self.lock = threading.Lock()

    def load_servers(self):
        with open(self.input_file, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def scan_port(self, ip, port):
        try:
            sock = socket.create_connection((ip, port), timeout=1)
            sock.close()
            result = f"{ip}:{port}"
            self.lock.acquire()
            with open(self.output_file, 'a') as file:
                file.write(result + '\n')
            self.lock.release()
        except (socket.timeout, socket.error):
            pass

    def run(self):
        servers = self.load_servers()
        threads = []
        for server in servers:
            for port in range(self.start_port, self.end_port + 1):
                thread = threading.Thread(target=self.scan_port, args=(server, port))
                threads.append(thread)
                thread.start()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    input_file = "servers.txt"
    output_file = "open_ssh_ports.txt"
    scanner = SSHPortScanner(input_file, output_file)
    scanner.run()
