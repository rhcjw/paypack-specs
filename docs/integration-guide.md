# PayPack AI Service Metadata — Integration Guide

## Overview

The PayPack AI Service Metadata standard enables AI agents to make informed payment decisions by evaluating service quality before initiating a transaction.

> **x402/AP2 defines HOW to pay. This standard defines whether the payment is WORTH IT.**

## Quick Start

### Step 1: Create your metadata file

Copy the example from [`examples/weather-api.example.json`](../examples/weather-api.example.json) and fill in your service details. The minimal required fields are:

- `service_id` — unique identifier (reverse-domain notation)
- `pricing.model` — `fixed`, `tiered`, or `dynamic`
- `pricing.amount` — base price per call
- `reputation.trust_score` — 0-100 composite score (calculated by PayPack Cloud, or self-reported for initial setup)

### Step 2: Host the file

Place the file at your service root so AI agents can auto-discover it:

```
https://your-api-domain.com/.well-known/ai-service-metadata.json
```

### Step 3: Verify

Use the PayPack metadata client to verify your file is correctly formatted and accessible:

```python
from paypack.metadata import fetch_metadata

metadata = fetch_metadata("https://your-api-domain.com")
print(f"✅ Metadata loaded: {metadata['service_name']}")
print(f"Trust Score: {metadata['reputation']['trust_score']}")
```

## Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `service_id` | ✅ | Unique identifier (reverse-domain notation) |
| `version` | ✅ | Schema version, e.g. `1.0.0` |
| `service_name` | — | Human-readable name |
| `description` | — | What this service does (optimized for AI comprehension) |
| `pricing.model` | ✅ | `fixed`, `tiered`, or `dynamic` |
| `pricing.amount` | ✅ | Base price per call |
| `pricing.currency` | ✅ | `USD`, `CNY`, `USDC`, `ETH` |
| `pricing.estimated_total_cost` | — | Total including fees (provided by PayPack Cloud) |
| `performance.avg_latency_ms` | — | Average latency (24h) |
| `performance.success_rate` | — | Success rate 0-1 (24h) |
| `performance.p99_latency_ms` | — | 99th percentile latency (24h) |
| `quality.accuracy_score` | — | Output accuracy for AI/ML APIs |
| `quality.data_freshness_sec` | — | Max data staleness for data APIs |
| `reputation.trust_score` | ✅ | Composite score 0-100 (PayPack Cloud) |
| `reputation.total_calls_24h` | — | Total calls in last 24h |
| `reputation.dispute_rate` | — | Dispute ratio (30 days) |
| `reputation.uptime_pct` | — | Uptime percentage (30 days) |
| `policy.refund_policy` | — | `none`, `auto_on_fail`, `manual_review` |
| `policy.data_retention_days` | — | Data retention period |
| `policy.sla.uptime` | — | Committed uptime, e.g. `99.9%` |
| `policy.sla.max_latency_ms` | — | Maximum latency guarantee |
| `policy.sla.support_response_h` | — | Guaranteed support response time |
| `endpoints` | — | List of API endpoints |

## AI Agent Usage Example

```python
from paypack import AgentPay
from paypack.metadata import fetch_metadata, should_pay

pay = AgentPay(...)

# Fetch the service metadata
metadata = fetch_metadata("https://api.weather.com")

# AI agent makes an autonomous decision
should_pay, reason = should_pay(metadata, budget=0.01, min_trust_score=80)

if should_pay:
    receipt = pay.send(
        to=metadata["pricing"]["payment_address"],
        amount=metadata["pricing"]["estimated_total_cost"]
    )
    print(f"✅ Payment successful: {receipt.tx_hash}")
else:
    print(f"❌ Payment rejected: {reason}")
```

## Disclaimer

> **IMPORTANT:** This metadata is provided for **machine reference only**. PayPack Cloud calculates trust scores based on historical transaction data but makes no warranty regarding the accuracy or completeness of the information. AI agents should use this data as one factor among many in their decision-making process. PayPack is not a credit rating agency and does not provide financial advice.
