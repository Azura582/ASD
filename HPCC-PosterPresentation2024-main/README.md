# Enhancing Early Detection and Visualization of Autism Spectrum Disorder

This project leverages **HPCC Systems** to improve the early detection and visualization of Autism Spectrum Disorder (ASD). HPCC Systems is an open-source, scalable platform designed for big data processing, making it ideal for managing and analyzing large datasets related to ASD diagnosis.

## HPCC Systems Overview

**HPCC Systems** (High-Performance Computing Cluster) is a distributed data processing platform that uses the **Thor** and **ROXIE** engines for data analytics and real-time querying.

### Key Benefits:
- **Scalability**: Process massive datasets in parallel for real-time analytics.
- **Efficiency**: Thor engine handles complex ETL tasks for data preprocessing and feature engineering.
- **Flexibility**: Integrated machine learning libraries support predictive model development.
- **ROXIE Query Engine**: Enables real-time, personalized recommendations based on user inputs.

## Project Objectives

- **Data Distribution**: Visualize differences between autistic and control subjects across age groups.
- **Model Evaluation**: Build predictive models (Logistic Regression, Random Forest) using HPCC’s machine learning libraries.
- **Feature Analysis**: Analyze important Q-Chat features using SHAP values.
- **Personalized Advice**: Provide tailored recommendations by integrating ROXIE queries with the Q-Chat interface.

## Methodology

1. **Data Collection & ETL Pipeline**: Use HPCC’s **Thor** engine to preprocess and transform Q-Chat data.
2. **Model Building**:
   - Logistic Regression, Random Forest, and SVM models.
   - Simplified with HPCC’s machine learning libraries.
3. **Model Evaluation**:
   - Accuracy, Confusion Matrix, and MCC used to assess model performance.
4. **Feature Analysis**:
   - Calculate SHAP values to interpret feature contributions efficiently.
5. **ROXIE Queries**:
   - Real-time queries for Q-Chat inputs (Yes/No) to offer personalized ASD diagnosis and recommendations.

## Results

- **Best Model**: Random Forest achieved an accuracy of **96.7%**.

![Example Poster 3 column (Blank) (4)](https://github.com/user-attachments/assets/8b7653e7-47a1-4410-9bd6-0fea0d11e915)
