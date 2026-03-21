import pytest
from pathlib import Path
from autofix.extractor import ErrorExtractor
from autofix.parser import read_last_lines

def test_extractor_python_traceback():
    extractor = ErrorExtractor()
    logs = [
        "Some normal log line",
        "Traceback (most recent call last):",
        "  File \"test.py\", line 1, in <module>",
        "    1/0",
        "ZeroDivisionError: division by zero",
        "Another normal line"
    ]
    errors = extractor.extract_errors(logs)
    assert len(errors) >= 1
    assert "ZeroDivisionError" in errors[0]['content']

def test_extractor_java_stacktrace():
    extractor = ErrorExtractor()
    logs = [
        "2024-01-01 10:00:00 INFO Starting app",
        "Exception in thread \"main\" java.lang.NullPointerException",
        "  at com.example.App.main(App.java:10)",
        "  at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)",
        "2024-01-01 10:00:01 INFO Stopped app"
    ]
    errors = extractor.extract_errors(logs)
    assert len(errors) >= 1
    assert "NullPointerException" in errors[0]['content']
    assert "at com.example.App.main" in errors[0]['content']

def test_extractor_web_error():
    extractor = ErrorExtractor()
    logs = [
        "127.0.0.1 - - [21/Mar/2026:09:02:07 +0000] \"GET /api/data HTTP/1.1\" 500 1024",
        "127.0.0.1 - - [21/Mar/2026:09:02:08 +0000] \"GET /favicon.ico HTTP/1.1\" 404 512"
    ]
    errors = extractor.extract_errors(logs)
    assert len(errors) == 2
    assert "500" in errors[0]['content']
    assert "404" in errors[1]['content']

def test_parser_read_last_lines(tmp_path):
    d = tmp_path / "test.log"
    content = "\n".join([f"Line {i}" for i in range(100)])
    d.write_text(content)
    
    lines = read_last_lines(d, n=10)
    assert len(lines) == 10
    assert lines[-1] == "Line 99"
