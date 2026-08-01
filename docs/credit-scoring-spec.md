# AI Agent Credit Scoring Standard

**Version:** v1.0.0-draft  
**Status:** 📌 DRAFT — Open for Community Feedback  
**Published:** 2026-08-01  
**Maintainer:** [PayPack](https://github.com/rhcjw/paypack-specs)

---

## 📄 One-Page Summary

### English

**Why:** AI agents are becoming economic actors — calling APIs, purchasing data, executing tasks. But there is no standard way to assess their trustworthiness. Reputation doesn't transfer across platforms.

**Our proposal:** A four-dimension credit scoring model for AI agent payment scenarios:

| Dimension | Weight | Measures |
|-----------|--------|----------|
| Payment Fulfillment Rate | 35% | Success rate of committed payments |
| Price Reasonableness | 25% | Whether prices fall within industry fair range |
| Transaction Stability | 20% | Regularity and predictability of behavior |
| Historical Reputation | 20% | Long-term accumulated evaluation |

**Score range:** 300–850  
**Trust tiers:** TRUSTED (740+) / VERIFIED (670–739) / BASIC (580–669) / UNVERIFIED (300–579)

**Complementary to:** ATEP, MeritScore, SwarmScore, IETF Trust Scoring

**Open for feedback** — This is a community-driven draft. Submit via [GitHub Issues](https://github.com/rhcjw/paypack-specs/issues).

### 中文

**为什么需要：** AI代理正在调用API、购买数据、执行任务。但如何判断一个AI代理是否值得信任？当前信誉无法跨平台携带，支付场景缺乏统一评估机制。

**我们的方案：** 面向AI代理支付场景的四维度征信评分模型：

| 维度 | 权重 | 核心衡量 |
|------|------|---------|
| 支付履约率 | 35% | 完成承诺支付的成功率 |
| 价格合理性 | 25% | 支付价格是否处于行业公允区间 |
| 交易稳定性 | 20% | 交易行为的规律性与可预测性 |
| 历史信誉 | 20% | 长期积累的综合评价 |

**评分范围：** 300–850  
**信任等级：** TRUSTED (740+) / VERIFIED (670+) / BASIC (580+) / UNVERIFIED (300-579)

**与现有标准互补：** ATEP、MeritScore、IETF Trust Scoring

**开放参与** — 目前为草案阶段，欢迎通过 GitHub 提交反馈。

---

## 1. Introduction

### 1.1 Background

With AI agents taking on increasingly important roles in the economy — from calling paid APIs and purchasing data services to executing complex tasks and completing settlements — a fundamental question remains unanswered:

**How do we determine if an AI agent is trustworthy?**

Currently, an agent's reputation cannot be carried across platforms; payment scenarios lack a standardized credit assessment mechanism; and merchants struggle to distinguish quality agents from high-risk ones. This "trust deficit" is constraining the healthy growth of the AI agent economy.

### 1.2 Purpose

This specification defines a credit scoring standard for AI agents, aiming to:

- Provide a unified, quantifiable method for credit assessment in payment scenarios
- Enable credit scores to be portable across platforms and verifiable
- Build trust infrastructure for the PayPack payment network and the broader AI agent economy

### 1.3 Scope

This specification covers:

- Dimension definitions and weight design for AI agent credit scoring
- Input data and calculation formulas
- Trust tier classification
- Query and verification interfaces
- Score update and decay mechanisms

This specification focuses on **payment-scenario credit assessment** for AI agents, not technical capability or general reputation systems.

---

## 2. Terms and Definitions

| Term | Definition |
|------|-----------|
| AI Agent | Autonomous software entity capable of making decisions and completing payments |
| Credit Score | Quantified assessment of an AI agent's creditworthiness, range 300-850 |
| Merchant | Entity providing services or goods to AI agents for payment |
| Payment Record | Single transaction data completed through PayPack |
| Price Deviation | Relative difference between actual payment and industry benchmark |
| Fulfillment Rate | Success rate of an AI agent completing promised payments |
| Scoring Period | Historical time window examined for scoring, default 90 days |
| Trust Tier | Trust level classification based on score range |

---

## 3. Scoring Model

### 3.1 Design Principles

- **Verifiability:** Scores must be based on auditable data
- **Portability:** Scores should transfer across platforms
- **Dynamism:** Scores decay over time, reflecting recent behavior
- **Transparency:** Dimensions and calculations are publicly documented
- **Economic Incentives:** Higher-credit agents receive lower barriers and better rates

### 3.2 Architecture

```
Credit Score = Σ(dimension_score_i × weight_i) × completeness_multiplier
Range: 300 – 850
```

---

## 4. Scoring Dimensions

### 4.1 Payment Fulfillment Rate (Weight: 35%)

Measures the reliability of an AI agent in fulfilling payment commitments.

```
Fulfillment Rate = successful_transactions / total_initiated_transactions
Period: past 90 days
```

| Fulfillment Rate | Dimension Score |
|------------------|-----------------|
| ≥ 98% | 95–100 |
| 95–98% | 85–94 |
| 90–95% | 70–84 |
| 80–90% | 50–69 |
| < 80% | 0–49 |

### 4.2 Price Reasonableness (Weight: 25%)

Measures whether an AI agent pays prices within the industry fair range.

```
Single Deviation = (actual_price - benchmark_price) / benchmark_price
Price Reasonableness Score = 100 - avg_deviation × penalty_coefficient
```

| Condition | Penalty |
|-----------|---------|
| Within fair range | 0 |
| Within 1.5× upper bound | -5 per 10% deviation |
| Beyond 1.5× upper bound | -15 per 10% deviation |

Benchmark prices are provided daily by PayPack Price Index Engine.

### 4.3 Transaction Stability (Weight: 20%)

Measures the regularity and predictability of AI agent transaction behavior.

```
Stability Score = 100 - (interval_stddev / avg_interval × 50)
```

| Coefficient of Variation | Stability |
|--------------------------|-----------|
| ≤ 0.3 | Excellent (90–100) |
| 0.3–0.6 | Good (70–89) |
| 0.6–1.0 | Fair (50–69) |
| > 1.0 | Poor (0–49) |

### 4.4 Historical Reputation (Weight: 20%)

Long-term accumulated evaluation based on account age, transaction volume, and user ratings.

```
Historical Score = min(100, base + activity_bonus + rating_bonus)
```

- Account age (30%): days active in network
- Transaction volume (30%): cumulative successful transactions
- User ratings (40%): average rating from service providers (1–5 ★ → 0–100)

### 4.5 Dimension Summary

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Payment Fulfillment Rate | 35% | Core reliability indicator |
| Price Reasonableness | 25% | Spending rationality |
| Transaction Stability | 20% | Behavioral predictability |
| Historical Reputation | 20% | Long-term accumulated trust |

---

## 5. Score Calculation

### 5.1 Composite Formula

```
Credit Score = 300 + (FulfillmentRate × 0.35 + PriceReasonableness × 0.25 + Stability × 0.20 + HistoricalReputation × 0.20) × 5.5
```

### 5.2 Completeness Multiplier

For new or low-volume agents, a completeness multiplier penalizes insufficient data:

| Valid Transactions | Multiplier |
|--------------------|------------|
| ≥ 50 | 1.00 |
| 20–49 | 0.85 |
| 10–19 | 0.70 |
| 5–9 | 0.50 |
| < 5 | 0.30 |

```
Final Score = floor(raw_score × completeness_multiplier)
```

### 5.3 Example

| Agent | Fulfillment | Price | Stability | Reputation | TX Count | Final Score |
|-------|-------------|-------|-----------|------------|----------|-------------|
| Agent A | 98% | 95 | 90 | 85 | 200 | 812 |
| Agent B | 92% | 70 | 75 | 60 | 45 | 658 |
| Agent C | 85% | 50 | 60 | 40 | 8 | 486 |
| Agent D (new) | — | — | — | 40 | 2 | 349 |

---

## 6. Trust Tiers

| Tier | Score Range | Description | Payment Limits |
|------|-------------|-------------|----------------|
| **TRUSTED** | 740–850 | Highly trusted | No single/batch limit |
| **VERIFIED** | 670–739 | Good record | ≤ $500/tx, ≤ $2,000/day |
| **BASIC** | 580–669 | Acceptable, monitor | ≤ $100/tx, ≤ $500/day |
| **UNVERIFIED** | 300–579 | New or risky | ≤ $20/tx, ≤ $100/day |

### Promotion Path

| Path | Condition |
|------|-----------|
| UNVERIFIED → BASIC | 10+ successful transactions, score ≥ 580 |
| BASIC → VERIFIED | 50+ successful transactions, Ed25519 key binding, score ≥ 670 |
| VERIFIED → TRUSTED | 200+ successful transactions, score ≥ 740 |

---

## 7. Data Input Specification

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| agent_id | string | Unique agent identifier | PayPack |
| merchant_id | string | Unique merchant identifier | PayPack |
| transaction_amount | decimal | Payment amount | Payment logs |
| service_code | string | Service type code | Payment logs |
| transaction_status | enum | SUCCESS / FAILED / REFUNDED | Payment logs |
| transaction_time | timestamp | Transaction timestamp | Payment logs |
| user_rating | decimal | User rating (1–5) | User feedback |
| benchmark_price | decimal | Industry benchmark | Price Index Engine |

---

## 8. Score Update & Decay

### 8.1 Update Frequency

- **Daily:** Full recalculation every UTC 00:00
- **Real-time:** Incremental update after each transaction

### 8.2 Time Decay

```
decay_weight = e^(-λ × days), λ = 0.01
```

| Age | Weight |
|-----|--------|
| 0–30 days | 1.0 |
| 31–60 days | 0.7 |
| 61–90 days | 0.4 |
| > 90 days | 0.1 |

### 8.3 Dormancy Decay

After 30 consecutive days without transactions, score decreases by 5 points monthly (max reduction: 50).

---

## 9. Query & Verification API

### 9.1 Query

```
GET /v1/credit/score/{agent_id}
```

Response:

```json
{
  "agent_id": "agent_abc123",
  "score": 742,
  "tier": "TRUSTED",
  "dimensions": {
    "fulfillment_rate": 96,
    "price_reasonableness": 88,
    "stability": 92,
    "historical_reputation": 78
  },
  "sample_count": 156,
  "last_updated": "2026-08-01T00:00:00Z"
}
```

### 9.2 Verification

```
GET /v1/credit/verify/{agent_id}
```

Returns signed score data for third-party verification.

---

## 10. Security & Privacy

- Scores use anonymized transaction data only
- Raw transaction details are not exposed via the public API
- Users may opt out at any time
- Anti-manipulation: volume weighting, reviewer reputation weighting, anomaly detection

---

## 11. Versioning & Governance

### 11.1 Versioning

Semantic versioning: MAJOR.MINOR.PATCH

- MAJOR: incompatible scoring model changes
- MINOR: backward-compatible dimension/weight changes
- PATCH: documentation fixes

### 11.2 Governance

| Phase | Model |
|-------|-------|
| **Current** | PayPack as maintainer, collecting community feedback |
| **Target** | Technical committee with early adopters |
| **Vision** | Submit to IETF or W3C standardization |

---

## Appendix A: Relationship to Existing Standards

| Standard | Relationship |
|----------|-------------|
| ATEP | Complementary — ATEP focuses on execution passport, this spec focuses on payment credit scoring |
| MeritScore | Complementary — MeritScore targets on-chain DeFi, this spec targets general AI payment |
| SwarmScore | Complementary — SwarmScore emphasizes technical execution, this spec emphasizes payment behavior |
| IETF Trust Scoring | Reference — dimension design aligns with IETF five-dimensional model |

---

> 📌 **This specification is currently in DRAFT and open for community feedback.**  
> 💬 Submit feedback via [GitHub Issues](https://github.com/rhcjw/paypack-specs/issues) or Pull Requests.  
> 📧 Contact maintainers: [GitHub](https://github.com/rhcjw)
