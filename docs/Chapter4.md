# Matrix-Matrix Multiplication

[![Chapter 4](Chapter4.png)](Chapter4_480p15.mp4)

**[Interactive Notebook](../notebooks/04_matrix_multiply.ipynb)**

## Summary

This chapter extends from vector operations to matrix-matrix multiplication for multi-hop path discovery:

- **Recall: Vector-Matrix Multiply** - Review of finding 1-hop neighbors using frontier vectors and adjacency matrices
- **Matrix-Matrix Multiply** - Computing A x A to discover 2-hop paths, with GraphBLAS syntax `mxm` and `@` operator
- **Multiplication Mechanics** - Step-by-step computation showing row-by-row multiplication and sparse optimization
- **Graph Interpretation** - How matrix entries translate to paths: direct edges vs multi-hop connections
- **Higher Powers** - Computing A², A³, and A^k for k-hop path counts
- **Diagonal Entries** - Understanding self-loops in powers as cycle counts (degree in A²)
- **Transitive Closure** - Finding all reachable pairs through iterative multiplication with ANY_PAIR semiring until fixed point
- **Applications** - Database query planning, network analysis, compiler optimization, and dependency resolution
- **Preview: Triangle Counting** - Introduction to using Hadamard product (A² ⊙ A) for detecting triangles
