import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import hash_file, scan_file

def test_hash_file_returns_none_for_missing_file():
    assert hash_file("nonexistent_file.xyz") is None

def test_hash_file_returns_hash_for_existing_file(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello world")
    result = hash_file(str(test_file))
    assert result is not None
    assert len(result) == 64

def test_scan_file_detects_known_signature(tmp_path):
    test_file = tmp_path / "malware.txt"
    test_file.write_text("malicious content")
    from main import hash_file
    file_hash = hash_file(str(test_file))
    signatures = {file_hash: "TestThreat"}
    result = scan_file(str(test_file), signatures)
    assert result is not None
    assert result["threat"] == "TestThreat"

def test_scan_file_returns_none_for_unknown_file(tmp_path):
    test_file = tmp_path / "clean.txt"
    test_file.write_text("clean content")
    result = scan_file(str(test_file), {})
    assert result is None
