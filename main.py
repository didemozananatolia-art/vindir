import os
import sys
import time
import socket
import threading
import webbrowser
import streamlit.web.cli as stcli

def find_free_port(start_port=8501):
    """Finds an available TCP port starting from start_port."""
    for port in range(start_port, start_port + 200):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return start_port

def main():
    # If running as a frozen PyInstaller bundle
    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Add bin folder (containing ffmpeg) to system PATH
    bin_dir = os.path.join(base_dir, "bin")
    if os.path.exists(bin_dir) and bin_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

    app_path = os.path.join(base_dir, "app.py")
    if not os.path.exists(app_path):
        # Fallback to local directory
        app_path = os.path.abspath("app.py")

    port = find_free_port(8501)
    url = f"http://localhost:{port}"

    print(f"=================================================")
    print(f"  YouTube Medya İndirici Başlatılıyor...")
    print(f"  Adres: {url}")
    print(f"=================================================")

    # Open the browser in a background thread
    def open_browser():
        time.sleep(1.8)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    sys.argv = [
        "streamlit",
        "run",
        app_path,
        f"--server.port={port}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false",
    ]

    try:
        sys.exit(stcli.main())
    except KeyboardInterrupt:
        print("\nUygulama kapatıldı.")
        sys.exit(0)

if __name__ == "__main__":
    main()
