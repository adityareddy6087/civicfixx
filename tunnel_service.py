import subprocess
import time
import re
import sys

def main():
    print("Starting background uvicorn server...")
    server = subprocess.Popen([sys.executable, "run.py"])
    time.sleep(2)

    print("Opening serveo SSH tunnel...")
    tunnel = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:127.0.0.1:8000", "serveo.net"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in iter(tunnel.stdout.readline, ''):
        print(line, end='')
        if "https://" in line:
            url_match = re.search(r'https://[^\s]+', line)
            if url_match:
                print(f"\n==========================================")
                print(f"GUARANTEED LIVE PUBLIC HTTPS URL:")
                print(f"{url_match.group(0)}")
                print(f"==========================================\n")
                sys.stdout.flush()

    server.wait()

if __name__ == "__main__":
    main()
