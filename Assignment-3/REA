# Assignment 3 – TOPSIS Implementation

This assignment implements the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) method using both a command line tool and a web service.

## Part 2 – Command Line Tool
The command line implementation accepts a CSV file, weights, and impacts, applies the TOPSIS method, and generates an output CSV containing Topsis Score and Rank.

Usage:
topsis input.csv "1,1,1,1,1" "+,+,-,+,+" output.csv

## Part 3 – Web Service
A Flask-based web service is implemented where the user uploads a CSV file, enters weights, impacts, and email ID. The server applies TOPSIS and sends the result CSV to the user via email.

How to run:
pip install -r requirements.txt  
python app.py  

Open in browser:
http://127.0.0.1:5000/

## Methodology
1. Read decision matrix from CSV file  
2. Normalize criteria values  
3. Apply user-defined weights  
4. Determine ideal best and ideal worst using impacts  
5. Compute TOPSIS score  
6. Rank alternatives  

## Output
The output file contains the original data along with Topsis Score and Rank. A higher Topsis Score represents a better alternative.


## Author
Vishesh  
Roll Number: 102303961
