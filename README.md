# German Credit Data – EDA Project

## Overview

This project explores the **German Credit Dataset** using exploratory data analysis (EDA) to understand patterns in borrower characteristics and their relationship to credit risk. The analysis is framed in a banking context and focuses on interpretability and business relevance.

## Objective

- Explore structure and quality of credit data  
- Identify differences between good and bad credit risk profiles  
- Analyze relationships between customer features and credit outcomes  
- Derive simple, interpretable insights relevant to credit risk analysis  


## Dataset
German Credit Risk Dataset taken from:  
https://www.kaggle.com/datasets/kabure/german-credit-data-with-risk

Original data can be found here:  
https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data

Key feature groups include:
- Loan characteristics (amount, duration, purpose)  
- Financial status (savings, checking account status)  
- Personal attributes (age, employment, housing)  
- Credit history information  

The dataset consist of the following columns:  
Age (numeric)  
Sex (text: male, female)  
Job (numeric: 0 - unskilled and non-resident, 1 - unskilled and resident, 2 - skilled, 3 - highly skilled)  
Housing (text: own, rent, or free)  
Saving accounts (text - little, moderate, quite rich, rich)  
Checking account (numeric, in DM - Deutsch Mark)  
Credit amount (numeric, in DM)  
Duration (numeric, in month)  
Purpose (text: car, furniture/equipment, radio/TV, domestic appliances, repairs, education, business, vacation/others)  
Risk (text: good, bad)

## Methodology

The analysis is structured into:

- Data overview (structure, types, missing values)  
- Target variable distribution  
- Univariate feature analysis  
- Bivariate analysis vs. credit risk  
- Segment-based risk insights  

## Tools

- Python  
- Pandas  
- Matplotlib / Seaborn  
- Jupyter Notebook  

## Note

This project is part of a portfolio to demonstrate structured data analysis skills in a credit risk context. It focuses on interpretability and business-relevant insights rather than predictive modeling.