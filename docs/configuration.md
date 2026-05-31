# Configuration

OSS Maintainer Kit works without configuration. Add `omk.toml` at the repository root when a project wants a custom audit gate or rule weights.

## Example

```toml
min_score = 90

[rule_weights]
readme-depth = 14
license = 12
tests = 12
ci = 10
package-manifest = 10
contributing-guide = 9
issue-template = 8
pr-template = 8
changelog = 8
security-policy = 9
```

## Fields

- `min_score`: default threshold used by `omk audit` when `--min-score` is not supplied.
- `[rule_weights]`: optional integer weights keyed by rule ID. Missing rule IDs keep their built-in defaults.

Command-line thresholds still take precedence:

```bash
omk audit . --min-score 95
```
