#!/usr/bin/env python3
"""launch.py — One command to start Fullmetal Anatomist."""

import os
import platform
import shutil
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

BASE = Path(__file__).resolve().parent
FRONTEND = BASE / "frontend"
VENV = BASE / "venv"
PORT = int(os.getenv("FMA_PORT", "8765"))
URL = f"http://127.0.0.1:{PORT}"


def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def teal(text: str) -> str:
    return f"\033[36m{text}\033[0m"


def red(text: str) -> str:
    return f"\033[31m{text}\033[0m"


def step(msg: str) -> None:
    print(f"\n{teal('⚗️')} {bold(msg)}")


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> None:
    subprocess.run(cmd, cwd=cwd, check=check)


def check_python() -> None:
    step("Checking Python version...")
    v = sys.version_info
    if v < (3, 11):
        print(red(f"Python 3.11+ required, got {v.major}.{v.minor}.{v.micro}"))
        sys.exit(1)
    print(f"  Python {v.major}.{v.minor}.{v.micro} ✅")


def check_node() -> None:
    step("Checking Node.js...")
    if not shutil.which("node"):
        print(red("Node.js not found! Install from https://nodejs.org/"))
        sys.exit(1)
    result = subprocess.run(["node", "--version"], capture_output=True, text=True)
    print(f"  Node {result.stdout.strip()} ✅")


def setup_venv() -> None:
    step("Setting up Python environment...")
    if not VENV.exists():
        run([sys.executable, "-m", "venv", str(VENV)])
    pip = str(VENV / ("Scripts" if platform.system() == "Windows" else "bin") / "pip")
    run([pip, "install", "-e", ".[dev]"], cwd=BASE)
    print("  Dependencies installed ✅")


def setup_frontend() -> None:
    step("Setting up frontend...")
    if not (FRONTEND / "node_modules").exists():
        run(["npm", "install"], cwd=FRONTEND)
    step("Building frontend...")
    run(["npm", "run", "build"], cwd=FRONTEND)
    print("  Frontend built ✅")


def start_server() -> None:
    step(f"Starting Fullmetal Anatomist on {URL}")
    python = str(VENV / ("Scripts" if platform.system() == "Windows" else "bin") / "python")
    proc = subprocess.Popen(
        [python, "-m", "uvicorn", "backend.main:app",
         "--host", "127.0.0.1", "--port", str(PORT)],
        cwd=str(BASE),
    )
    time.sleep(2)
    webbrowser.open(URL)
    print(f"\n{teal('⚗️')} {bold('Fullmetal Anatomist is running!')}")
    print(f"  Open {bold(URL)} in your browser")
    print(f"  Press Ctrl+C to stop\n")
    try:
        proc.wait()
    except KeyboardInterrupt:
        print(f"\n{teal('⚗️')} Shutting down...")
        proc.terminate()


def main() -> None:
    print(f"\n{teal('⚗️')} {bold('Fullmetal Anatomist')} — Starting up...")
    print('  "Equivalent Exchange: You give it textbook chapters,"')
    print('  "it gives you passing grades."\n')

    check_python()
    check_node()
    setup_venv()
    setup_frontend()
    start_server()


if __name__ == "__main__":
    main()
