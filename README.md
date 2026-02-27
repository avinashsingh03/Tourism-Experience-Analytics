# Tourism Experience Analytics

### Classification, Prediction and Recommendation System (Machine Learning Project)

🔗 **Live Web App:** https://tourism-experience-analytics03.streamlit.app/

---

##  Project Overview

Tourism platforms collect large amounts of user data such as ratings, travel history, visit patterns, and preferences. However, this data is rarely utilized effectively for improving user experience.

This project applies **Machine Learning and Data Analytics** to analyze tourism data and build an intelligent system that can:

* Predict user satisfaction (ratings)
* Predict travel behavior (visit mode)
* Recommend tourist attractions

The system processes user demographics, travel history, and attraction features to generate insights and personalized suggestions.

---

##  Objectives

The project performs three major tasks:

### 1️. Regression — Attraction Rating Prediction

Predict the rating a user is likely to give to a tourist attraction.

**Use Case**

* Helps tourism companies identify poorly performing attractions
* Improves service quality and customer satisfaction

---

### 2️. Classification — Visit Mode Prediction

Predict how a user will travel:

* Business
* Family
* Couples
* Friends

**Use Case**

* Personalized travel packages
* Targeted marketing campaigns

---

### 3️. Recommendation System — Attraction Suggestions

Recommend attractions based on:

* Past user behavior
* Similar users' preferences
* Attraction features

**Use Case**

* Personalized recommendations
* Increased customer engagement

---

##  Dataset Description

The dataset is relational and composed of multiple tables:

* Transaction Data (visits and ratings)
* User Data (demographics and location)
* City, Country, Region, Continent Data
* Attraction Information
* Attraction Types
* Visit Mode Categories

These datasets are merged to create a consolidated dataset for analysis and modeling.

---

##  Project Workflow

1. Data Cleaning
2. Data Preprocessing
3. Feature Engineering
4. Exploratory Data Analysis (EDA)
5. Model Training
6. Evaluation
7. Recommendation System
8. Deployment using Streamlit

---

##  Exploratory Data Analysis

EDA was performed to understand:

* User distribution across regions
* Popular attraction categories
* Visit behavior patterns
* Rating trends

Visualizations were created using charts and statistical summaries to identify patterns and relationships in the data.

---

##  Machine Learning Models

### Regression Model

Predicts attraction rating using user and attraction features.

### Classification Model

Predicts visit mode using user demographics and visit behavior.

### Recommendation System

Two approaches used:

* Collaborative Filtering
* Content-Based Filtering

---

##  Model Evaluation

### Classification Metrics

* Accuracy
* Precision
* Recall
* F1 Score

### Regression Metrics

* R² Score
* Mean Squared Error (MSE)
* Root Mean Squared Error (RMSE)

### Recommendation Metrics

* Mean Average Precision (MAP)
* Ranking relevance

---

##  Deployment

The project is deployed as an interactive **Streamlit web application**.

Users can:

* Enter location and preferences
* Predict visit mode
* Get recommended tourist attractions

**Try it here:**
https://tourism-experience-analytics03.streamlit.app/

---

##  Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* SQL
* Streamlit
* Jupyter Notebook

---

##  Repository Structure

```
├── data/
├── notebooks/
├── models/
├── app.py
├── requirements.txt
└── README.md
```

---

##  Future Improvements

* Deep Learning recommendation system
* Real-time user tracking
* Map-based attraction suggestions
* Mobile application integration

---

##  References

* Scikit-learn Documentation
* Pandas Documentation
* NumPy Documentation
* Machine Learning research articles

---

## Author

**Avinash Singh**
B.Tech Computer Science (AI)

---

If you found this project useful, please give the repository a star!
