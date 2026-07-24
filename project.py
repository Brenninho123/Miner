import os
import sys
import json
import hashlib
import argparse

SIGNATURES_FILE = "signatures.json"

def load_signatures():
    if not os.path.exists(SIGNATURES_FILE):
        return {}
    with open(SIGNATURES_FILE, "r") as f:
        return json.load(f)

def save_signatures(signatures):
    with open(SIGNATURES_FILE, "w") as f:
        json.dump(signatures, f, indent=4)

def hash_file(path, algo="sha256"):
    hasher = hashlib.new(algo)
    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, FileNotFoundError, OSError):
        return None

def scan_file(path, signatures):
    file_hash = hash_file(path)
    if file_hash is None:
        return None
    if file_hash in signatures:
        return {
            "path": path,
            "hash": file_hash,
            "threat": signatures[file_hash]
        }
    return None

def scan_directory(root, signatures):
    results = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            result = scan_file(full_path, signatures)
            if result:
                results.append(result)
    return results

def add_signature(path, threat_name, signatures):
    file_hash = hash_file(path)
    if file_hash is None:
        print(f"Could not hash file: {path}")
        return
    signatures[file_hash] = threat_name
    save_signatures(signatures)
    print(f"Added signature for {threat_name}: {file_hash}")

def main():
    parser = argparse.ArgumentParser(description="Simple hash-based antivirus scanner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("path", help="File or directory to scan")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("path", help="Path to malicious sample file")
    add_parser.add_argument("name", help="Threat name/label")

    args = parser.parse_args()
    signatures = load_signatures()

    if args.command == "scan":
        if os.path.isdir(args.path):
            results = scan_directory(args.path, signatures)
        elif os.path.isfile(args.path):
            result = scan_file(args.path, signatures)
            results = [result] if result else []
        else:
            print("Invalid path")
            sys.exit(1)

        if results:
            print(f"Found {len(results)} threat(s):")
            for r in results:
                print(f"  [!] {r['path']} -> {r['threat']} ({r['hash']})")
            sys.exit(1)
        else:
            print("No threats found")

    elif args.command == "add":
        add_signature(args.path, args.name, signatures)

if __name__ == "__main__":
    main()
