import sys
import os
import pandas as pd
import numpy as np

def topsis(input_file, weights, impacts, output_file):
    # Read CSV
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        raise FileNotFoundError("Input file not found")

    if df.shape[1] < 3:
        raise ValueError("Input file must contain three or more columns")

    data = df.iloc[:, 1:].values

    # Check numeric data
    if not np.issubdtype(data.dtype, np.number):
        raise ValueError("Columns from 2nd to last must contain numeric values only")

    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')

    if len(weights) != data.shape[1]:
        raise ValueError("Number of weights must be equal to number of criteria")

    if len(impacts) != data.shape[1]:
        raise ValueError("Number of impacts must be equal to number of criteria")

    for impact in impacts:
        if impact not in ['+', '-']:
            raise ValueError("Impacts must be either + or -")

    # Normalize the matrix
    norm = np.sqrt((data ** 2).sum(axis=0))
    normalized_data = data / norm

    # Weighted normalized matrix
    weighted_data = normalized_data * weights

    # Ideal best and worst
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted_data[:, i].max())
            ideal_worst.append(weighted_data[:, i].min())
        else:
            ideal_best.append(weighted_data[:, i].min())
            ideal_worst.append(weighted_data[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Distance calculation
    dist_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # Topsis score
    scores = dist_worst / (dist_best + dist_worst)

    df['Topsis Score'] = scores
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

    df.to_csv(output_file, index=False)

def main():
    if len(sys.argv) != 5:
        print("Usage: topsis <input_file> <weights> <impacts> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    try:
        topsis(input_file, weights, impacts, output_file)
        print("TOPSIS analysis completed successfully.")
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()

