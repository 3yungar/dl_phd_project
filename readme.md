# Deep Learning PhD Project

This repository contains code and data for the Deep Learning PhD project focused on predictive analytics methods and algorithms for energy management systems.

## Research Overview

### Objective

The primary objective of this research is to develop advanced predictive analytics methods and algorithms that improve the efficiency and reliability of energy management systems (EMS). By leveraging deep learning techniques, this project aims to forecast energy consumption, detect anomalies, and optimize energy distribution in various settings.

### Background

Energy management systems are critical in modern infrastructure, ensuring optimal energy use and minimizing waste. Traditional methods often fall short in handling the complexity and dynamic nature of energy systems. This research explores the potential of deep learning models, such as VAE-LSTM hybrids and transformer-based models, to provide robust solutions for energy forecasting and anomaly detection.

### Methodology

1. **Data Collection and Preprocessing**: Raw data is collected from various sensors and energy systems, stored in the `data/` directory, and processed using scripts in the `analysis/` directory.
2. **Model Development**: Deep learning models are developed and trained using the code in the `deep_learning/` directory. These models include variational autoencoders (VAE), long short-term memory (LSTM) networks, and transformer-based models.
3. **Evaluation and Optimization**: The models are evaluated based on their accuracy in predicting energy consumption and detecting anomalies. The best-performing models are further optimized and stored in the `models/` directory.

### Key Contributions

- Development of a VAE-LSTM hybrid model for unsupervised anomaly detection in time series data.
- Comparative analysis of transformer-based models versus traditional time series forecasting methods.
- Implementation of advanced preprocessing techniques to enhance model performance.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```