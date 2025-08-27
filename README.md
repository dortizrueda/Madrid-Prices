# 🏠 Rental Price Prediction - TFM

This repository contains the code and resources developed for my **Master's Final Project (TFM)**.  
The goal of the project is to build and evaluate machine learning models to predict rental property prices and to provide an interactive dashboard for exploration and prediction.

---

## 📌 Project Overview

- **Objective:** Predict rental prices of properties based on features such as size, location, and amenities.  
- **Approach:**  
  - Data preprocessing (handling numerical and categorical features).  
  - Training multiple regression models (Linear Regression, Ridge, Random Forest, Gradient Boosting, XGBoost).  
  - Model evaluation and hyperparameter tuning.  
  - Development of an interactive dashboard with **Streamlit**.  

- **Best Model:**  
  The **Random Forest** regressor achieved the best performance, with an $R^2$ of **0.8780**, outperforming other models in terms of predictive accuracy.

---

## 📂 Repository Structure
.


├── **data/**               # Dataset(s) used in the project


├── **notebooks/**           # Jupyter notebooks with EDA, training, and evaluation


├── **Python/**              # Streamlit app


│   ├── **app.py**           # Main dashboard script


│   ├── **pages/**           # Additional Streamlit pages


│   │   ├── **description.py**


│   │   └── **modelo.py**


│   └── **requirements.txt** # Python dependencies


└── **README.md**            # Project documentation



---

## ⚙️ Installation & Setup

Clone this repository and install the dependencies:

```bash
git clone https://github.com/dortizrueda/Madrid-Prices.git
cd <your-repo>
pip install -r Python/requirements.txt
```

## 📈 Experiment Tracking with MLflow

This project uses **MLflow** to track experiments, including model metrics, hyperparameters, and artifacts.  

To run MLflow locally:

```bash
mlflow ui
```
## 🚀 Run the Notebooks to prepare data and model

01_EDA.ipynb
02_Training.ipynb


## 🚀 Run the Dashboard

To launch the interactive dashboard:
```bash
streamlit run Python/app.py
```

Once executed, open the provided local URL in your browser to explore the application.

## 📊 Features of the Dashboard

### Data Overview: 
Visualize distributions of rental prices and property characteristics.

### Exploration: 
Interactive filters and plots for analyzing trends.

### Prediction: 
Enter property features manually and get an estimated rental price.


## 🔬 Models & Results

### Linear Regression / Ridge: Baseline models, $R^2 \approx 0.79$.

### Random Forest: Best performance with $R^2 = 0.8780$.

### Boosting (XGBoost, Gradient Boosting): Competitive, but slightly lower than Random Forest.

## 📌 Future Work

Improving the dashboard UI/UX for end users.

Implementing a voting system combining two predictive models.

Integrating additional socio-economic data to enhance prediction accuracy.

## 👤 Author

Developed by David Ortiz Rueda
Master’s in Big Data, Artificial Intelligence, and Data Engineering
University of Málaga