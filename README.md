# NSure
This repository contains the source code and data files used to develop the NSure dynamic web application MVP focused on providing users a convenient and simple experience in selecting their health insurance policies, bypassing the unnecessary costs involved in dealing with insurer brokers.

## File Structure Of the Repository
The development and functionality of the web application revolves around **6** core files provided in the repository. Namely:

### *1. model_development/NSure_Data.csv*
In this file is a !**generated**! dataset with 1,800 samples featuring 9 independent variables and 1 dependent variable feature. The Independent variables relate to different preference fields that users may have regarding their choice in selecting insurance plans, such as *CPM (euro cost per month)*, and the dependent variable refers to 1 of 18 possible existing insurance plan policies offered in the Dutch market by 6 insurance providers that the user ends up opting in for. It is important to stress that this dataset was **simulated and therefore is not indicative of true information regarding customer behaviour related to the named insurance products**. The dataset was simulated by generating 100 sample observations using unique combination of normal and binomial distributions for features of every respective insurance plan covered by the model. 

### *2. model_development/model_notebook.ipynb*
This file contains the python notebook used to train and develop the multi-class classification model which is used to create personalised predictions for insurance policy products in the Dutch market that users should opt in for depending on their personal preferences. The data used to train the models is directly pulled from the *NSure_Data.csv* file. Ultimately a random forest classifier is used as the model of choice. The random forest model is built using the machine learning library scikit-learn. The model is then stored as a python object using the *pickle* library.

### 3. *models/model.pkl*
This is a python object file which contains the serialized random forest model code trained in *model_notebook.ipynb*. This file is used to create predictions for users.

### 4. *NSure_app/main.py*
This file is a python script which implements the Flask micro web framework to enable the opportunity to directly link python code (*model.pkl*) with the HTML file (*home.html*). This framework allows us to route the input data provided by users on the web app to the ML model file to create predictions and send the predictions back to the dynamic website for users in order to provide them near-instant advice on purchasing health insurance products. 

### 5. *NSure_app/templates/home.html*
This code outlines the content and structure of the front-end website that is accessed by users to send their preference data in return for advice on insurance policies.

### 6. *NSure_app/static/css/style.css*
Whilst *home.html* provides the content and structure for the website, this file is responsible for addressing the presentation of the website.


## How to Install and Run the Web App

1) Clone the repository on your local machine
2) Go to the console/terminal/command prompt and from project root run the line ```python NSure_app/main.py```
3) Open http://127.0.0.1:5000/ on your web browser
4) Fill in all required form fields and click on the advise button
5) Scroll down until end of the section to see your recommended health insurance products 


## Credit
The resources used to create the code for the project are listed below:
1) https://iq.opengenus.org/web-app-ml-model-using-flask/
2) https://codepen.io/NielsVoogt/pen/eYBQpPR
3) https://www.w3schools.com/
