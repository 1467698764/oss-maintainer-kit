# Scoring Model

Each rule has a weight. The final score is:

```text
round(sum(passed rule weights) / sum(all rule weights) * 100)
```

Failed rules are prioritized by severity, weight, and rule ID. This keeps recommendations stable and focused on the highest-impact missing maintenance signals.

## Grades

| Grade | Range | Meaning |
| --- | --- | --- |
| `excellent` | 90-100 | Ready for public collaboration. |
| `healthy` | 75-89 | Solid foundation with a few gaps. |
| `needs-work` | 50-74 | Useful project, but contributors need more guidance. |
| `starter` | 0-49 | Early repository that should add basics before promotion. |
