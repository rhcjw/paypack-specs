# PVM Risk Level Assessment Rules (v1.0)

**Status:** Active | **Version:** 1.0 | **Date:** 2026-08-02

---

The `risk_level` field in `value-metadata.json` is a composite assessment derived from three core signals:

1. **Trust Score (`trust_score`)** from `credit-score.json`
2. **Price Fairness** from `price-index.json` (`benchmark`, `fair_upper`)
3. **Feedback Confidence** from `value-metadata.json` (`feedback_aggregate.confidence`)

---

## Assessment Rules

| Risk Level | Condition |
| :--- | :--- |
| `BLOCKED` | 1. `trust_score` < 50, OR<br>2. The quoted price exceeds 200% of `fair_upper`, OR<br>3. The merchant has a `dispute_rate` > 0.5 (50%) |
| `HIGH` | 1. `trust_score` is between 50-70, OR<br>2. The quoted price exceeds 100% of `fair_upper` (but ≤ 200%), OR<br>3. `feedback_aggregate.confidence` < 0.6 |
| `MEDIUM` | 1. `trust_score` is between 70-85, OR<br>2. `sample_count` < 30 (indicating statistically weak confidence) |
| `LOW` | 1. `trust_score` ≥ 85, AND<br>2. `sample_count` ≥ 30, AND<br>3. No other `HIGH`/`BLOCKED` conditions are met |

---

## Supplementary Rules

### sample_count Minimum Threshold

- `sample_count` ≥ 30: Price index is considered statistically reliable.
- `sample_count` < 30: Price index is generated but marked with `MEDIUM` risk. Consumers should treat benchmark values with caution.
- `sample_count` = 0: No price index available. `risk_level` defaults to `MEDIUM` until sufficient data accumulates.

### confidence Calculation

`feedback_aggregate.confidence` (0-1) is calculated as:

```
confidence = min(1.0, raw_confidence × time_decay)

raw_confidence = 1 - (1 / (1 + sqrt(total_reviews)))

time_decay = e^(-λ × days_since_last_review), λ = 0.01
```

- < 10 reviews → confidence is inherently low due to `raw_confidence` formula
- > 100 reviews + recent activity → confidence approaches 1.0
- Reviews older than 90 days carry negligible weight due to time decay

### dispute_rate

`dispute_rate` is calculated as:

```
dispute_rate = disputed_transactions / total_transactions (last 30 days)
```

A `dispute_rate` > 0.5 (50%) triggers `BLOCKED` regardless of other scores.

---

## Implementation Notes

- Risk assessment runs before every payment via the PVM overlay.
- The `BLOCKED` level is a hard stop — the payment MUST NOT proceed.
- `HIGH` triggers a warning that the AI agent or user must explicitly override.
- `MEDIUM` is informational — payment proceeds with a caution flag.
- `LOW` means all signals are green — payment proceeds normally.

---

*This document is part of the [PayPack Value Metadata Specification](../README.md).*
