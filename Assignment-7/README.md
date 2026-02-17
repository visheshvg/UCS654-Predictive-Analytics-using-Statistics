# Sampling Techniques and Model Performance Comparison

## Objective

The objective of this assignment is to apply different statistical sampling techniques on a credit card transaction dataset and evaluate how these sampling strategies influence the performance of various machine learning models.

---

## Dataset Description

The dataset contains 772 observations with 30 numerical features and a binary target variable `Class`.

Original class distribution:

- Class 0 (Non-Fraud): 763
- Class 1 (Fraud): 9

The dataset is highly imbalanced. Since the minority class contained only 9 samples, undersampling would have reduced the dataset to a very small size, making model evaluation unreliable.

Therefore, **minority class oversampling (with replacement)** was performed to match the size of the majority class.  

After balancing:

- Class 0: 763  
- Class 1: 763  
- Total samples: 1526  

This balanced dataset was used for all further sampling and modeling.

---

## Sampling Techniques Applied

Five statistical sampling techniques were implemented:

### 1. Simple Random Sampling
A random subset of 70% of the balanced dataset was selected where each observation had equal probability of being chosen.

### 2. Systematic Sampling
Every k-th observation was selected from the dataset based on a fixed sampling interval.

### 3. Stratified Sampling
The dataset was divided based on the target class, and proportional samples were drawn from each class to preserve class distribution.

### 4. Cluster Sampling
The dataset was divided into clusters based on transaction amount (using quantile-based grouping), and selected clusters were used as the sample.

### 5. Convenience Sampling
The first 70% of the dataset was selected as the sample for simplicity.

Each sampling technique used approximately 70% of the balanced dataset.

---

## Machine Learning Models Used

Five machine learning models were trained and evaluated:

- Logistic Regression  
- Decision Tree  
- Random Forest  
- K-Nearest Neighbors (KNN)  
- Support Vector Machine (SVM)  

A 70-30 train-test split was applied to each sample. Model performance was evaluated using **Accuracy**.

---

## Results

| Model               | Simple Random | Systematic | Stratified | Cluster | Convenience |
|---------------------|--------------|------------|------------|---------|-------------|
| Logistic Regression | 0.9564 | 0.8974 | 0.9128 | 0.9564 | 0.9346 |
| Decision Tree       | 0.9907 | 0.9934 | 0.9782 | 0.9927 | 0.9875 |
| Random Forest       | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| KNN                 | 0.9813 | 0.9869 | 0.9595 | 0.9782 | 0.9751 |
| SVM                 | 0.6885 | 0.7118 | 0.7196 | 0.8764 | 0.7103 |

---

## Visualization

A heatmap was generated to visually compare model accuracies across the five sampling techniques.

![Sampling Heatmap](sampling_heatmap.png)

The heatmap provides a clear representation of performance consistency and highlights the variation across sampling strategies.

---

## Observations

- **Random Forest** achieved perfect accuracy across all sampling methods. This suggests strong model capacity and robustness on the balanced dataset.
- **Decision Tree** also performed consistently well under all sampling techniques.
- **Logistic Regression and KNN** showed stable performance under most sampling strategies.
- **SVM** performed comparatively lower, likely due to sensitivity to hyperparameters and lack of feature scaling.
- Simple Random and Cluster sampling produced slightly more consistent results across models.

---

## Conclusion

This study demonstrates that sampling techniques can influence machine learning model performance. While ensemble-based models such as Random Forest showed robustness across all sampling methods, simpler models exhibited some variation depending on how the data was sampled.

Balancing the dataset using oversampling ensured meaningful training and evaluation. Among the tested models, ensemble methods performed the most consistently, indicating their effectiveness in classification tasks involving previously imbalanced data.

The experiment highlights the importance of selecting appropriate sampling strategies before model training, especially when dealing with skewed datasets.
