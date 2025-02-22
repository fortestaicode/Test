import subprocess
import json
import logging

# إعداد تسجيل الأخطاء
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SSHPortScannerMasscan:
    def __init__(self, input_file, output_file, start_port=22, end_port=65355):
        self.input_file = input_file
        self.output_file = output_file
        self.start_port = start_port
        self.end_port = end_port

    def load_servers(self):
        with open(self.input_file, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def scan_ports(self, ip):
        try:
            logging.info(f"Scanning {ip} from port {self.start_port} to port {self.end_port}")
            result = subprocess.run(
                ["masscan", "-p", f"{self.start_port}-{self.end_port}", ip, "--rate", "10000", "--open", "--output-format", "json"],
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error scanning {ip}: {e}")
            return []

    def run(self):
        servers = self.load_servers()
        with open(self.output_file, 'w') as file:
            for server in servers:
                results = self.scan_ports(server)
                for result in results:
                    if result['ports'][0]['port'] == 22:
                        logging.info(f"Found open SSH port on {server}:{result['ports'][0]['port']}")
                        file.write(f"{server}:{result['ports'][0]['port']}\n")

if __name__ == "__main__":
    input_file = "servers.txt"
    output_file = "open_ssh_ports.txt"
    scanner = SSHPortScannerMasscan(input_file, output_file)
    scanner.run()
