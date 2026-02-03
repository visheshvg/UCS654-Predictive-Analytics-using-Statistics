import pandas as pd
import numpy as np

def topsis(input_file, weights, impacts, output_file):
    df = pd.read_csv(input_file)

    if df.shape[1] < 3:
        raise ValueError("Input file must have at least 3 columns")

    data = df.iloc[:, 1:].values
    weights = list(map(float, weights.split(",")))
    impacts = impacts.split(",")

    if len(weights) != data.shape[1]:
        raise ValueError("Weights count must match criteria count")

    if len(impacts) != data.shape[1]:
        raise ValueError("Impacts count must match criteria count")

    for i in impacts:
        if i not in ["+", "-"]:
            raise ValueError("Impacts must be + or -")

    # Normalization
    norm = np.sqrt((data ** 2).sum(axis=0))
    norm_data = data / norm

    # Weighted
    weighted = norm_data * weights

    ideal_best = []
    ideal_worst = []

    for i, imp in enumerate(impacts):
        if imp == "+":
            ideal_best.append(weighted[:, i].max())
            ideal_worst.append(weighted[:, i].min())
        else:
            ideal_best.append(weighted[:, i].min())
            ideal_worst.append(weighted[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    d_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    d_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = d_worst / (d_best + d_worst)

    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)

    df.to_csv(output_file, index=False)
