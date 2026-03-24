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
IS_WINDOWS = platform.system() == "Windows"
BIN_DIR = VENV / ("Scripts" if IS_WINDOWS else "bin")
PORT = int(os.getenv("FMA_PORT", "8765"))
URL = f"http://127.0.0.1:{PORT}"




# ── Terminal helpers ───────────────────────────────────────────────

def _enable_ansi_windows() -> None:
    """Enable ANSI escape codes on Windows 10+ terminals."""
    if not IS_WINDOWS:
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass


def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def teal(text: str) -> str:
    return f"\033[36m{text}\033[0m"


def red(text: str) -> str:
    return f"\033[31m{text}\033[0m"


def step(msg: str) -> None:
    print(f"\n{teal('⚗️')} {bold(msg)}")


def run(cmd: list[str], cwd: Path | None = None, check: bool = True,
        env: dict | None = None) -> None:
    """Run a subprocess. Uses shell=True on Windows for .cmd scripts."""
    subprocess.run(cmd, cwd=cwd, check=check, env=env, shell=IS_WINDOWS)


# ── Checks ────────────────────────────────────────────────────────

def check_python() -> None:
    step("Checking Python version...")
    v = sys.version_info
    if v < (3, 11):
        print(red(f"Python 3.11+ required, got {v.major}.{v.minor}.{v.micro}"))
        print("  Download from: https://www.python.org/downloads/")
        sys.exit(1)
    print(f"  Python {v.major}.{v.minor}.{v.micro} ✅")


def check_node() -> None:
    step("Checking Node.js...")
    if not shutil.which("node"):
        print(red("Node.js not found!"))
        print("  Download from: https://nodejs.org/ (pick the LTS version)")
        sys.exit(1)
    result = subprocess.run(
        ["node", "--version"], capture_output=True, text=True, shell=IS_WINDOWS,
    )
    print(f"  Node {result.stdout.strip()} ✅")


def check_uv() -> None:
    step("Checking uv...")
    if not shutil.which("uv"):
        print(red("uv not found!"))
        if IS_WINDOWS:
            print('  Install: powershell -ExecutionPolicy ByPass -c '
                  '"irm https://astral.sh/uv/install.ps1 | iex"')
        else:
            print("  Install: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("  Then close & re-open your terminal.")
        sys.exit(1)
    result = subprocess.run(
        ["uv", "--version"], capture_output=True, text=True, shell=IS_WINDOWS,
    )
    print(f"  {result.stdout.strip()} ✅")


# ── Setup ────────────────────────────────────────────────────────

def setup_venv() -> None:
    step("Setting up Python environment...")
    if not VENV.exists():
        run(["uv", "venv", str(VENV)])
        run(["uv", "pip", "install", "-e", ".[dev]"], cwd=BASE)
        print("  Dependencies installed ✅")
    else:
        print("  venv already exists, skipping. (Delete venv/ to reinstall.)")


def setup_frontend() -> None:
    step("Setting up frontend...")
    needs_install = not (FRONTEND / "node_modules").exists()
    needs_build = not (FRONTEND / "dist").exists()

    if needs_install:
        run(["npm", "install"], cwd=FRONTEND)
    if needs_build:
        run(["npm", "run", "build"], cwd=FRONTEND)
        print("  Frontend built ✅")
    else:
        print("  Frontend already built, skipping. (Delete frontend/dist/ to rebuild.)")


# ── Server ───────────────────────────────────────────────────────

def start_server() -> None:
    step(f"Starting Fullmetal Anatomist on {URL}")
    python_exe = str(BIN_DIR / ("python.exe" if IS_WINDOWS else "python"))
    # Fall back to sys.executable if venv python doesn't exist
    if not Path(python_exe).exists():
        python_exe = sys.executable

    # IMPORTANT: Unset proxy vars so LLM API calls aren't blocked by corporate proxies
    env = os.environ.copy()
    for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'NO_PROXY', 'no_proxy']:
        env.pop(key, None)

    proc = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "backend.main:app",
         "--host", "127.0.0.1", "--port", str(PORT)],
        cwd=str(BASE),
        env=env,  # Use the cleaned environment
    )
    time.sleep(3)
    webbrowser.open(URL)
    print(f"\n{teal('⚗️')} {bold('Fullmetal Anatomist is running!')}")
    print(f"  Open {bold(URL)} in your browser")
    print(f"  Press Ctrl+C to stop\n")
    try:
        proc.wait()
    except KeyboardInterrupt:
        print(f"\n{teal('⚗️')} Shutting down...")
        proc.terminate()


# ── Main ─────────────────────────────────────────────────────────

def main() -> None:
    _enable_ansi_windows()
    print(f"\n{teal('⚗️')} {bold('Fullmetal Anatomist')} — Starting up...")
    print('  "Equivalent Exchange: You give it textbook chapters,"')
    print('  "it gives you passing grades."\n')

    check_python()
    check_node()
    check_uv()
    setup_venv()
    setup_frontend()
    print()
    start_server()


if __name__ == "__main__":
    main()
