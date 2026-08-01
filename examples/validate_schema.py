"""
PayPack Schema Validator — Example Usage

This script demonstrates how to read and validate PayPack's
ai-service-metadata.json against real-world service configurations.

Usage:
    python validate_schema.py

Dependencies:
    pip install jsonschema requests
"""
import json
from urllib.request import urlopen

# If jsonschema is not installed, fall back to basic validation
try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    print("[WARN] jsonschema not installed. Run: pip install jsonschema")
    print("[INFO] Running basic field check instead.\n")


def load_schema(path="schemas/v1/ai-service-metadata.json"):
    """Load the PayPack Service Metadata JSON Schema."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def basic_validate(instance, schema):
    """Fallback: check required fields exist."""
    required = schema.get("required", [])
    errors = []
    for field in required:
        if field not in instance:
            errors.append(f"Missing required field: {field}")
    return errors


def validate_service(instance, schema):
    """Validate a service metadata instance against the schema."""
    if HAS_JSONSCHEMA:
        try:
            validate(instance=instance, schema=schema)
            return []
        except ValidationError as e:
            return [e.message]
    else:
        return basic_validate(instance, schema)


# ===== Example service configurations =====

valid_service = {
    "service_id": "com.example.ocr.v1",
    "version": "1.0.0",
    "service_name": "Example OCR API",
    "description": "High-accuracy OCR for business documents.",
    "pricing": {
        "model": "fixed",
        "amount": 0.50,
        "currency": "CNY",
        "estimated_total_cost": 0.51
    },
    "performance": {
        "avg_latency_ms": 200,
        "success_rate": 0.995,
        "p99_latency_ms": 800
    },
    "reputation": {
        "trust_score": 92,
        "total_calls_24h": 50000,
        "dispute_rate": 0.002,
        "uptime_pct": 99.9
    },
    "policy": {
        "refund_policy": "auto_on_fail",
        "data_retention_days": 7,
        "sla": {
            "uptime": "99.9%",
            "max_latency_ms": 1000,
            "support_response_h": 24
        }
    },
    "endpoints": [
        {"path": "/v1/ocr", "method": "POST", "description": "Submit OCR job"}
    ]
}

invalid_service = {
    "service_id": "com.bad-service.v1"
    # Missing: version, pricing, reputation (all required)
}


if __name__ == "__main__":
    schema = load_schema()
    print(f"Schema loaded: {schema['title']}")
    print(f"Description: {schema['description']}\n")

    # Test 1: Valid service
    print("=" * 50)
    print("Test 1: Valid service configuration")
    errors = validate_service(valid_service, schema)
    if errors:
        print(f"❌ FAILED: {errors}")
    else:
        print("✅ PASSED — all required fields present and valid")

    # Test 2: Invalid service (missing required fields)
    print("\n" + "=" * 50)
    print("Test 2: Invalid service (missing required fields)")
    errors = validate_service(invalid_service, schema)
    if errors:
        print(f"✅ CORRECTLY REJECTED: {errors}")
    else:
        print("❌ SHOULD HAVE FAILED but passed")

    # Test 3: Load example files
    print("\n" + "=" * 50)
    print("Test 3: Validate bundled example files")
    for example_name in ["weather-api.example.json", "topup-service.example.json"]:
        try:
            with open(f"examples/{example_name}", "r", encoding="utf-8") as f:
                example = json.load(f)
            errors = validate_service(example, schema)
            if errors:
                print(f"❌ {example_name}: {errors}")
            else:
                print(f"✅ {example_name}: valid")
        except FileNotFoundError:
            print(f"⚠️ {example_name}: file not found")

    print("\nDone.")
