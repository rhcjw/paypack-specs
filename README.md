# PayPack Value Metadata Specification

> **x402/AP2 defines HOW to pay. This specification defines whether the payment is WORTH IT.**

## What is this?

This repository contains the open standard for AI service value metadata. It enables AI agents to evaluate service quality, trust, and cost before initiating a payment — making autonomous AI spending smarter and safer.

## The Problem It Solves

Before an AI agent pays for a service, it needs to know:

- **Is this service reliable?** → `trust_score`
- **Will I get what I paid for?** → `success_rate` + `refund_policy`
- **What's the real total cost?** → `estimated_total_cost`

This JSON file is the AI agent's "Yelp for services" — machine-readable, supports autonomous decision-making.

## Quick Links

- [Service Metadata Schema](schemas/v1/ai-service-metadata.json)
- [Credit System & Price Index](docs/credit-system.md) 🆕
- [Price Index SQL Schema](schemas/v1/price-index.sql) 🆕
- [Price Guard Hook Example](examples/price_guard.py) 🆕
- [Integration Guide](docs/integration-guide.md)
- [Example: Weather API](examples/weather-api.example.json)
- [Example: Top-Up Service](examples/topup-service.example.json)

## Quick Start

```python
from paypack.metadata import fetch_metadata, should_pay

# Fetch service metadata
metadata = fetch_metadata("https://api.weather.com")

# AI agent decides whether to pay
pay, reason = should_pay(metadata, budget=0.01, min_trust_score=80)
print(f"{'✅' if pay else '❌'} {reason}")
```

## For Service Providers

### Option 1 (Recommended): Self-host

Place `ai-service-metadata.json` at your service root:

```
https://your-api-domain.com/.well-known/ai-service-metadata.json
```

AI agents will auto-discover it. No code required.

### Option 2: PayPack Cloud

Log into [PayPack Cloud](https://paypack.cloud), fill in a simple form with your pricing, SLA, and refund policy, and we'll generate and host the metadata file for you.

## Disclaimer

This metadata is provided for **machine reference only**. PayPack Cloud calculates trust scores based on historical transaction data but makes no warranty regarding the accuracy or completeness of the information. AI agents should use this data as one factor among many in their decision-making process.

## License

Apache 2.0 — see [LICENSE](LICENSE)
