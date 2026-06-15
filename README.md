## Contributors

|       Name         | Role              |
|--------------------|-------------------|
| Bhausaheb Markande | Project Developer |
| Bhausaheb Markande & Tanmay Garje & Jaydip Gadekar| Testing           |
| Bhausaheb Markande & Tanmay Garje & Jaydip Gadekar | Documentation     |


Problem Statement

Law enforcement agencies often face difficulties in predicting future crime rates due to the large volume of crime data and complex relationships among different factors influencing criminal activities.

Traditional approaches lack automated prediction mechanisms and advanced analytical capabilities. There is a need for an intelligent system capable of analyzing historical crime data and generating future crime forecasts accurately.

The proposed system addresses this challenge by implementing machine learning and deep learning techniques to predict future crime rates and provide meaningful insights through graphical visualizations and analytical reports.



Objectives
Primary Objectives
To develop an intelligent crime prediction system.
To analyze historical crime data from different states of India.
To forecast future crime trends using machine learning algorithms.
To visualize crime patterns through interactive graphs.
To assist law enforcement agencies in crime analysis.
Secondary Objectives
To provide state-wise crime forecasting.
To compare crime trends among multiple states.
To improve prediction accuracy using deep learning techniques.
To provide a user-friendly graphical interface.
To generate analytical reports for decision-making.
Scope of the Project



The scope of the Crime Rate Prediction System includes:

Current Scope
State-wise crime prediction.
Historical crime trend analysis.
Crime data visualization.
User authentication.
Prediction storage and retrieval.
Model evaluation and performance analysis.
Future Scope
District-level prediction.
Real-time crime data integration.
Crime hotspot detection.
Mobile application development.
Cloud deployment.
AI-powered crime prevention recommendations.
Geographic Information System (GIS) integration.


Existing System

Existing crime analysis systems primarily focus on storing and retrieving crime records. These systems often lack predictive capabilities and advanced data analytics features.



Limitations
Manual analysis.
Time-consuming reporting.
No future prediction mechanism.
Limited visualization support.
Inability to identify long-term trends.



Proposed System

The proposed system utilizes Machine Learning and Deep Learning algorithms to analyze historical crime records and forecast future crime rates.

Features
Automated crime prediction.
State-wise crime forecasting.
Graphical trend visualization.
Historical crime analysis.
Interactive dashboard.
Database integration.
User authentication and management.
Technologies Used
Programming Language
Python 3.8+
Frontend
Tkinter GUI
Backend
Python
Database
MySQL
SQLite
Libraries
Data Analysis
Pandas
NumPy
Visualization
Matplotlib
Machine Learning
Scikit-Learn
Deep Learning
TensorFlow
Keras
LSTM
Image Processing
Pillow (PIL)


Project Structure
Crime Rate Prediction Project
│
├── assets/
│   ├── accuracy.png
│   ├── loss.png
│   ├── crime rate pred.jpg
│   └── GUI images
│
├── data/
│   └── crime_data_india.csv
│
├── Data migration/
│   └── db.py
│
├── Frontend/
│   ├── login.py
│   ├── registration.py
│   ├── Home.py
│   ├── guipage.py
│   ├── crime_wise_prediction.py
│   ├── Safety.py
│   └── State wise compare.py
│
├── Model Train/
│   ├── code.py
│   └── run_training.py
│
├── Model Testing/
│   └── evaluation.db
│
├── Outputs/
│   └── Plots/
│
├── saved_models/
│   └── State-wise LSTM Models
│
└── README.txt



System Architecture
+-------------------+
|    User Login     |
+---------+---------+
          |
          v
+-------------------+
| Crime Dashboard   |
+---------+---------+
          |
          v
+-------------------+
| Dataset Loading   |
+---------+---------+
          |
          v
+-------------------+
| Data Processing   |
+---------+---------+
          |
          v
+-------------------+
| Model Training    |
+---------+---------+
          |
          v
+-------------------+
| Crime Prediction  |
+---------+---------+
          |
          v
+-------------------+
| Visualization     |
+---------+---------+
          |
          v
+-------------------+
| Prediction Output |
+-------------------+
Dataset Description


Dataset Name

Crime Data India Dataset

Attributes
STATE/UT
YEAR
TOTAL IPC CRIMES
Crime Categories
State Information
Data Source

National Crime Records Bureau (NCRB)

Data Preprocessing

Before model training, the dataset undergoes several preprocessing steps:

Data Cleaning
Missing value handling.
Duplicate record removal.
Data validation.
Data Transformation
Feature selection.
Data normalization.
Time-series preparation.
Data Splitting
Training Dataset (80%)
Testing Dataset (20%)
Machine Learning and Deep Learning Model
LSTM (Long Short-Term Memory)

LSTM is a specialized Recurrent Neural Network (RNN) designed for time-series forecasting.

Advantages
Captures long-term dependencies.
Handles sequential data effectively.
Produces accurate forecasts.
Suitable for crime trend prediction.
Model Workflow
Historical Data
       |
       v
Data Preprocessing
       |
       v
Feature Engineering
       |
       v
LSTM Training
       |
       v
Prediction Model
       |
       v
Future Crime Forecast
Functional Modules
1. User Registration Module
User account creation.
Credential validation.
2. Login Module
User authentication.
Session management.
3. Dashboard Module
Main application interface.
Navigation management.
4. State-Wise Prediction Module
State selection.
Crime forecasting.
Future prediction display.
5. Crime-Wise Prediction Module
Category-wise analysis.
Crime-specific forecasting.
6. State Comparison Module
Multi-state comparison.
Trend evaluation.
7. Visualization Module
Graph generation.
Statistical representation.
8. Database Module
Prediction storage.
User management.
Results and Analysis

The developed system successfully predicts crime rates based on historical data.

Generated Outputs
State-wise prediction graphs.
Future crime forecasts.
Accuracy visualization.
Loss visualization.
Comparative analysis reports.
Performance

The model demonstrates strong predictive performance and effectively captures long-term crime trends.

Advantages
Accurate crime forecasting.
User-friendly GUI.
Automated analysis.
State-wise predictions.
Graphical visualization.
Scalable architecture.
Improved decision-making support.
Limitations
Dependent on dataset quality.
Prediction accuracy varies with data availability.
Limited real-time integration.
Requires periodic model retraining.
Future Enhancements
Integration with live crime databases.
Mobile application support.
Web deployment.
GIS-based crime mapping.
AI-powered recommendation systems.
District and city-level forecasting.
Real-time dashboard analytics.
