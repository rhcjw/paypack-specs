# PVM Trust Score Methodology (v1.0)

**Status:** Active | **Version:** 1.0 | **Date:** 2026-08-02

---

The PayPack `trust_score` is a composite metric from 0-100, derived from a three-dimensional weighted model. It appears in `credit-score.json` (normalized to 300-850 for the merchant credit score) and `ai-service-metadata.json` (raw 0-100 for service evaluation).

---

## 1. Price Integrity (40% weight)

**Input**: Historical transaction prices compared against the Price Index benchmark.

**Calculation**:
```
price_integrity_score = 100 × (1 - avg|price_deviation|)
```

Where:
```
price_deviation = (quoted_price - benchmark_price) / benchmark_price
```
Evaluation window: past 30 days. Average absolute deviation is capped at 1.0 (100%).

A merchant quoting exactly at the benchmark price achieves a perfect score of 100. A merchant consistently charging 50% above benchmark receives a score of 50.

---

## 2. Fulfillment Rate (30% weight)

**Input**: Historical transaction data from PayPack Cloud.

**Calculation**:
```
fulfillment_score = 100 × (successful_transactions / total_transactions)
```

A "successful" transaction is defined as one where:
- The service was delivered as described
- No refund was claimed within the protection period (default: 7 days)
- No dispute was filed by the buyer

Evaluation window: past 90 days. Transactions older than 90 days are weighted at 0.1 per the time decay formula.

---

## 3. User Rating (30% weight)

**Input**: Aggregated user feedback from `feedback_aggregate` in `value-metadata.json`.

**Calculation**: Weighted average of star ratings (1-5), using Bayesian adjustment to prevent small-sample bias:

```
user_rating_score = 100 × ( (bayesian_avg_rating - 1) / 4 )
```

Bayesian adjustment formula:
```
bayesian_avg_rating = (C × m + Σratings) / (C + n)

Where:
  C = minimum reviews for confidence (default: 10)
  m = prior mean (default: 3.0, neutral rating)
  n = actual number of reviews
  Σratings = sum of all individual ratings
```

This ensures a service with 5 stars from 2 reviews doesn't outrank one with 4.5 stars from 200 reviews.

---

## Final Score Calculation

```
trust_score = 0.4 × price_integrity_score
            + 0.3 × fulfillment_score
            + 0.3 × user_rating_score
```

The score is rounded to the nearest integer, clamped to [0, 100].

For `credit-score.json` merchant scoring, this 0-100 score is mapped to 300-850:
```
credit_score = 300 + trust_score × 5.5
```

---

## Data Source and Verification

- **Calculation methodology**: Fully open-source and community-verifiable.
- **Raw transaction data**: Managed and encrypted by PayPack Cloud to prevent manipulation. The raw data underpinning each score is not publicly exposed to protect merchant privacy and prevent gaming.
- **Future direction**: Exploring decentralized oracle solutions for v2.0 to further reduce trust assumptions.

This approach — "verifiable transparent trust" — ensures anyone can audit the formula, while the underlying data remains secured against manipulation. It is analogous to how credit bureaus publish their scoring methodology but do not expose individual credit histories.

---

*This document is part of the [PayPack Value Metadata Specification](../README.md).*
