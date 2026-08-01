# PayPack Value Metadata Specification (PVM)

**The Valuation & Trust Overlay for Agentic Payments**

PVM defines how AI agents, merchants, and payment facilitators express and consume *value signals* during agentic payments:

- 📊 **Price Index**: is this price fair?
- 🛡️ **Credit Score**: is this merchant trustworthy?
- ⭐ **Feedback Aggregate**: what do other buyers say?
- 🚦 **Risk Level**: should this payment be allowed?

**PVM sits ON TOP of x402 / AP2 / Alipay / WeChat.**  
It does NOT replace payment protocols — it enriches them with machine-readable trust signals.

> x402 V2 defines `maxAmountRequired` in the 402 response — but doesn't answer "is this amount reasonable?"  
> PVM fills this gap as a protocol-agnostic valuation overlay.

## 📄 Current Specifications

### 1. PVM Core (JSON Schema) 🆕
- **Status**: Active (v0.1.0)
- **Scope**: Core Value Metadata structure — embeds price index, credit score, and feedback into x402/AP2 payment responses.
- **Files**:
  - [`/schemas/v1/value-metadata.json`](./schemas/v1/value-metadata.json) — Core PVM schema
  - [`/schemas/v1/price-index.json`](./schemas/v1/price-index.json) — Price index sub-schema
  - [`/schemas/v1/credit-score.json`](./schemas/v1/credit-score.json) — Credit score sub-schema

### 2. AI Agent Credit Scoring Standard v1.0-draft
- **Status**: Draft / Community Feedback
- **Scope**: Defines a four-dimensional credit scoring model (300-850) for AI agents in payment scenarios.
- **File**: [`/specs/credit-scoring-spec.md`](./specs/credit-scoring-spec.md)

### 3. Service Metadata Schema (JSON Schema)
- **Status**: Active
- **Scope**: Standardized metadata for AI service evaluation (pricing, performance, reputation, SLA).
- **File**: [`/schemas/v1/ai-service-metadata.json`](./schemas/v1/ai-service-metadata.json)

### 4. Price Index SQL Schema
- **Status**: Active
- **Scope**: DDL for price index engine, merchant credit scoring, and user feedback tables.
- **File**: [`/schemas/v1/price-index.sql`](./schemas/v1/price-index.sql)

## 🧪 Examples

- [x402 402 Response with PVM embedded](./examples/x402-pvm-integration.example.json) 🆕 — Shows how x402 V2 payment response carries PVM trust signals
- [Price Guard Hook](./examples/price_guard.py) — Fail-open price check before payment
- [Schema Validator](./examples/validate_schema.py) — Python validator for service metadata
- [Weather API](./examples/weather-api.example.json) / [Top-Up Service](./examples/topup-service.example.json)

## 🗺️ Roadmap
- [x] Service Metadata Schema (v1.0)
- [x] Price Index + Credit Score JSON Schemas (v0.1.0) 🆕
- [x] x402 V2 + PVM integration example 🆕
- [x] Price Index SQL Schema (v1.0)
- [x] Credit Scoring Standard Draft (v1.0-draft)
- [ ] Price Index Methodology Specification — *Q3 2026*
- [ ] Trust Protocol Interoperability Standard — *Q4 2026*

## 🤝 Contributing
This is a community-driven effort. We welcome feedback, issues, and pull requests from developers, platforms, and researchers across the AI and payments ecosystem.

See **[CONTRIBUTING.md](./CONTRIBUTING.md)** for guidelines.

1. Read the [draft specification](./specs/credit-scoring-spec.md)
2. Open an [Issue](https://github.com/rhcjw/paypack-specs/issues) for feedback
3. Submit a [Pull Request](https://github.com/rhcjw/paypack-specs/pulls) for improvements
4. Join the [Discussions](https://github.com/rhcjw/paypack-specs/discussions)

## 📧 Contact
Maintainer: [rhcjw](https://github.com/rhcjw)

---

*Together, let's build the trust layer for AI agent payments.* 🛡️
