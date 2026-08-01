# Contributing to PayPack Specifications

Thanks for your interest in contributing to the PayPack Specifications repository! 🎉

## How to Contribute

### 1. Feedback & Discussion

For general feedback, questions, or ideas:
- 📣 Open a **[GitHub Discussion](https://github.com/rhcjw/paypack-specs/discussions)**
- 🐛 Report issues via **[GitHub Issues](https://github.com/rhcjw/paypack-specs/issues)**

### 2. Proposing Changes

1. **Fork** this repository
2. **Create a branch** for your changes:
   ```bash
   git checkout -b proposal/my-change
   ```
3. **Make your changes** — keep them focused and minimal
4. **Submit a Pull Request (PR)** with:
   - A clear title (e.g., `feat: add PVI calculation example`)
   - A description explaining what and why
   - Reference to any related Issue or Discussion
5. **Wait for review** — a maintainer will provide feedback

### 3. Pull Request Guidelines

- ✅ One PR = one logical change
- ✅ Keep discussions civil and constructive
- ✅ Update or add documentation if your change affects the spec
- ✅ Ensure CI checks pass (`validate.yml` will run automatically)

### 4. Specification Change Process

For changes to specifications (files in `specs/`, `schemas/v1/`):

1. Open a **[Discussion](https://github.com/rhcjw/paypack-specs/discussions)** to propose the idea
2. Gather community feedback (minimum 5 business days)
3. If consensus is reached, submit a PR with the change
4. The PR must include:
   - The spec change itself
   - Updated examples (if applicable)
   - A note in the spec's "Changelog" section (if one exists)

### 5. Code of Conduct

- Be respectful and inclusive
- Assume good intent
- Focus on the idea, not the person

## 规范对齐声明

本仓库中的 JSON Schema（`schemas/v1/*.json`）为权威定义，SQL 文件（`schemas/v1/*.sql`）为参考实现。若两者存在数值或权重差异，以 JSON Schema 为准。发现矛盾请提交 [Issue](https://github.com/rhcjw/paypack-specs/issues)。

## License

By contributing, you agree that your contributions will be licensed under the [Apache 2.0 License](LICENSE).
