import os
import platform
import multiprocessing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resolve_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

def detect_signatures_file():
    candidates = [
        resolve_path("data/signatures.json"),
        resolve_path("signatures.json"),
        os.path.join(os.path.expanduser("~"), ".miner", "signatures.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return candidates[0]

PROJECT = {
    "name": "Miner",
    "package": "com.brenninho.miner",
    "version": "0.1.0",
    "description": "An antivirus program written in Python.",
    "author": "Brenninho123",
    "license": "Apache-2.0",

    "base_dir": BASE_DIR,
    "main": "src/main.py",
    "source_dir": resolve_path("src"),

    "python_requires": ">=3.10",
    "platform": platform.system(),
    "cpu_count": multiprocessing.cpu_count(),

    "dependencies": [
        "watchdog>=4.0.0",
        "requests>=2.31.0",
        "psutil>=5.9.0"
    ],

    "dev_dependencies": [
        "pytest>=8.0.0"
    ],

    "signatures_file": detect_signatures_file(),
    "signatures_exists": os.path.exists(detect_signatures_file()),

    "scan": {
        "cpu_threshold": 50.0,
        "mem_threshold_mb": 500,
        "hash_algo": "sha256",
        "chunk_size": 65536,
        "max_workers": multiprocessing.cpu_count()
    },

    "build": {
        "entry_point": "src.main:main",
        "output_dir": resolve_path("dist"),
        "console_script": "miner-scan"
    },

    "assets": [
        "data/signatures.json",
        "README.md",
        "LICENSE"
    ]
}

def ensure_signatures_file():
    path = PROJECT["signatures_file"]
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("{}")
        PROJECT["signatures_exists"] = True
    return path
