# TOPSIS Web Service

This project implements a web-based TOPSIS solution using Flask.

---

## Functionality

- Upload input CSV file
- Enter weights and impacts
- Enter email ID
- TOPSIS is applied on server
- Result CSV is emailed to the user

---

## Methodology

1. Read CSV file from user
2. Validate weights and impacts
3. Normalize decision matrix
4. Apply weights
5. Compute ideal best and ideal worst
6. Calculate TOPSIS score
7. Rank alternatives
8. Email output file

---

## How to Run

pip install -r requirements.txt  
python app.py  

Open browser at `http://127.0.0.1:5000/`

---

## Output

The user receives a CSV file via email containing:
- Topsis Score
- Rank

---

## Author

Vishesh  
Roll No: 102303961
