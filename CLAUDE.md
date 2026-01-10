# CLAUDE.md

This is a Windmill project containing flows and scripts for personal automation.

## Windmill Documentation

For understanding Windmill concepts, syntax, and capabilities, refer to the official documentation:
- https://www.windmill.dev/docs

Key concepts:
- **Flows**: Multi-step workflows defined in `flow.yaml` files
- **Scripts**: Inline scripts (Python, TypeScript/Deno, etc.) referenced with `!inline` in flows
- **Resources**: External connections (databases, APIs) referenced with `$res:path/to/resource`
- **Variables**: Referenced with `$var:path/to/variable`
- **Input transforms**: JavaScript expressions to wire step outputs to inputs (e.g., `results.step_id.field`)

## Project Structure

```
f/
  perso/           # Personal workspace
    *.flow/        # Flow directories containing flow.yaml and inline scripts
```

## Common Patterns

- Flow inputs accessed via `flow_input.field_name`
- Previous step results accessed via `results.step_id.output` (for AI agents) or `results.step_id.field`
- Resources loaded with `resource('path/to/resource')`
