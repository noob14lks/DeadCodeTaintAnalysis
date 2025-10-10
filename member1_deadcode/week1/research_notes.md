# Dead Code Detection Research Notes

## Static Analysis
- Using AST to parse code and identify all defined functions and classes.
- Identifying function calls statically is challenging due to dynamic nature of Python.
- Can track references inside code to guess usage.

## Dynamic Analysis
- Running code with instrumentation to log which functions/classes get executed.
- Requires test cases or execution traces, which may be unavailable.

## Challenges
- Dynamic languages like Python have runtime features (dynamic imports, decorators).
- False positives can occur if functions are called indirectly (e.g., via `getattr`).

## Planned Approach
- Start with static extraction of all functions/classes.
- Collect usage data by manually labeling or dynamic tracing.
- Train ML classifier to predict unused code based on features like function length, name, call frequency.