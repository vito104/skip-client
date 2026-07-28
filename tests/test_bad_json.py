import pytest
import subprocess

def test_missing_auth_type():
    bad_json_file = "tests/bad-json/missing_auth_type.json"
    
    result = subprocess.run(
        ["python3", "src/client.py", "--server", bad_json_file], 
        capture_output=True, 
        text=True
    )
    
    assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
    
    assert "Traceback (most recent call last)" not in result.stderr, \
        f"Client crashed due to unhandled exception:\n{result.stderr}"
        
    assert "Error: Some fields are missing in server config" in result.stderr, \
        f"Expected specific error message in stderr, got:\n{result.stderr}"


def test_not_a_json():
    bad_json_file = "tests/bad-json/not_a_json.json"

    result = subprocess.run(
        ["python3", "src/client.py", "--server", bad_json_file], 
        capture_output=True, 
        text=True
    )

    assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
    
    assert "Traceback (most recent call last)" not in result.stderr, \
        f"Client crashed due to unhandled exception:\n{result.stderr}"
        
    assert "Error: Invalid json format" in result.stderr, \
        f"Expected specific error message in stderr, got:\n{result.stderr}"

def test_missing_port():
    bad_json_file = "tests/bad-json/missing_port.json"

    result = subprocess.run(
        ["python3", "src/client.py", "--peer", bad_json_file], 
        capture_output=True, 
        text=True
    )

    assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
    
    assert "Traceback (most recent call last)" not in result.stderr, \
        f"Client crashed due to unhandled exception:\n{result.stderr}"