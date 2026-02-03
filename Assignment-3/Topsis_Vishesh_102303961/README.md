# TOPSIS Command Line Package

This package implements the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) method to rank alternatives based on multiple criteria.

---

## Usage

topsis input.csv "1,1,1,1,2" "+,+,-,+,+" output.csv

- First column in input file represents alternatives
- Remaining columns represent criteria values (numeric only)

---

## Methodology

1. Read decision matrix from CSV file
2. Normalize criteria values
3. Apply weights to normalized matrix
4. Determine ideal best and ideal worst based on impacts
5. Calculate distance from ideal solutions
6. Compute TOPSIS score
7. Rank alternatives (Rank 1 is best)

---

## Output

The output CSV file contains:
- Original input data
- Topsis Score
- Rank

Higher TOPSIS score indicates a better alternative.

---

## Results Visualization

Results can be visualized using a bar graph of Topsis Score versus alternatives.
Higher bars indicate better-ranked alternatives.

---

## Author

Vishesh (Roll No: 102303961)
