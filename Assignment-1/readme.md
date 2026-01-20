# Assignment 1 – Learning Probability Density Function

## Objective
The objective of this assignment is to understand probability density functions by learning the parameters of a non-linear transformed random variable based on a roll-number-specific equation.

## Dataset Description
The dataset contains air quality measurements across India. In this assignment, only NO2 concentration values are used as the feature.

## Methodology

### Step 1: Data Preprocessing
Rows with missing NO2 values were removed to maintain numerical stability.

### Step 2: Non-linear Transformation
Each NO2 value (x) was transformed using the roll-number-based function:

z = x + 0.05 sin(1.5x)

This step introduces controlled non-linearity into the data.

### Step 3: PDF Parameter Estimation
The transformed data was assumed to follow a Gaussian-like distribution:

p̂(z) = c · exp(-λ(z − μ)²)

The parameters were estimated as follows:
- μ was computed as the mean of z
- λ was computed using the variance of z
- c was derived to ensure normalization of the PDF

This approach is based on maximum likelihood estimation principles.

## Results
The learned parameters are summarized in the table below:

| Parameter | Value |
|-----------|-------|
| μ         | 21.4500 |
| λ         | 0.002205 |
| c         | 0.026495 |

## Visualization
A histogram of the transformed variable z was plotted along with the estimated probability density function. The close alignment between the histogram and the PDF indicates a good fit.

## Conclusion
The experiment demonstrates how a simple transformation affects the underlying distribution and how probability density parameters can be learned analytically from data.
