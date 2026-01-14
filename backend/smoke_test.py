"""backend/smoke_test.py

Simple smoke test script for the Unified ASD Detection API.

Usage:
  - Activate your virtualenv and ensure backend is running on localhost:8000
  - Run: python3 backend/smoke_test.py

The script will test /health, /models, /predict/survey endpoints.
(image/video tests skipped if no example files provided)
"""

import sys
import requests
import json

API_BASE = "http://localhost:8000"
TIMEOUT = 15


def check_health():
    url = f"{API_BASE}/health"
    print(f"GET {url}")
    r = requests.get(url, timeout=TIMEOUT)
    print(r.status_code, r.text)
    r.raise_for_status()


def check_models():
    url = f"{API_BASE}/models"
    print(f"GET {url}")
    r = requests.get(url, timeout=TIMEOUT)
    print(r.status_code)
    try:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(r.text)
    r.raise_for_status()


def check_survey():
    url = f"{API_BASE}/predict/survey"
    payload = {
        "age": 36,
        "sex": "Male",
        "ethnicity": "Other",
        "jaundice": "no",
        "asd_history": "no",
        "respondent": "parent",
        "Q1": {"answer": "Yes"},
        "Q2": {"answer": "No"},
        "Q3": {"answer": "No"},
        "Q4": {"answer": "Yes"},
        "Q5": {"answer": "No"},
        "Q6": {"answer": "No"},
        "Q7": {"answer": "Yes"},
        "Q8": {"answer": "No"},
        "Q9": {"answer": "No"},
        "Q10": {"answer": "Yes"}
    }
    print(f"POST {url} (survey)")
    r = requests.post(url, json=payload, timeout=TIMEOUT)
    print(r.status_code)
    try:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(r.text)
    r.raise_for_status()


def main():
    try:
        check_health()
        print("\n" + "="*60 + "\n")
        check_models()
        print("\n" + "="*60 + "\n")
        check_survey()
        print("\n" + "="*60 + "\n")
        print("✓ SMOKE TESTS PASSED")
    except Exception as e:
        print("✗ ERROR:", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
