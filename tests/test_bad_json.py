import pytest
import os
import subprocess

def test_missing_auth_type():
    bad_json_file = "tests/bad-json/missing_auth_type.json"
    
    result = subprocess.run(
        ["python3", "src/client.py", "--server", bad_json_file], 
        capture_output=True, 
        text=True
    )
    
    assert "Traceback (most recent call last)" not in result.stderr, \
        f"Client crashed due unhandled exception (Traceback):\n{result.stderr}"
    
    return