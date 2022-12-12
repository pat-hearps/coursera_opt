For working on assignments for Coursera / UniMelb Discrete Optimisation course
https://www.coursera.org/learn/discrete-optimization

Assignments go in their own directory each under `/assignments` dir. But the following which would go in each assignment dir are gitignored:
- `data/`
- `handout.pdf`
- `_coursera` submission credentials (plain text file in each assignment directory)

To be clear, intended directory layout is:

```
- assignments/
  - a01_anyint/
  - a02_knapsack/
    - solver.py (solution file)
    - submit.py (from course)
    - _coursera (plain text file, gitignored)
    - handout.pdf (gitignored)
    - data/ (gitignored)
      - ks_4_0
      - ks_19_0
      - ... etc
    - notebooks/ (gitignored)

```

