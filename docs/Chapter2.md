# Semirings and Accumulation

[![Chapter 2](Chapter2.png)](Chapter2_480p15.mp4)

**[Interactive Notebook](../notebooks/02_semirings.ipynb)**

## Summary

This chapter explores how semirings customize matrix multiplication for different problems:

- **PLUS_TIMES Semiring** - Standard arithmetic for computing total costs, such as manufacturing production costs
- **MIN_PLUS Semiring** - Finding shortest paths by adding distances and keeping the minimum, used in routing and navigation
- **ANY_PAIR Semiring** - Testing reachability and connectivity without computing actual values, enabling early termination
- **Semiring Comparison** - How the same matrix structure produces different results depending on the chosen semiring
- **Common Semirings** - Reference table of PLUS_TIMES, MIN_PLUS, MAX_PLUS, ANY_PAIR, and PLUS_PAIR with their use cases
- **Accumulation** - How new results combine with existing data using accumulators (replacement, PLUS, MIN)
- **Single Source Shortest Path** - Complete algorithm demonstration using MIN_PLUS semiring with MIN accumulator, showing step-by-step convergence
