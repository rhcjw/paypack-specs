# PayPack Credit System — 信用与价格指数

> **开源部分：Schema + 计算公式 + SDK。评分权重与反作弊规则由 PayPack Cloud 管埋。**

## Overview

PayPack 信用系统让 AI Agent 在支付前判断两件事：

1. **敢不敢付** — 商户信不信得过？（credibility）
2. **值不值付** — 价格是否合理？（price fairness）

前者由 `merchant_risk_score` 的 trust_score 回答，后者由 `price_index_daily` 的 fair_range 回答。

## Architecture

```
AI Agent 调 API
    │
    ├──→ PayPack.pay()
    │       │
    │       ├──→ price_guard.check()  ← ← ←  价格指数引擎
    │       │       ├─ price OK → 放行
    │       │       ├─ price high → 告警但放行
    │       │       └─ price abnormal → 拦截
    │       │
    │       └──→ 执行支付
    │
    └──→ 用户反馈（1-5星 + 截图）
            │
            └──→ AI 核验 → 更新 merchant_risk_score
```

## Data Tables

| Table | Purpose | Open Source |
|-------|---------|-------------|
| `price_index_daily` | 每日基准价 + 公允区间 | ✅ Schema |
| `merchant_risk_score` | 商户信用分 + 价格诚信分 | ✅ Schema |
| `user_feedback` | 用户众包评分 | ✅ Schema |
| `service_type_dict` | 服务类型字典 | ✅ Schema |

See [schemas/v1/price-index.sql](../schemas/v1/price-index.sql) for the full DDL.

## Calculation Formula

### 公允价格区间 (Fair Price Range)

Uses Tukey's fences:

```
IQR = P75 - P25
fair_lower = max(0, P25 - 1.5 × IQR)
fair_upper = P75 + 1.5 × IQR
```

### 价格波动指数 (PVI)

```
PVI = (今日基准价 - N日前基准价) / N日前基准价 × 100%
```

| PVI | Level | Action |
|-----|-------|--------|
| < 5% | Stable | Normal |
| 5-15% | Mild | Watch trend |
| 15-30% | High | Deep analysis |
| > 30% | Extreme | Auto alert |

### 商户价格诚信分

```
Price Integrity Score =
  60% × (1 - avg|price_deviation|) +
  40% × avg(user_price_fairness_rating) / 5 × 100
```

| Score | Label |
|-------|-------|
| 90-100 | 🟢 价格良心 |
| 70-89 | 🟡 定价合理 |
| 50-69 | 🟠 略有偏高 |
| 0-49 | 🔴 严重偏离，纳入观察名单 |

## Integration

### Price Guard Hook

```python
from price_guard import check_price_sync

result = check_price_sync("bid_data_query", amount=0.50, merchant_id="m001")
if not result.allowed:
    return {"error": "PRICE_BLOCKED", "message": result.message}
# ... proceed with payment ...
```

See [examples/price_guard.py](../examples/price_guard.py) for the full example.

### Price Advice API (AI Agent SDK)

```python
# AI Agent queries before paying
advice = paypack.get_price_advice("bid_data_query", merchant_id="m001")
# Returns: {"benchmark": 0.50, "fair_range": [0.35, 0.65], "level": "normal"}
```

## What's Closed Source

- `trust_score` calculation weights — specific model parameters and feature engineering
- Anti-fraud rules — detection thresholds for wash trading, fake reviews
- Raw transaction data — historical payment database on PayPack Cloud

These are PayPack Cloud's competitive moat. The open-source Schema and formulas ensure transparency so the community can verify the methodology.

## Disclaimer

Credit scores and price indices are provided for **machine reference only**. PayPack Cloud makes no warranty regarding accuracy or completeness. AI agents should use this data as one factor among many.
