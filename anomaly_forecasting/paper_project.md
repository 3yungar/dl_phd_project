# Modeling and Evaluation of Models for Outlier Forecasting in Time Series

## Stage 1: Modeling in Classical Machine Learning

### Classical Machine Learning Models

- **Logistic Regression**: Used for binary classification with class balancing.
- **Support Vector Machine (SVM)**: Uses probabilistic predictions and class balancing.
- **Random Forest**: An ensemble of decision trees with class balancing.
- **XGBoost**: Gradient boosting of decision trees with class weight adjustment for imbalance.
- **LightGBM**: Gradient boosting with class balancing and efficient training.
- **CatBoost**: Gradient boosting optimized for categorical data, with class weights.

## Stage 2: Model Training and Evaluation

### Simple LSTM Network

- **Architecture**: Multiple LSTM layers followed by dense layers for classification.
- **Training**: On the task of predicting 30 steps ahead or directly on the classification task.

### LSTM Autoencoder

- **Architecture**: Encoder and decoder based on LSTM.
- **Training**: On the task of time series reconstruction.
  - Using reconstruction errors for anomaly classification or using latent representations for subsequent classifier training.

### Combination of LSTM Autoencoder and Separate LSTM Network

- **Architecture**: Encoder for compression, followed by a separate LSTM network for prediction or classification.
- **Training**: Two-stage — first the autoencoder, then the LSTM predictor.

### Variational Autoencoder (VAE)

- **Architecture**: Encoder and decoder with a variational approach.
- **Training**: On the reconstruction task with probabilistic modeling.
  - Using reconstruction errors or latent representations for anomaly classification.

## Stage 3: Performance Evaluation and Comparison

### Metrics

- **For anomaly classification**:

### Accuracy
$$
Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
$$

### Recall
$$
Recall = \frac{TP}{TP + FN}
$$

### Precision
$$
Precision = \frac{TP}{TP + FP}
$$

### F1 Score
$$
F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}
$$

These metrics are used to evaluate the quality of binary classification, where:
- \( TP \) — True Positives
- \( TN \) — True Negatives
- \( FP \) — False Positives
- \( FN \) — False Negatives

 - **ROC-AUC**: Area under the ROC curve, evaluating the quality of binary classification.


$$
\text{ROC-AUC} = \int_0^1 \text{TPR}(\text{FPR}) \, d(\text{FPR})
$$

Where:
- **TPR** (True Positive Rate) = \( \frac{TP}{TP + FN} \) — also known as **Recall**.
- **FPR** (False Positive Rate) = \( \frac{FP}{FP + TN} \) — the rate of false positives compared to all actual negatives.

ROC-AUC is used to assess the ability of a classifier to distinguish between the positive and negative classes. A value closer to 1 indicates a better model, while a value around 0.5 suggests random guessing.

### Visualization

- **ROC curves** to assess the trade-off between recall and precision.

## Stage 4: Additional Alternatives and Recommendations

### 1. Transformer-Based Models

- **Temporal Fusion Transformers (TFT)**: Effective for processing time series with various dependencies.
- **Advantages**: Ability to capture global dependencies and efficient parallel processing.

### 2. Convolutional Autoencoders (CAE)

- **Application**: Work well with data having local dependencies.
- **Combination**: Can be combined with LSTM to capture both spatial and temporal dependencies.

### 3. Hybrid Models

- **Classical machine learning models**: For example, Logistic Regression, SVM, Random Forest, XGBoost, LightGBM, CatBoost, which can be used in combination with autoencoders for anomaly detection.

###
