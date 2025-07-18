# Alzheimer's Risk Assessment Tool

This is a machine learning-based desktop application that allows users to assess their potential risk for Alzheimer’s disease by entering medical and lifestyle information. It uses a trained Gaussian Naive Bayes model and a user-friendly graphical interface.

---

## Features

* User-friendly interface built with `tkinter`
* Predicts Alzheimer’s risk based on 14 clinical and lifestyle features
* Real-time input validation with error messages
* Displays model accuracy after prediction
* Includes sample dataset used for training and testing

---

## Technologies Used

* Python 3.x
* pandas
* scikit-learn
* tkinter (for GUI)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jannah-ayman/alzheimer
cd alzheimer
```

### 2. Install Dependencies

Make sure you have Python 3 installed. Then install the required libraries:

```bash
pip install pandas scikit-learn
```

> `tkinter` is usually included with Python. If not, install it depending on your operating system.

---

## Included Files

* `index.py` – Main application script
* `alzheimers_disease_data.csv` – Labeled dataset used for training
* `README.md` – Project documentation

---

## How to Run

From your terminal or command prompt:

```bash
python index.py
```

Then:

1. Fill in all required fields in the GUI.
2. Click **Assess My Risk**.
3. A popup will display:

   * Prediction: **High Risk** or **Low Risk**
   * Model test accuracy
   * Disclaimer encouraging medical consultation

---

## Dataset Details

The file `alzheimers_disease_data.csv` is included in this repository and contains anonymized patient data. It includes:

* **Target column:** `Diagnosis` (1 = High Risk, 0 = Low Risk)
* **Ignored columns:** `PatientID`, `DoctorInCharge`
* **Features used:** age, gender, BMI, cholesterol, MMSE score, memory complaints, confusion, behavioral issues, etc.

The dataset is automatically loaded and split into training/testing sets within the script.

---

## Disclaimer

This tool is intended for educational purposes only. It is not a medical device and should not be used for diagnosis or treatment. Always consult a healthcare provider for medical advice.

---
