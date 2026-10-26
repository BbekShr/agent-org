# Perf

## Method
1. **Measure before touching anything.** A perf claim without a number is a guess. Use the
   inspection tools in `/{{SLUG}}-verify`: a trace, a profile, timings over N runs (report the
   median and spread), bundle size, query count.
2. **Find the dominant cost** in the measurement. Fix that, not what looks slow in the code.
3. **One change at a time**, re-measuring after each.
4. **Prove it held:** same measurement, same conditions, before and after, in the report. A change
   that doesn't move the number gets reverted, however elegant it is.
5. **Guard it** where cheap: a budget, a query-count assertion, a size limit, so it can't regress
   silently.

## In this project
<!-- FILL: the real measurement commands (profiler, trace, bundle analyzer, query logging), the
     budgets that exist (size limits, timing targets), the hot paths, and the environment to
     measure in (never production). -->
